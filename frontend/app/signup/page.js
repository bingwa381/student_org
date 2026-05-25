'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { register } from '../../lib/api';

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    gender: 'Male',
    date_of_birth: '',
    phone: '',
    course: '',
    year_of_study: '1st Year',
    payment_amount: 10000,
    payment_reference: '',
    payment_confirmed: false,
  });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await register(form);
      router.push('/dashboard');
    } catch (err) {
      setError(err.message || 'Registration failed.');
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 py-16">
      <div className="container mx-auto px-4">
        <div className="card mx-auto max-w-3xl p-10">
          <h1 className="text-3xl font-semibold text-slate-900">Create a student account</h1>
          <p className="mt-2 text-slate-600">Submit your registration and wait for admin approval.</p>
          <form onSubmit={handleSubmit} className="mt-8 grid gap-6">
            {error && <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Username</span>
                <input type="text" name="username" value={form.username} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Email</span>
                <input type="email" name="email" value={form.email} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-medium text-slate-700">First name</span>
                <input type="text" name="first_name" value={form.first_name} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Last name</span>
                <input type="text" name="last_name" value={form.last_name} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Password</span>
                <input type="password" name="password" value={form.password} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Course</span>
                <input type="text" name="course" value={form.course} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Phone</span>
                <input type="text" name="phone" value={form.phone} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-slate-700">Year of study</span>
                <select name="year_of_study" value={form.year_of_study} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3">
                  <option>1st Year</option>
                  <option>2nd Year</option>
                  <option>3rd Year</option>
                  <option>4th Year</option>
                  <option>Graduate</option>
                </select>
              </label>
            </div>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Date of birth</span>
              <input type="date" name="date_of_birth" value={form.date_of_birth} onChange={handleChange} className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3" />
            </label>
            <div className="flex items-center gap-3">
              <input type="checkbox" name="payment_confirmed" checked={form.payment_confirmed} onChange={handleChange} className="h-5 w-5 rounded" />
              <span className="text-sm text-slate-700">I confirm the payment of 10,000 TSH.</span>
            </div>
            <button type="submit" className="w-full rounded-2xl bg-slate-900 px-5 py-3 text-white transition hover:bg-slate-800">Create account</button>
          </form>
        </div>
      </div>
    </main>
  );
}
