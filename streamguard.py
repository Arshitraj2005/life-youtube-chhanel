import gdown
import subprocess
import time
import os
import requests

# 🚀 Configs
DRIVE_ID = "111xrQoewI2tNsoJ0hryCZekfbbINNjhy"
LOCAL_FILE = "video.mp4"
STREAM_KEY = "3gr0-q51j-d1ct-8702-bdb7"
STREAM_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
RENDER_WAKE_URL = "https://khushi-nfte.onrender.com"

def warm_up_render():
    print("🔥 Warming up Render instance...")
    try:
        requests.get(RENDER_WAKE_URL, timeout=5)
        print("✅ Render pinged successfully.")
    except Exception as e:
        print(f"⚠️ Render wake-up failed: {e}")

def download_video():
    if os.path.exists(LOCAL_FILE):
        print("📁 Video already exists, skipping download.")
        return
    print("⬇️ Downloading video from Google Drive...")
    try:
        gdown.download(id=DRIVE_ID, output=LOCAL_FILE, quiet=False)
        print("✅ Video downloaded.")
    except Exception as e:
        print(f"❌ Download error: {e}")
        time.sleep(5)
        exit(1)

def start_stream():
    print("🎥 Starting stream with FFmpeg...")
    try:
        subprocess.run([
            "ffmpeg", "-re", "-stream_loop", "-1",
            "-i", LOCAL_FILE,
            "-r", "30",                      # Force 30 fps
            "-c:v", "libx264",               # Re-encode H.264
            "-preset", "veryfast",
            "-b:v", "3000k",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "flv", STREAM_URL
        ], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ FFmpeg crashed. Retrying in 10 sec...")
        time.sleep(10)
        start_stream()

if __name__ == "__main__":
    warm_up_render()
    download_video()
    while True:
        start_stream()
