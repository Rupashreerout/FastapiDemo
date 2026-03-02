# Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create PostgreSQL Database
```sql
CREATE DATABASE hrms_db;
```

### 3. Configure Environment
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/hrms_db
APP_NAME=HRMS Lite API
APP_VERSION=1.0.0
DEBUG=False
CORS_ORIGINS=*
```

### 4. Run Migrations
```bash
alembic upgrade head
```

### 5. Start the Server
```bash
uvicorn app.main:app --reload
```

### 6. Access the API
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📝 Quick Test

### Create an Employee
```bash
curl -X POST "http://localhost:8000/api/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering"
  }'
```

### Mark Attendance
```bash
curl -X POST "http://localhost:8000/api/attendance" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "date": "2024-01-15",
    "status": "Present"
  }'
```

### Get Attendance Summary
```bash
curl "http://localhost:8000/api/attendance/employee/1/summary"
```

## 🎯 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the API using Swagger UI at `/docs`
3. Check the project structure in the README
