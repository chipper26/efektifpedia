import requests
import json
import os
from datetime import datetime

# --- KONFIGURASI AMAN ---
# Mengambil API Key dari Environment Variable (GitHub Secrets)
API_KEY = os.getenv("OPENROUTER_API_KEY") 
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

# Menentukan folder tujuan (drafts/) agar sesuai dengan konfigurasi Sveltia CMS kamu
FOLDER_TUJUAN = "blog" # Sesuaikan dengan folder konten blog kamu

PROMPT = f"""
Cari berita teknologi paling viral hari ini ({datetime.now().strftime('%d %B %Y')}).
Tulis artikel blog mendalam minimal 500 kata dalam Bahasa Indonesia.
Gunakan gaya bahasa profesional Sistem Informasi.
PENTING: Gunakan format Markdown murni tanpa tambahan teks penjelasan di luar markdown.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL BERITA VIRAL]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Tech News"
author: "Efektifpedia AI Bot"
---
"""

def tulis_artikel():
    # Validasi API Key
    if not API_KEY:
        print("❌ Error: OPENROUTER_API_KEY tidak ditemukan di environment variables!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia Bot"
    }
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": PROMPT}
        ]
    }

    print(f"🤖 Bot sedang meriset tren via OpenRouter ({MODEL})...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            hasil = response.json()
            konten = hasil['choices'][0]['message']['content']
            
            # Memastikan folder tujuan ada
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # Nama file menggunakan format tanggal agar rapi di CMS
            filename = os.path.join(FOLDER_TUJUAN, f"ai-news-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten)
            
            print(f"✅ BERHASIL! File draf tercipta di: {filename}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()