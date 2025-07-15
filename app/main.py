from flask import Flask, request, jsonify
import os
import threading
from app.luma_api import upload_image_to_luma, start_luma_job
from app.monitor_jobs import add_job

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
VIDEO_FOLDER = 'static/videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        user_id = data['from']
        image_url = data['content']['uri']
        local_image_path = os.path.join(UPLOAD_FOLDER, f"{user_id.replace(':', '_')}.jpg")
        os.system(f"curl -o {local_image_path} {image_url}")
        upload_id = upload_image_to_luma(local_image_path)
        job_id = start_luma_job(upload_id)
        add_job(job_id, user_id)
        return jsonify({"status": "image received and job started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def index():
    files = os.listdir(VIDEO_FOLDER)
    files = sorted([f for f in files if f.endswith(".mp4")], reverse=True)
    return f"<h1>Vídeos gerados</h1>" + "".join([f"<video src='/static/videos/{f}' controls width='400'></video><br>" for f in files])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
