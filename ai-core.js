let isSpeaking = false;
const synth = window.speechSynthesis;

function setupAudio() {
    const btn = document.getElementById('btn-speak');
    if(!btn) return;

    btn.onclick = () => {
        const text = document.getElementById('post-content').innerText;
        if (isSpeaking) { synth.cancel(); isSpeaking = false; btn.innerText = "Dengarkan"; return; }
        
        isSpeaking = true;
        btn.innerText = "Berhenti";
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'id-ID';
        utterance.onend = () => { isSpeaking = false; btn.innerText = "Dengarkan"; };
        synth.speak(utterance);
    };
}