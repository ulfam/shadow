import os
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import aiofiles
import json
from processing.transcribe import transcribe_video
from processing.render import render_shadowing_video

app = FastAPI(title="Shadowing UK API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class ProcessingRequest(BaseModel):
    youtube_url: Optional[str] = None
    repeats: int = 3


class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    message: str
    error: Optional[str] = None


# Global job storage (in production, use Redis or database)
jobs = {}

# Ensure data directories exist
DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "input"
WORK_DIR = DATA_DIR / "work"
OUTPUT_DIR = DATA_DIR / "output"

for dir_path in [INPUT_DIR, WORK_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def get_job_dirs(job_id: str):
    """Get job-specific directories"""
    return {
        "input": INPUT_DIR / job_id,
        "work": WORK_DIR / job_id,
        "output": OUTPUT_DIR / job_id,
    }


@app.post("/api/process", response_model=dict)
async def process_video(
    background_tasks: BackgroundTasks,
    youtube_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    repeats: int = Form(3),
):
    """Start video processing job"""
    if not youtube_url and not file:
        raise HTTPException(
            status_code=400, detail="Either YouTube URL or file upload required"
        )

    if repeats < 1 or repeats > 10:
        raise HTTPException(status_code=400, detail="Repeats must be between 1 and 10")

    job_id = str(uuid.uuid4())
    job_dirs = get_job_dirs(job_id)

    # Create job directories
    print(f"Creating job directories for {job_id}:")
    for dir_path in job_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")

    # Initialize job status
    jobs[job_id] = {
        "status": "starting",
        "progress": 0.0,
        "message": "Initializing job...",
        "error": None,
    }

    # Add background task
    background_tasks.add_task(process_video_job, job_id, youtube_url, file, repeats)

    return {"job_id": job_id, "message": "Processing started"}


async def process_video_job(
    job_id: str, youtube_url: Optional[str], file: Optional[UploadFile], repeats: int
):
    """Background task for video processing"""
    try:
        job_dirs = get_job_dirs(job_id)
        jobs[job_id]["status"] = "downloading"
        jobs[job_id]["message"] = "Downloading video..."
        jobs[job_id]["progress"] = 5.0

        # Download or save uploaded file
        input_path = job_dirs["input"] / "input.mp4"

        if youtube_url:
            # Download from YouTube
            await download_youtube_video(youtube_url, input_path)
        else:
            # Save uploaded file
            async with aiofiles.open(input_path, "wb") as f:
                content = await file.read()
                await f.write(content)

        jobs[job_id]["status"] = "transcribing"
        jobs[job_id]["message"] = "Transcribing audio..."
        jobs[job_id]["progress"] = 20.0

        # Transcribe video
        segments = await transcribe_video(input_path, job_dirs["work"])

        jobs[job_id]["status"] = "rendering"
        jobs[job_id]["message"] = "Rendering shadowing video..."
        jobs[job_id]["progress"] = 60.0

        # Render shadowing video
        output_path = job_dirs["output"] / "output.mp4"
        work_dir = job_dirs["work"]  # Use the correct work directory
        await render_shadowing_video(
            input_path, segments, repeats, output_path, work_dir
        )

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Processing completed successfully!"
        jobs[job_id]["progress"] = 100.0

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["message"] = "Processing failed"
        jobs[job_id]["error"] = str(e)
        print(f"Error in job {job_id}: {e}")


async def download_youtube_video(url: str, output_path: Path):
    """Download video from YouTube using yt-dlp"""
    try:
        cmd = [
            "yt-dlp",
            "-f",
            "best[height<=720][ext=mp4]/best[ext=mp4]/best",
            "-o",
            str(output_path),
            "--no-playlist",
            "--no-warnings",
            "--quiet",
            url,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if "ERROR - Precondition check failed" in error_msg:
                raise Exception(
                    "This YouTube video cannot be downloaded. It may be restricted, private, or unavailable."
                )
            elif "HTTP Error 403" in error_msg:
                raise Exception(
                    "Access denied to this YouTube video. It may be private or restricted."
                )
            elif "Video unavailable" in error_msg:
                raise Exception(
                    "This YouTube video is unavailable or has been removed."
                )
            else:
                raise Exception(f"YouTube download failed: {error_msg}")

    except subprocess.TimeoutExpired:
        raise Exception("YouTube download timed out. Please try a shorter video.")
    except Exception as e:
        raise Exception(f"Download error: {str(e)}")


@app.get("/api/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job processing status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        error=job["error"],
    )


@app.get("/api/download/{job_id}")
async def download_result(job_id: str):
    """Download processed video"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")

    output_path = get_job_dirs(job_id)["output"] / "output.mp4"

    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")

    return FileResponse(
        path=output_path, filename=f"shadowing_{job_id}.mp4", media_type="video/mp4"
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Shadowing UK API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
