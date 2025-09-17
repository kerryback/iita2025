#!/usr/bin/env python3
"""
Transcribe video with manual ffmpeg path setting
"""

import os
import sys
import whisper
from datetime import timedelta

# Add ffmpeg to PATH before importing whisper audio module
ffmpeg_path = r"C:\Users\kerry\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

def transcribe_video_directly(video_path, model_size="tiny"):
    """Transcribe video using Whisper with ffmpeg in PATH"""
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)

    print(f"Transcribing {video_path}...")
    # Use FP32 for CPU
    result = model.transcribe(video_path, fp16=False)

    return result

def create_srt(transcription, output_path="captions.srt"):
    """Create SRT file from transcription"""
    with open(output_path, 'w', encoding='utf-8') as f:
        if 'segments' in transcription:
            for i, segment in enumerate(transcription['segments'], start=1):
                # Format timestamps
                start_seconds = segment['start']
                end_seconds = segment['end']

                # Convert to SRT format (HH:MM:SS,mmm)
                start_time = f"{int(start_seconds//3600):02d}:{int((start_seconds%3600)//60):02d}:{int(start_seconds%60):02d},{int((start_seconds%1)*1000):03d}"
                end_time = f"{int(end_seconds//3600):02d}:{int((end_seconds%3600)//60):02d}:{int(end_seconds%60):02d},{int((end_seconds%1)*1000):03d}"

                # Write SRT format
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")

    return output_path

if __name__ == "__main__":
    video_file = "columbo_clip.mp4"

    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found!")
        exit(1)

    print("Columbo Clip Transcription")
    print("=" * 50)

    try:
        # Test ffmpeg availability
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] FFmpeg found in PATH")
        else:
            print("[WARNING] FFmpeg may not be properly configured")
    except:
        print("[WARNING] Could not verify ffmpeg")

    print("\nTranscribing video...")
    transcription = transcribe_video_directly(video_file, model_size="tiny")

    print("\n" + "=" * 50)
    print("TRANSCRIPTION:")
    print("=" * 50)
    print(transcription['text'].strip())
    print("=" * 50)

    # Create SRT file
    srt_file = create_srt(transcription, "columbo_captions.srt")
    print(f"\n[SUCCESS] SRT file created: {srt_file}")

    # Show how to use the SRT file
    print("\nTo add captions to your video:")
    print("1. Use a video player like VLC that supports SRT files")
    print("2. Or use ffmpeg command:")
    print(f'   ffmpeg -i {video_file} -vf "subtitles={srt_file}" columbo_final.mp4')