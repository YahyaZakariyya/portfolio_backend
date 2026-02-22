# Portfolio Backend — Django + DRF

A production-ready **Django REST Framework** backend for a developer portfolio. Engineered with clean architecture, read-only public APIs, and a fully customized admin panel for content management.

---

## ⚡ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   Client (Frontend)              │
│              React / Next.js / etc.              │
└─────────────┬───────────────────────┬────────────┘
              │  GET requests only    │
              ▼                       ▼
┌─────────────────────────────────────────────────┐
│            Django REST Framework API             │
│                                                  │
│  /api/profile/     → ProfileView (APIView)       │
│  /api/skills/      → SkillListView (ListAPI)     │
│  /api/projects/    → ProjectListView (ListAPI)   │
│  /api/projects/<slug>/ → ProjectDetailView       │
│  /api/experience/  → ExperienceListView (ListAPI)│
│  /api/education/   → EducationListView (ListAPI) │
│                                                  │
│  ┌──────────────────────────────────────────┐    │
│  │ Middleware Stack                          │    │
│  │  ├─ SecurityMiddleware                   │    │
│  │  ├─ WhiteNoiseMiddleware (static files)  │    │
│  │  ├─ CorsMiddleware (CORS headers)        │    │
│  │  ├─ SessionMiddleware                    │    │
│  │  └─ AuthenticationMiddleware             │    │
│  └──────────────────────────────────────────┘    │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│                MySQL Database                    │
│                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ Profile  │ │  Skill   │ │   Project    │    │
│  │ (1 row)  │ │ (N rows) │ │  (N rows)    │    │
│  └──────────┘ └──────────┘ └──────────────┘    │
│  ┌──────────────┐ ┌────────────────┐            │
│  │  Experience  │ │   Education    │            │
│  │  (N rows)    │ │   (N rows)     │            │
│  └──────────────┘ └────────────────┘            │
└─────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Framework      | Django 6.0                          |
| API Layer      | Django REST Framework 3.16          |
| Database       | MySQL (SQLite for local dev)        |
| Static Files   | WhiteNoise                          |
| CORS           | django-cors-headers                 |
| Config         | python-decouple (.env)              |
| WSGI Server    | Gunicorn                            |

---

## 📁 Project Structure

```
portfolio_backend/
├── manage.py
├── requirements.txt
├── gunicorn.conf.py
├── .env.example
├── .gitignore
│
├── portfolio_backend/          # Project config
│   ├── settings/
│   │   ├── __init__.py         # Auto-selects dev/prod
│   │   ├── base.py             # Shared settings
│   │   ├── development.py      # Dev overrides (SQLite, browsable API)
│   │   └── production.py       # Prod security (HSTS, SSL, etc.)
│   ├── urls.py                 # Root URL config
│   ├── wsgi.py
│   └── asgi.py
│
└── portfolio/                  # Main app
    ├── models.py               # 5 models + abstract base
    ├── serializers.py          # Read-only serializers
    ├── views.py                # GET-only API views
    ├── urls.py                 # App URL patterns
    ├── admin.py                # Customized admin
    └── migrations/
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd portfolio_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Database Setup

**For MySQL (production):**
```bash
mysql -u root -p -e "CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
# Update DB_* variables in .env
export DJANGO_ENV=production
```

**For SQLite (development — default):**
```bash
# No setup needed, works out of the box
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

| Method | Endpoint                  | Description                    |
|--------|---------------------------|--------------------------------|
| GET    | `/`                       | API root (endpoint discovery)  |
| GET    | `/api/profile/`           | Developer profile (singleton)  |
| GET    | `/api/skills/`            | All skills by category         |
| GET    | `/api/projects/`          | All projects (list view)       |
| GET    | `/api/projects/<slug>/`   | Project detail by slug         |
| GET    | `/api/experience/`        | Work experience timeline       |
| GET    | `/api/education/`         | Education history              |

> ⚠️ Only `GET` and `OPTIONS` are allowed. All other methods return `405 Method Not Allowed`.

---

## 🔐 Security

- **No authentication required** — public read-only APIs
- **CORS restricted** to configured frontend origins
- **Rate limiting** — 100 req/min (dev), 60 req/min (prod)
- **Production hardening** — HSTS, SSL redirect, secure cookies, XSS protection
- **Environment variables** — no secrets in code

---

## 🏭 Production Deployment

### Using Gunicorn

```bash
export DJANGO_ENV=production
python manage.py collectstatic --noinput
gunicorn -c gunicorn.conf.py portfolio_backend.wsgi:application
```

### Environment Variables (Production)

```env
SECRET_KEY=<generate-a-strong-50-char-key>
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=<strong-password>
DB_HOST=localhost
DB_PORT=3306
CORS_ALLOWED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
```

---

## 🧑‍💼 Admin Panel

Access at `/admin/` with your superuser credentials.

**Features:**
- Custom list displays with key fields
- Inline ordering via `list_editable`
- Search across names, descriptions
- Filter by category (Skills), featured status (Projects), current status (Experience)
- Auto-slug generation for Projects
- Singleton enforcement for Profile (only one allowed)
- Organized fieldsets with collapsible timestamp sections

---

## 📊 Data Models

### Profile (Singleton)
`full_name` · `title` · `bio` · `years_of_experience` · `email` · `linkedin_url` · `github_url` · `resume_url` · `avatar_url`

### Skill
`name` · `category` (Backend/Frontend/DevOps/Database/Tools/Other) · `proficiency_level` (1-100) · `icon` · `order`

### Project
`name` · `slug` · `description` · `tech_stack` (JSON) · `github_url` · `live_url` · `thumbnail_url` · `architecture_summary` · `key_features` (JSON) · `featured` · `order`

### Experience
`company_name` · `role` · `start_date` · `end_date` · `description` · `technologies_used` (JSON) · `company_url` · `is_current` · `order` · **computed: `duration`**

### Education
`institute_name` · `degree` · `field_of_study` · `start_year` · `end_year` · `description` · `grade` · `order`

---

## 📝 Dev Credentials (Local Only)

```
Admin URL: http://localhost:8000/admin/
Username:  admin
Password:  admin123
```
