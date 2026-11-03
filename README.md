# Shadowing UK

A full-stack web application for creating shadowing practice videos from YouTube content. The app automatically transcribes videos, segments them into phrases, and creates practice videos with repeated phrases and pauses.

## Features

- **YouTube Integration**: Process videos directly from YouTube URLs
- **File Upload**: Upload local video files (MP4 format)
- **AI Transcription**: Uses faster-whisper for accurate speech recognition
- **Automatic Segmentation**: Cuts videos into natural phrases
- **Shadowing Practice**: Repeats each phrase with configurable pauses
- **Burned-in Subtitles**: Displays recognized text as on-screen captions
- **Progress Tracking**: Real-time processing status updates
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS

## Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Lucide React** icons

### Backend
- **FastAPI** (Python)
- **faster-whisper** (CTranslate2) for ASR
- **yt-dlp** for YouTube downloads
- **FFmpeg** for video processing
- **Background Tasks** for async processing

## Prerequisites

- **Node.js 18+** and **npm**
- **Python 3.8+** and **pip**
- **FFmpeg** installed and available in PATH
- **Git**

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shadowing-uk
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Install FFmpeg** (if not already installed)
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **Windows:**
   Download from [FFmpeg official website](https://ffmpeg.org/download.html)

## Usage

### Development Mode

1. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend development server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`

### Production Mode

1. **Build the frontend**
   ```bash
   npm run build
   npm start
   ```

2. **Start the backend with uvicorn**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## How It Works

### Processing Pipeline

1. **Input**: User provides YouTube URL or uploads video file
2. **Download**: Video is downloaded and normalized to H.264/AAC format
3. **Transcription**: faster-whisper transcribes audio into segments with timestamps
4. **Segmentation**: Small gaps (<0.35s) are merged unless punctuation is present
5. **Rendering**: For each phrase:
   - Cut video segment with FFmpeg
   - Add burned-in subtitles
   - Create pause video (1.5× phrase duration)
   - Repeat block N times
6. **Concatenation**: All segments are combined into final output video


### Possible improvements
1. Store previously created unique videos to be able to switch between them
2. Make black screen work
3. Make it accesible from other devices - moblie phoe and for Roma via private link
4. Add opportunity to search video by topic



### File Structure

```
shadowing-uk/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main page component
├── components/            # React components
│   └── ui/               # shadcn/ui components
├── lib/                  # Utility functions
├── backend/              # FastAPI backend
│   ├── main.py           # Main API server
│   └── processing/       # Video processing modules
│       ├── transcribe.py # ASR transcription
│       └── render.py     # Video rendering
├── data/                 # Job data (created automatically)
│   ├── input/           # Input videos
│   ├── work/            # Temporary files
│   └── output/          # Final videos
├── package.json          # Frontend dependencies
├── requirements.txt      # Backend dependencies
└── README.md            # This file
```

## API Endpoints

- `POST /api/process` - Start video processing job
- `GET /api/status/{job_id}` - Get job status and progress
- `GET /api/download/{job_id}` - Download processed video
- `GET /api/health` - Health check

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Optional: Override default settings
MAX_VIDEO_DURATION=900  # 15 minutes in seconds
WHISPER_MODEL=medium.en # Whisper model to use
```

### FFmpeg Settings

The app uses these FFmpeg settings for optimal quality:

- **Video Codec**: H.264 with CRF 18 (high quality)
- **Audio Codec**: AAC 128k
- **Preset**: veryfast (good balance of speed/quality)
- **Subtitle Style**: White text with black outline, 28px font

## Limitations

- **Maximum video duration**: 15 minutes
- **Supported formats**: MP4 (input/output)
- **Maximum repeats**: 10
- **Processing time**: Depends on video length and complexity

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Test with: `ffmpeg -version`

2. **YouTube download fails**
   - Check internet connection
   - Verify YouTube URL is valid
   - Some videos may be restricted

3. **Processing takes too long**
   - Reduce video length
   - Check system resources
   - Consider using a smaller Whisper model

4. **Memory issues**
   - Close other applications
   - Process shorter videos
   - Increase system RAM

### Debug Mode

Enable debug logging in the backend:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) for fast speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloads
- [FFmpeg](https://ffmpeg.org/) for video processing
- [shadcn/ui](https://ui.shadcn.com/) for beautiful UI components 