import ffmpeg
import os
import subprocess

# Input video and subtitle file paths
video_path = r'C:\Users\xeldrago\OneDrive - MSFT\Attachments\Movies\Mozhi _ Tamil Full Movie _ Prithviraj _ Jyothika _ Prakash Raj.mp4'
subtitle_path = r'C:\Users\xeldrago\OneDrive - MSFT\Attachments\Movies\tmg-mozhi-cd1.srt'

# Output video path with embedded subtitles
output_path = 'output_video_with_subtitles.mp4'

# Check if the input files exist
if not os.path.isfile(video_path):
    print("Input video file not found.")
    exit()

if not os.path.isfile(subtitle_path):
    print("Subtitle file not found.")
    exit()

try:
    cmd = (
        ffmpeg.input(video_path)
        .output(output_path, vf=f'subtitles="{subtitle_path}"')
        .compile()
    )

    subprocess.run(cmd, stderr=subprocess.PIPE, check=True)
    print("Subtitles embedded successfully to", output_path)
except subprocess.CalledProcessError as e:
    print("Error:", e)
    print("FFmpeg stderr output:\n", e.stderr.decode())
