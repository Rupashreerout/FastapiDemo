# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Backend URL
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and set your backend URL:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Start Development Server
```bash
npm run dev
```

The app will open at `http://localhost:3000`

## 📝 What's Next?

1. **Make sure your backend is running** on `http://localhost:8000`
2. **Open the app** in your browser
3. **Start using the HRMS Lite system!**

## 🎯 Features Available

- ✅ Dashboard with statistics
- ✅ Add and manage employees
- ✅ Mark and view attendance
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

## 🚀 Build for Production

```bash
npm run build
```

The production build will be in the `dist` folder.

## 📦 Deploy to Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set `VITE_API_BASE_URL` environment variable
4. Deploy!

See `README.md` for detailed deployment instructions.
