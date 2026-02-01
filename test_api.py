import os
import requests
import json

# Mengambil key Trinity yang kamu siapkan
API_KEY = os.getenv("OPENROUTER_API_KEY_BACKUP")
URL = "https://openrouter.ai/api/v1/chat/completions"

def test_koneksi():
    if not API_KEY:
        print("❌ GAGAL: Secret OPENROUTER_API_KEY_BACKUP tidak terbaca!")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [{"role": "user", "content": "Katakan 'API Trinity Aktif' jika kamu mendengarku."}]
    }

    print("🚀 Mencoba menghubungi Trinity AI...")
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            hasil = response.json()['choices'][0]['message']['content']
            print(f"✅ BERHASIL! Respon AI: {hasil}")
        else:
            print(f"❌ GAGAL: Status {response.status_code}")
            print(f"Pesan Error: {response.text}")
    except Exception as e:
        print(f"⚠️ Kendala teknis: {e}")

if __name__ == "__main__":
    test_koneksi()