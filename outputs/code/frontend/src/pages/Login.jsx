/**
 * Login.jsx
 * Login page with email/password form and optional TOTP 2FA step.
 */

import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, verify2FA, error, clearError } = useAuth();

  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // 2FA state
  const [requires2FA, setRequires2FA] = useState(false);
  const [tempToken, setTempToken] = useState(null);
  const [totpCode, setTotpCode] = useState('');

  const redirectTo = location.state?.from?.pathname || '/dashboard';

  // --- Handle login form submit ---
  const handleLogin = async (e) => {
    e.preventDefault();
    clearError();
    setSubmitting(true);

    try {
      const result = await login(email, password);

      if (result.requiresTwoFactor) {
        setRequires2FA(true);
        setTempToken(result.tempToken);
      } else {
        navigate(redirectTo, { replace: true });
      }
    } catch {
      // Error is set in the useAuth hook
    } finally {
      setSubmitting(false);
    }
  };

  // --- Handle 2FA verification ---
  const handle2FAVerify = async (e) => {
    e.preventDefault();
    clearError();
    setSubmitting(true);

    try {
      await verify2FA(tempToken, totpCode);
      navigate(redirectTo, { replace: true });
    } catch {
      // Error is set in the useAuth hook
    } finally {
      setSubmitting(false);
    }
  };

  // ----- Styles -----
  const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f0f2f5',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  };

  const cardStyle = {
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    padding: '40px',
    width: '100%',
    maxWidth: '400px',
  };

  const inputStyle = {
    width: '100%',
    padding: '10px 12px',
    border: '1px solid #d9d9d9',
    borderRadius: '6px',
    fontSize: '14px',
    marginBottom: '16px',
    boxSizing: 'border-box',
  };

  const buttonStyle = {
    width: '100%',
    padding: '10px 16px',
    backgroundColor: '#1677ff',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '16px',
    cursor: submitting ? 'not-allowed' : 'pointer',
    opacity: submitting ? 0.7 : 1,
  };

  const errorStyle = {
    backgroundColor: '#fff2f0',
    border: '1px solid #ffccc7',
    borderRadius: '6px',
    padding: '8px 12px',
    color: '#ff4d4f',
    marginBottom: '16px',
    fontSize: '14px',
  };

  // ----- Render 2FA step -----
  if (requires2FA) {
    return (
      <div style={containerStyle}>
        <div style={cardStyle}>
          <h2 style={{ textAlign: 'center', marginBottom: '8px' }}>Two-Factor Authentication</h2>
          <p style={{ textAlign: 'center', color: '#666', marginBottom: '24px' }}>
            Enter the 6-digit code from your authenticator app.
          </p>

          {error && <div style={errorStyle}>{error}</div>}

          <form onSubmit={handle2FAVerify}>
            <input
              type="text"
              placeholder="Enter 6-digit code"
              value={totpCode}
              onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              style={{ ...inputStyle, textAlign: 'center', fontSize: '24px', letterSpacing: '8px' }}
              maxLength={6}
              autoFocus
              required
            />
            <button type="submit" style={buttonStyle} disabled={submitting || totpCode.length !== 6}>
              {submitting ? 'Verifying...' : 'Verify'}
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: '16px' }}>
            <button
              type="button"
              onClick={() => {
                setRequires2FA(false);
                setTempToken(null);
                setTotpCode('');
                clearError();
              }}
              style={{ background: 'none', border: 'none', color: '#1677ff', cursor: 'pointer' }}
            >
              Back to login
            </button>
          </p>
        </div>
      </div>
    );
  }

  // ----- Render login form -----
  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h2 style={{ textAlign: 'center', marginBottom: '8px' }}>TechNova Platform</h2>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '24px' }}>
          Sign in to your account
        </p>

        {error && <div style={errorStyle}>{error}</div>}

        <form onSubmit={handleLogin}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '4px', fontWeight: 500 }}>
            Email
          </label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={inputStyle}
            required
            autoFocus
          />

          <label htmlFor="password" style={{ display: 'block', marginBottom: '4px', fontWeight: 500 }}>
            Password
          </label>
          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
            required
          />

          <button type="submit" style={buttonStyle} disabled={submitting}>
            {submitting ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  );
}
