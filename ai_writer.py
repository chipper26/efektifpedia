import requests
import json
import os
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
# Mengambil API Key dari Environment Variable (GitHub Secrets)
API_KEY = os.getenv("OPENROUTER_API_KEY") 
PEXELS_KEY = os.getenv("PEXELS_API_KEY") # Tambahkan ini di GitHub Secrets!
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

# Folder tujuan artikel agar terbaca oleh Sveltia CMS
FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS (PERSONA) ---
DAFTAR_PENULIS = [
    "Nadira Kusuma",
    "Budi Santoso",
    "Citra Anggraini",
    "Andi Wijaya",
    "Raka Santosa",
    "Aditya Mahendra"
]

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

Di bagian paling akhir setelah artikel selesai, tuliskan tepat satu kata kunci singkat dalam bahasa Inggris untuk mencari gambar thumbnail yang relevan (contoh: 'technology', 'server', 'ai'). Tulis saja katanya di baris baru tanpa tanda baca.
"""

def get_pexels_thumbnail(query):
    """Fungsi mengambil foto asli dari API Pexels"""
    if not PEXELS_KEY:
        # Fallback jika key belum diset
        return "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"
    
    headers = {"Authorization": PEXELS_KEY}
    pexels_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                # Mengambil URL gambar ukuran besar yang sudah di-crop
                return data['photos'][0]['src']['landscape']
    except Exception as e:
        print(f"⚠️ Gagal mengambil gambar Pexels: {e}")
    
    return "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: OPENROUTER_API_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia Bot"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}]
    }

    print(f"🤖 Bot sedang meriset tren untuk penulis: {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            # --- LOGIKA EKSTRAKSI KEYWORD & THUMBNAIL ---
            lines = raw_content.strip().split('\n')
            keyword = lines[-1].strip().lower() # Keyword dari AI
            artikel_body = "\n".join(lines[:-1]) 
            
            # Ambil URL gambar resmi dari Pexels
            img_url = get_pexels_thumbnail(keyword)

            # Masukkan thumbnail ke dalam Frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"ai-news-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Penulis: {PENULIS_HARI_INI} | Gambar: {keyword}")
            print(f"Link Gambar: {img_url}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()