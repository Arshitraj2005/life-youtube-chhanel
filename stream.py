import subprocess
import time

def stream_video(link):
    print(f"🎥 Streaming: {link}")
    while True:
        try:
            subprocess.run([
                "ffmpeg", "-re",
                "-i", link,
                "-c:v", "copy", "-c:a", "aac",
                "-f", "flv", "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ Stream crashed. Restarting after 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    drive_link = "https://drive.google.com/uc?id=1l2D5FA9lKWLpf6bZoRTkH8NbwNsloQ29&export=download"
    stream_video(drive_link)
