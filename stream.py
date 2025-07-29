import os
import subprocess

# === CONFIG ===
VIDEO_URL = "https://drive.google.com/uc?id=1wnkZ4AnJJo7WyDQXmuV7VFtOW39xwBt9&confirm=t"
VIDEO_PATH = "video.mp4"
STREAM_KEY = "0akr-61bb-wc67-4qgr-c2xc"  # Replace with your real key

# === STEP 1: Download video if not already exists ===
if not os.path.exists(VIDEO_PATH):
    print("📥 Downloading video from Google Drive...")
    subprocess.run([
        "wget", "-O", VIDEO_PATH, VIDEO_URL
    ])
else:
    print("✅ Video already exists, skipping download.")

# === STEP 2: Launch FFmpeg to dual YouTube stream ===
ffmpeg_command = f"""
ffmpeg -re -i {VIDEO_PATH} \
-map 0:v -map 0:a \
-c:v libx264 -preset veryfast -tune zerolatency \
-c:a aac -b:a 128k -ar 44100 \
-f tee "[f=flv]rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}|[f=flv]rtmp://b.rtmp.youtube.com/live2/{STREAM_KEY}?backup=1"
"""

print("🚀 Launching stream...")
subprocess.run(ffmpeg_command, shell=True)
