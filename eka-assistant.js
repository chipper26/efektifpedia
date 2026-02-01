// --- KONFIGURASI ASISTEN EKA ---
const TRINITY_API_KEY = "MASUKKAN_API_KEY_TRINITY_DI_SINI"; 
const WA_NUMBER = "6285889847355";
const WA_LINK = `https://wa.me/${WA_NUMBER}?text=Halo%20Admin%20Efektifpedia,%20saya%20ingin%20konsultasi%20order%20artikel.`;

// --- TEMPLATE HTML & CSS ---
const chatHTML = `
<style>
    #ai-chat-widget { font-family: 'Segoe UI', Roboto, sans-serif; transition: all 0.3s ease; }
    .chat-bubble { width: 330px; height: 450px; background: white; border-radius: 15px; display: none; flex-direction: column; box-shadow: 0 10px 25px rgba(0,0,0,0.2); border: 1px solid #0d6efd; overflow: hidden; position: absolute; bottom: 80px; right: 0; }
    .chat-header { background: #0d6efd; color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
    .chat-body { flex: 1; overflow-y: auto; padding: 15px; background: #f8f9fa; display: flex; flex-direction: column; gap: 10px; }
    .chat-footer { padding: 10px; border-top: 1px solid #eee; background: white; display: flex; gap: 8px; }
    .msg { max-width: 85%; padding: 8px 12px; border-radius: 15px; font-size: 14px; line-height: 1.4; }
    .msg-ai { background: #e2edff; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
    .msg-user { background: #0d6efd; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
    .chat-btn { width: 60px; height: 60px; border-radius: 50%; background: #0d6efd; border: none; color: white; font-size: 28px; cursor: pointer; box-shadow: 0 4px 15px rgba(13,110,253,0.4); display: flex; align-items: center; justify-content: center; transition: 0.3s; }
    .chat-btn:hover { transform: scale(1.1); background: #0a58ca; }
</style>

<div id="ai-chat-widget" style="position: fixed; bottom: 100px; right: 18px; z-index: 10000;">
    <div id="chat-box" class="chat-bubble">
        <div class="chat-header">
            <span>🤖 Eka - Efektifpedia Asisten</span>
            <span onclick="toggleChat()" style="cursor:pointer; font-size: 20px;">&times;</span>
        </div>
        <div id="chat-content" class="chat-body">
            <div class="msg msg-ai">Halo! Saya <strong>Eka</strong>. Ada yang bisa saya bantu seputar jasa tulis artikel Efektifpedia? 😊</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="user-input" placeholder="Tanya sesuatu..." style="flex: 1; border: 1px solid #ddd; border-radius: 20px; padding: 8px 15px; outline: none;">
            <button onclick="sendMessage()" style="border: none; background: #0d6efd; color: white; border-radius: 50%; width: 38px; height: 38px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
            </button>
        </div>
    </div>
    <button id="chat-toggle" class="chat-btn" onclick="toggleChat()">🤖</button>
</div>
`;

// Masukkan ke Body
document.body.insertAdjacentHTML('beforeend', chatHTML);

const chatBox = document.getElementById('chat-box');
const chatContent = document.getElementById('chat-content');
const userInput = document.getElementById('user-input');

// Fungsi buka/tutup chat
window.toggleChat = function() {
    chatBox.style.display = (chatBox.style.display === 'none' || chatBox.style.display === '') ? 'flex' : 'none';
};

// Fungsi kirim pesan
window.sendMessage = async function() {
    const message = userInput.value.trim();
    if (!message) return;

    chatContent.innerHTML += `<div class="msg msg-user">${message}</div>`;
    userInput.value = '';
    chatContent.scrollTop = chatContent.scrollHeight;

    const systemPrompt = `Kamu adalah Eka, asisten AI dari Efektifpedia.
    - Layanan: Jasa tulis artikel kreatif (Basic 15rb, Pro 250rb, Premium 500rb).
    - Aturan: Jawab dengan ramah dan singkat. 
    - Penting: Jika user ingin beli, pesan, atau tanya harga detail, arahkan untuk klik link WA ini: ${WA_LINK}`;

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
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": message}
                ]
            })
        });

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;

        chatContent.innerHTML += `<div class="msg msg-ai"><strong>Eka:</strong> ${aiResponse}</div>`;
        chatContent.scrollTop = chatContent.scrollHeight;
    } catch (error) {
        chatContent.innerHTML += `<div class="msg msg-ai" style="color:red;">Aduh, Eka sedang gangguan. Coba lagi nanti ya!</div>`;
    }
};

userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});