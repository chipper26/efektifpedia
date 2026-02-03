import os
import requests
import json
import random
from datetime import datetime
import re

# --- KONFIGURASI AMAN ---
API_KEY = str(os.getenv("API_AI_KEY", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip()
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS ---
DAFTAR_PENULIS = ["Nadira Kusuma", "Budi Santoso", "Citra Anggraini", "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"]

# --- BIDANG (Ganti spasi & agar lebih aman saat dicari) ---
DAFTAR_BIDANG = [
    "Tutorial Tools AI terbaru",
    "Review Software Produktivitas",
    "Tutorial Web Development",
    "Review Gadget dan Hardware",
    "Tips Windows dan Android",
    "Tutorial Desain Digital"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
BIDANG_HARI_INI = random.choice(DAFTAR_BIDANG)

PROMPT = f"""
Tulis artikel tutorial/review teknologi untuk Efektifpedia.
TOPIK: {BIDANG_HARI_INI}.
Tulis minimal 600 kata dalam Bahasa Indonesia.

Wajib sertakan Frontmatter:
---
title: "[JUDUL]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: Review & Tutorial
author: "{PENULIS_HARI_INI}"
---
Di baris terakhir, tulis satu kata kunci Inggris untuk gambar.
"""

def get_pexels_url(query):
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY: return fallback_img
    headers = {"Authorization": PEXELS_KEY}
    try:
        res = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=1", headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json()['photos'][0]['src']['landscape']
    except: pass
    return fallback_img

def tulis_artikel():
    if not API_KEY: return
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": MODEL, "messages": [{"role": "user", "content": PROMPT}]}
    
    try:
        response = requests.post(URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip().lower().split()[-1]
            artikel_body = "\n".join(lines[:-1])
            img_url = get_pexels_url(keyword)

            # --- TRICK AGAR KONEK KE KATEGORI ---
            # Kita paksa tulisannya bersih tanpa kutip dan tanpa spasi aneh
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            # Paksa baris category agar PERSIS sama dengan yang dicari JavaScript
            konten_final = re.sub(r'category:.*', 'category: Review & Tutorial', konten_final)
            
            if not os.path.exists(FOLDER_TUJUAN): os.makedirs(FOLDER_TUJUAN)
            filename = os.path.join(FOLDER_TUJUAN, f"tutorial-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            print(f"✅ Berhasil! Kategori: Review & Tutorial")
        else:
            print(f"❌ API Error")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    tulis_artikel()