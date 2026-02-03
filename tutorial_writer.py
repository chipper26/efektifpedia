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

# --- PROMPT (DISESUAIKAN DENGAN STRUKTUR HTML BLOG) ---
PROMPT = f"""
Tulis artikel untuk Efektifpedia.
BIDANG: {BIDANG_HARI_INI}.

WAJIB FRONTMATTER (Pastikan kategori menggunakan tanda kutip dua):
---
title: "[JUDUL MENARIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Review & Tutorial"
author: "{PENULIS_HARI_INI}"
---

INSTRUKSI:
1. Tulis minimal 600 kata dalam Bahasa Indonesia.
2. Gaya bahasa profesional namun mudah dimengerti.
3. Gunakan Markdown murni.

PENTING UNTUK VISUAL:
Setelah artikel selesai, di baris paling terakhir sendiri, tuliskan 3 kata kunci bahasa Inggris yang spesifik menggambarkan isi artikel untuk mencari gambar di Pexels.
Contoh jika bahas ChatGPT: 'chatgpt robot laptop'
Contoh jika bahas Smartphone: 'smartphone camera tech'
Tulis 3 kata tersebut tanpa tanda baca apapun.
"""

def get_pexels_thumbnail(query):
    """Fungsi mengambil gambar dengan query jamak agar lebih akurat"""
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY: return fallback_img
    
    # Membersihkan query dari baris terakhir AI
    clean_query = query.strip().lower().replace(".", "").replace('"', "")
    
    headers = {"Authorization": PEXELS_KEY}
    # Mencari gambar landscape yang relevan
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=5&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                # Ambil satu secara acak dari 5 hasil agar bervariasi
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

    print(f"🛠️ Sedang menyusun 'Review & Tutorial' oleh {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_data = response.json()
            raw_content = res_data['choices'][0]['message']['content']
            
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip() # 3 kata kunci terakhir
            artikel_body = "\n".join(lines[:-1]) 
            
            img_url = get_pexels_thumbnail(keyword)

            # Injeksi thumbnail dan memastikan format frontmatter terbaca script blog.html
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"tutorial-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Gambar dicari dengan query: {keyword}")
            print(f"🔗 URL Gambar: {img_url}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Kendala: {str(e)}")

if __name__ == "__main__":
    tulis_artikel()