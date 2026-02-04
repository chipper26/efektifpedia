import requests
import json
import os
import random
from datetime import datetime
import re

# --- KONFIGURASI AMAN ---
API_KEY = str(os.getenv("OPENROUTER_API_KEY", "")).strip() 
PEXELS_KEY = str(os.getenv("PEXELS_API_KEY", "")).strip() 
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

# Folder tujuan artikel agar terbaca oleh Sveltia CMS
FOLDER_TUJUAN = "blog" 

# --- DAFTAR PENULIS (PERSONA) ---
DAFTAR_PENULIS = ["Nadira Kusuma", "Budi Santoso", "Citra Anggraini", "Andi Wijaya", "Raka Santosa", "Aditya Mahendra"]

# --- DAFTAR SUDUT PANDANG ---
SUDUT_PANDANG = [
    "fokus pada inovasi perangkat keras (hardware) terbaru",
    "fokus pada terobosan perangkat lunak (software) dan aplikasi",
    "fokus pada dampak sosial dan kemanusiaan dari teknologi tersebut",
    "fokus pada persaingan pasar antar perusahaan raksasa teknologi",
    "fokus pada bagaimana tren ini mengubah gaya hidup masyarakat",
    "fokus pada aspek keamanan siber dan perlindungan data pribadi",
    "fokus pada efisiensi kerja dan produktivitas di masa depan"
]

PENULIS_HARI_INI = random.choice(DAFTAR_PENULIS)
GAYA_BAHASA_HARI_INI = random.choice(SUDUT_PANDANG)

# --- PROMPT DENGAN ATURAN H4 & SPACING ---
PROMPT = f"""
Cari berita teknologi yang paling viral, hangat, dan banyak dibicarakan dalam seminggu terakhir hingga hari ini ({datetime.now().strftime('%d %B %Y')}).
Tulis artikel blog mendalam minimal 600 kata dalam Bahasa Indonesia.

Gunakan gaya bahasa profesional Sistem Informasi yang informatif, namun ulas secara {GAYA_BAHASA_HARI_INI}.
Pastikan isi artikel benar-benar relevan dengan tren teknologi global saat ini.

ATURAN FORMAT VISUAL (PENTING):
1. Gunakan format '#### ' (Heading 4) untuk setiap sub-judul atau poin pembahasan baru.
2. WAJIB memberikan SATU BARIS KOSONG sebelum dan sesudah setiap '#### ' agar tidak menempel dengan paragraf.
3. Gunakan format Markdown murni tanpa tambahan teks penjelasan di luar artikel.

Wajib sertakan Frontmatter di bagian paling atas:
---
title: "[JUDUL BERITA VIRAL YANG MENARIK]"
date: "{datetime.now().strftime('%Y-%m-%d')}"
category: "Tech News"
author: "{PENULIS_HARI_INI}"
---

PENTING UNTUK THUMBNAIL:
Di baris paling terakhir sendiri setelah artikel selesai, tuliskan tepat satu kata kunci bahasa Inggris (keyword) untuk mencari gambar di Pexels (contoh: 'ai', 'smartphone', 'cybersecurity'). Tulis saja SATU KATA tersebut tanpa tanda baca.
"""

def get_pexels_url(query):
    """Fungsi hanya mengambil URL LINK gambar resmi dari Pexels"""
    fallback_img = "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&w=800"
    if not PEXELS_KEY:
        return fallback_img
    
    # Bersihkan query
    clean_query = query.strip().lower().replace(".", "").replace('"', "").split()[-1]
    headers = {"Authorization": PEXELS_KEY}
    pexels_url = f"https://api.pexels.com/v1/search?query={clean_query}&per_page=1&orientation=landscape"
    
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
        print("❌ Error: OPENROUTER_API_KEY tidak ditemukan!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://efektifpedia.com",
        "X-Title": "Efektifpedia News Bot"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.8
    }

    print(f"🤖 Meriset tren viral hari ini dengan sudut pandang: {GAYA_BAHASA_HARI_INI}...")
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data), timeout=60)
        if response.status_code == 200:
            raw_content = response.json()['choices'][0]['message']['content']
            
            # --- LOGIKA EKSTRAKSI ---
            lines = [l for l in raw_content.strip().split('\n') if l.strip()]
            keyword = lines[-1].strip().lower().split()[-1]
            artikel_body = "\n".join(lines[:-1]) 

            # --- LOGIKA AUTO-SEPARATOR (SINKRONISASI CMS & BLOG) ---
            # Pastikan H4 memiliki jarak kosong yang cukup
            artikel_body = re.sub(r'\n*(#### .*)\n*', r'\n\n\1\n\n', artikel_body)
            # Bersihkan jarak yang terlalu lebar
            artikel_body = re.sub(r'\n{3,}', r'\n\n', artikel_body)
            
            # AMBIL URL GAMBAR
            img_url = get_pexels_url(keyword)

            # Injeksi thumbnail ke Frontmatter
            konten_final = artikel_body.replace(
                f"author: \"{PENULIS_HARI_INI}\"", 
                f"author: \"{PENULIS_HARI_INI}\"\nthumbnail: \"{img_url}\""
            )
            
            # Pastikan Kategori Tech News (Hapus kutip liar jika ada)
            konten_final = re.sub(r'category:.*', 'category: "Tech News"', konten_final)
            
            if not os.path.exists(FOLDER_TUJUAN):
                os.makedirs(FOLDER_TUJUAN)
            
            # Nama file unik
            filename = os.path.join(FOLDER_TUJUAN, f"news-{datetime.now().strftime('%Y%m%d-%H%M')}.md")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(konten_final)
            
            print(f"✅ BERHASIL! Berita hari ini: {keyword}")
            print(f"🔗 Thumbnail: {img_url}")
        else:
            print(f"❌ Gagal di OpenRouter. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    tulis_artikel()