/**
 * App.jsx
 * Root component with React Router setup and protected routes.
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />

          {/* Protected routes — any authenticated user */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Admin-only routes */}
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute roles={['admin']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* PM and above routes */}
          <Route
            path="/projects/*"
            element={
              <ProtectedRoute roles={['admin', 'executive', 'pm', 'team_lead', 'team_member', 'finance_manager']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Finance routes */}
          <Route
            path="/invoices/*"
            element={
              <ProtectedRoute roles={['admin', 'finance_manager', 'executive']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Client portal */}
          <Route
            path="/portal/*"
            element={
              <ProtectedRoute roles={['client_user']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Reports */}
          <Route
            path="/reports/*"
            element={
              <ProtectedRoute roles={['admin', 'executive', 'pm', 'finance_manager']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* 404 */}
          <Route
            path="*"
            element={
              <div style={{ textAlign: 'center', padding: '4rem', fontFamily: 'sans-serif' }}>
                <h1>404 - Page Not Found</h1>
                <p>The page you are looking for does not exist.</p>
                <a href="/dashboard" style={{ color: '#1677ff' }}>Go to Dashboard</a>
              </div>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
