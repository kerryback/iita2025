#!/usr/bin/env python3
"""
Transcribe video and add captions using Whisper
Works with the extracted clip
"""

import os
import whisper
from datetime import timedelta

def transcribe_video(video_path, model_size="tiny"):
    """Transcribe video using Whisper"""
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)

    print(f"Transcribing {video_path}...")
    # Set fp16=False to use FP32 on CPU
    result = model.transcribe(video_path, fp16=False, verbose=True)

    return result

def create_srt(transcription, output_path="captions.srt"):
    """Create SRT file from transcription"""
    print(f"Creating SRT file: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(transcription['segments'], start=1):
            # Format timestamps
            start = str(timedelta(seconds=segment['start']))[:-3].replace('.', ',')
            end = str(timedelta(seconds=segment['end']))[:-3].replace('.', ',')

            # Ensure proper format
            if len(start.split(':')[0]) == 1:
                start = '0' + start
            if len(end.split(':')[0]) == 1:
                end = '0' + end

            # Write SRT format
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")

    return output_path

def burn_subtitles_ffmpeg(video_path, srt_path, output_path="output_captioned.mp4"):
    """Use ffmpeg to burn subtitles into video"""
    import subprocess

    # Try to find ffmpeg
    ffmpeg_paths = [
        "ffmpeg",
        r"C:\Users\kerry\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe",
        r"C:\ProgramData\ffmpeg\bin\ffmpeg.exe",
    ]

    ffmpeg_cmd = None
    for path in ffmpeg_paths:
        try:
            subprocess.run([path, "-version"], capture_output=True, check=True)
            ffmpeg_cmd = path
            print(f"Found ffmpeg at: {path}")
            break
        except:
            continue

    if not ffmpeg_cmd:
        print("FFmpeg not found. Please ensure ffmpeg is installed and in PATH")
        return None

    print(f"Adding subtitles to video...")

    # Use subtitles filter to burn in the captions
    cmd = [
        ffmpeg_cmd,
        '-i', video_path,
        '-vf', f"subtitles='{srt_path}':force_style='Fontsize=24,PrimaryColour=&Hffffff&,OutlineColour=&H000000&,Outline=2'",
        '-c:a', 'copy',
        '-y',
        output_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Video with captions saved to: {output_path}")
            return output_path
        else:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error running ffmpeg: {e}")
        return None

if __name__ == "__main__":
    # Input video (the clip we extracted)
    video_file = "columbo_clip.mp4"

    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found!")
        print("Please run the extraction script first.")
        exit(1)

    print("Columbo Clip Transcription and Captioning")
    print("=" * 50)

    # Step 1: Transcribe
    print("\nStep 1: Transcribing audio...")
    transcription = transcribe_video(video_file, model_size="tiny")

    print("\nTranscription:")
    print(transcription['text'])

    # Step 2: Create SRT
    print("\nStep 2: Creating SRT file...")
    srt_file = create_srt(transcription, "columbo_captions.srt")

    # Step 3: Add captions to video
    print("\nStep 3: Adding captions to video...")
    output_file = burn_subtitles_ffmpeg(video_file, srt_file, "columbo_with_captions.mp4")

    if output_file:
        print(f"\n✓ Success! Video with captions: {output_file}")
    else:
        print("\n✗ Could not add captions with ffmpeg.")
        print(f"However, SRT file created: {srt_file}")
        print("You can use a video player that supports SRT files to view with captions.")