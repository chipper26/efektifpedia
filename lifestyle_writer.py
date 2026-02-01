import os
import requests
import json
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
# Menggunakan API Key cadangan sesuai strategi kita
API_KEY = os.getenv("OPENROUTER_API_KEY_BACKUP") 
PEXELS_KEY = os.getenv("PEXELS_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS (Karyawan Efektifpedia) ---
DAFTAR_PENULIS = [
    "Nadira Kusuma", "Budi Santoso", "Citra Anggraini",
    "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"
]

# --- DAFTAR BIDANG EDUKASI (UMUM) ---
# AI akan memilih satu bidang ini lalu menentukan sub-topik sendiri
DAFTAR_BIDANG = [
    "Cloud Computing (SaaS, IaaS, PaaS, Virtualisasi)",
    "Arsitektur Software (Microservices, Monolith, Decoupling)",
    "Tutorial Pemrograman Python (Sintaks dasar hingga menengah)",
    "Jaringan Komputer (Protokol Internet, IP Address, OSI Layer)",
    "Sejarah Teknologi (Sejarah AI, Komputer, dan Internet)",
    "Database Management (SQL vs NoSQL, Optimasi Query)",
    "Cyber Security (Enkripsi Dasar, Keamanan Data, Firewall)",
    "Pengembangan Web (HTML, CSS Dasar, Konsep Frontend/Backend)"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
BIDANG_HARI_INI = random.choice(DAFTAR_BIDANG)

PROMPT = f"""
Tugas kamu adalah menjadi pengajar teknologi di Efektifpedia.
HARI INI FOKUS PADA BIDANG: {BIDANG_HARI_INI}.

INSTRUKSI:
1. Pilih satu sub-topik spesifik dari bidang tersebut yang penting untuk dipelajari pemula.
2. Tulis artikel edukasi mendalam minimal 600 kata dalam Bahasa Indonesia.
3. Gunakan gaya bahasa yang mudah dipahami, sertakan contoh kasus atau contoh kode jika relevan.
4. JANGAN membuat judul yang membosankan. Buat judul yang bikin orang ingin belajar.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL SPESIFIK DAN EDUKATIF]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Edukasi"
author: "{PENULIS_HARI_INI}"
---

PENTING: Di bagian paling akhir setelah artikel selesai, tuliskan tepat satu kata kunci singkat dalam bahasa Inggris untuk mencari gambar thumbnail di Pexels (contoh: 'coding', 'server', 'books'). Tulis saja katanya di baris baru tanpa tanda baca.
"""

def get_pexels_thumbnail(query):
    # Fallback gambar edukasi jika API bermasalah
    fallback_img = "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
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
    return fallback_img

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: OPENROUTER_API_KEY_BACKUP tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}]
    }

    print(f"📚 EduBot sedang menyusun materi tentang {BIDANG_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            lines = raw_content.strip().split('\n')
            keyword = lines[-1].strip().lower()
            artikel_body = "\n".join(lines[:-1]) 
            
            img_url = get_pexels_thumbnail(keyword)

            # Injeksi thumbnail ke frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # File disimpan dengan awalan edu agar rapi
            filename = os.path.join(FOLDER_TUJUAN, f"edu-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Bidang: {BIDANG_HARI_INI} | Penulis: {PENULIS_HARI_INI}")
        else:
            print(f"❌ Gagal. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala: {e}")

if __name__ == "__main__":
    tulis_artikel()