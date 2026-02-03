import requests
import json
import os
import random
from datetime import datetime
import re

# --- KONFIGURASI AMAN ---
# Pastikan nama Secret di GitHub sesuai (API_AI_KEY dan PEXELS_API_KEY)
API_KEY = str(os.getenv("API_AI_KEY", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip()
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS ---
DAFTAR_PENULIS = ["Nadira Kusuma", "Budi Santoso", "Citra Anggraini", "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"]

# --- DAFTAR BIDANG INOVASI ---
DAFTAR_BIDANG = [
    "Inovasi Kecerdasan Buatan (AI) Masa Depan",
    "Teknologi Energi Terbarukan yang Revolusioner",
    "Terobosan Eksplorasi Luar Angkasa Modern",
    "Perkembangan Komputasi Kuantum",
    "Inovasi Transportasi Listrik dan Otonom",
    "Evolusi Teknologi Medis dan Bioteknologi"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
BIDANG_HARI_INI = random.choice(DAFTAR_BIDANG)

# --- PROMPT KATEGORI INNOVATION ---
PROMPT = f"""
Cari tren inovasi teknologi terbaru mengenai {BIDANG_HARI_INI}.
Tulis artikel blog mendalam minimal 600 kata dalam Bahasa Indonesia.

Gunakan gaya bahasa profesional namun inspiratif. 
Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL INOVASI YANG MENGEJUTKAN]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Innovation"
author: "{PENULIS_HARI_INI}"
---

PENTING:
Gunakan format Markdown murni. 
Di baris paling terakhir setelah artikel selesai, tuliskan tepat satu kata kunci singkat dalam bahasa Inggris (hanya satu kata) untuk gambar thumbnail (contoh: 'future', 'innovation', 'robot', 'tech'). 
Tulis saja katanya tanpa tanda baca.
"""

def get_pexels_url(query):
    """Logika: Mengambil URL gambar resmi dari Pexels"""
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    headers = {"Authorization": PEXELS_KEY}
    # Per page 1 untuk efisiensi
    pexels_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return data['photos'][0]['src']['landscape']
    except Exception as e:
        print(f"⚠️ Gagal mengambil Pexels: {e}")
    
    return fallback_img

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: API_AI_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia Innovation Bot"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.8
    }

    print(f"🚀 Menjelajahi inovasi: {BIDANG_HARI_INI} oleh {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data), timeout=60)
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            # --- LOGIKA EKSTRAKSI ---
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            # Mengambil tepat satu kata kunci di baris terakhir
            keyword = lines[-1].strip().lower().split()[-1] 
            artikel_body = "\n".join(lines[:-1]) 
            
            # AMBIL URL GAMBAR
            img_url = get_pexels_url(keyword)

            # Masukkan link URL ke dalam Frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            # PAKSA KATEGORI: Innovation agar sinkron dengan blog.html
            konten_final = re.sub(r'category:.*', 'category: "Innovation"', konten_final)
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # Nama file unik
            filename = os.path.join(FOLDER_TUJUAN, f"innovation-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Kategori: Innovation")
            print(f"🔗 Thumbnail: {img_url} (Keyword: {keyword})")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()