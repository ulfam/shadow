import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from faster_whisper import WhisperModel
import json


async def transcribe_video(video_path: Path, work_dir: Path) -> List[Dict[str, Any]]:
    """
    Transcribe video using faster-whisper and return segments
    """
    print(f"Starting transcription of {video_path}")

    # Load Whisper model
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")

    # Transcribe
    segments, info = model.transcribe(
        str(video_path),
        beam_size=5,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=120,  # было 500 → чаще режем на паузах
            max_speech_duration_s=5,      # принудительно дробим длинную речь
            speech_pad_ms=50,       # меньше склейки из-за паддинга
            # threshold=0.55,             # опционально: чуть выше порог речи
            ),

        no_speech_threshold=0.2,
        )

    # Process segments
    processed_segments = []
    segments_list = list(segments)  # Convert generator to list
    print(f"Found {len(segments_list)} raw segments from Whisper")
    for segment in segments_list:
        print(f"\nSegment type: {type(segment)}")
        print(f"\nSegment: {segment.text}")
        # Merge small gaps unless there's punctuation
        if processed_segments:
            last_segment = processed_segments[-1]
            gap = segment.start - last_segment["end"]

            # If gap is small (< 0.35s) and no punctuation, merge
            if gap < 0.3 and not has_punctuation(last_segment["text"]):
                last_segment["end"] = segment.end
                last_segment["text"] += " " + segment.text
                continue

        processed_segments.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": [
                    {"start": w.start, "end": w.end, "word": w.word}
                    for w in segment.words
                ],
            }
        )

    print(f"\nProcessed into {len(processed_segments)} final segments\n")

    # Save segments to JSON
    segments_file = work_dir / "segments.json"
    with open(segments_file, "w") as f:
        json.dump(processed_segments, f, indent=2)

    # Create SRT file for subtitles
    srt_file = work_dir / "segments.srt"
    create_srt_file(processed_segments, srt_file)

    return processed_segments


def has_punctuation(text: str) -> bool:
    """Check if text ends with punctuation"""
    return text.strip()[-1] in ".!?"


def create_srt_file(segments: List[Dict[str, Any]], srt_path: Path):
    """Create SRT subtitle file from segments"""
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"]

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
