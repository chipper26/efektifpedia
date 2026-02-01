import os
import requests
import json
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
API_KEY = os.getenv("OPENROUTER_API_KEY_BACKUP") 
PEXELS_KEY = os.getenv("PEXELS_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS (Sesuai Karyawan Kemarin) ---
DAFTAR_PENULIS = [
    "Nadira Kusuma",
    "Budi Santoso",
    "Citra Anggraini",
    "Andi Wijaya",
    "Raka Santosa",
    "Aditya Mahendra"
]

# Daftar Topik Lifestyle (Variasi agar tidak Cloud Computing terus)
DAFTAR_TOPIK = [
    "Tips produktivitas kerja remote (WFA) agar tetap fokus",
    "Pentingnya gaya hidup minimalis untuk kesehatan mental di era digital",
    "Cara memanfaatkan AI untuk belajar skill baru secara mandiri",
    "Tips menata meja kerja (desk setup) minimalis untuk meningkatkan inspirasi",
    "Panduan memulai kebiasaan membaca buku di tengah kesibukan digital",
    "Manfaat 'Digital Detox' bagi kesehatan mata dan pikiran"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
TOPIK_HARI_INI = random.choice(DAFTAR_TOPIK)

PROMPT = f"""
Tulis artikel blog menarik tentang: {TOPIK_HARI_INI}.
Target pembaca: Anak muda dan profesional digital.
Panjang artikel: Minimal 500 kata dalam Bahasa Indonesia yang santai tapi edukatif.
JANGAN bahas tentang Cloud Computing atau Infrastruktur IT berat.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL MENARIK SESUAI TOPIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Lifestyle"
author: "{PENULIS_HARI_INI}"
---

Di bagian paling akhir setelah artikel selesai, tuliskan tepat satu kata kunci singkat dalam bahasa Inggris untuk mencari gambar thumbnail di Pexels (contoh: 'workspace', 'meditation', 'reading'). Tulis saja katanya di baris baru tanpa tanda baca.
"""

def get_pexels_thumbnail(query):
    if not PEXELS_KEY:
        return "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&w=800"
    
    headers = {"Authorization": PEXELS_KEY}
    pexels_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return data['photos'][0]['src']['landscape']
    except Exception:
        pass
    return "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&w=800"

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: API_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}]
    }

    print(f"🎨 Lifestyle Bot sedang menulis topik '{TOPIK_HARI_INI}' untuk penulis: {PENULIS_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            lines = raw_content.strip().split('\n')
            keyword = lines[-1].strip().lower()
            artikel_body = "\n".join(lines[:-1]) 
            
            img_url = get_pexels_thumbnail(keyword)

            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"lifestyle-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Topik: {TOPIK_HARI_INI} | Penulis: {PENULIS_HARI_INI}")
        else:
            print(f"❌ Gagal. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala: {e}")

if __name__ == "__main__":
    tulis_artikel()