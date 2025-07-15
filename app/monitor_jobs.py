import time
import threading
import os
import requests
from app.luma_api import check_job_status
from app.blip_api import send_video_to_user

JOBS = []

def add_job(job_id, user_id):
    JOBS.append((job_id, user_id))

def download_video(video_url, filename):
    r = requests.get(video_url)
    path = os.path.join("static/videos", filename)
    with open(path, "wb") as f:
        f.write(r.content)
    return path

def monitor_jobs():
    while True:
        for job in JOBS[:]:
            job_id, user_id = job
            result = check_job_status(job_id)
            if result.get("status") == "completed":
                video_url = result["video_url"]
                filename = f"{user_id.replace(':', '_')}_{job_id}.mp4"
                local_path = download_video(video_url, filename)
                send_video_to_user(user_id, video_url)
                JOBS.remove(job)
        time.sleep(30)

threading.Thread(target=monitor_jobs, daemon=True).start()
