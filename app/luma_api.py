import requests

API_KEY = "SUA_API_KEY"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def upload_image_to_luma(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        r = requests.post("https://api.luma.ai/v1/upload", headers=HEADERS, files=files)
        return r.json()['upload_id']

def start_luma_job(upload_id):
    payload = {
        "input": {
            "image_id": upload_id,
            "prompt": "Futuristic AI scene with the person and Blip mascot"
        }
    }
    r = requests.post("https://api.luma.ai/v1/video", headers=HEADERS, json=payload)
    return r.json()['job_id']

def check_job_status(job_id):
    r = requests.get(f"https://api.luma.ai/v1/video/{job_id}", headers=HEADERS)
    return r.json()
