# PostgreSQL Setup Guide

## Step 1: Create PostgreSQL Database and User

Connect to PostgreSQL as the postgres superuser:

```bash
sudo -u postgres psql
```

Then run these commands in the PostgreSQL prompt:

```sql
-- Create a database
CREATE DATABASE fight_predictor;

-- Create a user (replace 'your_password' with a strong password)
CREATE USER fight_predictor_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fight_predictor TO fight_predictor_user;

-- Exit PostgreSQL
\q
```

## Step 2: Set Environment Variable

You have two options for configuring the database connection:

### Option A: Using DATABASE_URL (Recommended)

Add to your `.env` file:
```bash
DATABASE_URL=postgresql://fight_predictor_user:your_password@localhost:5432/fight_predictor
```

### Option B: Using Individual Variables

Add to your `.env` file:
```bash
DB_NAME=fight_predictor
DB_USER=fight_predictor_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Step 3: Run Migrations

With the environment variable set, run migrations:

```bash
pipenv run python manage.py migrate
```

## Step 4: Create Superuser (Optional)

If you need admin access:

```bash
pipenv run python manage.py createsuperuser
```

## Step 5: Migrate Existing Data (If Applicable)

If you have existing data in SQLite that you want to migrate:

1. **Export data from SQLite:**
   ```bash
   # Temporarily switch back to SQLite
   unset DATABASE_URL
   pipenv run python manage.py dumpdata > data_backup.json
   ```

2. **Switch to PostgreSQL:**
   ```bash
   # Set DATABASE_URL back to PostgreSQL
   export DATABASE_URL=postgresql://fight_predictor_user:your_password@localhost:5432/fight_predictor
   ```

3. **Load data into PostgreSQL:**
   ```bash
   pipenv run python manage.py loaddata data_backup.json
   ```

## Troubleshooting

### Connection Refused
- Make sure PostgreSQL is running: `sudo systemctl status postgresql`
- Check PostgreSQL is listening: `sudo netstat -plnt | grep 5432`

### Authentication Failed
- Verify the user and password are correct
- Check PostgreSQL authentication settings in `/etc/postgresql/*/main/pg_hba.conf`

### Permission Denied
- Make sure the user has proper privileges on the database
- Try: `GRANT ALL PRIVILEGES ON DATABASE fight_predictor TO fight_predictor_user;`

### Test Connection
You can test the connection manually:
```bash
psql -h localhost -U fight_predictor_user -d fight_predictor
```

## Development vs Production

- **Development**: If `DATABASE_URL` is not set, the app will use SQLite (no setup needed)
- **Production**: Set `DATABASE_URL` to use PostgreSQL

This allows you to develop locally with SQLite and deploy with PostgreSQL without code changes!

