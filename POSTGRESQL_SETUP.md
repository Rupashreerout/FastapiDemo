# PostgreSQL Setup Guide

## 📋 Prerequisites

- PostgreSQL installed on your system
- PostgreSQL service running

## 🚀 Quick Setup Steps

### 1. Install PostgreSQL (if not installed)

**Windows:**
- Download from: https://www.postgresql.org/download/windows/
- Run the installer and follow the setup wizard
- Remember the password you set for the `postgres` user

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2. Create the Database

Open PostgreSQL command line or pgAdmin:

**Using psql (Command Line):**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE hrms_db;

# Exit psql
\q
```

**Using pgAdmin:**
1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `hrms_db`
5. Click "Save"

### 3. Update .env File

Edit the `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hrms_db
```

**Replace:**
- `your_password` - Your PostgreSQL password
- `postgres` - Your PostgreSQL username (if different)
- `localhost` - Database host (if different)
- `5432` - PostgreSQL port (default is 5432)
- `hrms_db` - Database name

### 4. Run Database Migrations

```bash
cd C:\Users\rupas\Downloads\Project\fastapidemo\FastapiDemo
alembic upgrade head
```

This will create all the necessary tables (employees, attendance).

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

## ✅ Verify Connection

1. Check if the server starts without errors
2. Visit http://localhost:8000/docs
3. Try creating an employee via the API

## 🔧 Troubleshooting

### Connection Refused Error

**Problem:** `could not connect to server: Connection refused`

**Solution:**
- Make sure PostgreSQL service is running
- Check if PostgreSQL is listening on port 5432
- Verify firewall settings

**Windows:**
```bash
# Check if PostgreSQL service is running
services.msc
# Look for "postgresql-x64-XX" service
```

**Linux:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Authentication Failed

**Problem:** `password authentication failed for user "postgres"`

**Solution:**
- Verify the password in `.env` file matches your PostgreSQL password
- Reset PostgreSQL password if needed:

```sql
ALTER USER postgres WITH PASSWORD 'new_password';
```

### Database Does Not Exist

**Problem:** `database "hrms_db" does not exist`

**Solution:**
- Create the database (see step 2 above)
- Or update `.env` to use an existing database

### Port Already in Use

**Problem:** Port 5432 is already in use

**Solution:**
- Check if another PostgreSQL instance is running
- Or change the port in PostgreSQL config and update `.env`

## 📝 Default PostgreSQL Credentials

If you just installed PostgreSQL, the default credentials are usually:
- **Username:** `postgres`
- **Password:** (the one you set during installation)
- **Host:** `localhost`
- **Port:** `5432`

## 🔒 Security Note

Never commit your `.env` file to version control. It contains sensitive database credentials.

---

**Need Help?** Check the main README.md for more information.
