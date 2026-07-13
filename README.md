# 🎓 StudExa — Student Progress Monitoring System

> A full-stack Student Progress Monitoring System built with **Django**, enabling students to submit academic achievements, automatically calculate reward points, and streamline faculty verification through a role-based workflow.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-darkgreen?style=for-the-badge&logo=django)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

# 📌 Overview

StudExa is a centralized platform designed for colleges and universities to digitally manage student achievements.

Instead of maintaining spreadsheets or paper records, students can submit achievements online, faculty members verify submissions, and administrators manage point rules through a single dashboard.

The system automatically awards points based on predefined achievement categories and maintains a leaderboard to encourage student participation.

---

# ✨ Features

## 👨‍🎓 Student Portal

- Student Registration & Login
- Secure Authentication
- Upload Achievement Certificates
- Automatic Point Calculation
- View Submission Status
- Track Total Points
- Personal Dashboard
- Leaderboard Ranking

---

## 👨‍🏫 Faculty Portal

- Review Submitted Achievements
- Approve / Reject Requests
- Add Review Remarks
- View Pending Submissions
- Manage Student Records

---

## 👨‍💼 Admin Portal

- Manage Users
- Configure Point Rules
- Bulk Approve/Reject Achievements
- Access Complete Database
- Dashboard Analytics

---

# 🚀 Key Highlights

✅ Role-Based Authentication

✅ Automatic Point Calculation

✅ Achievement Verification Workflow

✅ Certificate Upload Support

✅ Leaderboard System

✅ Admin Configurable Rules

✅ Responsive Dashboard

✅ Secure Django Authentication

---

# 🏆 Achievement Point System

| Achievement | Points |
|-------------|--------|
| 🥇 Hackathon Winner (National) | 50 |
| 🌍 Hackathon Winner (International) | 70 |
| 🥈 Runner-Up (National) | 35 |
| 🎯 Hackathon Participation | 10 |
| 📄 Indexed Journal Publication | 60 |
| 🌐 International Conference | 40 |
| 🧠 Patent Granted | 100 |
| 📑 Patent Filed | 50 |
| ☁ AWS / Google / Microsoft Certification | 30 |
| 📚 NPTEL / Coursera Certification | 15 |

> Point rules are fully configurable by the administrator.

---

# 🔄 System Workflow

```text
Student Registration
        │
        ▼
Student Login
        │
        ▼
Submit Achievement
        │
        ▼
Upload Proof Document
        │
        ▼
Automatic Point Calculation
        │
        ▼
Faculty Review
      ┌───────┐
      │       │
 Approved   Rejected
      │
      ▼
Points Added
      │
      ▼
Dashboard Updated
      │
      ▼
Leaderboard Updated
```

---

# 📂 Project Structure

```
spms_project/
│
├── manage.py
├── requirements.txt
├── setup.sh
├── setup.bat
│
├── spms_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── spms/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── admin.py
    ├── urls.py
    ├── templates/
    │   └── spms/
    └── management/
        └── commands/
            └── seed_data.py
```

---


## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Migrations

```bash
python manage.py migrate
```

---

## Seed Initial Data

```bash
python manage.py seed_data
```

---

## Run Server

```bash
python manage.py runserver
```

Visit

```
http://127.0.0.1:8000/
```

---



# 🛠 Tech Stack

| Technology | Usage |
|------------|------|
| Python | Backend Language |
| Django 4.2 | Web Framework |
| SQLite | Database |
| HTML5 | UI |
| CSS3 | Styling |
| Django Templates | Frontend Rendering |
| Pillow | Image/File Handling |

---

# 📸 Screens

- Landing Page
- Login
- Registration
- Student Dashboard
- Faculty Dashboard
- Admin Dashboard
- Achievement Submission
- Leaderboard

> *(Add screenshots here after uploading them to GitHub.)*

---

# 📈 Future Enhancements

- 📧 Email Notifications
- 📱 Mobile Responsive UI
- 📊 Analytics Dashboard
- 🏅 Digital Badge System
- 📄 PDF Report Generation
- ☁ Cloud Storage Support
- 🔔 Real-Time Notifications
- 📥 Excel Export
- REST API Integration

---

# 💡 Why StudExa?

Managing student achievements manually is time-consuming and error-prone.

StudExa automates the entire lifecycle—from submission and verification to automatic point allocation—providing transparency, efficiency, and a centralized platform for students, faculty, and administrators.

---



## ⭐ If you found this project useful, don't forget to star the repository!
