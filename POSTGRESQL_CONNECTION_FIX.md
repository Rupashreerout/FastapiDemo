# PostgreSQL Connection Fix Guide

## 🔧 Quick Fix Steps

### Option 1: Update .env with Correct Password (Recommended)

1. **Find your PostgreSQL password:**
   - If you remember it, use that
   - If you forgot it, see Option 2 below

2. **Edit the `.env` file:**
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/hrms_db
   ```
   Replace `YOUR_ACTUAL_PASSWORD` with your PostgreSQL password.

### Option 2: Reset PostgreSQL Password

**Windows (using pgAdmin or psql):**

1. Open Command Prompt as Administrator
2. Navigate to PostgreSQL bin directory (usually):
   ```bash
   cd "C:\Program Files\PostgreSQL\15\bin"
   ```
   (Replace `15` with your PostgreSQL version)

3. Connect to PostgreSQL:
   ```bash
   psql -U postgres
   ```

4. If it asks for password and you don't know it, you may need to:
   - Check `pg_hba.conf` file and temporarily set authentication to `trust`
   - Or use Windows authentication

5. Once connected, reset password:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

6. Update `.env` file with the new password

### Option 3: Create Database if Missing

1. Connect to PostgreSQL:
   ```bash
   psql -U postgres
   ```

2. Create the database:
   ```sql
   CREATE DATABASE hrms_db;
   ```

3. Verify it exists:
   ```sql
   \l
   ```

4. Exit:
   ```sql
   \q
   ```

### Option 4: Test Connection

Test your connection string:

```bash
psql -U postgres -h localhost -d hrms_db
```

If this works, your credentials are correct.

## 📝 Common Issues

### Issue: "password authentication failed"
**Solution:** Password in `.env` doesn't match PostgreSQL password

### Issue: "database does not exist"
**Solution:** Create the database (see Option 3)

### Issue: "connection refused"
**Solution:** 
- Check if PostgreSQL service is running
- Verify port 5432 is correct
- Check firewall settings

## ✅ After Fixing

1. Update `.env` file with correct credentials
2. Restart your FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

## 🔍 Find PostgreSQL Installation

**Windows:**
- Default location: `C:\Program Files\PostgreSQL\[version]\`
- Check Services: `services.msc` → Look for "postgresql-x64-XX"

**Check if PostgreSQL is running:**
```bash
# In Command Prompt
sc query postgresql-x64-15
```

Replace `15` with your version number.
