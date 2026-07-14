# Trekking Management System

A full stack Trek Management System developed using **Flask** , **Vue.js 3**, **SQLite**, **SQLAlchemy**, **JWT** **Authentication**, **Celery**, and **Redis**.
The application follows a REST API architecture with a Vue.js Single Page Application frontend. It provides separate dashboards for Admin, Staff, and Trekkers, enabling efficient management of trekking events, bookings, staff assignments, user profiles, scheduled background jobs, and performance optimization using Redis caching.

---

# Project Overview

The Trekking Management System simplifies the process of organizing and managing trekking events. It enables administrators to manage treks and staff members, staff to supervise assigned treks and participants, and trekkers to browse, book, and track their trekking history. Trekker can also export booking history , and recieve automated email remiders.
The backend is implemented using Flask REST APIs, while the frontend is built as a Vue.js Single Page Application communicating through JSON APIs.
---

#  Features

##  Admin

- Secure JWT Authentication
- Dashboard Analytics
- Manage Treks (Create, Update, Delete)
- Manage Staff Members
- Manage Trekkers
- Activate / Deactivate Users
- Assign Staff to Treks
- Prevent Staff Double Assignment
- Manage Trek Status
- View All Bookings
- Search and Filter Data

---

##  Staff

- Secure Login
- Dashboard
- View Assigned Treks
- Update Trek Status
- View Trek Participants
- Manage Profile
---

## Trekker

- Register and Login
- Browse available treks
- Search treks by name
- Filter treks by difficulty
- Filter treks by duration
- View detailed trek information
- Book available treks
- Prevent duplicate bookings
- Cancel bookings
- View complete booking history
- Manage personal profile
- Edit profile
- Export Trekking History as CSV

---

# Additional Features

- RESTful API Architecture
- JWT Authentication
- Role-Based Authorization
- Password Hashing using Werkzeug
- Email Notifications using Flask-Mail
- Background Jobs using Celery
- Redis Message Broker
- Redis Result Backend
- Redis API Caching
- Responsive Bootstrap UI
- Search & Filtering
- Staff Date Conflict Validation
- Duplicate Booking Prevention
- Automatic Trek Slot Management

---
# Background Jobs (Celery + Redis)
- Daily Reminder
Sends reminder emails for upcoming treks
Runs automatically every day
- Monthly Admin Report
Generates monthly trekking report
Includes:
Number of completed treks
Number of participants
Most popular trek
Sends HTML report via email
- CSV Export
User-triggered asynchronous CSV export
Generates trekking history
Emails CSV file once export is complete
- Performance Optimization
Redis-based API Caching
Cached Frequently Accessed Trek APIs
Automatic Cache Expiry
---
# Technologies Used

| Technology | Purpose |
|------------|---------|
| Flask | Backend web framework |
| SQLAlchemy | ORM for SQLite database |
| SQLite | Database |
| Vue.js3|  Fronted SPA |
| Bootstrap 5 | Responsive frontend |
| HTML5 | Page structure |
| CSS3 | Styling |
| Werkzeug | Password hashing |
| Celery | Background Jobs|
| Redis | Celery Broker, Result Backend, Cache |
| Vue Router  | Client side routing |
| Vite  | Frontend CDevelopment and Build Tool|
| Flask-CORS  | Cross-origin resource sharing|
| Flask-JWT-Extended | JWT Authentication |
| Flask Mail| Email Services |

---

# Project Structure

```
trekking-management-v2
│
├── README.md
│
├── backend
│   ├── app.py
│   ├── config.py
│   ├── create_db.py
│   ├── models.py
│   ├── extensions.py
│   ├── celery_worker.py
│   │
│   ├── routes
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── staff.py
│   │   ├── trek.py
│   │   └── trekker.py
│   │
│   ├── tasks
│   │   └── tasks.py
│   │
│   ├── templates
│   │   ├── reminder.html
│   │   └── monthly_report.html
│   │
│   └── exports
│
├── frontend
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   │
│   └── src
│       ├── main.js
│       ├── App.vue
│       ├── router
│       ├── views
│       └── components
|
|── requirements.txt
|── .gitignore
```

---

# Database Schema

The project consists of five database tables.

## User

Stores all application users.

**Fields**

- id
- name
- email
- password
- phone
- role
- status
- created_at

roles

- admin
- staff
- trekker


---

## Trek

Stores trekking event information.

**Fields**

- id
- trek_name
- location
- difficulty
- duration
- description
- total_slots
- available_slots
- assigned_staff_id
- status
- start_date
- end_date
- created_at

Status values

- Penidng
- Open
- Ongoing
- Completed
- Closed

---

## Booking

Stores trekking booking records.

**Fields**

- id
- user_id
- trek_id
- booking_date
- status

Booking Status

- Booked
- Cancelled
- Completed

---

# Database Relationships

- One Staff → Many Treks
- One Trek → Many Bookings
- One Trekker → Many Bookings

---

# REST API Modules
The backend exposes REST APIs for:
- Authentication
- Admin Management
- Staff Management
- Trek Management
- Trek Booking
- User Profile
- Dashboard Analytics
- CSV Export
- Background Jobs

---

# How to Run the Project

## 1. Clone Repository

```bash
git clone https://github.com/24f1002360/trekking-management-v2.git
cd trekking-management-v2
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate

Mac/Linux

```bash
source venv/bin/activate
```
Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

---

## 5. Start Redis 

```bash
redis-server
```

---

## 6. Start Celery Worker

```bash
cd ../backend
celery -A celery_worker.celery worker --loglevel=info
```

---


## 7. Start Celery Beat

```bash
cd ../backend
celery -A celery_worker.celery beat --loglevel=info
```

---

## 8. Create Database

```bash
cd ../backend
python create_db.py
```

---

## 9. Start Backend

```bash
cd ../backend
python app.py
```
---

## 10. Start Frontend

```bash
cd ../frontend
npm run dev
```

Backend

```
http://127.0.0.1:5000
```

Frontend

```
http://localhost:5173
```
---

# Application Workflow

```
                User Login
                    │
        ┌───────────┼───────────┐
        │           │           |
     Admin       Staff      Trekker
        │           │           │
        │           │           │
Create Treks   View Assigned   Browse Treks
Assign Staff      Treks         Book Trek
Manage Users   Update Status   View History
View Reports                  Export CSV
        |
Background Jobs (Celery + Redis)
        │
        ├── Daily Reminder Emails
        ├── Monthly HTML Report
        └── Async CSV Export

---
