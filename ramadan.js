/**
 * Efektifpedia Ramadan Engine - V2 (Fixed Position)
 */

const CONFIG_RAMADAN = {
    tglTarget: "2026-02-18T00:00:00", // Awal Puasa 2026
    lokasi: "Jakarta",
    negara: "Indonesia"
};

function initRamadanFeature() {
    // 1. Cek apakah elemen sudah ada (biar tidak double)
    if (document.getElementById('ramadan-special-bar')) return;

    // 2. Buat elemen Banner
    const banner = document.createElement('div');
    banner.id = "ramadan-special-bar";
    
    // CSS yang lebih kuat untuk menimpa Navbar
    banner.style.cssText = `
        background: linear-gradient(45deg, #0d6efd, #1a1a1a) !important;
        color: #ffca28 !important;
        text-align: center !important;
        padding: 12px 10px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        z-index: 99999 !important;
        box-shadow: 0 2px 15px rgba(0,0,0,0.3) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 10px !important;
        border-bottom: 2px solid #ffca28 !important;
    `;
    
    banner.innerHTML = `<span id="ramadan-text">Menyiapkan info Ramadan...</span>`;
    document.body.prepend(banner);

    // 3. Dorong Navbar kamu ke bawah agar tidak tertutup
    // Navbar Bootstrap biasanya punya class .fixed-top
    const navbar = document.querySelector('.navbar.fixed-top');
    if (navbar) {
        navbar.style.top = "45px"; // Dorong navbar ke bawah setinggi banner
    }
    // Dorong konten body juga
    document.body.style.marginTop = "45px";

    updateStatus();
    setInterval(updateStatus, 1000);
}

async function updateStatus() {
    const textEl = document.getElementById('ramadan-text');
    if (!textEl) return;

    const sekarang = new Date();
    const target = new Date(CONFIG_RAMADAN.tglTarget);
    const selisih = target - sekarang;

    if (selisih > 0) {
        const d = Math.floor(selisih / (1000 * 60 * 60 * 24));
        const h = Math.floor((selisih % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((selisih % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((selisih % (1000 * 60)) / 1000);
        textEl.innerHTML = `🌙 Menuju Ramadan: ${d} Hari ${h}j ${m}m ${s}s lagi`;
    } else {
        let jadwal = sessionStorage.getItem('jadwal_sholat');
        if (!jadwal) {
            fetchJadwal();
            textEl.innerHTML = `✨ Selamat Menunaikan Ibadah Puasa`;
        } else {
            const j = JSON.parse(jadwal);
            textEl.innerHTML = `🌙 Imsak: ${j.Imsak} | Maghrib: ${j.Maghrib} | Isya: ${j.Isha}`;
        }
    }
}

async function fetchJadwal() {
    try {
        const response = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${CONFIG_RAMADAN.lokasi}&country=${CONFIG_RAMADAN.negara}&method=2`);
        const result = await response.json();
        if(result.data) sessionStorage.setItem('jadwal_sholat', JSON.stringify(result.data.timings));
    } catch (err) { console.error("API Error"); }
}

// Jalankan langsung tanpa menunggu DOMContentLoaded jika perlu
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRamadanFeature);
} else {
    initRamadanFeature();
}