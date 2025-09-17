#!/usr/bin/env python3
"""
Add manual caption to video clip
"""

try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def add_caption_to_video(video_path, caption_text, output_path="output_with_caption.mp4"):
    """Add a caption to the entire video"""

    video = VideoFileClip(video_path)

    # Create text clip (using default font)
    txt_clip = (TextClip(text=caption_text, font_size=48, color='white',
                         stroke_color='black', stroke_width=3,
                         size=(int(video.w * 0.9), None))
               .with_position(('center', 'bottom'))
               .with_duration(video.duration))

    # Composite video with text
    final = CompositeVideoClip([video, txt_clip])

    # Write the final video
    print(f"Saving video with caption to: {output_path}")
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Clean up
    video.close()
    final.close()

    return output_path


if __name__ == "__main__":
    # Add the famous Columbo line as caption
    caption = "Oh, there's just one more thing..."

    video_file = "columbo_clip.mp4"
    output_file = "columbo_with_caption.mp4"

    print(f"Adding caption to {video_file}")
    add_caption_to_video(video_file, caption, output_file)
    print(f"Done! Video saved as {output_file}")