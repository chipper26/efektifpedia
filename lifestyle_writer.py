import os
import requests
import random
from datetime import datetime

# Daftar Topik agar tidak bosan
topics = [
    "Tips produktivitas kerja remote untuk pemula",
    "Manfaat gaya hidup minimalis di era digital",
    "Cara belajar skill baru secara otodidak dengan AI",
    "Tips menjaga kesehatan mental bagi pekerja digital",
    "Strategi mengatur waktu dengan teknik Pomodoro",
    "Rekomendasi gadget esensial untuk meja kerja minimalis"
]

selected_topic = random.choice(topics)

def generate_article():
    api_key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Tuliskan artikel blog dalam bahasa Indonesia tentang: {selected_topic}. JANGAN bahas Cloud Computing. Gunakan format Markdown, sertakan tips praktis, dan buat gaya bahasa yang asik untuk anak muda."
    
    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# (Tambahkan logika save file & integrasi Pexels seperti di script pertamamu)
print(f"Sedang memproses topik: {selected_topic}")