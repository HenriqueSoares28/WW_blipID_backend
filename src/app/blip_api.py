import os
import requests

BLIP_KEY = os.environ.get("BLIP_API_KEY")

def send_video_to_user(user_id, video_url):
    headers = {
        "Authorization": f"Key {BLIP_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": user_id,
        "type": "application/vnd.lime.media-link+json",
        "content": {
            "uri": video_url,
            "type": "video/mp4",
            "title": "Seu vídeo está pronto!",
            "text": "Veja o vídeo que criamos para você com IA e o Blipinho 🤖"
        }
    }
    requests.post("https://http.msging.net/messages", headers=headers, json=payload)
