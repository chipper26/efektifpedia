import os
import requests
import json
import random
from datetime import datetime
import re

# --- KONFIGURASI AMAN ---
# Menggunakan API_AI_KEY_BACKUP sesuai pola environment kamu
API_KEY = str(os.getenv("OPENROUTER_API_KEY_BACKUP", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip()
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS ---
DAFTAR_PENULIS = [
    "Nadira Kusuma", "Budi Santoso", "Citra Anggraini",
    "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"
]

# --- DAFTAR BIDANG EDUKASI ---
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

# --- PROMPT DENGAN INSTRUKSI H4 & SPACING ---
PROMPT = f"""
Tugas kamu adalah menjadi pengajar teknologi di Efektifpedia.
HARI INI FOKUS PADA BIDANG: {BIDANG_HARI_INI}.

INSTRUKSI ARTIKEL:
1. Pilih satu sub-topik spesifik dari bidang tersebut yang penting untuk dipelajari pemula.
2. Tulis artikel edukasi mendalam minimal 600 kata dalam Bahasa Indonesia.
3. Gunakan gaya bahasa yang mudah dipahami, sertakan contoh kasus atau contoh kode jika relevan.

ATURAN FORMAT VISUAL (PENTING):
- Gunakan format '#### ' (Heading 4) untuk setiap sub-judul atau poin pembahasan baru agar sinkron dengan CMS.
- WAJIB memberikan SATU BARIS KOSONG sebelum dan sesudah setiap '#### ' agar tidak menempel dengan paragraf.
- Gunakan format Markdown murni.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL SPESIFIK DAN EDUKATIF]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Edukasi"
author: "{PENULIS_HARI_INI}"
---

PENTING UNTUK THUMBNAIL:
Di baris paling terakhir sendiri setelah artikel selesai, tuliskan tepat satu kata kunci bahasa Inggris (keyword) yang paling mewakili visual artikel. 
Tulis saja SATU KATA tersebut di baris paling terakhir tanpa tanda baca.
"""

def get_pexels_thumbnail(query):
    """Fungsi mengambil URL gambar yang relevan dari Pexels"""
    fallback_img = "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    # Membersihkan query: ambil kata terakhir
    clean_query = query.strip().lower().replace(".", "").replace('"', "").split()[-1]
    
    headers = {"Authorization": PEXELS_KEY}
    # Ambil 3 pilihan agar bisa di-random sedikit
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=3&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return random.choice(data['photos'])['src']['landscape']
    except Exception as e:
        print(f"⚠️ Gagal mengambil gambar Pexels: {e}")
    
    return fallback_img

def tulis_artikel():
    if not API_KEY:
        print("❌ Error: OPENROUTER_API_KEY_BACKUP tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia EduBot"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.7
    }

    print(f"📚 EduBot sedang menyusun materi tentang {BIDANG_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data), timeout=60)
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            # Pisahkan body artikel dengan keyword terakhir
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip().lower().split()[-1]
            artikel_body = "\n".join(lines[:-1]) 

            # --- LOGIKA AUTO-SEPARATOR (SINKRONISASI CMS) ---
            # Memaksa baris kosong di sekitar H4 agar tampilan rapi
            artikel_body = re.sub(r'\n*(#### .*)\n*', r'\n\n\1\n\n', artikel_body)
            # Membersihkan tumpukan enter yang lebih dari dua
            artikel_body = re.sub(r'\n{3,}', r'\n\n', artikel_body)
            
            # Ambil URL Gambar
            img_url = get_pexels_thumbnail(keyword)

            # Injeksi thumbnail ke Frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            # Pastikan kategori tetap Edukasi (Hapus kutip jika AI nulis sembarangan)
            konten_final = re.sub(r'category:.*', 'category: "Edukasi"', konten_final)
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            filename = os.path.join(FOLDER_TUJUAN, f"edu-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Format Edukasi H4 telah diterapkan.")
            print(f"🖼️ Relevansi Gambar: {keyword} -> {img_url}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()