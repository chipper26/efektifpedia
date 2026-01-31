import requests
import json
import os
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
# Mengambil API Key dari Environment Variable (GitHub Secrets)
API_KEY = os.getenv("OPENROUTER_API_KEY") 
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

# Folder tujuan artikel agar terbaca oleh Sveltia CMS
FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS (PERSONA) ---
# Kamu bisa ganti atau tambah nama-nama tim kamu di sini
DAFTAR_PENULIS = [
    "Nadira Kusuma",
    "Budi Santoso",
    "Citra Anggraini",
    "Andi Wijaya",
    "Raka Santosa",
    "Aditya Mahendra"
]

# Pilih satu nama secara acak
PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)

PROMPT = f"""
Cari berita teknologi paling viral hari ini ({datetime.now().strftime('%d %B %Y')}).
Tulis artikel blog mendalam minimal 500 kata dalam Bahasa Indonesia.
Gunakan gaya bahasa profesional Sistem Informasi yang informatif.
PENTING: Gunakan format Markdown murni tanpa tambahan teks penjelasan di luar markdown.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL BERITA VIRAL]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Tech News"
author: "{PENULIS_HARI_INI}"
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

    print(f"🤖 Bot sedang meriset tren untuk penulis: {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            hasil = response.json()
            konten = hasil['choices'][0]['message']['content']
            
            # Memastikan folder blog/ ada sebelum menulis file
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # Nama file unik berdasarkan waktu
            filename = os.path.join(FOLDER_TUJUAN, f"ai-news-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten)
            
            print(f"✅ BERHASIL! Artikel oleh '{PENULIS_HARI_INI}' tersimpan di: {filename}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()