import os
import requests
import json
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
API_KEY = str(os.getenv("API_AI_KEY", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip()
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS TETAP ---
DAFTAR_PENULIS = [
    "Nadira Kusuma", "Budi Santoso", "Citra Anggraini",
    "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"
]

# --- DAFTAR BIDANG REVIEW & TUTORIAL ---
DAFTAR_BIDANG = [
    "Tutorial Tools AI (ChatGPT, Gemini, Midjourney)",
    "Review Software Produktivitas (Notion, Trello, Obsidian)",
    "Tutorial Web Development Modern",
    "Review Gadget & Tech Gear Terbaru",
    "Tips Optimasi Sistem Windows & Android",
    "Tutorial Desain Visual (Canva, Figma, CapCut)",
    "Review Layanan Cloud & Keamanan Digital",
    "Panduan Otomasi & Scripting Pemula"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
BIDANG_HARI_INI = random.choice(DAFTAR_BIDANG)

# --- PROMPT (LEBIH TEGAS & AKURAT) ---
PROMPT = f"""
Tulis artikel tutorial/review untuk blog Efektifpedia.
TOPIK: {BIDANG_HARI_INI}.

WAJIB FRONTMATTER (Gunakan kutip pada kategori):
---
title: "[JUDUL MENARIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Review & Tutorial"
author: "{PENULIS_HARI_INI}"
---

INSTRUKSI:
1. Tulis minimal 600 kata, gaya bahasa edukatif tapi santai.
2. Berikan langkah praktis atau analisis mendalam.
3. Gunakan Markdown.

PENTING UNTUK GAMBAR:
Di akhir artikel, tuliskan 2-3 kata kunci bahasa Inggris yang SANGAT RELEVAN dengan isi artikel untuk pencarian gambar.
Contoh: 'chatgpt ai laptop' atau 'smartphone review camera'.
Tulis saja kata kunci tersebut di BARIS TERAKHIR tanpa tanda baca apapun.
"""

def get_pexels_thumbnail(query):
    """Fungsi mengambil gambar dengan query yang lebih lengkap"""
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY: return fallback_img
    
    # Ambil seluruh keyword dari baris terakhir (maksimal 3 kata)
    clean_query = query.strip().lower().replace(".", "").replace('"', "")
    
    headers = {"Authorization": PEXELS_KEY}
    # Cari gambar landscape yang benar-benar relevan
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=5&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                # Pilih secara acak dari 5 hasil teratas agar bervariasi
                return random.choice(data['photos'])['src']['landscape']
    except:
        pass
    return fallback_img

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: API_AI_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.7
    }

    print(f"🛠️ Bot sedang bekerja untuk {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_data = response.json()
            raw_content = res_data['choices'][0]['message']['content']
            
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip() # Ambil keyword pencarian gambar
            artikel_body = "\n".join(lines[:-1]) 
            
            img_url = get_pexels_thumbnail(keyword)

            # Injeksi thumbnail ke frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"tutorial-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Gambar dicari dengan: {keyword}")
            print(f"🔗 URL Gambar: {img_url}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Kendala: {str(e)}")

if __name__ == "__main__":
    tulis_artikel()