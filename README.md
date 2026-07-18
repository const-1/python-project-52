# Task Manager

[![Actions Status](https://github.com/const-1/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/const-1/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=const-1_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=const-1_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=const-1_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=const-1_python-project-52)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-16-purple.svg)](https://www.postgresql.org/)
[![Render](https://img.shields.io/badge/deployed%20on-render-46a2f1.svg)](https://render.com)

**Task Manager** is a web application for managing tasks, built as part of the Hexlet educational project. It allows you to create tasks, assign executors, manage statuses and labels, and filter tasks by various criteria.

## Features

- **User management:** registration, authentication, profile editing and deletion (only for the user themselves).
- **Status management:** create, edit, and delete statuses (authenticated users only).
- **Label management:** create, edit, and delete labels (authenticated users only).
- **Task management:** create, edit, delete (only the author), view details.
- **Task filtering:** by status, executor, label, and show only your own tasks.
- **Responsive interface** with Bootstrap 5.
- **Error monitoring** via Rollbar.

## Technology Stack

- **Backend:** Python 3.12, Django 6.0, Django ORM
- **Database:** PostgreSQL (production), SQLite (development)
- **Frontend:** Bootstrap 5, Django Templates
- **Deployment:** Render.com (or other PaaS), Gunicorn
- **Monitoring:** Rollbar
- **Tools:** uv (package manager), Ruff (linter and formatter), GitHub Actions (CI/CD), SonarCloud (code quality)

## Quick Start

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 14+ (for production, SQLite works locally)
- uv (recommended) or pip

### Installation

1. **Clone the repository:**
   ```
   git clone git@github.com:const-1/python-project-52.git
   cd python-project-52
   ```

2. **Create and activate a virtual environment with uv:**
   ```
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```
   uv pip install -e .
   ```

4. **Create a .env file in the project root and add environment variables (see "Environment Variables" section).**

5. **Run database migrations:**
   ```
   uv run manage.py migrate
   ```

6. **Start the development server:**
   ```
   uv run manage.py runserver
   ```

7. **Open http://127.0.0.1:8000 in your browser.**

- Usage:

- Register a new user or log in.
- Create statuses and labels for tasks.
- Create tasks, assign executors, and attach labels.
- Use the filter form above the task table to filter by status, executor, label, or show only your tasks.
- Edit or delete tasks (only the author can delete)

- Project Commands (Makefile):

- make install – install dependencies.
- make migrate – apply migrations.
- make collectstatic – collect static files.
- make build – build the project (used on the server).
- make render-start – start the application via Gunicorn (for the server).

- Deployment:

- The project is deployed on Render.com (or any other PaaS) and is available at:
- https://your-service.onrender.com
- For deployment, use:
- Build Command: make build
- Start Command: make render-start

- Environment Variables:

- The following variables must be set in a .env file (locally) or in the service settings (on the server):
- SECRET_KEY=<your-secret-key>
- DEBUG=True  # or False for production
- DATABASE_URL=sqlite:///db.sqlite3  # or postgresql://...
- ROLLBAR_ACCESS_TOKEN=<your-rollbar-token>
- ROLLBAR_ENVIRONMENT=production  # optional

- Testing:

- Run tests with:
- uv run manage.py test
- Tests cover all CRUD operations for users, statuses, tasks, and labels, as well as filtering and access control.

- Code Quality:

- Use ruff for linting and formatting:

- ruff check .       # lint the code
- ruff check --fix . # automatically fix issues
- ruff format .      # format the code

- License:

- This project is part of the Hexlet educational program.

    




