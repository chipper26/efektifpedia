// --- KONFIGURASI RAMADAN ---
const TANGGAL_PUASA = new Date("March 1, 2025 00:00:00").getTime(); // Sesuaikan estimasi tanggal puasa
const KOTA_ID = "1301"; // Contoh ID Kota Jakarta (Cek di aladhan API atau serupa)

async function inisialisasiRamadan() {
    // 1. Buat elemen Banner di atas Navbar
    const banner = document.createElement('div');
    banner.id = "ramadan-banner";
    banner.style = "background: linear-gradient(90deg, #0d6efd, #6610f2); color: white; text-align: center; padding: 8px; font-size: 0.9rem; font-weight: bold; position: fixed; top: 0; width: 100%; z-index: 2000; display: none;";
    document.body.prepend(banner);

    // Tambahkan padding ke body agar tidak tertutup banner
    document.body.style.paddingTop = "115px"; 

    updateBanner();
    setInterval(updateBanner, 1000); // Update tiap detik
}

function updateBanner() {
    const sekarang = new Date().getTime();
    const selisih = TANGGAL_PUASA - sekarang;
    const banner = document.getElementById('ramadan-banner');

    if (selisih > 0) {
        // --- MODE COUNTDOWN ---
        const hari = Math.floor(selisih / (1000 * 60 * 60 * 24));
        const jam = Math.floor((selisih % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const menit = Math.floor((selisih % (1000 * 60 * 60)) / (1000 * 60));
        const detik = Math.floor((selisih % (1000 * 60)) / 1000);

        banner.innerHTML = `🌙 Menuju Ramadan: ${hari} Hari ${jam}j ${menit}m ${detik}s lagi`;
        banner.style.display = "block";
    } else {
        // --- MODE JADWAL SHOLAT (WAKTU PUASA) ---
        ambilJadwalSholat(banner);
    }
}

async function ambilJadwalSholat(el) {
    const tgl = new Date();
    const tglStr = `${tgl.getFullYear()}-${tgl.getMonth()+1}-${tgl.getDate()}`;
    
    try {
        // Menggunakan API Aladhan (Gratis & Cepat)
        const res = await fetch(`https://api.aladhan.com/v1/timingsByCity/${tglStr}?city=Jakarta&country=Indonesia&method=2`);
        const data = await res.json();
        const jadwal = data.data.timings;

        const sekarangJam = tgl.getHours() + ":" + tgl.getMinutes();
        
        // Cek apakah sekarang waktu Imsak, Buka, atau Sholat
        el.innerHTML = `✨ Ramadan Karim | Imsak: ${jadwal.Imsak} • Subuh: ${jadwal.Fajr} • Maghrib (Buka): ${jadwal.Maghrib}`;
        el.style.display = "block";
    } catch (e) {
        el.innerHTML = `🌙 Selamat Menunaikan Ibadah Puasa`;
    }
}

// Jalankan saat halaman siap
document.addEventListener("DOMContentLoaded", inisialisasiRamadan);