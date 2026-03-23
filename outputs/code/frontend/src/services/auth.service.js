/**
 * auth.service.js
 * Authentication service — login, logout, token storage, and refresh.
 */

import api from './api.service';

const ACCESS_TOKEN_KEY = 'technova_access_token';
const REFRESH_TOKEN_KEY = 'technova_refresh_token';
const USER_KEY = 'technova_user';

// ---------------------------------------------------------------------------
// Token storage (uses localStorage; swap to secure cookie for production)
// ---------------------------------------------------------------------------
const getAccessToken = () => localStorage.getItem(ACCESS_TOKEN_KEY);
const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN_KEY);

const setTokens = ({ accessToken, refreshToken }) => {
  if (accessToken) localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

const clearTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

// ---------------------------------------------------------------------------
// User storage
// ---------------------------------------------------------------------------
const getStoredUser = () => {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

const setStoredUser = (user) => {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

// ---------------------------------------------------------------------------
// Auth API calls
// ---------------------------------------------------------------------------

/**
 * Login with email + password.
 * Returns the full response data (may include requiresTwoFactor).
 */
const login = async (email, password) => {
  const response = await api.post('/api/auth/login', { email, password });
  const data = response.data.data;

  if (!data.requiresTwoFactor && data.tokens) {
    setTokens(data.tokens);
    setStoredUser(data.user);
  }

  return data;
};

/**
 * Verify 2FA code after login.
 */
const verify2FA = async (tempToken, code) => {
  const response = await api.post('/api/auth/2fa/verify', { tempToken, code });
  const data = response.data.data;

  if (data.tokens) {
    setTokens(data.tokens);
    setStoredUser(data.user);
  }

  return data;
};

/**
 * Register a new account.
 */
const register = async ({ email, password, firstName, lastName }) => {
  const response = await api.post('/api/auth/register', {
    email,
    password,
    firstName,
    lastName,
  });
  const data = response.data.data;

  if (data.tokens) {
    setTokens(data.tokens);
    setStoredUser(data);
  }

  return data;
};

/**
 * Refresh access token using the stored refresh token.
 */
const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await api.post('/api/auth/refresh', { refreshToken });
  const tokens = response.data.data.tokens;
  setTokens(tokens);
  return tokens;
};

/**
 * Logout — call API and clear local state.
 */
const logout = async () => {
  try {
    await api.post('/api/auth/logout');
  } catch {
    // Ignore errors — we clear local state regardless
  }
  clearTokens();
};

/**
 * Fetch the current user profile from the API.
 */
const getProfile = async () => {
  const response = await api.get('/api/auth/me');
  const user = response.data.data;
  setStoredUser(user);
  return user;
};

/**
 * Setup 2FA for the current user.
 */
const setup2FA = async () => {
  const response = await api.post('/api/auth/2fa/setup');
  return response.data.data;
};

/**
 * Check if the user is authenticated (has a stored access token).
 */
const isAuthenticated = () => !!getAccessToken();

const authService = {
  login,
  verify2FA,
  register,
  refreshAccessToken,
  logout,
  getProfile,
  setup2FA,
  isAuthenticated,
  getAccessToken,
  getRefreshToken,
  getStoredUser,
  clearTokens,
};

export default authService;
