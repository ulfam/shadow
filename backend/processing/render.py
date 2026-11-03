import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any


async def render_shadowing_video(
    input_path: Path,
    segments: List[Dict[str, Any]],
    repeats: int,
    output_path: Path,
    work_dir: Path,
):
    """
    Render shadowing video with repeated phrases and pauses
    """
    print(f"Render function called with:")
    print(f"  input_path: {input_path}")
    print(f"  work_dir: {work_dir}")
    print(f"  output_path: {output_path}")
    print(f"  segments count: {len(segments)}")
    print(f"  Current working directory: {Path.cwd()}")
    print(f"  work_dir absolute: {work_dir.absolute()}")
    print(f"  output_path absolute: {output_path.absolute()}")

    # Handle case where no segments are found
    if not segments:
        print("No segments found, creating a simple output video")
        # Create a simple copy of the input video as output
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-i",
            str(input_path),
            "-c",
            "copy",
            str(output_path),
        ]

        result = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            raise Exception(f"FFmpeg copy error: {stderr.decode()}")
        return

    print(f"Processing {len(segments)} segments with {repeats} repeats each")

    # Create temporary files list
    concat_list = []
    srt_content = ""
    srt_number = 1
    start_time = 0

    for i, segment in enumerate(segments):
        phrase_duration = segment["end"] - segment["start"]
        pause_duration = phrase_duration * 1.5
        print(f"Processing segment {i+1}/{len(segments)}: {segment['text'][:50]}...")

        # Add repeated blocks to concat list
        for repeat in range(repeats):
            # Create phrase video with subtitles
            phrase_video = work_dir / f"phrase_{i:04d}.mp4"
            await create_phrase_video(
                input_path,
                segment,
                phrase_video,
            )
            concat_list.append(str(phrase_video.absolute()))
            srt_content += f"{srt_number}\n"
            srt_content += f"{start_time} --> {start_time + phrase_duration}\n"
            srt_content += f"{segment['text']}\n\n"
            start_time += phrase_duration
            srt_number += 1

            # Create pause video
            pause_video = work_dir / f"pause_{i:04d}.mp4"
            await create_pause_video(
                pause_duration,
                segment["text"],
                pause_video,
            )
            srt_content += f"{srt_number}\n"
            srt_content += f"{start_time} --> {start_time + pause_duration}\n"
            srt_content += f"{segment['text']}\n\n"
            start_time += pause_duration
            srt_number += 1
            concat_list.append(str(pause_video.absolute()))

    print(f"Concatenating {len(concat_list)} video segments...")
    # Concatenate all videos

    with open(work_dir / "srt_concatenated_content.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
    await concatenate_videos(concat_list, output_path, work_dir)


async def create_phrase_video(
    input_path: Path,
    segment: Dict[str, Any],
    output_path: Path,
):
    """Create video clip for a single phrase with burned-in subtitles"""

    # Calculate duration
    duration = segment["end"] - segment["start"]

    # Create temporary SRT file for this phrase
    # Subtitles should start at 0 and last for the full duration
    srt_content = f"""1
{format_timestamp(0)} --> {format_timestamp(duration)}
{segment['text']}
"""

    srt_file = output_path.parent / f"temp_{output_path.stem}.srt"
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(srt_content)

    # FFmpeg command to cut video and add subtitles
    # Use -t (duration) instead of -to when -ss is after -i
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-i",
        str(input_path),
        "-ss",
        str(segment["start"]),
        "-t",  # Use duration instead of -to for better accuracy
        str(duration),
        "-vf",
        f"subtitles={srt_file}:force_style='Fontsize=28,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3,Outline=1,Shadow=1,Alignment=6'",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-avoid_negative_ts",
        "make_zero",
        "-vsync",
        "0",  # Use passthrough instead of cfr for better sync
        "-async",
        "1",
        "-fflags",
        "+genpts",  # Generate presentation timestamps
        "-start_number",
        "0",  # Start frame numbering at 0
        str(output_path),
    ]

    try:
        result = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {stderr.decode()}")

    finally:
        # Clean up temporary SRT file
        if srt_file.exists():
            srt_file.unlink()


async def create_pause_video(
    duration: float,
    text: str,
    output_path: Path,
):
    """Create a black video with silence for the specified duration"""

    # Create temporary SRT file for this pause
    srt_content = f"""1
{format_timestamp(0)} --> {format_timestamp(duration)}
{text}
"""

    srt_file = output_path.parent / f"temp_{output_path.stem}.srt"
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(srt_content)

    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-f",
        "lavfi",
        "-i",
        f"color=black:size=1280x720:duration={duration}",
        "-f",
        "lavfi",
        "-i",
        f"anullsrc=channel_layout=stereo:sample_rate=44100:duration={duration}",
        "-vf",
        f"subtitles={srt_file.absolute()}:force_style='FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=6'",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        str(output_path),
    ]

    try:
        result = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            raise Exception(f"FFmpeg pause video error: {stderr.decode()}")
    except Exception as e:
        print(f"Error creating pause video: {e}")
        raise e
    finally:
        # Clean up temporary SRT file
        if srt_file.exists():
            srt_file.unlink()


async def concatenate_videos(video_paths: List[str], output_path: Path, work_dir: Path):
    """Concatenate multiple videos into one"""

    # Create concat file in the work directory
    concat_file = work_dir / "concat_list.txt"
    print(
        f"Creating concat srt file: {work_dir.absolute() / 'srt_concatenated_content.srt'}"
    )
    print(f"Output path: {output_path.absolute()}")
    print(f"Work dir: {work_dir.absolute()}")
    print(f"Video paths to concatenate:")
    with open(concat_file, "w") as f:
        for i, video_path in enumerate(video_paths):
            print(f"  {i+1}: {video_path}")
            f.write(f"file '{video_path}'\n")

    # FFmpeg concat command
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        # "-vf",
        # f"subtitles={work_dir.absolute() / 'srt_concatenated_content.srt'}:force_style='FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=6'",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-fps_mode",  # Maintain sync during concat
        "passthrough",
        "-async",  # Audio sync
        "1",
        "-avoid_negative_ts",
        "make_zero",
        "-fflags",
        "+genpts",  # Regenerate presentation timestamps
        "-strict",
        "-2",
        "-loglevel",
        "info",
        str(output_path),
    ]

    try:
        result = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            raise Exception(f"FFmpeg concat error: {stderr.decode()}")

    finally:
        # Clean up concat file
        if concat_file.exists():
            concat_file.unlink()


def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
