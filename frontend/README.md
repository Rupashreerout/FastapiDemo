# HRMS Lite Frontend

A production-ready React frontend for the HRMS Lite system, built with React 18, Vite, and modern UI components.

## 🚀 Features

- **Employee Management**: Add, view, and delete employees
- **Attendance Management**: Mark and view attendance records
- **Dashboard**: Overview of key metrics and quick actions
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Proper loading indicators for better UX

## 📋 Prerequisites

- Node.js 16+ and npm/yarn
- Running FastAPI backend (see backend README for setup)

## 🛠️ Installation

### 1. Install Dependencies

```bash
npm install
```

or

```bash
yarn install
```

### 2. Configure Environment Variables

Create a `.env` file in the frontend directory:

```bash
cp .env.example .env
```

Edit `.env` and set your backend API URL:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

**For Production:**
Replace with your deployed backend URL:
```env
VITE_API_BASE_URL=https://your-backend-url.com/api
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── Dashboard.jsx
│   │   ├── EmployeeForm.jsx
│   │   ├── EmployeeList.jsx
│   │   ├── AttendanceForm.jsx
│   │   ├── AttendanceList.jsx
│   │   ├── Loader.jsx
│   │   ├── ErrorAlert.jsx
│   │   └── SuccessAlert.jsx
│   ├── pages/               # Page components
│   │   ├── EmployeesPage.jsx
│   │   └── AttendancePage.jsx
│   ├── services/            # API service layer
│   │   └── api.js
│   ├── App.jsx             # Main app component
│   └── main.jsx            # Entry point
├── public/                 # Static assets
├── .env.example            # Example environment variables
├── package.json
├── vite.config.js
└── README.md
```

## 🎯 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## 🌐 API Integration

The frontend communicates with the FastAPI backend through REST API calls. All API calls are centralized in `src/services/api.js`.

### API Endpoints Used

**Employees:**
- `GET /employees` - Get all employees
- `POST /employees` - Create employee
- `DELETE /employees/{id}` - Delete employee

**Attendance:**
- `GET /attendance` - Get all attendance records
- `GET /attendance/employee/{employee_id}` - Get attendance by employee
- `GET /attendance/employee/{employee_id}/summary` - Get attendance summary
- `POST /attendance` - Mark attendance

## 🚀 Deployment on Vercel

### Prerequisites

1. GitHub account
2. Vercel account (sign up at [vercel.com](https://vercel.com))

### Deployment Steps

#### 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 2. Deploy to Vercel

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (Select your account)
# - Link to existing project? No
# - Project name? hrms-lite-frontend
# - Directory? ./frontend
# - Override settings? No
```

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: Your production backend URL (e.g., `https://your-backend.vercel.app/api`)
6. Click "Deploy"

#### 3. Configure Environment Variables

In Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - `VITE_API_BASE_URL` = `https://your-backend-url.com/api`

#### 4. Redeploy

After adding environment variables, trigger a new deployment:
- Go to "Deployments" tab
- Click "..." on the latest deployment
- Select "Redeploy"

### Custom Domain (Optional)

1. Go to project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## 🔧 Configuration

### Changing Backend URL

**Development:**
Update `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

**Production:**
Update environment variable in Vercel dashboard or deployment platform.

### CORS Configuration

Ensure your backend has CORS enabled for your frontend domain. In the backend `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.vercel.app"],
    ...
)
```

## 🐛 Troubleshooting

### API Connection Issues

1. **Check Backend URL**: Verify `VITE_API_BASE_URL` in `.env` is correct
2. **Check Backend Status**: Ensure backend is running
3. **Check CORS**: Verify backend allows requests from your frontend origin
4. **Check Network Tab**: Open browser DevTools → Network tab to see API calls

### Build Errors

1. **Clear Cache**: Delete `node_modules` and `.vite` folder, then reinstall
2. **Check Node Version**: Ensure Node.js 16+ is installed
3. **Check Dependencies**: Run `npm install` again

### Deployment Issues

1. **Environment Variables**: Ensure all required env vars are set in Vercel
2. **Build Command**: Verify build command is `npm run build`
3. **Output Directory**: Verify output directory is `dist`

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🎨 UI Features

- **Responsive Design**: Works on mobile, tablet, and desktop
- **Loading States**: Spinner animations during API calls
- **Error Handling**: User-friendly error messages
- **Success Messages**: Confirmation messages for successful actions
- **Form Validation**: Client-side validation with helpful error messages
- **Modern Styling**: Gradient backgrounds, smooth transitions, and card-based layouts

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using React and Vite**
