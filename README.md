# HRMS Lite Backend API

A production-ready Human Resource Management System (HRMS) Lite backend built with FastAPI and PostgreSQL.

## 🚀 Features

- **Employee Management**: Create, read, and delete employees
- **Attendance Management**: Mark and track employee attendance
- **RESTful API**: Clean, well-documented REST endpoints
- **Database Migrations**: Alembic for version-controlled database schema changes
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Input Validation**: Pydantic schemas for request/response validation
- **CORS Support**: Configured for cross-origin requests
- **Production Ready**: Environment-based configuration, deployment-ready

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd FastapiDemo
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

Create a PostgreSQL database:

```sql
CREATE DATABASE hrms_db;
```

### 5. Configure environment variables

Copy the example environment file and update it with your database credentials:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and update the `DATABASE_URL`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/hrms_db
```

### 6. Run database migrations

Initialize Alembic (if not already done):

```bash
alembic init alembic
```

Create the initial migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migrations:

```bash
alembic upgrade head
```

## 🏃 Running the Application

### Development mode

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Employee Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/employees` | Create a new employee |
| GET | `/api/employees` | Get all employees |
| GET | `/api/employees/{id}` | Get employee by ID |
| DELETE | `/api/employees/{id}` | Delete an employee |

### Attendance Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attendance` | Mark attendance |
| GET | `/api/attendance` | Get all attendance records |
| GET | `/api/attendance/employee/{employee_id}` | Get attendance by employee |
| GET | `/api/attendance/employee/{employee_id}/summary` | Get attendance summary |

## 📝 API Examples

### Create Employee

```bash
POST /api/employees
Content-Type: application/json

{
  "employee_id": "EMP001",
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "department": "Engineering"
}
```

### Mark Attendance

```bash
POST /api/attendance
Content-Type: application/json

{
  "employee_id": 1,
  "date": "2024-01-15",
  "status": "Present"
}
```

### Get Attendance Summary

```bash
GET /api/attendance/employee/1/summary
```

Response:
```json
{
  "success": true,
  "employee_id": 1,
  "total_present_days": 25
}
```

## 🗄️ Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history
```

## 🚀 Deployment on Render

### 1. Prepare for deployment

Ensure your `requirements.txt` is up to date and your `.env` file is configured (but don't commit it).

### 2. Create a Render account

1. Go to [Render](https://render.com)
2. Sign up or log in

### 3. Create a PostgreSQL database

1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Configure:
   - **Name**: hrms-db (or your preferred name)
   - **Database**: hrms_db
   - **User**: (auto-generated)
   - **Password**: (auto-generated)
   - **Region**: Choose closest to you
4. Click "Create Database"
5. Copy the **Internal Database URL** (you'll use this in the web service)

### 4. Create a Web Service

1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your repository (GitHub/GitLab)
4. Configure:
   - **Name**: hrms-api (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `DATABASE_URL`: Use the Internal Database URL from step 3
     - `APP_NAME`: HRMS Lite API
     - `APP_VERSION`: 1.0.0
     - `DEBUG`: False
     - `CORS_ORIGINS`: * (or specific origins)

### 5. Deploy

1. Click "Create Web Service"
2. Render will build and deploy your application
3. Once deployed, your API will be available at the provided URL

### 6. Run migrations (if not in build command)

If migrations aren't run automatically, SSH into your Render instance and run:

```bash
alembic upgrade head
```

## 📁 Project Structure

```
FastapiDemo/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection and session
│   ├── core/
│   │   ├── __init__.py
│   │   └── exceptions.py       # Custom exception classes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py         # Employee SQLAlchemy model
│   │   └── attendance.py       # Attendance SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── employee.py         # Employee Pydantic schemas
│   │   └── attendance.py       # Attendance Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── employee_service.py # Employee business logic
│   │   └── attendance_service.py # Attendance business logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── employee.py         # Employee API routes
│   │   └── attendance.py       # Attendance API routes
│   └── utils/
│       └── __init__.py
├── alembic/                    # Alembic migration files
│   ├── versions/               # Migration versions
│   ├── env.py                  # Alembic environment config
│   └── script.py.mako          # Migration template
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
└── README.md                   # This file
```

## 🔒 Error Handling

The API returns structured error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource (e.g., employee_id or email already exists)
- `500 Internal Server Error`: Server error

## 🧪 Testing

You can test the API using:

1. **Swagger UI**: http://localhost:8000/docs (interactive API documentation)
2. **ReDoc**: http://localhost:8000/redoc (alternative API documentation)
3. **cURL** or **Postman**: Use the examples provided above

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ using FastAPI and PostgreSQL**
