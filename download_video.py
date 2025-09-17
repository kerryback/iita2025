#!/usr/bin/env python3
"""
YouTube Video Downloader using yt-dlp
Downloads a YouTube video as MP4
"""

import os
import sys
from pathlib import Path
import yt_dlp


def download_youtube_video(url, output_path="downloads", filename="columbo_one_more_thing.mp4"):
    """Download YouTube video using yt-dlp"""
    print(f"Downloading video from: {url}")

    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    output_file = os.path.join(output_path, filename)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_file,
        'quiet': False,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"\nVideo Title: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 'Unknown')} seconds")

        print(f"\nVideo saved as: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=QxBnaMGP2aY"

    # Download the video
    video_file = download_youtube_video(url)
    print("\nYou can now specify the time range for creating a GIF from this video.")
    print("Example: Start at 10 seconds, duration 3 seconds")