const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

async function request(path, options = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const body = await response.json().catch(() => null);

  if (!response.ok) {
    const error = body?.detail || body?.message || 'API request failed';
    throw new Error(error);
  }

  return body;
}

export async function login(credentials) {
  const data = await request('/auth/token/', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
  localStorage.setItem('authToken', data.access);
  return data;
}

export async function register(payload) {
  const data = await request('/students/register/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
  return data;
}

export async function fetchDashboard() {
  return request('/dashboard/');
}
