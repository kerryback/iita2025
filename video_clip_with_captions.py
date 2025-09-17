#!/usr/bin/env python3
"""
Video Clip Extractor with Closed Captions
Extracts a clip from video, keeps audio, and adds closed captions using Whisper
"""

import sys
import os
import argparse
from pathlib import Path
try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper
import json
from datetime import timedelta


def extract_clip(video_path, start_time, duration, output_path="output_clip.mp4"):
    """Extract a clip from video with audio"""
    print(f"Extracting clip from {start_time}s to {start_time + duration}s")

    video = VideoFileClip(video_path)

    # Validate time range
    if start_time >= video.duration:
        print(f"Error: Start time ({start_time}s) is beyond video duration ({video.duration:.2f}s)")
        return None

    end_time = min(start_time + duration, video.duration)

    # Extract the clip with audio
    clip = video.subclipped(start_time, end_time)

    # Save the clip
    print(f"Saving clip to: {output_path}")
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    clip.close()
    video.close()

    return output_path


def transcribe_audio(video_path, model_size="base"):
    """Transcribe audio from video using Whisper"""
    print(f"Transcribing audio using Whisper ({model_size} model)...")
    print("This may take a moment on first run to download the model...")

    model = whisper.load_model(model_size)
    result = model.transcribe(video_path, verbose=False)

    return result


def create_srt_file(transcription, output_path="captions.srt"):
    """Create SRT subtitle file from transcription"""
    print(f"Creating subtitle file: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(transcription['segments'], start=1):
            # Format timestamps
            start = str(timedelta(seconds=segment['start']))[:-3].replace('.', ',')
            end = str(timedelta(seconds=segment['end']))[:-3].replace('.', ',')

            # Ensure proper timestamp format (HH:MM:SS,mmm)
            if len(start.split(':')[0]) == 1:
                start = '0' + start
            if len(end.split(':')[0]) == 1:
                end = '0' + end

            # Write SRT format
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")

    return output_path


def add_subtitles_to_video(video_path, srt_path, output_path="output_with_captions.mp4"):
    """Add subtitles to video using moviepy"""
    print(f"Adding captions to video...")

    video = VideoFileClip(video_path)

    # Parse SRT file
    subtitles = []
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n\n')

        for block in content:
            lines = block.split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text = ' '.join(lines[2:])

                # Parse timestamps
                start_str, end_str = time_line.split(' --> ')
                start_time = parse_srt_time(start_str)
                end_time = parse_srt_time(end_str)

                subtitles.append({
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })

    # Create text clips for subtitles
    clips = [video]

    for sub in subtitles:
        txt_clip = (TextClip(sub['text'], fontsize=24, color='white',
                             stroke_color='black', stroke_width=2,
                             font='Arial', method='caption', size=(video.w * 0.8, None))
                   .set_position(('center', 'bottom'))
                   .set_start(sub['start'])
                   .set_duration(sub['end'] - sub['start']))

        clips.append(txt_clip)

    # Composite video with subtitles
    final = CompositeVideoClip(clips)

    # Write the final video
    print(f"Saving video with captions to: {output_path}")
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Clean up
    video.close()
    final.close()

    return output_path


def parse_srt_time(time_str):
    """Convert SRT timestamp to seconds"""
    time_str = time_str.replace(',', '.')
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def add_subtitles_with_ffmpeg(video_path, srt_path, output_path="output_with_captions.mp4"):
    """Alternative: Add subtitles using ffmpeg (burned in)"""
    import subprocess

    print(f"Adding captions to video using ffmpeg...")

    cmd = [
        'ffmpeg', '-i', video_path, '-vf', f"subtitles={srt_path}",
        '-c:a', 'copy', '-y', output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Video with captions saved to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error adding subtitles with ffmpeg: {e}")
        print("Falling back to moviepy method...")
        return add_subtitles_to_video(video_path, srt_path, output_path)


def main():
    parser = argparse.ArgumentParser(description="Extract video clip with audio and add captions")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("start", type=float, help="Start time in seconds")
    parser.add_argument("duration", type=float, help="Duration in seconds")
    parser.add_argument("-o", "--output", default="output_with_captions.mp4",
                       help="Output video filename")
    parser.add_argument("-m", "--model", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--srt-only", action="store_true",
                       help="Only generate SRT file, don't embed captions")
    parser.add_argument("--no-captions", action="store_true",
                       help="Extract clip without adding captions")
    parser.add_argument("--method", default="ffmpeg", choices=["ffmpeg", "moviepy"],
                       help="Method to add subtitles (default: ffmpeg)")

    args = parser.parse_args()

    # Extract the clip
    clip_path = "temp_clip.mp4" if not args.no_captions else args.output
    extracted_clip = extract_clip(args.video, args.start, args.duration, clip_path)

    if not extracted_clip:
        sys.exit(1)

    if args.no_captions:
        print(f"Clip extracted successfully: {extracted_clip}")
        return

    # Transcribe the audio
    transcription = transcribe_audio(extracted_clip, args.model)

    # Create SRT file
    srt_file = create_srt_file(transcription, "captions.srt")

    if args.srt_only:
        print(f"SRT file created: {srt_file}")
        print(f"Video clip: {extracted_clip}")
        return

    # Add subtitles to video
    if args.method == "ffmpeg":
        final_video = add_subtitles_with_ffmpeg(extracted_clip, srt_file, args.output)
    else:
        final_video = add_subtitles_to_video(extracted_clip, srt_file, args.output)

    # Clean up temp file
    if os.path.exists("temp_clip.mp4"):
        os.remove("temp_clip.mp4")

    print(f"\nCompleted! Video with captions saved to: {final_video}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        print("\nVideo Clip Extractor with Closed Captions")
        print("=" * 50)
        print("\nAvailable video: downloads/columbo_one_more_thing.mp4")
        print("Video duration: 572 seconds (9 minutes 32 seconds)")
        print("\nUsage:")
        print("  python video_clip_with_captions.py VIDEO START DURATION [options]")
        print("\nExample (extract 5 seconds starting at 30s with captions):")
        print("  python video_clip_with_captions.py downloads/columbo_one_more_thing.mp4 30 5")
        print("\nOptions:")
        print("  -o OUTPUT         Output filename")
        print("  -m MODEL          Whisper model (tiny/base/small/medium/large)")
        print("  --no-captions     Extract clip without captions")
        print("  --srt-only        Only generate SRT file")
        print("  --method METHOD   Use ffmpeg or moviepy for subtitles")
        print("\nPlease specify the time range you want to extract.")