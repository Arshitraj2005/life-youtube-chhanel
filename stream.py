# stream.py
import os
import time

# 🔴 Your YouTube Stream Key
STREAM_KEY = "mbbh-5q15-4khd-q11h-4cds"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"


def start_stream():
    print("🚀 Starting Stream...")
    while True:
        os.system(
            f'ffmpeg -re -stream_loop -1 -i video.mp4 '
            f'-c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k '
            f'-pix_fmt yuv420p -g 50 -c:a aac -b:a 128k '
            f'-f flv "{RTMP_URL}"')
        print("🔁 Restarting in 5 sec...")
        time.sleep(5)


if __name__ == "__main__":
    start_stream()
