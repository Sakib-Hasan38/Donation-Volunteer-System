# Donation & Volunteer Management System

A full-stack web application built with **Python** and **Django** to connect donors, volunteers, and administrators. The platform allows users to donate items or funds, apply to become volunteers, manage donation drives, and track volunteer assignments.

## Features

- **User Roles & Authentication:** Separate registration, login, and profile management for **Donors**, **Volunteers**, and **Admins**.
- **Donation Management:** Donors can submit new donations (cloth, food, money, etc.), upload item images, and view their donation history and approval status.
- **Volunteer Portal:** Users can register as volunteers, view assigned pickup/delivery tasks, and update collection statuses.
- **Admin Dashboard:** Administrators can verify donors and volunteers, approve/reject donations, assign volunteers to specific donation requests, and manage gallery items.
- **Media & Gallery:** Displays community events and donation campaigns with image uploads.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Bootstrap, JavaScript
- **Database:** SQLite3 (`db.sqlite3`)

## Project Structure

```text
donation/
├── app/            # Main Django app (models, views, urls, templates, static files)
├── donation/       # Project configuration (settings.py, urls.py, wsgi.py)
├── media/          # Uploaded images for donations, volunteers, and gallery
├── db.sqlite3      # SQLite database
└── manage.py       # Django command-line utility
```

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Donation-Volunteer-System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Django (and any required packages):**
   ```bash
   pip install django pillow
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Open in your browser:**
   Visit `http://127.0.0` to view the application.

## Author

- **Sakib Hasan** — [@Sakib-Hasan38](https://github.com)
-
