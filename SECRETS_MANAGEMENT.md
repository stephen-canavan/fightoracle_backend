# Secrets Management Best Practices

## Understanding the Risk

Storing passwords in `.env` files is actually **the standard practice** for development, but you're right to be concerned. The security comes from:

1. **Never committing** `.env` to version control (✅ already in `.gitignore`)
2. **Restricting file permissions** on the server
3. **Using secrets managers** in production environments

## Development (Local) - .env Files

For local development, `.env` files are acceptable and standard practice. Here's how to secure them:

### 1. Set Proper File Permissions

On your VPS, restrict access to the `.env` file:

```bash
# Only owner can read/write (600 = rw-------)
chmod 600 .env

# Verify permissions
ls -la .env
# Should show: -rw------- 1 user user ...
```

### 2. Use a Separate User Account

Run your application as a dedicated user (not root):

```bash
# Create a dedicated user
sudo useradd -m -s /bin/bash fight_predictor

# Transfer ownership
sudo chown fight_predictor:fight_predictor .env
```

## Production - Better Alternatives

For production on a VPS, consider these options:

### Option 1: Systemd Environment File (Recommended for VPS)

Store secrets in a systemd environment file with restricted permissions:

1. **Create environment file** (`/etc/fight_predictor/env`):

   ```bash
   sudo nano /etc/fight_predictor/env
   ```

   Add your secrets:

   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost:5432/fight_predictor
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Set restrictive permissions**:

   ```bash
   sudo chmod 600 /etc/fight_predictor/env
   sudo chown fight_predictor:fight_predictor /etc/fight_predictor/env
   ```

3. **Update systemd service** to load from this file:
   ```ini
   [Service]
   EnvironmentFile=/etc/fight_predictor/env
   ```

### Option 2: Use Individual Environment Variables (Most Secure)

Set environment variables directly in systemd without a file:

```ini
[Service]
Environment="SECRET_KEY=your-secret-key"
Environment="DATABASE_URL=postgresql://user:password@localhost:5432/fight_predictor"
Environment="DEBUG=False"
```

**Note**: This still stores secrets in the systemd service file, but it's better than a `.env` file in the project directory.

### Option 3: PostgreSQL .pgpass File

For database passwords specifically, use PostgreSQL's `.pgpass` file:

1. **Create** `~/.pgpass`:

   ```
   localhost:5432:fight_predictor:fight_predictor_user:your_password
   ```

2. **Set permissions**:

   ```bash
   chmod 600 ~/.pgpass
   ```

3. **Update DATABASE_URL** to omit password:
   ```
   DATABASE_URL=postgresql://fight_predictor_user@localhost:5432/fight_predictor
   ```

### Option 4: Secrets Manager (Best for Cloud/Enterprise)

For cloud deployments or enterprise setups:

- **AWS**: AWS Secrets Manager or Parameter Store
- **Azure**: Azure Key Vault
- **Google Cloud**: Secret Manager
- **HashiCorp Vault**: Self-hosted secrets management
- **Docker Secrets**: If using Docker Swarm

## Recommended Setup for Your VPS

Here's what I recommend for your deployment:

### Step 1: Create Systemd Environment File

```bash
# Create directory
sudo mkdir -p /etc/fight_predictor
sudo nano /etc/fight_predictor/env
```

Add your secrets (one per line, no quotes needed):

```
SECRET_KEY=your-generated-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/fight_predictor
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
SECURE_COOKIE=True
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Step 2: Secure the File

```bash
# Set restrictive permissions
sudo chmod 600 /etc/fight_predictor/env

# Set ownership to your app user
sudo chown fight_predictor:fight_predictor /etc/fight_predictor/env
```

### Step 3: Update Systemd Service

Your systemd service file should reference this:

```ini
[Unit]
Description=Fight Predictor API
After=network.target postgresql.service

[Service]
User=fight_predictor
Group=fight_predictor
WorkingDirectory=/home/fight_predictor/fight_predictor
EnvironmentFile=/etc/fight_predictor/env
ExecStart=/home/fight_predictor/.local/share/virtualenvs/fight_predictor-xxx/bin/gunicorn \
    --config gunicorn_config.py fight_predictor.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 4: Remove .env from Project Directory

Once using systemd environment file:

```bash
# Remove .env from project (keep .env.example for reference)
rm .env
```

## Additional Security Measures

1. **Use Strong Passwords**: Generate strong, unique passwords for each service
2. **Rotate Secrets Regularly**: Change passwords and keys periodically
3. **Limit Access**: Only give access to users who need it
4. **Audit Access**: Monitor who accesses secret files
5. **Use Different Credentials**: Dev, staging, and production should have different credentials
6. **Encrypt Backups**: If backing up `.env` or environment files, encrypt them

## Quick Security Checklist

- [ ] `.env` file has permissions `600` (owner read/write only)
- [ ] `.env` is in `.gitignore` (✅ already done)
- [ ] Using dedicated user account (not root)
- [ ] Systemd environment file has permissions `600`
- [ ] Database user has minimal required privileges
- [ ] Different credentials for dev/staging/production
- [ ] Regular secret rotation schedule

## Summary

- **Development**: `.env` files are fine with `chmod 600`
- **Production**: Use systemd environment files (`/etc/fight_predictor/env`) with `chmod 600`
- **Best Practice**: Never store secrets in code or commit them to version control
- **File Permissions**: Always use `600` (owner read/write only) for secret files

The key is that secrets will always be stored somewhere - the security comes from:

1. Proper file permissions
2. Not committing to version control
3. Limiting access to necessary users only
4. Using system-level environment files in production
