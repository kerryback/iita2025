#!/usr/bin/env python3
"""
Extract audio from video and transcribe using Whisper
"""

import os
import whisper
from datetime import timedelta
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy import VideoFileClip

def extract_audio(video_path, audio_path="temp_audio.wav"):
    """Extract audio from video using moviepy"""
    print(f"Extracting audio from {video_path}...")
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, logger=None)
    video.close()
    return audio_path

def transcribe_audio_file(audio_path, model_size="tiny"):
    """Transcribe audio file using Whisper"""
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)

    print(f"Transcribing audio...")
    # Transcribe with FP32 for CPU
    result = model.transcribe(audio_path, fp16=False)

    return result

def create_srt(transcription, output_path="captions.srt"):
    """Create SRT file from transcription"""
    print(f"Creating SRT file: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        if 'segments' in transcription:
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

def add_captions_with_moviepy(video_path, transcription, output_path="output_with_captions.mp4"):
    """Add captions to video using moviepy"""
    try:
        from moviepy.editor import TextClip, CompositeVideoClip
    except ImportError:
        from moviepy import TextClip, CompositeVideoClip

    print("Adding captions to video using moviepy...")

    video = VideoFileClip(video_path)
    clips = [video]

    # Add text clips for each segment
    if 'segments' in transcription:
        for segment in transcription['segments']:
            txt_clip = (TextClip(text=segment['text'].strip(),
                                font_size=36,
                                color='white',
                                stroke_color='black',
                                stroke_width=2,
                                size=(int(video.w * 0.9), None))
                       .with_position(('center', 'bottom'))
                       .with_start(segment['start'])
                       .with_duration(segment['end'] - segment['start']))
            clips.append(txt_clip)

    # Composite all clips
    final = CompositeVideoClip(clips)

    # Write final video
    print(f"Saving to {output_path}...")
    final.write_videofile(output_path, codec='libx264', audio_codec='aac', logger=None)

    video.close()
    final.close()

    return output_path

if __name__ == "__main__":
    # Input video
    video_file = "columbo_clip.mp4"

    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found!")
        exit(1)

    print("Columbo Clip - Audio Transcription and Captioning")
    print("=" * 50)

    # Step 1: Extract audio
    print("\nStep 1: Extracting audio...")
    audio_file = extract_audio(video_file, "columbo_audio.wav")

    # Step 2: Transcribe
    print("\nStep 2: Transcribing audio...")
    transcription = transcribe_audio_file(audio_file, model_size="tiny")

    print("\nTranscription:")
    print("-" * 30)
    print(transcription['text'])
    print("-" * 30)

    # Step 3: Create SRT
    print("\nStep 3: Creating SRT file...")
    srt_file = create_srt(transcription, "columbo_captions.srt")
    print(f"SRT file created: {srt_file}")

    # Step 4: Add captions to video
    print("\nStep 4: Adding captions to video...")
    output_file = add_captions_with_moviepy(video_file, transcription, "columbo_with_captions.mp4")

    # Clean up temp audio
    if os.path.exists(audio_file):
        os.remove(audio_file)

    print(f"\n✓ Complete! Video with captions: {output_file}")
    print(f"✓ SRT file: {srt_file}")