import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-100 py-16">
      <div className="container mx-auto px-4">
        <div className="card p-10">
          <div className="grid gap-8 lg:grid-cols-2 items-center">
            <div>
              <span className="inline-flex rounded-full bg-blue-100 px-4 py-1 text-sm font-semibold text-blue-700">
                Education Management
              </span>
              <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900">A modern student registration and management system.</h1>
              <p className="mt-4 text-slate-600">Secure authentication, role-based dashboards, registration approval, attendance, exams, fees, and analytics in one unified experience.</p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/login" className="rounded-lg bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700">
                  Login
                </Link>
                <Link href="/signup" className="rounded-lg border border-slate-300 px-6 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-50">
                  Sign Up
                </Link>
              </div>
            </div>
            <div className="rounded-3xl bg-gradient-to-br from-slate-900 to-blue-600 p-10 text-white shadow-xl">
              <h2 className="text-2xl font-semibold">Campus dashboard</h2>
              <p className="mt-4 text-slate-200">Role-aware interface for admins, teachers, and students with fast access to approvals, announcements, and metrics.</p>
              <div className="mt-8 grid gap-4 sm:grid-cols-2">
                <div className="rounded-3xl bg-white/10 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-300">Students</p>
                  <p className="mt-4 text-3xl font-semibold">1,250+</p>
                </div>
                <div className="rounded-3xl bg-white/10 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-300">Courses</p>
                  <p className="mt-4 text-3xl font-semibold">128</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
