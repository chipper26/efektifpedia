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
    "Tutorial Tools AI (Cara pakai ChatGPT, Midjourney, atau Gemini untuk produktivitas)",
    "Review Software/Aplikasi (Aplikasi manajemen tugas, editor foto, atau browser)",
    "Tutorial Web Development (Panduan praktis HTML, CSS, atau Deployment situs)",
    "Review Gadget & Hardware (Spesifikasi smartphone, TWS, atau aksesoris laptop)",
    "Tips & Tutorial Windows/Android (Optimasi sistem, fitur tersembunyi, keamanan)",
    "Tutorial Desain Digital (Canva, Figma, atau editing video simpel)",
    "Review Layanan Digital (Cloud storage, VPN, atau platform belajar online)",
    "Panduan Pemrograman Praktis (Membuat bot, otomasi script, atau pengenalan API)"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
BIDANG_HARI_INI = random.choice(DAFTAR_BIDANG)

# --- PROMPT (DIPERBAIKI UNTUK FILTER KATEGORI) ---
PROMPT = f"""
Tugas kamu adalah menulis artikel untuk Efektifpedia.
FOKUS MATERI: {BIDANG_HARI_INI}.

Wajib sertakan Frontmatter di bagian paling atas dengan format PERSIS seperti ini:
---
title: "[JUDUL MENARIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Review & Tutorial"
author: "{PENULIS_HARI_INI}"
---

INSTRUKSI KONTEN:
1. Tulis minimal 600 kata dalam Bahasa Indonesia.
2. Artikel harus berupa Panduan/Tutorial atau Review Mendalam.
3. Gunakan Markdown murni.

PENTING:
Kategori wajib menggunakan tanda kutip "Review & Tutorial" agar simbol ampersand terbaca oleh sistem filter blog.
Di baris paling terakhir (setelah artikel selesai), tuliskan satu kata kunci bahasa Inggris untuk gambar (Contoh: smartphone).
"""

def get_pexels_thumbnail(query):
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    clean_query = query.strip().lower().replace(".", "").replace('"', "").split()[-1]
    headers = {"Authorization": PEXELS_KEY}
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=3&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
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
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia Bot"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.7
    }

    print(f"🛠️ Sedang memproses artikel oleh {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_data = response.json()
            raw_content = res_data['choices'][0]['message']['content']
            
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip()
            artikel_body = "\n".join(lines[:-1]) 
            
            img_url = get_pexels_thumbnail(keyword)

            # Memastikan kategori terbungkus kutip saat replace author
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"tutorial-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! File tersimpan: {filename}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Kendala teknis: {str(e)}")

if __name__ == "__main__":
    tulis_artikel()