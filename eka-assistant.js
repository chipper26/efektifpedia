// --- KONFIGURASI ASISTEN EKA (GROQ + SECURE BRIDGE) ---
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyxROd8MmUWnxidQChVqSICejmas5DfDBfAdoC1tiazmBdBgqH9gnj8ocaYj0FNf1mO/exec"; 
const MODERATOR_NUMBER = "6285889847355"; 
const WA_LINK = `https://wa.me/${MODERATOR_NUMBER}?text=Halo%20Moderator%20Efektifpedia,%20saya%20ingin%20konsultasi%20order%20artikel.`;

// --- TEMPLATE HTML & CSS ---
const chatHTML = `
<style>
    #ai-chat-widget { font-family: 'Segoe UI', Roboto, sans-serif; transition: all 0.3s ease; }
    .chat-bubble { width: 330px; height: 450px; background: white; border-radius: 15px; display: none; flex-direction: column; box-shadow: 0 10px 25px rgba(0,0,0,0.2); border: 1px solid #0d6efd; overflow: hidden; position: absolute; bottom: 80px; right: 0; }
    .chat-header { background: #0d6efd; color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
    .chat-body { flex: 1; overflow-y: auto; padding: 15px; background: #f8f9fa; display: flex; flex-direction: column; gap: 10px; }
    .chat-footer { padding: 10px; border-top: 1px solid #eee; background: white; display: flex; gap: 8px; }
    .msg { max-width: 85%; padding: 8px 12px; border-radius: 15px; font-size: 14px; line-height: 1.4; white-space: pre-wrap; word-wrap: break-word; }
    .msg-ai { background: #e2edff; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
    .msg-user { background: #0d6efd; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
    .chat-btn { width: 60px; height: 60px; border-radius: 50%; background: #0d6efd; border: none; color: white; font-size: 28px; cursor: pointer; box-shadow: 0 4px 15px rgba(13,110,253,0.4); display: flex; align-items: center; justify-content: center; transition: 0.3s; }
    .wa-btn-chat { display: inline-block; background: #25d366; color: white; padding: 8px 15px; border-radius: 20px; text-decoration: none; font-weight: bold; font-size: 13px; margin-top: 10px; transition: 0.3s; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    
    /* Animasi Ngetik */
    .typing { display: flex; gap: 3px; padding: 10px; }
    .dot { width: 6px; height: 6px; background: #999; border-radius: 50%; animation: blink 1.4s infinite both; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0%, 80%, 100% { opacity: 0.2; } 40% { opacity: 1; } }
</style>

<div id="ai-chat-widget" style="position: fixed; bottom: 100px; right: 18px; z-index: 10000;">
    <div id="chat-box" class="chat-bubble">
        <div class="chat-header">
            <span>🤖 Eka - Efektifpedia Asisten</span>
            <span onclick="toggleChat()" style="cursor:pointer; font-size: 20px;">&times;</span>
        </div>
        <div id="chat-content" class="chat-body">
            <div class="msg msg-ai">Halo! Saya <strong>Eka</strong>. Ada yang bisa saya bantu? ⚡</div>
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

document.body.insertAdjacentHTML('beforeend', chatHTML);

const chatBox = document.getElementById('chat-box');
const chatContent = document.getElementById('chat-content');
const userInput = document.getElementById('user-input');

window.toggleChat = function() {
    chatBox.style.display = (chatBox.style.display === 'none' || chatBox.style.display === '') ? 'flex' : 'none';
};

function cleanAndFormat(text) {
    let cleanText = text.replace(/\*/g, ""); // Hapus bintang
    const waPattern = /https:\/\/wa\.me\/[^\s]+/g;
    return cleanText.replace(waPattern, (match) => {
        return `<br><a href="${match}" target="_blank" class="wa-btn-chat">Hubungi Moderator WhatsApp</a>`;
    });
}

window.sendMessage = async function() {
    const message = userInput.value.trim();
    if (!message) return;

    chatContent.innerHTML += `<div class="msg msg-user">${message}</div>`;
    userInput.value = '';
    
    // Tambahkan indikator ngetik
    const typingId = "typing-" + Date.now();
    chatContent.innerHTML += `<div id="${typingId}" class="msg msg-ai typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
    chatContent.scrollTop = chatContent.scrollHeight;

    const systemPrompt = `Kamu adalah Eka, asisten AI Efektifpedia. JANGAN gunakan simbol markdown. Link WA: ${WA_LINK}`;

    try {
        const response = await fetch(GOOGLE_SCRIPT_URL, {
            method: "POST",
            body: JSON.stringify({
                "messages": [
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": message}
                ]
            })
        });

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;

        // Hapus indikator ngetik sebelum jawaban muncul
        const typingElem = document.getElementById(typingId);
        if (typingElem) typingElem.remove();

        chatContent.innerHTML += `<div class="msg msg-ai"><strong>Eka:</strong> ${cleanAndFormat(aiResponse)}</div>`;
        chatContent.scrollTop = chatContent.scrollHeight;
    } catch (error) {
        const typingElem = document.getElementById(typingId);
        if (typingElem) typingElem.remove();
        chatContent.innerHTML += `<div class="msg msg-ai" style="color:red;">Maaf, sedang gangguan.</div>`;
    }
};

userInput.addEventListener("keypress", function(event) { if (event.key === "Enter") sendMessage(); });