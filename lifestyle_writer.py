import os
import requests
import json
import random
from datetime import datetime

# --- KONFIGURASI AMAN ---
API_KEY = os.getenv("OPENROUTER_API_KEY_BACKUP") 
PEXELS_KEY = os.getenv("PEXELS_API_KEY")
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

# --- PROMPT DENGAN INSTRUKSI VISUAL KHUSUS ---
PROMPT = f"""
Tugas kamu adalah menjadi pengajar teknologi di Efektifpedia.
HARI INI FOKUS PADA BIDANG: {BIDANG_HARI_INI}.

INSTRUKSI ARTIKEL:
1. Pilih satu sub-topik spesifik dari bidang tersebut yang penting untuk dipelajari pemula.
2. Tulis artikel edukasi mendalam minimal 600 kata dalam Bahasa Indonesia.
3. Gunakan gaya bahasa yang mudah dipahami, sertakan contoh kasus atau contoh kode jika relevan.
4. Gunakan format Markdown murni.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL SPESIFIK DAN EDUKATIF]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Edukasi"
author: "{PENULIS_HARI_INI}"
---

PENTING UNTUK THUMBNAIL:
Di bagian paling akhir setelah artikel selesai, tuliskan tepat satu kata kunci (keyword) bahasa Inggris yang paling mewakili visual artikel ini agar relevan. 
Contoh: jika bahas database gunakan 'database', jika bahas keamanan gunakan 'cyber-security', jika bahas kode gunakan 'programming'.
Tulis saja SATU KATA tersebut di baris paling terakhir tanpa tanda baca.
"""

def get_pexels_thumbnail(query):
    """Fungsi mengambil URL gambar yang relevan dari Pexels"""
    fallback_img = "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    # Membersihkan query: ambil kata terakhir, hapus titik atau kutip
    clean_query = query.strip().lower().replace(".", "").replace('"', "").split()[-1]
    
    headers = {"Authorization": PEXELS_KEY}
    # Ambil 3 pilihan agar bisa di-random sedikit tapi tetap relevan
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=3&orientation=landscape"
    
    try:
        res = requests.get(pexels_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                # Pilih secara acak dari 3 hasil teratas agar tidak bosan tapi tetap nyambung
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
        "temperature": 0.7 # Kreativitas menengah agar edukasi tidak kaku
    }

    print(f"📚 EduBot sedang menyusun materi tentang {BIDANG_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            # Pisahkan body artikel dengan keyword terakhir
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip()
            artikel_body = "\n".join(lines[:-1]) 
            
            # Ambil hanya URL-nya saja (Hemat Storage GitHub!)
            img_url = get_pexels_thumbnail(keyword)

            # Masukkan thumbnail URL ke dalam Frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # Penamaan file dengan awalan edu agar terorganisir
            filename = os.path.join(FOLDER_TUJUAN, f"edu-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Materi: {BIDANG_HARI_INI}")
            print(f"🖼️ Relevansi Gambar: {keyword} -> {img_url}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()