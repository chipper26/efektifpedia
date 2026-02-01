// Konfigurasi Asisten Eka
const TRINITY_API_KEY = "MASUKKAN_API_KEY_TRINITY_DISINI";
const WA_LINK = "https://wa.me/6285889847355";

// Template HTML untuk Chatbox
const chatHTML = `
<div id="ai-chat-widget" style="position: fixed; bottom: 100px; right: 20px; z-index: 9999; font-family: sans-serif;">
    <div id="chat-box" style="display: none; width: 320px; height: 450px; background: white; border: 1px solid #0d6efd; border-radius: 15px; flex-direction: column; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
        <div style="background: #0d6efd; color: white; padding: 15px; border-radius: 15px 15px 0 0; font-weight: bold; display: flex; justify-content: space-between;">
            <span>🤖 Eka - Efektifpedia Asisten</span>
            <span onclick="toggleChat()" style="cursor:pointer;">✖</span>
        </div>
        <div id="chat-content" style="flex: 1; overflow-y: auto; padding: 15px; font-size: 14px; background: #f9f9f9;">
            <p style="background: #e2edff; padding: 8px; border-radius: 10px;"><strong>Eka:</strong> Halo! Saya Eka. Ada yang bisa saya bantu tentang jasa penulisan artikel Efektifpedia? 😊</p>
        </div>
        <div style="padding: 10px; border-top: 1px solid #eee; display: flex; gap: 5px;">
            <input type="text" id="user-input" placeholder="Tanya sesuatu..." style="flex: 1; border: 1px solid #ccc; border-radius: 20px; padding: 8px 15px; outline: none;">
            <button onclick="sendMessage()" style="border: none; background: #0d6efd; color: white; border-radius: 50%; width: 35px; height: 35px; cursor: pointer;">➤</button>
        </div>
    </div>
    <button id="chat-toggle" onclick="toggleChat()" style="width: 60px; height: 60px; border-radius: 50%; background: #0d6efd; border: none; color: white; font-size: 28px; cursor: pointer; box-shadow: 0 4px 15px rgba(13,110,253,0.4); margin-left: auto; display: block; transition: 0.3s;">
        🤖
    </button>
</div>
`;

// Masukkan HTML ke Body secara otomatis
document.body.insertAdjacentHTML('beforeend', chatHTML);

function toggleChat() {
    const box = document.getElementById('chat-box');
    box.style.display = box.style.display === 'none' ? 'flex' : 'none';
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const content = document.getElementById('chat-content');
    if (!input.value.trim()) return;

    const userMsg = input.value;
    content.innerHTML += `<div style="text-align: right; margin-bottom: 10px;"><span style="background: #0d6efd; color: white; padding: 8px; border-radius: 10px; display: inline-block;">${userMsg}</span></div>`;
    input.value = '';
    content.scrollTop = content.scrollHeight;

    const briefing = `Kamu adalah Eka, asisten ramah dari Efektifpedia.
    Layanan: Jasa tulis artikel (Basic 15rb, Pro 250rb, Premium 500rb).
    Tugas: Jawab pertanyaan dengan singkat. Jika user ingin beli, order, atau tanya harga detail, arahkan untuk chat ke WhatsApp melalui link: ${WA_LINK}`;

    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${TRINITY_API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "model": "google/gemini-2.0-flash-001",
                "messages": [
                    {"role": "system", "content": briefing},
                    {"role": "user", "content": userMsg}
                ]
            })
        });
        const data = await response.json();
        const aiMsg = data.choices[0].message.content;
        content.innerHTML += `<p style="background: #e2edff; padding: 8px; border-radius: 10px; margin-bottom: 10px;"><strong>Eka:</strong> ${aiMsg}</p>`;
        content.scrollTop = content.scrollHeight;
    } catch (e) {
        content.innerHTML += `<p style="color:red; font-size: 12px;">Gagal terhubung. Pastikan API Key benar.</p>`;
    }
}