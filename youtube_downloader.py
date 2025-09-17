#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads a YouTube video as MP4
"""

import sys
from pathlib import Path
from pytube import YouTube


def download_youtube_video(url, output_path="downloads", filename=None):
    """Download YouTube video and return the file path"""
    print(f"Downloading video from: {url}")

    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)

    try:
        # Create YouTube object
        yt = YouTube(url)

        print(f"Video Title: {yt.title}")
        print(f"Video Length: {yt.length} seconds")

        # Get the highest resolution stream with audio
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if not stream:
            # If no progressive stream, get the highest quality video stream
            stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()

        if not stream:
            raise Exception("No suitable video stream found")

        print(f"Stream Quality: {stream.resolution}")

        # Download the video
        print(f"Downloading...")
        if filename:
            output_file = stream.download(output_path=output_path, filename=filename)
        else:
            output_file = stream.download(output_path=output_path)

        print(f"Downloaded successfully to: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=QxBnaMGP2aY"

    # Download the video
    video_file = download_youtube_video(url, filename="columbo_one_more_thing.mp4")
    print(f"\nVideo saved as: {video_file}")
    print("\nYou can now specify the time range for creating a GIF from this video.")