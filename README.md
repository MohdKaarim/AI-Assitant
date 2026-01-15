# AI Language Tutor

An AI-powered language learning application with OCR text extraction and pronunciation feedback.

## Quick Start

### Prerequisites
- Node.js and npm
- Python 3.8+
- Tesseract OCR (Download from: https://github.com/UB-Mannheim/tesseract/wiki)

### Running the Application

1. **Start Backend** (in one terminal):
   ```powershell
   .\start_backend.ps1
   ```

2. **Start Frontend** (in another terminal):
   ```powershell
   .\start_frontend.ps1
   ```

3. **Open Browser**: Navigate to `http://localhost:4200`

## Manual Setup

### Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

### Frontend
```powershell
cd frontend
npm start
```

## Features
- 📸 OCR text extraction (English, Arabic, Tamil)
- 🎤 Real-time pronunciation feedback
- 🤖 AI-powered tutoring

## Troubleshooting

### Backend won't start
- Ensure Python dependencies are installed: `pip install -r requirements.txt`
- Install Tesseract OCR from the link above

### Frontend won't start
- Run `npm install` in the frontend directory
- Check that port 4200 is available

### OCR not working
- Verify Tesseract is installed and in PATH
- Check backend console for error messages
