/**
 * Efektifpedia Ramadan Engine - V3 (Inject Under Navbar)
 */

const CONFIG_RAMADAN = {
    tglTarget: "2026-02-18T00:00:00", // Awal Puasa 2026
    lokasi: "Jakarta",
    negara: "Indonesia"
};

function initRamadanFeature() {
    // 1. Cek apakah elemen sudah ada
    if (document.getElementById('ramadan-special-bar')) return;

    // 2. Buat elemen Banner
    const banner = document.createElement('div');
    banner.id = "ramadan-special-bar";
    
    // Style: Tidak lagi fixed, tapi mengikuti aliran dokumen (static)
    // Diletakkan tepat di bawah navbar
    banner.style.cssText = `
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: #ffca28;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        width: 100%;
        box-shadow: inset 0 -2px 5px rgba(0,0,0,0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #ffca28;
    `;
    
    banner.innerHTML = `<i class="bi bi-moon-stars-fill"></i> <span id="ramadan-text">Menghitung hari...</span>`;

    // 3. Masukkan tepat di bawah Navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.parentNode.insertBefore(banner, navbar.nextSibling);
    }

    // 4. Update konten
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
        // --- MODE HITUNG MUNDUR ---
        const d = Math.floor(selisih / (1000 * 60 * 60 * 24));
        const h = Math.floor((selisih % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((selisih % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((selisih % (1000 * 60)) / 1000);
        textEl.innerHTML = `Menuju Ramadan 1447H: ${d} Hari, ${h}j ${m}m ${s}s lagi`;
    } else {
        // --- MODE JADWAL SHOLAT ---
        let jadwal = sessionStorage.getItem('jadwal_sholat');
        if (!jadwal) {
            fetchJadwal();
            textEl.innerHTML = `Selamat Berpuasa ✨`;
        } else {
            const j = JSON.parse(jadwal);
            textEl.innerHTML = `🌙 Imsak: ${j.Imsak} | Maghrib (Buka): ${j.Maghrib} | Isya: ${j.Isha}`;
        }
    }
}

async function fetchJadwal() {
    try {
        const response = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${CONFIG_RAMADAN.lokasi}&country=${CONFIG_RAMADAN.negara}&method=2`);
        const result = await response.json();
        if(result.data) sessionStorage.setItem('jadwal_sholat', JSON.stringify(result.data.timings));
    } catch (err) { console.error("Gagal ambil jadwal"); }
}

// Jalankan
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRamadanFeature);
} else {
    initRamadanFeature();
}