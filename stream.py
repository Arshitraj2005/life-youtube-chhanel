import gdown
import subprocess
import time
import os

drive_id = "1l2D5FA9lKWLpf6bZoRTkH8NbwNsloQ29"
local_file = "video.mp4"
stream_url = "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"  # ← Replace with your YouTube key

def download_video():
    if not os.path.exists(local_file):
        print("📥 Downloading from Google Drive...")
        gdown.download(id=drive_id, output=local_file, quiet=False)
    else:
        print("✅ Video already exists, skipping download.")

def stream_loop():
    while True:
        print("🎥 Starting stream...")
        try:
            subprocess.run([
                "ffmpeg", "-re",
                "-i", local_file,
                "-c:v", "copy", "-c:a", "aac",
                "-f", "flv", stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Restarting in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
