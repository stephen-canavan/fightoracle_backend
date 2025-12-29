# Deployment Checklist for Fight Predictor API

## 🔴 CRITICAL - Must Fix Before Deployment

### Security Issues

1. **SECRET_KEY** - Currently hardcoded. Must use environment variable:

   ```python
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

   Generate a new secret key: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

2. **DEBUG** - Set to `False` in production. Use environment variable:

   ```python
   DEBUG = os.getenv("DEBUG", "False").lower() == "true"
   ```

3. **JWT Token Lifetimes** - Currently 10s/15s (likely a bug). Should be:

   - ACCESS_TOKEN_LIFETIME: 15 minutes (900 seconds) or 1 hour
   - REFRESH_TOKEN_LIFETIME: 7 days or 30 days

4. **ALLOWED_HOSTS** - Currently `["*"]`. Set to your actual domain:

   ```python
   ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
   ```

5. **CORS** - `CORS_ALLOW_ALL_ORIGINS = True` is insecure. Remove this and use:

   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://your-frontend-domain.com",
   ]
   ```

6. **Security Headers** - Add these for HTTPS:
   ```python
   SECURE_SSL_REDIRECT = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

### Database

7. **SQLite → PostgreSQL/MySQL** - SQLite is not suitable for production:
   - Install PostgreSQL: `sudo apt-get install postgresql postgresql-contrib`
   - Update DATABASES setting to use PostgreSQL
   - Install psycopg2: `pipenv install psycopg2-binary`

### Static Files

8. **STATIC_ROOT** - Required for production:
   ```python
   STATIC_ROOT = BASE_DIR / "staticfiles"
   ```
   Run `python manage.py collectstatic` before deployment

### Environment Variables

9. **Secrets Management** - Use systemd environment file (recommended) instead of `.env`:

   - Create `/etc/fight_predictor/env` with your secrets
   - Set permissions: `sudo chmod 600 /etc/fight_predictor/env`
   - See `SECRETS_MANAGEMENT.md` for detailed instructions

   **For development only**, you can use `.env` file (never commit):

   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgresql://user:password@localhost:5432/fight_predictor
   SECURE_COOKIE=True
   ```

   Set permissions: `chmod 600 .env`

## 🟡 IMPORTANT - Should Fix

### Code Quality

11. **Remove debug print statement** - Already fixed in `api/views/token.py`

12. **Logging Configuration** - Add proper logging:
    ```python
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'django.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
    ```

### Missing Files

13. **.gitignore** - Create to exclude:

    - `*.pyc`, `__pycache__/`
    - `.env`
    - `db.sqlite3`
    - `staticfiles/`
    - `logs/`
    - `*.log`

14. **requirements.txt** - Generate from Pipfile:
    ```bash
    pipenv requirements > requirements.txt
    ```

### Deployment Files

15. **WSGI Server** - Install gunicorn:

    ```bash
    pipenv install gunicorn
    ```

16. **Create gunicorn config** - `gunicorn_config.py`:

    ```python
    bind = "0.0.0.0:8000"
    workers = 3
    timeout = 120
    ```

17. **Systemd Service** - Create `/etc/systemd/system/fight_predictor.service`:

    ```ini
    [Unit]
    Description=Fight Predictor API
    After=network.target postgresql.service

    [Service]
    User=fight_predictor
    Group=fight_predictor
    WorkingDirectory=/path/to/fight_predictor
    EnvironmentFile=/etc/fight_predictor/env
    Environment="PATH=/path/to/venv/bin"
    ExecStart=/path/to/venv/bin/gunicorn --config gunicorn_config.py fight_predictor.wsgi:application
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

    **Important**: The `EnvironmentFile=/etc/fight_predictor/env` loads secrets from the secure environment file (see `SECRETS_MANAGEMENT.md`)

18. **Nginx Configuration** - Reverse proxy example:

    ```nginx
    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /path/to/fight_predictor/staticfiles/;
        }
    }
    ```

## 🟢 NICE TO HAVE

19. **Error Monitoring** - Consider Sentry or similar

20. **Backup Strategy** - Set up database backups

21. **Health Check Endpoint** - Add `/api/health/` endpoint

22. **Rate Limiting** - Consider adding rate limiting for API endpoints

23. **API Documentation** - Add drf-spectacular or similar for OpenAPI docs

## Testing Checklist

- [ ] Test all API endpoints
- [ ] Test authentication flow
- [ ] Test CORS with frontend
- [ ] Test static file serving
- [ ] Test database migrations
- [ ] Load test the API
- [ ] Test error handling

## Deployment Steps

1. Set up PostgreSQL database
2. Create `.env` file with all secrets
3. Install dependencies: `pipenv install`
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic`
6. Test locally with production settings
7. Set up gunicorn service
8. Configure Nginx
9. Set up SSL certificate (Let's Encrypt)
10. Test deployment
11. Monitor logs
