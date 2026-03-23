'use strict';

const { v4: uuidv4 } = require('uuid');
const db = require('../config/database');
const { setAuditBefore } = require('../middleware/audit.middleware');

// ---------------------------------------------------------------------------
// Validation helpers
// ---------------------------------------------------------------------------
const VALID_PROJECT_STATUSES = ['draft', 'active', 'on_hold', 'completed', 'archived'];
const VALID_TASK_STATUSES = ['todo', 'in_progress', 'in_review', 'done'];
const VALID_TASK_PRIORITIES = ['low', 'medium', 'high', 'critical'];
const VALID_MILESTONE_STATUSES = [
  'pending', 'in_progress', 'awaiting_approval',
  'approved', 'revision_requested', 'completed',
];

const isValidUUID = (str) =>
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(str);

const isValidDate = (str) => !isNaN(Date.parse(str));

// ---------------------------------------------------------------------------
// GET /api/projects — List projects with filtering, sorting, pagination
// ---------------------------------------------------------------------------
const listProjects = async (req, res) => {
  try {
    const {
      status,
      client_id,
      search,
      sort_by = 'created_at',
      sort_order = 'desc',
      page = 1,
      limit = 20,
    } = req.query;

    const pageNum = Math.max(1, parseInt(page, 10) || 1);
    const pageSize = Math.min(100, Math.max(1, parseInt(limit, 10) || 20));
    const offset = (pageNum - 1) * pageSize;

    // Allowed sort columns (whitelist to prevent SQL injection)
    const allowedSortColumns = ['name', 'status', 'start_date', 'deadline', 'budget', 'created_at'];
    const sortCol = allowedSortColumns.includes(sort_by) ? sort_by : 'created_at';
    const sortDir = sort_order.toLowerCase() === 'asc' ? 'ASC' : 'DESC';

    let whereConditions = ['p.deleted_at IS NULL'];
    const params = [];
    let paramIndex = 1;

    if (status && VALID_PROJECT_STATUSES.includes(status)) {
      whereConditions.push(`p.status = $${paramIndex++}`);
      params.push(status);
    }

    if (client_id && isValidUUID(client_id)) {
      whereConditions.push(`p.client_id = $${paramIndex++}`);
      params.push(client_id);
    }

    if (search && search.trim()) {
      whereConditions.push(`(p.name ILIKE $${paramIndex} OR p.description ILIKE $${paramIndex})`);
      params.push(`%${search.trim()}%`);
      paramIndex++;
    }

    // Client users can only see their own projects
    if (req.user.roles.includes('client_user') && req.user.clientId) {
      whereConditions.push(`p.client_id = $${paramIndex++}`);
      params.push(req.user.clientId);
    }

    const whereClause = whereConditions.join(' AND ');

    // Count total
    const countResult = await db.query(
      `SELECT COUNT(*) AS total FROM projects p WHERE ${whereClause}`,
      params
    );
    const total = parseInt(countResult.rows[0].total, 10);

    // Fetch page
    const dataResult = await db.query(
      `SELECT p.id, p.name, p.description, p.status, p.start_date, p.deadline,
              p.budget, p.created_at, p.updated_at,
              c.name AS client_name, c.id AS client_id
       FROM projects p
       LEFT JOIN clients c ON c.id = p.client_id
       WHERE ${whereClause}
       ORDER BY p.${sortCol} ${sortDir}
       LIMIT $${paramIndex++} OFFSET $${paramIndex++}`,
      [...params, pageSize, offset]
    );

    return res.status(200).json({
      success: true,
      data: dataResult.rows,
      pagination: {
        page: pageNum,
        limit: pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      },
    });
  } catch (err) {
    console.error('List projects error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// GET /api/projects/:projectId — Get single project
// ---------------------------------------------------------------------------
const getProject = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID format.' });
    }

    const result = await db.query(
      `SELECT p.*, c.name AS client_name
       FROM projects p
       LEFT JOIN clients c ON c.id = p.client_id
       WHERE p.id = $1 AND p.deleted_at IS NULL`,
      [projectId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }

    const project = result.rows[0];

    // Client users can only view projects for their organisation
    if (req.user.roles.includes('client_user') && req.user.clientId !== project.client_id) {
      return res.status(403).json({ success: false, error: 'Access denied.' });
    }

    return res.status(200).json({ success: true, data: project });
  } catch (err) {
    console.error('Get project error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// POST /api/projects — Create project
// ---------------------------------------------------------------------------
const createProject = async (req, res) => {
  try {
    const { name, description, clientId, startDate, deadline, budget, status } = req.body;

    // --- Validation ---
    if (!name || !clientId || !startDate || !deadline) {
      return res.status(400).json({
        success: false,
        error: 'Required fields: name, clientId, startDate, deadline.',
      });
    }
    if (name.length > 255) {
      return res.status(400).json({ success: false, error: 'Name must be 255 characters or fewer.' });
    }
    if (!isValidUUID(clientId)) {
      return res.status(400).json({ success: false, error: 'Invalid clientId format.' });
    }
    if (!isValidDate(startDate) || !isValidDate(deadline)) {
      return res.status(400).json({ success: false, error: 'Invalid date format.' });
    }
    if (new Date(deadline) <= new Date(startDate)) {
      return res.status(400).json({ success: false, error: 'Deadline must be after start date.' });
    }
    if (budget !== undefined && budget !== null && (isNaN(budget) || budget < 0)) {
      return res.status(400).json({ success: false, error: 'Budget must be a non-negative number.' });
    }

    const projectStatus = status && VALID_PROJECT_STATUSES.includes(status) ? status : 'active';

    // Verify client exists
    const clientCheck = await db.query('SELECT id FROM clients WHERE id = $1', [clientId]);
    if (clientCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Client not found.' });
    }

    const projectId = uuidv4();
    const result = await db.query(
      `INSERT INTO projects (id, client_id, name, description, status, start_date, deadline, budget, created_by)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
       RETURNING *`,
      [projectId, clientId, name.trim(), description || null, projectStatus, startDate, deadline, budget || null, req.user.id]
    );

    return res.status(201).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Create project error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// PATCH /api/projects/:projectId — Update project
// ---------------------------------------------------------------------------
const updateProject = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID format.' });
    }

    // Fetch current project for audit "before" snapshot
    const existing = await db.query(
      'SELECT * FROM projects WHERE id = $1 AND deleted_at IS NULL',
      [projectId]
    );
    if (existing.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }
    setAuditBefore(req, existing.rows[0]);

    const { name, description, status, startDate, deadline, budget } = req.body;

    // Build dynamic SET clause
    const setClauses = [];
    const params = [];
    let paramIndex = 1;

    if (name !== undefined) {
      if (name.length > 255) {
        return res.status(400).json({ success: false, error: 'Name must be 255 characters or fewer.' });
      }
      setClauses.push(`name = $${paramIndex++}`);
      params.push(name.trim());
    }
    if (description !== undefined) {
      setClauses.push(`description = $${paramIndex++}`);
      params.push(description);
    }
    if (status !== undefined) {
      if (!VALID_PROJECT_STATUSES.includes(status)) {
        return res.status(400).json({
          success: false,
          error: `Invalid status. Allowed: ${VALID_PROJECT_STATUSES.join(', ')}`,
        });
      }
      setClauses.push(`status = $${paramIndex++}`);
      params.push(status);
    }
    if (startDate !== undefined) {
      if (!isValidDate(startDate)) {
        return res.status(400).json({ success: false, error: 'Invalid start date.' });
      }
      setClauses.push(`start_date = $${paramIndex++}`);
      params.push(startDate);
    }
    if (deadline !== undefined) {
      if (!isValidDate(deadline)) {
        return res.status(400).json({ success: false, error: 'Invalid deadline.' });
      }
      setClauses.push(`deadline = $${paramIndex++}`);
      params.push(deadline);
    }
    if (budget !== undefined) {
      if (budget !== null && (isNaN(budget) || budget < 0)) {
        return res.status(400).json({ success: false, error: 'Budget must be a non-negative number.' });
      }
      setClauses.push(`budget = $${paramIndex++}`);
      params.push(budget);
    }

    if (setClauses.length === 0) {
      return res.status(400).json({ success: false, error: 'No fields to update.' });
    }

    setClauses.push(`updated_at = NOW()`);
    params.push(projectId);

    const result = await db.query(
      `UPDATE projects SET ${setClauses.join(', ')} WHERE id = $${paramIndex} AND deleted_at IS NULL RETURNING *`,
      params
    );

    return res.status(200).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Update project error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// DELETE /api/projects/:projectId — Soft-delete
// ---------------------------------------------------------------------------
const deleteProject = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID format.' });
    }

    const existing = await db.query(
      'SELECT * FROM projects WHERE id = $1 AND deleted_at IS NULL',
      [projectId]
    );
    if (existing.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }
    setAuditBefore(req, existing.rows[0]);

    await db.query(
      'UPDATE projects SET deleted_at = NOW(), updated_at = NOW() WHERE id = $1',
      [projectId]
    );

    return res.status(200).json({ success: true, data: { message: 'Project deleted.' } });
  } catch (err) {
    console.error('Delete project error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// GET /api/projects/:projectId/members
// ---------------------------------------------------------------------------
const listProjectMembers = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID.' });
    }

    const result = await db.query(
      `SELECT pm.id, pm.project_role, pm.joined_at,
              u.id AS user_id, u.email, u.first_name, u.last_name
       FROM project_members pm
       JOIN users u ON u.id = pm.user_id
       WHERE pm.project_id = $1
       ORDER BY pm.joined_at ASC`,
      [projectId]
    );

    return res.status(200).json({ success: true, data: result.rows });
  } catch (err) {
    console.error('List project members error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// POST /api/projects/:projectId/members
// ---------------------------------------------------------------------------
const addProjectMember = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { userId, projectRole } = req.body;

    if (!isValidUUID(projectId) || !userId || !isValidUUID(userId)) {
      return res.status(400).json({ success: false, error: 'Valid projectId and userId are required.' });
    }

    // Verify project exists
    const projectCheck = await db.query(
      'SELECT id FROM projects WHERE id = $1 AND deleted_at IS NULL',
      [projectId]
    );
    if (projectCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }

    // Verify user exists
    const userCheck = await db.query('SELECT id FROM users WHERE id = $1 AND deleted_at IS NULL', [userId]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'User not found.' });
    }

    // Check for duplicate
    const dupeCheck = await db.query(
      'SELECT id FROM project_members WHERE project_id = $1 AND user_id = $2',
      [projectId, userId]
    );
    if (dupeCheck.rows.length > 0) {
      return res.status(409).json({ success: false, error: 'User is already a member of this project.' });
    }

    const memberId = uuidv4();
    const role = projectRole || 'member';

    const result = await db.query(
      `INSERT INTO project_members (id, project_id, user_id, project_role)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [memberId, projectId, userId, role]
    );

    return res.status(201).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Add project member error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// GET /api/projects/:projectId/tasks
// ---------------------------------------------------------------------------
const listTasks = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID.' });
    }

    const { status, assignee_id, priority, page = 1, limit = 50 } = req.query;

    const pageNum = Math.max(1, parseInt(page, 10) || 1);
    const pageSize = Math.min(100, Math.max(1, parseInt(limit, 10) || 50));
    const offset = (pageNum - 1) * pageSize;

    let whereConditions = ['t.project_id = $1'];
    const params = [projectId];
    let paramIndex = 2;

    if (status && VALID_TASK_STATUSES.includes(status)) {
      whereConditions.push(`t.status = $${paramIndex++}`);
      params.push(status);
    }
    if (assignee_id && isValidUUID(assignee_id)) {
      whereConditions.push(`t.assignee_id = $${paramIndex++}`);
      params.push(assignee_id);
    }
    if (priority && VALID_TASK_PRIORITIES.includes(priority)) {
      whereConditions.push(`t.priority = $${paramIndex++}`);
      params.push(priority);
    }

    const whereClause = whereConditions.join(' AND ');

    const countResult = await db.query(
      `SELECT COUNT(*) AS total FROM tasks t WHERE ${whereClause}`,
      params
    );

    const dataResult = await db.query(
      `SELECT t.*, u.first_name AS assignee_first_name, u.last_name AS assignee_last_name
       FROM tasks t
       LEFT JOIN users u ON u.id = t.assignee_id
       WHERE ${whereClause}
       ORDER BY t.created_at DESC
       LIMIT $${paramIndex++} OFFSET $${paramIndex++}`,
      [...params, pageSize, offset]
    );

    return res.status(200).json({
      success: true,
      data: dataResult.rows,
      pagination: {
        page: pageNum,
        limit: pageSize,
        total: parseInt(countResult.rows[0].total, 10),
        totalPages: Math.ceil(parseInt(countResult.rows[0].total, 10) / pageSize),
      },
    });
  } catch (err) {
    console.error('List tasks error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// POST /api/projects/:projectId/tasks
// ---------------------------------------------------------------------------
const createTask = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID.' });
    }

    const { title, description, status, priority, assigneeId, dueDate, estimatedHours } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: 'Task title is required.' });
    }
    if (title.length > 255) {
      return res.status(400).json({ success: false, error: 'Title must be 255 characters or fewer.' });
    }

    // Verify project exists
    const projectCheck = await db.query(
      'SELECT id FROM projects WHERE id = $1 AND deleted_at IS NULL',
      [projectId]
    );
    if (projectCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }

    const taskStatus = status && VALID_TASK_STATUSES.includes(status) ? status : 'todo';
    const taskPriority = priority && VALID_TASK_PRIORITIES.includes(priority) ? priority : 'medium';

    if (assigneeId && !isValidUUID(assigneeId)) {
      return res.status(400).json({ success: false, error: 'Invalid assigneeId format.' });
    }
    if (dueDate && !isValidDate(dueDate)) {
      return res.status(400).json({ success: false, error: 'Invalid due date.' });
    }
    if (estimatedHours !== undefined && (isNaN(estimatedHours) || estimatedHours < 0)) {
      return res.status(400).json({ success: false, error: 'Estimated hours must be a non-negative number.' });
    }

    const taskId = uuidv4();
    const result = await db.query(
      `INSERT INTO tasks (id, project_id, title, description, status, priority, assignee_id, due_date, estimated_hours)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
       RETURNING *`,
      [
        taskId, projectId, title.trim(), description || null,
        taskStatus, taskPriority,
        assigneeId || null, dueDate || null, estimatedHours || null,
      ]
    );

    return res.status(201).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Create task error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// PATCH /api/projects/:projectId/tasks/:taskId
// ---------------------------------------------------------------------------
const updateTask = async (req, res) => {
  try {
    const { projectId, taskId } = req.params;
    if (!isValidUUID(projectId) || !isValidUUID(taskId)) {
      return res.status(400).json({ success: false, error: 'Invalid ID format.' });
    }

    const existing = await db.query(
      'SELECT * FROM tasks WHERE id = $1 AND project_id = $2',
      [taskId, projectId]
    );
    if (existing.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Task not found.' });
    }
    setAuditBefore(req, existing.rows[0]);

    const { title, description, status, priority, assigneeId, dueDate, estimatedHours } = req.body;

    // Team members can only update their own tasks
    if (
      req.user.roles.includes('team_member') &&
      !req.user.roles.includes('admin') &&
      !req.user.roles.includes('pm') &&
      !req.user.roles.includes('team_lead') &&
      existing.rows[0].assignee_id !== req.user.id
    ) {
      return res.status(403).json({ success: false, error: 'You can only update tasks assigned to you.' });
    }

    const setClauses = [];
    const params = [];
    let paramIndex = 1;

    if (title !== undefined) {
      if (title.length > 255) {
        return res.status(400).json({ success: false, error: 'Title must be 255 characters or fewer.' });
      }
      setClauses.push(`title = $${paramIndex++}`);
      params.push(title.trim());
    }
    if (description !== undefined) {
      setClauses.push(`description = $${paramIndex++}`);
      params.push(description);
    }
    if (status !== undefined) {
      if (!VALID_TASK_STATUSES.includes(status)) {
        return res.status(400).json({
          success: false,
          error: `Invalid status. Allowed: ${VALID_TASK_STATUSES.join(', ')}`,
        });
      }
      setClauses.push(`status = $${paramIndex++}`);
      params.push(status);
    }
    if (priority !== undefined) {
      if (!VALID_TASK_PRIORITIES.includes(priority)) {
        return res.status(400).json({
          success: false,
          error: `Invalid priority. Allowed: ${VALID_TASK_PRIORITIES.join(', ')}`,
        });
      }
      setClauses.push(`priority = $${paramIndex++}`);
      params.push(priority);
    }
    if (assigneeId !== undefined) {
      if (assigneeId !== null && !isValidUUID(assigneeId)) {
        return res.status(400).json({ success: false, error: 'Invalid assigneeId format.' });
      }
      setClauses.push(`assignee_id = $${paramIndex++}`);
      params.push(assigneeId);
    }
    if (dueDate !== undefined) {
      if (dueDate !== null && !isValidDate(dueDate)) {
        return res.status(400).json({ success: false, error: 'Invalid due date.' });
      }
      setClauses.push(`due_date = $${paramIndex++}`);
      params.push(dueDate);
    }
    if (estimatedHours !== undefined) {
      if (estimatedHours !== null && (isNaN(estimatedHours) || estimatedHours < 0)) {
        return res.status(400).json({ success: false, error: 'Estimated hours must be a non-negative number.' });
      }
      setClauses.push(`estimated_hours = $${paramIndex++}`);
      params.push(estimatedHours);
    }

    if (setClauses.length === 0) {
      return res.status(400).json({ success: false, error: 'No fields to update.' });
    }

    setClauses.push(`updated_at = NOW()`);
    params.push(taskId);
    params.push(projectId);

    const result = await db.query(
      `UPDATE tasks SET ${setClauses.join(', ')}
       WHERE id = $${paramIndex++} AND project_id = $${paramIndex}
       RETURNING *`,
      params
    );

    return res.status(200).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Update task error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// GET /api/projects/:projectId/milestones
// ---------------------------------------------------------------------------
const listMilestones = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID.' });
    }

    const result = await db.query(
      `SELECT m.*, u.first_name AS approved_by_first_name, u.last_name AS approved_by_last_name
       FROM milestones m
       LEFT JOIN users u ON u.id = m.approved_by
       WHERE m.project_id = $1
       ORDER BY m.target_date ASC`,
      [projectId]
    );

    return res.status(200).json({ success: true, data: result.rows });
  } catch (err) {
    console.error('List milestones error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

// ---------------------------------------------------------------------------
// POST /api/projects/:projectId/milestones
// ---------------------------------------------------------------------------
const createMilestone = async (req, res) => {
  try {
    const { projectId } = req.params;
    if (!isValidUUID(projectId)) {
      return res.status(400).json({ success: false, error: 'Invalid project ID.' });
    }

    const { name, targetDate, status, requiresClientApproval } = req.body;

    if (!name || !targetDate) {
      return res.status(400).json({ success: false, error: 'Name and targetDate are required.' });
    }
    if (name.length > 255) {
      return res.status(400).json({ success: false, error: 'Name must be 255 characters or fewer.' });
    }
    if (!isValidDate(targetDate)) {
      return res.status(400).json({ success: false, error: 'Invalid target date.' });
    }

    // Verify project exists
    const projectCheck = await db.query(
      'SELECT id FROM projects WHERE id = $1 AND deleted_at IS NULL',
      [projectId]
    );
    if (projectCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Project not found.' });
    }

    const msStatus = status && VALID_MILESTONE_STATUSES.includes(status) ? status : 'pending';
    const milestoneId = uuidv4();

    const result = await db.query(
      `INSERT INTO milestones (id, project_id, name, target_date, status, requires_client_approval)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [milestoneId, projectId, name.trim(), targetDate, msStatus, requiresClientApproval || false]
    );

    return res.status(201).json({ success: true, data: result.rows[0] });
  } catch (err) {
    console.error('Create milestone error:', err);
    return res.status(500).json({ success: false, error: 'Internal server error.' });
  }
};

module.exports = {
  listProjects,
  getProject,
  createProject,
  updateProject,
  deleteProject,
  listProjectMembers,
  addProjectMember,
  listTasks,
  createTask,
  updateTask,
  listMilestones,
  createMilestone,
};
