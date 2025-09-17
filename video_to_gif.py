#!/usr/bin/env python3
"""
Video to GIF Converter
Converts a portion of a video file to GIF
"""

import sys
import os
import argparse

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    print("Error: moviepy not installed. Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
    from moviepy.editor import VideoFileClip


def create_gif_from_video(video_path, start_time, duration, output_gif="output.gif",
                         fps=10, scale=None, optimize=True):
    """
    Extract a clip from video and convert to GIF

    Args:
        video_path: Path to the video file
        start_time: Start time in seconds
        duration: Duration of the clip in seconds
        output_gif: Output GIF file path
        fps: Frames per second for the GIF
        scale: Width of the GIF (height will be proportional)
        optimize: Whether to optimize the GIF size
    """
    print(f"Creating GIF from {start_time}s to {start_time + duration}s")

    try:
        # Load the video
        print(f"Loading video: {video_path}")
        video = VideoFileClip(video_path)

        print(f"Video duration: {video.duration:.2f} seconds")

        # Validate time range
        if start_time >= video.duration:
            print(f"Error: Start time ({start_time}s) is beyond video duration ({video.duration:.2f}s)")
            sys.exit(1)

        end_time = min(start_time + duration, video.duration)
        actual_duration = end_time - start_time

        # Extract the clip
        print(f"Extracting clip from {start_time}s to {end_time:.2f}s (duration: {actual_duration:.2f}s)")
        clip = video.subclip(start_time, end_time)

        # Resize if scale is specified
        if scale:
            print(f"Resizing to width: {scale}px")
            clip = clip.resize(width=scale)

        # Convert to GIF
        print(f"Converting to GIF: {output_gif}")
        print("This may take a moment...")

        # Use different optimization settings for better quality
        clip.write_gif(output_gif, fps=fps, program='ffmpeg', opt="OptimizePlus" if optimize else None)

        # Clean up
        clip.close()
        video.close()

        print(f"\nGIF created successfully: {output_gif}")
        print(f"File size: {os.path.getsize(output_gif) / 1024 / 1024:.2f} MB")
        return output_gif

    except Exception as e:
        print(f"Error creating GIF: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert video clip to GIF")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("start", type=float, help="Start time in seconds")
    parser.add_argument("duration", type=float, help="Duration in seconds")
    parser.add_argument("-o", "--output", default="output.gif", help="Output GIF filename")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Frames per second (default: 10)")
    parser.add_argument("-w", "--width", type=int, help="Width of the GIF (height will be proportional)")
    parser.add_argument("--no-optimize", action="store_true", help="Disable GIF optimization")

    args = parser.parse_args()

    # Create the GIF
    create_gif_from_video(
        args.video,
        args.start,
        args.duration,
        args.output,
        fps=args.fps,
        scale=args.width,
        optimize=not args.no_optimize
    )


if __name__ == "__main__":
    # Check if run with arguments
    if len(sys.argv) > 1:
        main()
    else:
        # Interactive mode
        print("\nVideo to GIF Converter")
        print("=" * 50)
        print("\nAvailable video: downloads/columbo_one_more_thing.mp4")
        print("Video duration: 572 seconds (9 minutes 32 seconds)")
        print("\nTo create a GIF, run:")
        print("  python video_to_gif.py downloads/columbo_one_more_thing.mp4 START_TIME DURATION")
        print("\nExample:")
        print("  python video_to_gif.py downloads/columbo_one_more_thing.mp4 30 3 -o columbo.gif")
        print("\nOptions:")
        print("  -o OUTPUT    Output filename (default: output.gif)")
        print("  -f FPS       Frames per second (default: 10)")
        print("  -w WIDTH     Width in pixels (height scales proportionally)")
        print("\nPlease specify the time range you want to convert to GIF.")