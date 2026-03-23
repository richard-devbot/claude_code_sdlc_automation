/**
 * ProtectedRoute.jsx
 * Route guard component that redirects unauthenticated users to /login
 * and optionally enforces role-based access.
 */

import { Navigate, useLocation } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

/**
 * @param {object} props
 * @param {React.ReactNode} props.children       The protected page/component
 * @param {string[]}        [props.roles]         Optional list of allowed roles
 * @param {string}          [props.redirectTo]    Where to redirect if unauthorized (default: /login)
 */
export default function ProtectedRoute({
  children,
  roles = [],
  redirectTo = '/login',
}) {
  const { isAuthenticated, loading, user, hasAnyRole } = useAuth();
  const location = useLocation();

  // Show nothing while checking auth state
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading...</p>
      </div>
    );
  }

  // Not authenticated — redirect to login (preserve intended destination)
  if (!isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Role check — if roles are specified, the user must have at least one
  if (roles.length > 0 && !hasAnyRole(...roles)) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>Access Denied</h2>
        <p>
          You do not have permission to view this page. Required role(s):{' '}
          <strong>{roles.join(', ')}</strong>.
        </p>
        <p>
          Your current role(s): <strong>{user?.roles?.join(', ') || 'none'}</strong>.
        </p>
      </div>
    );
  }

  return children;
}
