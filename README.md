# Khamsat Clone – Backend API

A production-ready Django REST API that powers a freelancer marketplace (Khamsat-style). It includes user auth (JWT), services listings, transactions and wallet, ratings, dashboards, chat via WebSockets, and background jobs with Celery.

## Features

- JWT auth (access/refresh) with blacklist
- Users and profiles
- Services listing and management
- Transactions and order lifecycle
- Wallet with balances and signals
- Ratings and reviews
- Real-time chat via Django Channels + Redis
- Background jobs with Celery + Celery Beat
- API docs with drf-spectacular (Swagger/Redoc)

## Tech Stack

- Django 5.2, Django REST Framework
- Channels + channels-redis
- Celery 5.5 with Redis
- PostgreSQL
- drf-spectacular
- SimpleJWT
- django-redis cache

## Project Structure

- `manage.py`
- `src/` Django project
  - `settings.py`, `urls.py`, `asgi.py`, `wsgi.py`, `celery.py`, `routing.py`
- Apps
  - `users`, `user_profile`, `services`, `transaction`, `wallet`, `rating`, `chat`, `dashboard`, `admin`
- `media/` for uploads
- `.env` for configuration (gitignored)
- `requirements.txt`

## Requirements

- Python 3.11+ (recommended)
- PostgreSQL 14+ (or compatible)
- Redis 6+
- pip / virtualenv or uv/poetry
- Access to SMTP (Gmail) or Brevo API key for emails

## Environment Variables

Create a `.env` file in `src/` (same folder as `manage.py`):

```
# Django
SECRET_KEY=your-secret-key
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1

# Postgres
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1

# Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/2
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/3

# Email
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=app_password

# Optional
BREVO_API_KEY=your_brevo_key
```

Notes:
- `ALLOWED_HOSTS` is set in env; code’s `settings.py` currently has `ALLOWED_HOSTS = []`. Adjust for production.
- `CACHES` default is pinned to `redis://127.0.0.1:6379/1`. Change if needed.

## Installation

- Create and activate a virtual environment.
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Apply migrations:

```bash
python manage.py migrate
```

- (Optional) Create a superuser:

```bash
python manage.py createsuperuser
```

- Collect static (for production):

```bash
python manage.py collectstatic --noinput
```

## Running the App (Local)

- Start Redis and Postgres
- Start Django (ASGI ready):

```bash
python manage.py runserver
```

- Start Celery worker:

```bash
celery -A src worker -l info
```

- Start Celery Beat (scheduled tasks):

```bash
celery -A src beat -l info
```

- API Docs:
  - Swagger UI: http://127.0.0.1:8000/api/docs/
  - Redoc: http://127.0.0.1:8000/api/redoc/
  - Schema: http://127.0.0.1:8000/api/schema/

## WebSockets

- ASGI app set in `src/asgi.py` with routing in `src/routing.py`.
- Redis channel layer configured via env `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`.
- Chat consumers in `chat/consumers.py`; websocket URL patterns in `chat/routing.py`.

## JWT Auth

- SimpleJWT configured in `REST_FRAMEWORK` and `SIMPLE_JWT`.
- Default lifetimes:
  - Access: 10 minutes
  - Refresh: 7 days
- Auth header: `Authorization: Bearer <token>`

## Key URLs

- `auth/` → `users` endpoints
- `profile/` → `user_profile` endpoints
- `services/` → services endpoints
- `transaction/` → transactions and orders
- `chat/` → chat REST APIs; WS via Channels
- `rating/` → ratings and reviews
- `dashboard/` → dashboards & scheduled tasks
- `wallet/` → wallet operations
- `admin/` → custom admin endpoints (Django admin UI is commented out)

Check each app’s `urls.py` for details.

## Caching

- `django-redis` configured at `redis://127.0.0.1:6379/1`. If your Redis is on another host/DB, update `CACHES` in `settings.py`.

## Emails

- SMTP via Gmail:
  - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (App Password)
- `DEFAULT_FROM_EMAIL` is the host user.

Alternatively, set `BREVO_API_KEY` and connect through your email sending logic if implemented.

