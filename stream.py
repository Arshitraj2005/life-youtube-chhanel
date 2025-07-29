import gdown
import subprocess
import time
import os

# 🎬 Your Google Drive video ID
drive_id = "1wnkZ4AnJJo7WyDQXmuV7VFtOW39xwBt9"
local_file = "video.mp4"

# 🔑 YouTube Stream Key via Environment Variable
stream_key = os.environ.get("3gr0-q51j-d1ct-8702-bdb7")

# 🔁 Stream URL using tee muxer (Primary + Backup)
stream_url = (
    f"[f=flv]rtmp://a.rtmp.youtube.com/live2/{stream_key}|"
    f"[f=flv]rtmp://b.rtmp.youtube.com/live2/{stream_key}"
)

def download_video():
    if os.path.exists(local_file):
        print("✅ Video already exists, skipping download.")
        return

    print("📥 Starting download from Google Drive...")
    try:
        gdown.download(id=drive_id, output=local_file, quiet=False)
        print("✅ Download complete.")
    except Exception as e:
        print(f"🚨 Download failed: {e}")
        time.sleep(5)
        exit(1)

def stream_loop():
    while True:
        print("🎥 Starting stream...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",
                "-i", local_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-f", "tee",
                stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
