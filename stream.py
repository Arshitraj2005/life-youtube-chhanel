import gdown
import subprocess
import time
import os

# 🎬 Google Drive video ID
drive_id = "1wnkZ4AnJJo7WyDQXmuV7VFtOW39xwBt9"
local_file = "video.mp4"

# 🔑 YouTube stream key
stream_key = "0akr-61bb-wc67-4qgr-c2xc"

# 🌐 Primary + Backup RTMP URLs (without format flags)
stream_url = (
    f"rtmp://a.rtmp.youtube.com/live2/{stream_key}|"
    f"rtmp://b.rtmp.youtube.com/live2/{stream_key}?backup=1"
)

def download_video():
    if os.path.exists(local_file):
        print("✅ Video already exists, skipping download.")
        return
    print("📥 Downloading video from Google Drive...")
    try:
        gdown.download(id=drive_id, output=local_file, quiet=False)
        print("✅ Download complete.")
    except Exception as e:
        print(f"🚨 Download failed: {e}")
        time.sleep(5)
        exit(1)

def stream_loop():
    while True:
        print("🎥 Starting live stream...")
        try:
            subprocess.run([
                "ffmpeg", "-re", "-i", local_file,
                "-map", "0:v:0", "-map", "0:a:0",
                "-c:v", "copy", "-c:a", "aac",
                "-f", "tee", f"[f=flv]{stream_url}"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
