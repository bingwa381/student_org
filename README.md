# Student Management & Registration System

This repository contains a Django backend and a Next.js frontend for a modern student management system.

## Features
- Role-based authentication for students, teachers, and admins
- Student registration, approval workflow, and profile management
- Department, class, subject, attendance, payment, exam, and result models
- REST API with JWT authentication and Swagger documentation
- Responsive React/Next.js frontend with Tailwind CSS
- Docker Compose setup with PostgreSQL
- Demo seed command for sample data

## Backend Setup

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and seed demo data:

```bash
python manage.py migrate
python manage.py seed_demo
```

3. Start the Django server:

```bash
python manage.py runserver
```

4. API docs are available at `http://localhost:8000/swagger/`.

## Frontend Setup

1. Change into the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

2. Open `http://localhost:3000` in your browser.

## Docker Setup

Run everything with Docker Compose:

```bash
docker compose up --build
```

## Sample Accounts

- Admin: `admin` / `Admin1234`
- Teacher: `teacher1` / `Teacher1234`
- Student: `student1` / `Student1234`

## Notes

- Update `SECRET_KEY` in environment variables for production.
- Use `DATABASE_URL` to connect to PostgreSQL in production.
