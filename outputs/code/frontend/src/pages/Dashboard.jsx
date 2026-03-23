/**
 * Dashboard.jsx
 * Role-based dashboard that displays different content based on the user's role.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import { apiGet } from '../services/api.service';

export default function Dashboard() {
  const { user, logout, hasRole, hasAnyRole } = useAuth();
  const navigate = useNavigate();

  const [projects, setProjects] = useState([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [stats, setStats] = useState({ total: 0, active: 0, completed: 0 });

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const res = await apiGet('/api/projects', {
          params: { limit: 10, sort_by: 'updated_at', sort_order: 'desc' },
        });
        const data = res.data.data || [];
        setProjects(data);
        setStats({
          total: res.data.pagination?.total || data.length,
          active: data.filter((p) => p.status === 'active').length,
          completed: data.filter((p) => p.status === 'completed').length,
        });
      } catch {
        // Silently fail — dashboard will show empty state
      } finally {
        setLoadingProjects(false);
      }
    };

    fetchProjects();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  // ----- Styles -----
  const pageStyle = {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f0f2f5',
    minHeight: '100vh',
  };

  const headerStyle = {
    backgroundColor: '#001529',
    color: '#fff',
    padding: '0 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: '64px',
  };

  const contentStyle = {
    padding: '24px',
    maxWidth: '1200px',
    margin: '0 auto',
  };

  const cardStyle = {
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    padding: '20px',
    marginBottom: '16px',
  };

  const statCardStyle = {
    ...cardStyle,
    textAlign: 'center',
    flex: '1',
    minWidth: '150px',
  };

  const badgeStyle = (color) => ({
    display: 'inline-block',
    padding: '2px 8px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 600,
    backgroundColor: color,
    color: '#fff',
  });

  const statusColors = {
    active: '#52c41a',
    draft: '#1677ff',
    on_hold: '#faad14',
    completed: '#722ed1',
    archived: '#8c8c8c',
  };

  // ----- Render role-specific greeting -----
  const getRoleLabel = () => {
    if (hasRole('admin')) return 'Administrator';
    if (hasRole('executive')) return 'Executive';
    if (hasRole('pm')) return 'Project Manager';
    if (hasRole('team_lead')) return 'Team Lead';
    if (hasRole('finance_manager')) return 'Finance Manager';
    if (hasRole('client_user')) return 'Client Portal';
    return 'Team Member';
  };

  return (
    <div style={pageStyle}>
      {/* Header */}
      <header style={headerStyle}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h3 style={{ margin: 0 }}>TechNova Platform</h3>
          <span style={{ opacity: 0.65, fontSize: '14px' }}>|</span>
          <span style={{ opacity: 0.65, fontSize: '14px' }}>{getRoleLabel()}</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ fontSize: '14px' }}>
            {user?.firstName} {user?.lastName}
          </span>
          <button
            onClick={handleLogout}
            style={{
              background: 'transparent',
              border: '1px solid rgba(255,255,255,0.3)',
              color: '#fff',
              padding: '4px 12px',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Content */}
      <main style={contentStyle}>
        <h2>Welcome back, {user?.firstName || 'User'}</h2>

        {/* Stats row */}
        <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
          <div style={statCardStyle}>
            <div style={{ fontSize: '32px', fontWeight: 700, color: '#1677ff' }}>{stats.total}</div>
            <div style={{ color: '#666' }}>Total Projects</div>
          </div>
          <div style={statCardStyle}>
            <div style={{ fontSize: '32px', fontWeight: 700, color: '#52c41a' }}>{stats.active}</div>
            <div style={{ color: '#666' }}>Active</div>
          </div>
          <div style={statCardStyle}>
            <div style={{ fontSize: '32px', fontWeight: 700, color: '#722ed1' }}>{stats.completed}</div>
            <div style={{ color: '#666' }}>Completed</div>
          </div>
        </div>

        {/* Role-specific sections */}
        {hasAnyRole('admin', 'executive') && (
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Executive Overview</h3>
            <p style={{ color: '#666' }}>
              KPI dashboards, profitability analysis, and team utilisation reports are available
              from the Reports section.
            </p>
          </div>
        )}

        {hasAnyRole('admin', 'pm', 'team_lead') && (
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Resource Management</h3>
            <p style={{ color: '#666' }}>
              View resource allocation, team utilisation, and capacity forecasts.
            </p>
          </div>
        )}

        {hasRole('finance_manager') && (
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Financial Overview</h3>
            <p style={{ color: '#666' }}>
              Manage invoices, billing rates, and QuickBooks integration from the Finance section.
            </p>
          </div>
        )}

        {hasRole('client_user') && (
          <div style={cardStyle}>
            <h3 style={{ marginTop: 0 }}>Your Projects</h3>
            <p style={{ color: '#666' }}>
              View project progress, approve milestones, and communicate with your project team.
            </p>
          </div>
        )}

        {/* Recent projects */}
        <div style={cardStyle}>
          <h3 style={{ marginTop: 0 }}>Recent Projects</h3>

          {loadingProjects ? (
            <p style={{ color: '#666' }}>Loading projects...</p>
          ) : projects.length === 0 ? (
            <p style={{ color: '#666' }}>No projects found.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #f0f0f0', textAlign: 'left' }}>
                  <th style={{ padding: '8px' }}>Project</th>
                  <th style={{ padding: '8px' }}>Client</th>
                  <th style={{ padding: '8px' }}>Status</th>
                  <th style={{ padding: '8px' }}>Deadline</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project) => (
                  <tr key={project.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '8px' }}>{project.name}</td>
                    <td style={{ padding: '8px', color: '#666' }}>{project.client_name || '-'}</td>
                    <td style={{ padding: '8px' }}>
                      <span style={badgeStyle(statusColors[project.status] || '#8c8c8c')}>
                        {project.status?.replace('_', ' ')}
                      </span>
                    </td>
                    <td style={{ padding: '8px', color: '#666' }}>
                      {project.deadline
                        ? new Date(project.deadline).toLocaleDateString()
                        : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  );
}
