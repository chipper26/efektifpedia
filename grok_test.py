import os
from groq import Groq

# --- KONFIGURASI ---
# Masukkan API Key Groq kamu di sini
API_KEY_GROQ = "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"

client = Groq(api_key=API_KEY_GROQ)

def test_chat():
    print("🚀 Menghubungi Groq LPU...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Saran: Pakai model Llama yang stabil di Groq
            messages=[
                {
                    "role": "user",
                    "content": "Halo Groq! Jika kamu mendengarku, katakan 'Groq Aktif' dengan sangat cepat."
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True
        )

        print("🤖 Respon Groq: ", end="")
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
        print("\n\n✅ Tes Berhasil!")
        
    except Exception as e:
        print(f"\n❌ Gagal: {e}")

if __name__ == "__main__":
    test_chat()