# AutoML - FastAPI Backend Integration ✅

## ✨ What's New

Your AutoML application now has a **modern FastAPI backend** that replaces Streamlit, enabling seamless integration with your React frontend!

---

## 🚀 Quick Start Guide

### 1. Start the Backend API

```bash
cd C:\Users\ASUS\Desktop\Teachable\AutoML
python api_server.py
```

**Backend will run on**: `http://localhost:8000`  
**API Docs**: `http://localhost:8000/docs`

### 2. Frontend is Already Running

Your React frontend is already running on `http://localhost:1321` and is configured to proxy API requests to the backend.

### 3. Complete the Integration

Due to gitignore restrictions, you need to manually create one file:

**Create `frontend/src/lib/apiClient.ts`** - See the [Integration Guide](walkthrough.md) for the complete code.

Alternatively, you can find the API client code in the walkthrough document.

---

## 📋 What's Been Implemented

### ✅ Backend (FastAPI)
- **File Upload**: CSV/Excel file handling with validation
- **Data Cleaning**:
  - Handle null values (mean, median, mode, fill methods)
  - Remove duplicates
  - Data type conversion
  - Column encoding (label, one-hot, ordinal)
  - Data filtering
  - Column management (drop, rename)
- **Model Training**:
  - Classification models (Logistic Regression, Random Forest, Decision Tree, SVM)
  - Regression models (Linear, Random Forest, Decision Tree, SVM, XGBoost)
  - Background task processing
  - Progress tracking
  - Results and metrics
- **Session Management**: Multi-user support with automatic cleanup
- **CORS Configuration**: Enabled for frontend communication

### ✅ Frontend Integration Setup
- TypeScript type definitions (`src/types/api.ts`)
- Vite proxy configuration for API requests
- API client template (manual creation needed)

---

## 📁 Key Files

| File | Description |
|------|-------------|
| `api_server.py` | Main FastAPI application |
| `app/api/routes/upload.py` | File upload endpoints |
| `app/api/routes/cleaning.py` | Data cleaning endpoints |
| `app/api/routes/training.py` | Model training endpoints |
| `app/api/session.py` | Session management |
| `frontend/src/types/api.ts` | TypeScript type definitions |
| `frontend/vite.config.ts` | API proxy configuration |
| `.env` | Environment configuration |

---

## 🔌 API Endpoints

### Upload
- `POST /api/upload/` - Upload dataset
- `GET /api/upload/{session_id}/info` - Get dataset info
- `GET /api/upload/{session_id}/preview` - Preview dataset
- `GET /api/upload/{session_id}/download` - Download cleaned data

### Cleaning
- `POST /api/cleaning/nulls` - Handle null values
- `POST /api/cleaning/duplicates` - Remove duplicates
- `POST /api/cleaning/convert-type` - Convert data types
- `POST /api/cleaning/encode` - Encode categorical columns
- `POST /api/cleaning/filter` - Filter data
- `POST /api/cleaning/columns` - Manage columns

### Training
- `POST /api/training/train` - Start model training
- `GET /api/training/status/{session_id}` - Get training status
- `GET /api/training/results/{session_id}` - Get training results

---

## 🧪 Test the Backend

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Interactive API Docs
Visit `http://localhost:8000/docs` to see:
- All available endpoints
- Request/response schemas
- Try out API calls directly

---

## 📖 Next Steps

1. **Start the backend** (if not already running): `python api_server.py`
2. **Create the API client**: Copy code from [walkthrough.md](walkthrough.md) to `frontend/src/lib/apiClient.ts`
3. **Update frontend pages**: Integrate API calls in Clean.tsx and Train.tsx (examples provided in walkthrough)
4. **Test the integration**: Upload a CSV file and verify it works end-to-end

---

## 📚 Documentation

- **[Integration Guide](walkthrough.md)**: Complete setup and integration instructions
- **[Implementation Plan](implementation_plan.md)**: Technical architecture details
- **[Task Checklist](task.md)**: Development progress tracker

---

## ⚙️ Configuration

Edit `.env` to customize:
```env
API_PORT=8000
CORS_ORIGINS=http://localhost:1321
UPLOAD_DIR=./data/uploads
MODELS_DIR=./models
```

---

## 🆘 Support

**Backend not starting?**
- Check if port 8000 is available
- Verify dependencies: `pip install -r requirements.txt`

**API requests failing?**
- Ensure backend is running
- Check browser console for errors
- Verify CORS settings in `.env`

**Need help?**
- Check the logs in the terminal where backend is running
- Visit `/docs` endpoint for API documentation
- Review [walkthrough.md](walkthrough.md) for detailed guidance

---

**Happy Coding! 🎉**
