# Fight Oracle API

Django backend for www.fightoracle.ie

## Setup

1. Create python virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. Apply migrations

   ```bash
   python manage.py migrate
   ```

3. Run server
   ```bash
   python manage.py runserver
   ```
