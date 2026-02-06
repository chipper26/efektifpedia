/**
 * EFEKTIFPEDIA AI CORE - Service
 * Menangani interaksi chat dengan OpenRouter
 */

const EFEKTIFPEDIA_AI_CORE = "sk-or-v1-b38...53b"; // Masukkan kunci asli kamu di sini

async function askAI() {
    const inputField = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const typing = document.getElementById('typing');
    const btnSend = document.getElementById('btn-send');
    const question = inputField.value.trim();
    
    // Mengambil teks artikel untuk konteks
    const postContent = document.getElementById('post-content');
    const articleText = postContent ? postContent.innerText : "Tidak ada konteks artikel.";

    if (!question) return;

    // UI: Tampilkan pesan user
    chatHistory.innerHTML += `<div class="msg msg-user">${question}</div>`;
    inputField.value = '';
    btnSend.disabled = true;
    typing.style.display = 'block';
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${EFEKTIFPEDIA_AI_CORE}`,
                "Content-Type": "application/json",
                "X-Title": "Efektifpedia AI Core"
            },
            body: JSON.stringify({
                "model": "google/gemini-2.0-flash-001",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Kamu adalah EFEKTIFPEDIA AI CORE. Jawablah pertanyaan pembaca dengan ramah, edukatif, dan ringkas berdasarkan konteks artikel yang diberikan."
                    },
                    {
                        "role": "user", 
                        "content": `Konteks Artikel: ${articleText}\n\nPertanyaan: ${question}`
                    }
                ]
            })
        });

        const data = await response.json();
        
        if (data.choices && data.choices[0]) {
            const aiResponse = data.choices[0].message.content;
            chatHistory.innerHTML += `<div class="msg msg-ai">${aiResponse}</div>`;
        } else {
            throw new Error("Respon API tidak valid");
        }

    } catch (e) {
        console.error("AI Error:", e);
        chatHistory.innerHTML += `<div class="msg msg-ai text-danger">Maaf kawan, otak AI sedang tidak sinkron. Coba lagi ya.</div>`;
    } finally {
        typing.style.display = 'none';
        btnSend.disabled = false;
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}