'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login } from '../../lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await login({ username, password });
      router.push('/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed.');
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 py-16">
      <div className="container mx-auto px-4">
        <div className="card mx-auto max-w-xl p-10">
          <h1 className="text-3xl font-semibold text-slate-900">Login to your portal</h1>
          <p className="mt-2 text-slate-600">Use your student or teacher credentials to continue.</p>
          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            {error && <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Username</span>
              <input value={username} onChange={(e) => setUsername(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 focus:border-blue-500 focus:outline-none" />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Password</span>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 focus:border-blue-500 focus:outline-none" />
            </label>
            <button type="submit" className="w-full rounded-2xl bg-slate-900 px-5 py-3 text-white transition hover:bg-slate-800">Sign in</button>
          </form>
        </div>
      </div>
    </main>
  );
}
