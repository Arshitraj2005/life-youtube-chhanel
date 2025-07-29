import gdown
import subprocess
import time
import os
import socket
import psutil
from flask import Flask

# 🎬 Google Drive video ID
drive_id = "1wnkZ4AnJJo7WyDQXmuV7VFtOW39xwBt9"
local_file = "video.mp4"

# 🔑 YouTube stream key
stream_key = "3gr0-q51j-d1ct-8702-bdb7"
stream_url = f"rtmps://a.rtmp.youtube.com:443/live2/{stream_key}"  # Secure RTMPS!

# 🌐 Dummy Flask Server (for Render web service)
app = Flask(__name__)
@app.route("/")
def home():
    return "✅ Stream bot is live!"
def start_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

def kill_old_ffmpeg():
    for proc in psutil.process_iter(["name", "cmdline"]):
        if "ffmpeg" in proc.info["name"]:
            proc.kill()

def test_port(host="a.rtmp.youtube.com", port=443):
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect((host, port))
        return True
    except:
        return False

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
        if not test_port():
            print("🚫 Cannot reach RTMP server. Retrying in 10 sec...")
            time.sleep(10)
            continue

        kill_old_ffmpeg()
        print("🎥 Starting stream...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",
                "-i", local_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-f", "flv",
                stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=start_flask).start()
    download_video()
    stream_loop()
