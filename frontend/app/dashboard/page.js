'use client';

import { useEffect, useState } from 'react';
import { fetchDashboard } from '../../lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboard()
      .then((data) => setStats(data))
      .catch(() => setError('Unable to load dashboard data.'));
  }, []);

  return (
    <main className="min-h-screen bg-slate-100 py-16">
      <div className="container mx-auto px-4">
        <div className="card p-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-semibold text-slate-900">Dashboard</h1>
              <p className="mt-2 text-slate-600">Quick insight into enrollment, approvals, and activity.</p>
            </div>
            <button className="rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Refresh</button>
          </div>
          {error && <div className="mt-6 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
          {stats ? (
            <div className="mt-8 grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
              <div className="rounded-3xl bg-slate-950 p-6 text-white">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Total students</p>
                <p className="mt-4 text-4xl font-semibold">{stats.total_students}</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Approved</p>
                <p className="mt-4 text-4xl font-semibold text-slate-900">{stats.approved_students}</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Pending</p>
                <p className="mt-4 text-4xl font-semibold text-slate-900">{stats.pending_students}</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Teachers</p>
                <p className="mt-4 text-4xl font-semibold text-slate-900">{stats.total_teachers}</p>
              </div>
            </div>
          ) : (
            <div className="mt-8 rounded-3xl bg-white p-8 shadow-sm">
              <p className="text-slate-500">Loading statistics...</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
