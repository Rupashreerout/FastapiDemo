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

## 🚀 Production Deployment

For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Quick Deployment Summary

#### Backend (Render)

1. **Create PostgreSQL Database on Render**
   - Go to Render Dashboard → New → PostgreSQL
   - Copy Internal Database URL

2. **Deploy Backend**
   - New → Web Service
   - Connect GitHub repository
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Environment Variables**:
     - `DATABASE_URL`: PostgreSQL Internal Database URL
     - `CORS_ORIGINS`: Your frontend URL (update after frontend deployment)
     - `APP_NAME`: HRMS Lite API
     - `APP_VERSION`: 1.0.0
     - `DEBUG`: False

3. **Note Backend URL**: `https://your-backend.onrender.com`

#### Frontend (Vercel)

1. **Deploy to Vercel**
   - Import GitHub repository
   - **Root Directory**: `frontend`
   - **Framework**: Vite
   - **Build Command**: `npm run build`
   - **Environment Variable**:
     - `VITE_API_BASE_URL`: `https://your-backend.onrender.com/api`

2. **Update Backend CORS**
   - Go back to Render
   - Update `CORS_ORIGINS` with your Vercel URL
   - Redeploy backend

### Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed step-by-step instructions.

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
