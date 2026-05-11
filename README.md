# 🗓️ Event Management System

A full-featured Django web application for managing events, users, and RSVPs — with role-based access control, email notifications, and an admin dashboard.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [User Roles](#user-roles)
- [Key Functionality](#key-functionality)
- [Email Configuration](#email-configuration)
- [Running the Project](#running-the-project)

---

## ✨ Features

- User registration with **email-based account activation**
- Role-based access control: **Admin**, **Organizer**, **Participant**
- Organizer dashboard with event statistics (total, upcoming, past)
- Create, edit, and view events with category support
- Participants can **RSVP to events** and receive confirmation emails
- Search events by name or date
- User management: list, view details, assign roles, delete users
- Group/permission management
- Personal RSVP dashboard for participants

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 |
| Database | SQLite (default) / PostgreSQL-ready |
| Auth | Django built-in auth + token-based email activation |
| Email | Django SMTP backend |
| Image handling | Pillow |
| Static files | WhiteNoise |
| Environment config | python-decouple |
| Production server | Gunicorn |

---

## 📁 Project Structure

```
project-root/
├── core/                          # Shared templates app
│   └── templates/
│       ├── base.html
│       ├── homepage.html
│       ├── loggednav.html
│       ├── nonlogged.html
│       └── nopermission.html
│
├── events/                        # Events app
│   ├── models.py                  # Event, Category models
│   ├── views.py                   # Event CRUD, RSVP, dashboard
│   ├── forms.py
│   └── signals.py
│
├── users/                         # Users app
│   ├── models.py
│   ├── views.py                   # Auth, role management, user CRUD
│   ├── forms.py
│   └── signals.py                 # Auto-assign group, send activation email
│
├── event_management_project/      # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/                     # Global templates directory
├── static/                        # CSS, images
├── staticfiles/                   # Collected static files
├── media/                         # Uploaded media
│   └── media_asset/
├── .env                           # Environment variables (not committed)
├── manage.py
├── requirements.txt
├── populate_db.py                 # DB seeding script
└── db.sqlite3
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- A virtual environment tool (venv or similar)

### Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <project-folder>
```

**2. Create and activate a virtual environment**
```bash
python -m venv event_env
source event_env/bin/activate        # Linux/macOS
event_env\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root (see [Environment Variables](#environment-variables) below).

**5. Apply migrations**
```bash
python manage.py migrate
```

**6. (Optional) Populate the database with sample data**
```bash
python manage.py populate_db
```

**7. Create a superuser**
```bash
python manage.py createsuperuser
```

**8. Collect static files**
```bash
python manage.py collectstatic
```

**9. Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django
SECRET_KEY=your-secret-key-here

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your account password.

---

## 👥 User Roles

The system uses Django's group-based permissions with three roles:

| Role | Permissions |
|---|---|
| **Admin** | Full access — manage users, assign roles, create groups, delete participants |
| **Organizer** | Access to organizer dashboard, create and edit events |
| **Participant** | Browse events, RSVP, view personal RSVP dashboard |

> New users are automatically assigned the **Participant** role upon registration via a post-save signal.

---

## ⚙️ Key Functionality

### Authentication Flow
- Register → receive activation email → click link → account activated → sign in

### Event Management (Organizer/Admin)
- Create events with name, date, time, location, category, and image
- Edit existing events
- View organizer dashboard filtered by all / upcoming / past events

### RSVP (Participant)
- Browse and search all events
- RSVP to an event (one-time, duplicate prevented)
- Receive a confirmation email upon RSVP
- View all RSVPd events on personal dashboard

### Admin Panel
- Assign roles to users
- Create permission groups
- View user list with search
- Delete users

---

## 📧 Email Configuration

The project uses Django's SMTP backend. Two automatic emails are sent:

1. **Account Activation Email** — sent on user registration via `users/signals.py`
2. **RSVP Confirmation Email** — sent when a participant RSVPs to an event via `events/views.py`

Both use `EMAIL_HOST_USER` defined in your `.env`.

---

## ▶️ Running the Project

**Development:**
```bash
python manage.py runserver
```

**Production (with Gunicorn):**
```bash
gunicorn event_management_project.wsgi:application --bind 0.0.0.0:8000
```

---

## 📦 Requirements

See [`requirements.txt`](requirements.txt) for the full list. Key packages:

- `Django==5.2`
- `Pillow` — image handling
- `python-decouple` — environment variable management
- `gunicorn` — production WSGI server
- `whitenoise` — static file serving
- `psycopg2-binary` — PostgreSQL support (if switching from SQLite)

---

## 📝 License

This project is for educational/personal use. Feel free to adapt it for your own needs.