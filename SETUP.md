# Shadowing UK - Quick Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** and **npm**
- **Python 3.8+** and **pip**
- **FFmpeg** (install via package manager)

### Installation & Setup

1. **Install FFmpeg** (if not already installed):
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # Windows: Download from https://ffmpeg.org/download.html
   ```

2. **Install dependencies**:
   ```bash
   # Frontend
   npm install
   
   # Backend
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Start the application**:
   ```bash
   # Option 1: Use the startup script (recommended)
   ./start-dev.sh
   
   # Option 2: Manual start
   # Terminal 1: Backend
   cd backend && python main.py
   
   # Terminal 2: Frontend
   npm run dev
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🧪 Testing

### Verify Setup
```bash
python test-setup.py
```

### Test API (when backend is running)
```bash
python test-api.py
```

## 📖 How to Use

1. **Open** http://localhost:3000 in your browser
2. **Choose input method**:
   - YouTube URL: Paste a YouTube link
   - File Upload: Upload an MP4 video file
3. **Configure settings**:
   - Number of repeats (default: 3)
   - Confirm rights to use content
4. **Process video**: Click "Process Video"
5. **Wait for completion**: Monitor progress in real-time
6. **Download result**: Get your shadowing practice video

## 🎯 Features

- **Automatic Transcription**: AI-powered speech recognition
- **Smart Segmentation**: Natural phrase breaks with punctuation awareness
- **Shadowing Practice**: Repeated phrases with 1.5× pause duration
- **Burned-in Subtitles**: On-screen captions for each phrase
- **Progress Tracking**: Real-time status updates
- **Modern UI**: Beautiful, responsive interface

## 🔧 Technical Details

### Processing Pipeline
1. **Download/Normalize**: YouTube download or file processing
2. **Transcribe**: faster-whisper ASR with word timestamps
3. **Segment**: Merge small gaps, preserve punctuation breaks
4. **Render**: Create phrase videos with subtitles + pause videos
5. **Repeat**: Duplicate each [phrase + pause] block N times
6. **Concatenate**: Combine all segments into final video

### File Structure
```
shadowing-uk/
├── app/                    # Next.js frontend
├── components/            # React components
├── backend/              # FastAPI backend
│   ├── main.py           # API server
│   └── processing/       # Video processing
├── data/                 # Job data (auto-created)
└── package.json          # Dependencies
```

### API Endpoints
- `POST /api/process` - Start processing
- `GET /api/status/{job_id}` - Check progress
- `GET /api/download/{job_id}` - Download result
- `GET /api/health` - Health check

## 🛠️ Troubleshooting

### Common Issues

**FFmpeg not found**:
```bash
# Verify installation
ffmpeg -version
```

**Python packages missing**:
```bash
cd backend
pip install -r requirements.txt
```

**Port conflicts**:
- Backend: Change port in `backend/main.py`
- Frontend: Change port in `package.json` scripts

**Memory issues**:
- Process shorter videos
- Close other applications
- Consider smaller Whisper model

### Debug Mode
Enable detailed logging in backend:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Notes

- **Maximum video duration**: 15 minutes
- **Supported formats**: MP4 (input/output)
- **Processing time**: Varies with video length
- **Output quality**: H.264/AAC, high quality settings
- **Subtitle style**: White text with black outline

## 🎉 Ready to Use!

Your Shadowing UK application is now ready for creating practice videos. The system will automatically handle transcription, segmentation, and video processing to create effective shadowing practice materials. 