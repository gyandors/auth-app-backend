# Auth App Backend

## Description

This is a simple user authentication system built with Django and Django REST Framework. It allows users to register, login, and logout. It also supports two-factor authentication (2FA) using TOTP.

## Setup and Run

### Windows

1. **Clone repository**

   ```bash
   git clone https://github.com/gyandors/auth-app-backend.git
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**

   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
