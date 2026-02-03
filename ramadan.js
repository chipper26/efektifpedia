/**
 * Efektifpedia Ramadan Engine
 * Fitur: Countdown, Live Jadwal Sholat (API), & Auto-Banner
 */

const CONFIG_RAMADAN = {
    tglTarget: "2026-02-18T00:00:00", // Estimasi awal puasa 2026
    lokasi: "Jakarta",
    negara: "Indonesia"
};

async function initRamadanFeature() {
    // 1. Ciptakan elemen Banner secara dinamis
    const banner = document.createElement('div');
    banner.id = "ramadan-special-bar";
    // Style gradasi emas-biru khas ramadan
    banner.style = `
        background: linear-gradient(45deg, #0d6efd, #212529);
        color: #ffca28;
        text-align: center;
        padding: 10px 5px;
        font-size: 14px;
        font-weight: bold;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #ffca28;
    `;
    
    // Tambahkan ikon lampu hias ramadan (Bootstrap Icons)
    banner.innerHTML = `<i class="bi bi-moon-stars"></i> <span id="ramadan-text">Memuat info...</span>`;
    document.body.prepend(banner);

    // 2. Geser layout body agar tidak tertutup banner (asumsi navbar kamu fixed)
    document.body.style.paddingTop = "125px"; 

    // 3. Jalankan Loop Logic
    updateStatus();
    setInterval(updateStatus, 1000);
}

async function updateStatus() {
    const textEl = document.getElementById('ramadan-text');
    const sekarang = new Date();
    const target = new Date(CONFIG_RAMADAN.tglTarget);
    const selisih = target - sekarang;

    if (selisih > 0) {
        // --- MODE COUNTDOWN (SEBELUM PUASA) ---
        const d = Math.floor(selisih / (1000 * 60 * 60 * 24));
        const h = Math.floor((selisih % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((selisih % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((selisih % (1000 * 60)) / 1000);
        
        textEl.innerHTML = `Menuju Ramadan 1447H: ${d} Hari, ${h} Jam, ${m} Menit, ${s} Detik lagi`;
    } else {
        // --- MODE LIVE JADWAL (SAAT PUASA) ---
        // Kita simpan di sessionStorage agar tidak hit API terus-terusan tiap detik
        let jadwal = sessionStorage.getItem('jadwal_sholat');
        if (!jadwal) {
            fetchJadwal();
            textEl.innerHTML = `Selamat Menunaikan Ibadah Puasa ✨`;
        } else {
            const j = JSON.parse(jadwal);
            textEl.innerHTML = `🌙 Imsak: ${j.Imsak} | Subuh: ${j.Fajr} | Maghrib (Buka): ${j.Maghrib} | Isya: ${j.Isha}`;
        }
    }
}

async function fetchJadwal() {
    try {
        const response = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${CONFIG_RAMADAN.lokasi}&country=${CONFIG_RAMADAN.negara}&method=2`);
        const result = await response.json();
        sessionStorage.setItem('jadwal_sholat', JSON.stringify(result.data.timings));
    } catch (err) {
        console.log("Gagal ambil jadwal");
    }
}

// Jalankan otomatis
document.addEventListener("DOMContentLoaded", initRamadanFeature);