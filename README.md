# 🎓 StudExa — Student Progress Monitoring System

A full-stack web application built with **Django + SQLite** for tracking student academic achievements, automatic point calculation, and faculty verification.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ installed
- pip (Python package manager)

### 1. Install & Run (Mac/Linux)
```bash
cd spms_project
bash setup.sh
python3 manage.py runserver
```

### 1. Install & Run (Windows)
```
cd spms_project
setup.bat
python manage.py runserver
```

### 2. Open in browser
```
http://127.0.0.1:8000
```

---

## 🔑 Login Credentials (after setup)

| Role    | Email                | Password   |
|---------|----------------------|------------|
| Admin   | admin@spms.com       | admin123   |
| Faculty | faculty@spms.com     | faculty123 |
| Student | student@spms.com     | student123 |

---

## 📁 Project Structure

```
spms_project/
├── manage.py
├── requirements.txt
├── setup.sh          ← Mac/Linux setup
├── setup.bat         ← Windows setup
├── spms_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── spms/
    ├── models.py     ← User, Achievement, PointRule
    ├── views.py      ← All role-based views
    ├── forms.py      ← Registration, Login, Upload forms
    ├── admin.py      ← Django admin config
    ├── urls.py       ← All URL routes
    ├── templates/
    │   └── spms/
    │       ├── base.html
    │       ├── index.html          ← Landing page
    │       ├── login.html
    │       ├── register.html
    │       ├── student_dashboard.html
    │       ├── my_submissions.html
    │       ├── faculty_dashboard.html
    │       ├── review_achievement.html
    │       ├── admin_dashboard.html
    │       ├── manage_users.html
    │       └── leaderboard.html
    └── management/
        └── commands/
            └── seed_data.py  ← Initial data seeder
```

---

## 🏆 Point System

| Achievement                    | Points |
|--------------------------------|--------|
| Hackathon Winner (National)    | 50 pts |
| Hackathon Winner (International)| 70 pts|
| Runner Up (National)           | 35 pts |
| Hackathon Participation        | 10 pts |
| Research — Indexed Journal     | 60 pts |
| Research — Int'l Conference    | 40 pts |
| Patent — Granted               | 100 pts|
| Patent — Filed                 | 50 pts |
| Certificate — AWS/Google/MS    | 30 pts |
| Certificate — NPTEL/Coursera   | 15 pts |

*Point rules can be edited by admin at `/admin/spms/pointrule/`*

---

## 🔄 Workflow

1. **Student registers** → selects role as Student
2. **Student uploads achievement** → fills form, uploads proof document
3. **Points auto-assigned** based on category + level + result rules
4. **Faculty reviews** → approves or rejects with remarks
5. **On approval** → points added to student's total score
6. **Dashboard updates** → student sees score, rank, and breakdown

---

## ⚙️ Admin Panel

Django's built-in admin is available at:
```
http://127.0.0.1:8000/admin/
```
Login with admin@spms.com / admin123

From admin you can:
- Add/edit Point Rules
- Manage all users
- Bulk approve/reject achievements
- View all data

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (db.sqlite3)
- **Frontend**: HTML5, CSS3 (no frameworks)
- **Auth**: Django's built-in auth with custom User model
- **File uploads**: Django FileField + Pillow
