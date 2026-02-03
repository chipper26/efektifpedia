import os
import requests
import json
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
# Menggunakan API_AI_KEY sesuai mapping di file .yml
API_KEY = str(os.getenv("API_AI_KEY", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip()
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS TETAP ---
DAFTAR_PENULIS = ["Nadira Kusuma", "Budi Santoso", "Citra Anggraini", "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"]

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

# --- PROMPT (LOGIKA KATEGORI & KEYWORD GAMBAR) ---
PROMPT = f"""
Tulis artikel tutorial/review untuk blog Efektifpedia.
FOKUS MATERI: {BIDANG_HARI_INI}.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL MENARIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Review & Tutorial"
author: "{PENULIS_HARI_INI}"
---

INSTRUKSI:
1. Tulis minimal 600 kata dalam Bahasa Indonesia.
2. Berikan langkah praktis atau analisis kelebihan & kekurangan.
3. Gunakan Markdown murni.

PENTING UNTUK GAMBAR:
Di baris paling terakhir sendiri setelah artikel selesai, tuliskan tepat satu kata kunci bahasa Inggris yang paling mewakili visual artikel (contoh: 'laptop', 'code', 'smartphone', 'robot'). Tulis saja satu kata tersebut tanpa tanda baca.
"""

def get_pexels_url(query):
    """Logika contek: Mengambil satu URL gambar resmi dari Pexels"""
    fallback_img = "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    headers = {"Authorization": PEXELS_KEY}
    # Per page 1 agar efisien sesuai logika contek
    pexels_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return data['photos'][0]['src']['landscape']
    except Exception as e:
        print(f"⚠️ Gagal mengambil link Pexels: {e}")
    
    return fallback_img

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: API_AI_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia TutorialBot"
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
            raw_content = response.json()['choices'][0]['message']['content']
            
            # --- LOGIKA EKSTRAKSI CONTEK ---
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            # Mengambil tepat satu kata kunci di baris terakhir
            keyword = lines[-1].strip().lower().split()[-1] 
            artikel_body = "\n".join(lines[:-1]) 
            
            # Ambil URL Gambar
            img_url = get_pexels_url(keyword)

            # Injeksi thumbnail dan kunci kategori agar tidak pecah di blog.html
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            ).replace(
                'category: Review & Tutorial', 'category: "Review & Tutorial"'
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"tutorial-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Keyword Gambar: {keyword}")
            print(f"🔗 Thumbnail: {img_url}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Kendala: {str(e)}")

if __name__ == "__main__":
    tulis_artikel()