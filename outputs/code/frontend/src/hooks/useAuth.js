/**
 * useAuth.js
 * Custom React hook for authentication state management.
 */

import { useState, useEffect, useCallback, createContext, useContext } from 'react';
import authService from '../services/auth.service';

// ---------------------------------------------------------------------------
// Auth Context
// ---------------------------------------------------------------------------
const AuthContext = createContext(null);

/**
 * AuthProvider wraps the application and provides auth state to all children.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(authService.getStoredUser());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // On mount, verify the stored token is still valid
  useEffect(() => {
    const verifyAuth = async () => {
      if (!authService.isAuthenticated()) {
        setLoading(false);
        return;
      }
      try {
        const profile = await authService.getProfile();
        setUser(profile);
      } catch {
        // Token is invalid or expired — try refresh
        try {
          await authService.refreshAccessToken();
          const profile = await authService.getProfile();
          setUser(profile);
        } catch {
          // Refresh also failed — clear state
          authService.clearTokens();
          setUser(null);
        }
      } finally {
        setLoading(false);
      }
    };

    verifyAuth();
  }, []);

  // --- Login ---
  const login = useCallback(async (email, password) => {
    setError(null);
    try {
      const data = await authService.login(email, password);
      if (!data.requiresTwoFactor) {
        setUser(data.user);
      }
      return data;
    } catch (err) {
      const message =
        err.response?.data?.error || 'Login failed. Please try again.';
      setError(message);
      throw err;
    }
  }, []);

  // --- Verify 2FA ---
  const verify2FA = useCallback(async (tempToken, code) => {
    setError(null);
    try {
      const data = await authService.verify2FA(tempToken, code);
      setUser(data.user);
      return data;
    } catch (err) {
      const message =
        err.response?.data?.error || 'Invalid 2FA code. Please try again.';
      setError(message);
      throw err;
    }
  }, []);

  // --- Register ---
  const register = useCallback(async (formData) => {
    setError(null);
    try {
      const data = await authService.register(formData);
      setUser(data);
      return data;
    } catch (err) {
      const message =
        err.response?.data?.error || 'Registration failed. Please try again.';
      setError(message);
      throw err;
    }
  }, []);

  // --- Logout ---
  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
    setError(null);
  }, []);

  // --- Role checks ---
  const hasRole = useCallback(
    (role) => {
      if (!user?.roles) return false;
      return user.roles.includes(role);
    },
    [user]
  );

  const hasAnyRole = useCallback(
    (...roles) => {
      if (!user?.roles) return false;
      return roles.some((r) => user.roles.includes(r));
    },
    [user]
  );

  const isAdmin = useCallback(() => hasRole('admin'), [hasRole]);

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login,
    verify2FA,
    register,
    logout,
    hasRole,
    hasAnyRole,
    isAdmin,
    clearError: () => setError(null),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * useAuth hook — must be used within an AuthProvider.
 */
export default function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
