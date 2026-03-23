'use strict';

const express = require('express');
const router = express.Router();
const projectController = require('../controllers/project.controller');
const { authenticate, authorize } = require('../middleware/auth.middleware');
const { auditLog } = require('../middleware/audit.middleware');

// All project routes require authentication
router.use(authenticate);

// ---------------------------------------------------------------------------
// Project CRUD
// ---------------------------------------------------------------------------

/**
 * GET /api/projects
 * List all projects with filtering, sorting, and pagination
 * Roles: admin, executive, pm, team_lead, team_member, finance_manager
 */
router.get(
  '/',
  authorize('admin', 'executive', 'pm', 'team_lead', 'team_member', 'finance_manager'),
  projectController.listProjects
);

/**
 * GET /api/projects/:projectId
 * Get a single project by ID
 * Roles: admin, executive, pm, team_lead, team_member, finance_manager, client_user
 */
router.get(
  '/:projectId',
  authorize('admin', 'executive', 'pm', 'team_lead', 'team_member', 'finance_manager', 'client_user'),
  projectController.getProject
);

/**
 * POST /api/projects
 * Create a new project
 * Roles: admin, pm
 */
router.post(
  '/',
  authorize('admin', 'pm'),
  auditLog('CREATE', 'project'),
  projectController.createProject
);

/**
 * PATCH /api/projects/:projectId
 * Update an existing project
 * Roles: admin, pm
 */
router.patch(
  '/:projectId',
  authorize('admin', 'pm'),
  auditLog('UPDATE', 'project'),
  projectController.updateProject
);

/**
 * DELETE /api/projects/:projectId
 * Soft-delete a project
 * Roles: admin
 */
router.delete(
  '/:projectId',
  authorize('admin'),
  auditLog('DELETE', 'project'),
  projectController.deleteProject
);

// ---------------------------------------------------------------------------
// Project Members
// ---------------------------------------------------------------------------

/**
 * GET /api/projects/:projectId/members
 * List team members of a project
 */
router.get(
  '/:projectId/members',
  authorize('admin', 'executive', 'pm', 'team_lead', 'team_member'),
  projectController.listProjectMembers
);

/**
 * POST /api/projects/:projectId/members
 * Add a member to a project
 */
router.post(
  '/:projectId/members',
  authorize('admin', 'pm'),
  auditLog('ADD_MEMBER', 'project'),
  projectController.addProjectMember
);

// ---------------------------------------------------------------------------
// Tasks within a Project
// ---------------------------------------------------------------------------

/**
 * GET /api/projects/:projectId/tasks
 * List tasks for a project
 */
router.get(
  '/:projectId/tasks',
  authorize('admin', 'executive', 'pm', 'team_lead', 'team_member', 'client_user'),
  projectController.listTasks
);

/**
 * POST /api/projects/:projectId/tasks
 * Create a task within a project
 * Roles: admin, pm, team_lead
 */
router.post(
  '/:projectId/tasks',
  authorize('admin', 'pm', 'team_lead'),
  auditLog('CREATE', 'task'),
  projectController.createTask
);

/**
 * PATCH /api/projects/:projectId/tasks/:taskId
 * Update a task (status, assignee, details — Kanban drag-and-drop)
 * Roles: admin, pm, team_lead, team_member
 */
router.patch(
  '/:projectId/tasks/:taskId',
  authorize('admin', 'pm', 'team_lead', 'team_member'),
  auditLog('UPDATE', 'task'),
  projectController.updateTask
);

// ---------------------------------------------------------------------------
// Milestones within a Project
// ---------------------------------------------------------------------------

/**
 * GET /api/projects/:projectId/milestones
 * List milestones for a project
 */
router.get(
  '/:projectId/milestones',
  authorize('admin', 'executive', 'pm', 'team_lead', 'team_member', 'client_user'),
  projectController.listMilestones
);

/**
 * POST /api/projects/:projectId/milestones
 * Create a milestone
 * Roles: admin, pm
 */
router.post(
  '/:projectId/milestones',
  authorize('admin', 'pm'),
  auditLog('CREATE', 'milestone'),
  projectController.createMilestone
);

module.exports = router;
