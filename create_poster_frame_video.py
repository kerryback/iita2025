#!/usr/bin/env python3
"""
Create a video with the final frame at the beginning as a poster frame
"""

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except ImportError:
    from moviepy import VideoFileClip, concatenate_videoclips

def create_poster_frame_video(input_video, output_video, poster_duration=0.1):
    """
    Create a video with the final frame at the beginning
    """
    print(f"Loading video: {input_video}")
    video = VideoFileClip(input_video)

    # Get the final frame as a short clip
    final_frame_time = video.duration - 0.01  # Just before the end
    poster_clip = video.subclipped(final_frame_time, video.duration).with_duration(poster_duration)

    # Concatenate poster frame + original video
    final_video = concatenate_videoclips([poster_clip, video])

    print(f"Creating video with poster frame: {output_video}")
    final_video.write_videofile(output_video, codec='libx264', audio_codec='aac', logger=None)

    video.close()
    final_video.close()

    return output_video

if __name__ == "__main__":
    input_file = "columbo_2p5sec_with_captions.mp4"
    output_file = "columbo_with_poster_frame.mp4"

    create_poster_frame_video(input_file, output_file)
    print(f"Done! New video: {output_file}")
    print("This video will show the final frame at the start and when played will show the full sequence.")