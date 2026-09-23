#!/usr/bin/env python3
"""Cuda questionnaire builder -> interactive HTML + Markdown + CSV.
Convention: "question text::opt1::opt2" -> '::' marks choice options (chips).
"""
import csv, json, os, re

OUT = "/root/cuda-ai/site/questionnaire"
os.makedirs(OUT, exist_ok=True)

SECTIONS = [
("A", "Brand & Identitas", "🎨", [
 "Nama brand induk final: \"Cuda\" — atau ada alternatif?::Cuda::Masbraw Cuda::lainnya (sebutkan)",
 "Nama dua produk: \"Cuda AI\" & \"Cuda Agent\" — fix atau mau ganti?::fix::ganti (sebutkan)",
 "Tagline landing: \"Cuda AI buat mikir. Cuda Agent buat ngerjain.\" — oke atau mau versi lain?::oke::ganti (sebutkan)",
 "Domain yang mau dipakai (mis. cuda.my.id / cudai.app)? Sudah punya domain apa saja?",
 "Logo: monogram huruf C (rounded-square/hexagon), atau mau dibikin dari nol dengan konsep lain?::monogram C::bikin baru",
 "Accent dua room: biru #4f8cff (AI) + violet #8b5cf6 (Agent) — setuju?::setuju::satu warna aja::ganti (sebutkan)",
 "Bahasa UI default: Indonesia, Inggris, atau dua-duanya (switch)?::Indonesia::Inggris::dua-duanya",
 "Istilah Indonesia (Misi/Langkah/Izin/Struk/Serahan) dipertahankan atau campur Inggris?::Indonesia::campur::Inggris",
 "Agent kalau \"ngomong\" pakai nama siapa?::Cuda::nama lain (sebutkan)::tanpa nama",
 "Perlu maskot/karakter visual?::tidak::ya (konsepnya)",
 "Cuda jadi bagian keluarga brand Masbraw/ZieDev, atau brand berdiri sendiri?::keluarga Masbraw::berdiri sendiri::ZieDev",
 "Credit/footer: \"Cuda by ...\" mau ditulis apa?",
]),
("B", "Positioning & Target User", "🎯", [
 "User utama v1: kamu sendiri, teman kampus, atau publik luas?::kamu sendiri::teman kampus::publik",
 "Cuda mau jadi produk komersial (dijual) atau alat pribadi dulu?::komersial::pribadi dulu::dua-duanya",
 "Kalau dijual: target pasar utama?::mahasiswa::freelancer::UMKM::developer",
 "Satu kalimat: \"Cuda beda dari ChatGPT karena ____\"",
 "Fitur mana yang jadi pembunuh utama (bikin orang pindah ke Cuda)?",
 "Target realistis Cuda AI vs ChatGPT/Gemini/Claude?",
 "Target segmen Cuda Agent vs Manus/Claude Cowork?",
 "Perlu mode \"lokal/offline\" (data tidak keluar dari device)?::perlu::tidak perlu::nanti",
 "Ada kebutuhan privasi khusus (data kampus, data klien)?",
 "Pesaing lokal Indonesia yang perlu diperhatikan?",
 "Cuda mau dipakai untuk jualan jasa (agent-as-a-service)?::ya::tidak::mungkin nanti",
 "Target jumlah user 3 bulan pertama?",
 "Perlu halaman pricing publik sejak v1?::ya::tidak::nanti",
 "Perlu mode team/kantor (multi-user satu workspace)?::v1::nanti::tidak perlu",
]),
("C", "Scope & Prioritas MVP", "📦", [
 "Kerjakan P0–P4 dulu (AI + Agent inti), P5–P7 nyusul — setuju?::setuju::kerjakan semua::potong lagi",
 "Pilih satu: Cuda AI dulu sampai sempurna, atau dua-duanya jalan bareng?::AI dulu::bareng",
 "Target kapan MVP harus jadi (tanggal/perkiraan)?",
 "3 fitur WAJIB ada di v1?",
 "Fitur yang boleh ditunda / tidak perlu sama sekali?",
 "Compare mode (2 model jawab bareng) prioritas atau nice-to-have?::prioritas::nice-to-have::tidak perlu",
 "Deep Research mode (riset multi-step otomatis) masuk v1?::ya::tidak::nanti",
 "Voice input (STT) & read aloud (TTS) masuk v1?::dua-duanya::salah satu::nanti",
 "Multi-sesi agent paralel masuk v1?::v1::nanti",
 "Berapa template Playbook yang wajib ada di v1?::3::6::10+",
 "Jadwal/cron misi otomatis masuk v1?::v1::nanti",
 "MCP connector masuk v1 atau v2?::v1::v2::tidak perlu",
]),
("D", "Stack & Arsitektur", "🏗️", [
 "Frontend: Next.js 16 atau Nuxt 4?::Next.js 16::Nuxt 4::terserah kamu",
 "TypeScript strict mode?::ya::tidak",
 "Styling: Tailwind 4 + komponen sendiri, atau pakai UI kit jadi?::Tailwind + komponen sendiri::UI kit (sebutkan)",
 "ORM: Prisma atau Drizzle?::Prisma::Drizzle::terserah kamu",
 "State management frontend: Zustand, Jotai, atau React Query + context?::Zustand::Jotai::React Query+context::terserah kamu",
 "Streaming: chat pakai SSE dan agent pakai WebSocket — setuju?::setuju::semua WebSocket::semua SSE",
 "Monorepo: npm workspaces atau pnpm/turborepo?::npm workspaces::pnpm+turbo::terserah kamu",
 "Paket packages/ui terpisah atau komponen langsung di apps/web?::terpisah::langsung",
 "Agent runtime: Node/Fastify, atau Python/FastAPI (ekosistem tool lebih kaya)?::Node/Fastify::Python/FastAPI::terserah kamu",
 "Validasi event pakai Zod di dua sisi — setuju?::setuju::pakai lain",
 "Perlu API publik Cuda (REST / OpenAI-compatible)?::ya::tidak::nanti",
 "Perlu multi-tenant sejak awal (untuk dijual nanti)?::ya::tidak::nanti",
 "Perlu framework i18n atau switch bahasa manual?::framework::manual",
 "Testing: Vitest + Playwright — oke?::oke::tambah lain",
 "Box ini tidak ada Docker. Dev agent-node di VPS atau tetap di box ini?::VPS::box ini::laptop bekas",
 "Monorepo Cuda digabung dengan Meridian (pakai gateway-nya) atau berdiri sendiri?::gabung gateway::berdiri sendiri",
]),
("E", "Hosting, Infra & Biaya", "☁️", [
 "Web deploy ke Vercel (project baru \"cuda\") atau self-host?::Vercel::self-host VPS::dua-duanya",
 "Agent-node jalan di mana?::VPS Linode::STB Armbian::laptop bekas::box ini",
 "Kalau STB: sanggup nyala 24/7? Resource masih cukup (sekarang ada AdGuard + bot)?",
 "TLS/domain: Caddy otomatis, Cloudflare Tunnel permanen, atau pakai domain Vercel?::Caddy::CF Tunnel::domain Vercel",
 "Database produksi: Neon free, Supabase free, atau SQLite di VPS?::Neon::Supabase::SQLite VPS",
 "Storage file (upload + artifact): lokal VPS, Cloudflare R2, atau Supabase Storage?::lokal VPS::R2::Supabase",
 "Backup otomatis ke mana?::GitHub::Google Drive::S3/R2::tidak perlu",
 "Budget infra bulanan yang wajar (Rp)?",
 "Kalau agent-node down: fallback tampil error, atau Cuda AI tetap jalan penuh?::error saja::AI tetap jalan",
 "Perlu queue (Redis/BullMQ) atau cukup in-memory dulu?::in-memory::Redis",
 "Monitoring v1: Sentry, Uptime Kuma, atau cukup log?::Sentry::Uptime Kuma::log saja::gabungan",
 "Log retention berapa lama?::7 hari::30 hari::90 hari",
 "Disk box ini 99% penuh (sisa 2.6GB). Boleh gue bersihkan project lama? mana yang aman dihapus?",
 "Build berat boleh dijalankan di VPS (SSH) biar tidak makan disk box ini?::boleh::jangan::box ini saja",
]),
("F", "Cuda AI — UX & Fitur Chat", "💬", [
 "Layout default: sidebar terbuka atau collapsed?::terbuka::collapsed",
 "Jawaban AI: gaya polos (Claude) atau bubble (ChatGPT)?::polos::bubble::campuran",
 "Perlu Projects/Ruang Kerja sejak v1?::ya::tidak::nanti",
 "Instruksi permanen per Ruang Kerja (custom instruction) perlu?::perlu::tidak",
 "Organisasi percakapan: folder bertingkat, tag, atau cuma list?::folder::tag::list saja",
 "Search percakapan: full-text saja atau + semantik?::full-text::+semantik",
 "Perlu pin / arsip / hapus massal?::semua::sebagian (sebutkan)",
 "Composer: Enter = kirim, atau Shift+Enter = kirim?::Enter::Shift+Enter::bisa diatur",
 "Draft auto-save lintas device?::perlu::tidak",
 "Prompt library (Resep) dengan variabel + berapa resep bawaan?",
 "Persona chips bawaan: mau apa saja?",
 "Slash command yang kamu mau ada?",
 "Tipe file attach wajib: gambar/PDF/DOCX/XLSX/CSV/kode — pilih semua yang wajib",
 "Batas ukuran file upload?::10MB::25MB::50MB::100MB",
 "Perlu OCR untuk PDF scan & gambar?::perlu::tidak",
 "Web search: pakai Firecrawl (key sudah ada) atau tambah engine lain?::Firecrawl::Firecrawl+tambahan::lain",
 "Default toggle web search: on atau off?::off::on",
 "Image generation: model mana & kuota per hari?",
 "Read aloud (TTS): perlu suara bahasa Indonesia?::perlu::Inggris cukup::tidak perlu",
 "STT bahasa Indonesia untuk voice input?::perlu::tidak",
 "Branching (edit pesan → fork cabang): seberapa penting?::penting::nice-to-have::tidak perlu",
 "Perlu fitur \"lanjutkan jawaban\" (continue generating)?::perlu::tidak",
 "Rating jawaban (👍👎 + alasan) perlu?::perlu::tidak",
 "Export PDF rapi dengan header/brand Cuda?::perlu::tidak::MD cukup",
 "Share thread publik: langsung publik atau harus klik Publish?::harus Publish::langsung::tidak perlu",
 "Perlu mode sementara (percakapan tidak disimpan)?::perlu::tidak",
]),
("G", "Cuda AI — Artifact & Memory", "🧩", [
 "Artifact otomatis dibuka kalau kode lebih dari berapa baris?::15::30::50::selalu tanya",
 "Tipe artifact wajib: HTML/React/SVG/Mermaid/chart/dokumen — pilih yang wajib",
 "Artifact boleh menjalankan JS sendiri di sandbox iframe?::boleh::tidak (render statis)",
 "Berapa versi history artifact yang disimpan?::5::10::tak terbatas",
 "Targeted edit (highlight → \"pendekin ini\") masuk v1?::v1::nanti",
 "Publish artifact → link publik yang bisa dicabut?::ya::tidak perlu",
 "Artifact bisa diedit manual oleh kamu (bukan cuma AI)?::ya::tidak",
 "Perlu halaman galeri semua artifact?::perlu::tidak",
 "Apa yang boleh diingat otomatis? (nama, preferensi, project, jadwal, data sensitif?)",
 "Perlu halaman Memory yang bisa dilihat/diedit/dihapus?::perlu::tidak",
 "Scope memory: global / per Ruang Kerja / per percakapan?::global::per Ruang Kerja::per percakapan::gabungan",
 "Perlu penjelasan \"kenapa ini diingat?\" (sumber fakta)?::perlu::tidak",
 "Fakta lama otomatis jadi kadaluwarsa (valid_at/invalid_at)?::ya::tidak",
 "Perlu import riwayat dari ChatGPT/Hermes ke Cuda?::perlu::tidak",
]),
("H", "Cuda Agent — Model Mental & Alur Misi", "🤖", [
 "Mulai misi: form goal khusus, atau dari chat biasa lalu naik jadi misi?::form::dari chat::dua-duanya",
 "Agent wajib tampilkan Rencana dulu & minta persetujuan sebelum jalan?::ya::langsung jalan::bisa diatur",
 "Setelah plan di-approve, agent boleh eksekusi semua langkah tanpa tanya lagi?::boleh::tetap tanya per aksi berisiko",
 "Perlu tampilan Board (kanban) selain timeline?::perlu::timeline cukup",
 "Timeline default: kartu terbuka semua atau collapsed?::collapsed::terbuka",
 "\"Current step\" selalu di-pin di atas?::ya::tidak",
 "Perlu estimasi waktu & biaya sebelum misi jalan?::perlu::tidak",
 "Kalau agent nyangkut: langsung eskalasi atau coba ulang dulu?::langsung eskalasi::coba 3x lalu eskalasi",
 "Batas maksimal langkah per misi (default)?::8::12::20::50",
 "Batas aksi/tool call per misi (default)?::25::50::100",
 "Batas waktu per misi (default)?::10 menit::30 menit::1 jam::tanpa batas",
 "Batas biaya per misi (Rp, default)?",
 "Agent boleh bertanya balik ke kamu di tengah misi?::boleh::tidak",
 "Perlu mode \"diskusi\" (agent cuma ngobrol, tidak eksekusi) di room agent?::perlu::tidak",
 "Perlu \"fork misi\" (ulang dari langkah tertentu)?::perlu::tidak",
 "Perlu bandingkan 2 rencana lalu pilih?::perlu::tidak",
 "Format Serahan (hasil akhir) yang wajib: md/pdf/zip/link/gambar?",
 "Agent boleh kirim hasil otomatis ke Telegram/WA?::boleh::harus tanya dulu::tidak",
]),
("I", "Cuda Agent — Kontrol, Izin & Keamanan", "🛡️", [
 "Default autonomy level: Sarankan, Draf, atau Eksekusi?::Sarankan::Draf::Eksekusi",
 "Aksi apa saja yang WAJIB minta izin? (deploy/hapus/kirim/bayar/network/tulis file)",
 "Perlu matriks izin per tool (selalu/tanya/tidak) yang bisa diubah user?::perlu::tidak",
 "Izin bisa \"ingat pilihan ini untuk misi ini\"?::bisa::selalu tanya ulang",
 "Perlu mode paranoid (semua aksi tanya)?::perlu::tidak",
 "Perlu mode gas (semua aksi otomatis, tanpa tanya)?::perlu::tidak::dengan peringatan",
 "Kalau izin ditolak, agent harus ngapain?::re-plan::stop::tanya alternatif",
 "Kartu izin auto-pause kalau tidak dijawab berapa lama?::2 menit::5 menit::tidak auto-pause",
 "Agent hanya boleh akses folder workspace misi?::ya::boleh lebih luas",
 "Akses internet agent: bebas atau whitelist domain?::bebas::whitelist::bebas+tanya",
 "Agent boleh jalankan sudo?::tidak::boleh (bahaya)",
 "Command berbahaya (rm -rf, dd, curl|bash) diblok total?::blok::tanya dulu::bebas",
 "Log diredact (API key/token disembunyikan otomatis)?::ya::tidak",
 "Audit trail bisa diekspor (JSON/PDF)?::perlu::tidak",
 "Undo aksi file: cukup git-based, atau perlu trash bin juga?::git saja::+trash bin",
 "Checkpoint otomatis tiap langkah atau tiap N langkah?::tiap langkah::tiap 3 langkah",
 "Berapa checkpoint disimpan sebelum auto-prune?::20::50::tak terbatas",
 "Kalau nanti ada Docker: perlu network namespace terpisah per misi?::perlu::tidak",
 "Data misi disimpan berapa lama sebelum dihapus otomatis?::7 hari::30 hari::permanen",
 "Cuda boleh simpan credential/API key user untuk tool? Bagaimana enkripsinya?",
]),
("J", "Cuda Agent — Tool & Kemampuan", "🔧", [
 "Tool prioritas v1 (pilih 6–8 dari daftar di plan §5.3)?",
 "Tool browser (Playwright) masuk v1?::v1::nanti",
 "Tool scraping Firecrawl langsung jadi tool agent?::ya::tidak",
 "Tool generate gambar untuk agent?::perlu::tidak",
 "Tool bikin PDF/DOCX/XLSX?::perlu::tidak",
 "Tool git (commit/branch/push) + auto-push ke GitHub?::perlu+auto push::perlu, tanpa auto push::tidak",
 "Tool deploy (Vercel/GitHub Pages) di v1?::v1::nanti",
 "Tool kirim email/WhatsApp/Telegram?::perlu::tidak",
 "Tool query database lokal (SQL)?::perlu::tidak",
 "Tool RAG atas file workspace (tanya-jawab dokumen misi)?::perlu::tidak",
 "Tool olah CSV/XLSX besar (100k baris)?::perlu::tidak",
 "Tool convert file (docx→pdf, img→webp, dll)?::perlu::tidak",
 "Tool monitoring uptime situs + alert?::perlu::tidak",
 "Tool scrape sosmed (IG/TikTok) — sadar batasan ToS, tetap mau?::tidak::ya dengan batasan",
 "Tool OSINT (pakai scam-hunt yang sudah ada)?::perlu::tidak",
 "Agent bisa simpan Playbook dari misi sukses (belajar sendiri)?::boleh::tidak",
 "Tool jalankan skrip/plugin custom buatan user?::perlu::tidak",
 "Perlu marketplace tool/plugin dari orang lain?::perlu::tidak::nanti",
]),
("K", "Model, Provider & Routing", "🧠", [
 "Urutan prioritas provider: TeamORouter, Ldrcloud, Meridian, Genspark — tulis urutannya",
 "Model default Cuda AI (cepat & murah)?",
 "Model default Cuda Agent planner (reasoning kuat)?",
 "Model untuk executor (murah & cepat)?",
 "Model untuk summarizer/compressor?",
 "User boleh ganti model per percakapan/misi?::boleh::model tetap::admin saja",
 "Berapa model dalam rantai fallback sebelum menyerah?::2::3::5",
 "Kalau semua provider down: pesan/aksi apa yang muncul?",
 "Perlu limit token per user per hari?::perlu (berapa)::tidak",
 "Perlu BYO key (user bawa API key sendiri)?::perlu::tidak",
 "Perlu expose endpoint OpenAI-compatible dari Cuda?::perlu::tidak::nanti",
 "Markup billing Rupiah per token berapa persen?::0%::10%::20%::lain",
 "Perlu model lokal (llama.cpp di STB) sebagai opsi offline?::perlu::tidak",
 "Perlu prompt caching untuk hemat biaya?::perlu::tidak",
]),
("L", "Data, Akun & Auth", "🔐", [
 "Metode login: email+password, magic link, Google OAuth, Telegram login?::email+pw::magic link::Google::Telegram",
 "Perlu mode tamu (tanpa login) di v1?::perlu::tidak",
 "Perlu multi-device sync?::perlu::tidak",
 "Data percakapan disimpan di server, lokal browser, atau dua-duanya?::server::lokal::dua-duanya",
 "Perlu export semua data (GDPR-style)?::perlu::tidak",
 "Perlu hapus akun self-service?::perlu::tidak",
 "Perlu role admin terpisah?::perlu::tidak",
 "Batas percakapan/misi untuk user gratis?",
 "Data user boleh dipakai untuk training/evaluasi?::tidak::boleh anonim::tanya dulu",
 "Perlu enkripsi at-rest untuk isi percakapan?::perlu::tidak",
 "Perlu session timeout / 2FA?::2FA::timeout::dua-duanya::tidak",
 "Username publik untuk link share (mis. /share/c/ziee)?::perlu::slug acak saja",
]),
("M", "Billing & Monetisasi", "💰", [
 "Model bisnis: gratis total, freemium, atau berbayar?::gratis::freemium::berbayar",
 "Kalau freemium: batas gratisnya apa (pesan/hari, misi/bulan)?",
 "Harga paket bulanan yang wajar (Rp)?",
 "Metode bayar: QRIS, transfer bank, Midtrans, crypto?",
 "Pakai kredit (credit system) atau langganan flat?::kredit::langganan::dua-duanya",
 "Perlu halaman invoice/riwayat pembayaran?::perlu::tidak",
 "Kuota agent dipisah dari kuota chat?::dipisah::digabung",
 "Perlu referral/affiliate?::perlu::tidak",
 "Perlu free trial?::7 hari::14 hari::tidak",
 "Biaya API upstream ditanggung siapa (kamu atau user)?::kamu::user::dibagi",
 "Rate limit anti-abuse: berapa per menit?::10::30::60::tanpa limit",
 "Perlu paket khusus mahasiswa?::perlu::tidak",
]),
("N", "Desain Visual & Bahasa", "🎨", [
 "Tema default: dark, light, atau ikut sistem?::dark::light::ikut sistem",
 "Light mode masuk v1?::v1::nanti::tidak perlu",
 "Font Inter + JetBrains Mono — oke?::oke::ganti (sebutkan)",
 "Density: Cuda AI lega, Cuda Agent padat — setuju?::setuju::ubah",
 "Animasi/transisi: halus banyak, atau minim & cepat?::halus::minim::sedang",
 "Suara notifikasi saat misi selesai?::perlu::tidak",
 "Notifikasi push browser?::perlu::tidak",
 "Icon set Lucide — oke?::oke::ganti",
 "Perlu ilustrasi/empty state custom (dibuatkan)?::perlu::tidak::pakai icon saja",
 "Onboarding: wizard 3 langkah atau langsung pakai?::wizard::langsung::tidak perlu",
 "Landing marketing lengkap atau cuma redirect ke app?::lengkap::redirect::landing ringkas",
 "Perlu demo interaktif di landing?::perlu::tidak",
 "Target aksesibilitas WCAG AA?::target AA::seadanya",
 "Perlu keyboard shortcut lengkap + halaman cheat sheet?::perlu::tidak",
 "User boleh ganti warna accent sendiri?::boleh::tetap",
 "Ada referensi visual/situs yang kamu suka untuk jadi acuan? (kirim link)",
]),
("O", "Mobile & PWA", "📱", [
 "Prioritas: desktop dulu atau mobile dulu?::desktop::mobile::dua-duanya",
 "PWA installable di v1?::v1::nanti",
 "Offline mode (baca riwayat tanpa internet)?::perlu::tidak",
 "Cuda Agent di HP pakai tab bar (Misi/Aktivitas/Workspace/Serahan) — setuju?::setuju::ubah",
 "Notifikasi HP saat misi selesai via bot Telegram?::perlu::tidak",
 "Swipe gesture (arsip/hapus) di mobile?::perlu::tidak",
 "Ukuran font default di HP?::kecil::sedang::besar",
 "Mode lanskap untuk lihat timeline + workspace bareng?::perlu::tidak",
 "Perlu quick action share-ke-Cuda dari app lain?::perlu::tidak",
 "App Android native nanti, atau PWA cukup?::PWA cukup::native nanti",
]),
("P", "Integrasi & Ekosistem", "🔌", [
 "Integrasi wajib: GitHub, Telegram, Google Drive, Notion — pilih yang wajib v1",
 "Perlu integrasi dengan project kamu yang lain (Meridian, masbraw-chat lama)?::perlu::tidak",
 "Migrasi data dari masbraw-chat lama perlu?::perlu::tidak::mulai bersih",
 "Perlu bot Telegram sebagai front-end Cuda (chat lewat TG)?::perlu::tidak::nanti",
 "Perlu integrasi WhatsApp?::perlu::tidak::nanti",
 "Perlu integrasi kalender/tugas (Google Calendar, Todoist)?::perlu::tidak",
 "Perlu webhook keluar (hasil misi dikirim ke endpoint kamu)?::perlu::tidak",
 "Perlu API key Cuda untuk dipakai app lain?::perlu::tidak",
 "Perlu integrasi Hermes (Cuda jadi tool Hermes, atau sebaliknya)?::Cuda jadi tool::Hermes jadi tool::tidak",
 "MCP server mana yang mau dipasang dulu?",
 "Perlu integrasi pembayaran di v1?::v1::nanti",
 "Perlu kirim laporan via email?::perlu::tidak",
]),
("Q", "Operasional, Monitoring & QA", "⚙️", [
 "Siapa yang maintain setelah jadi?::kamu sendiri::kamu + gue::orang lain",
 "Perlu CI/CD GitHub Actions untuk deploy otomatis?::perlu::tidak",
 "Perlu staging environment terpisah?::perlu::tidak",
 "Target test coverage?::40%::70%::90%::seadanya",
 "Load test: berapa misi paralel harus kuat?::3::5::10::20",
 "Kalau ada bug produksi, notif ke mana?::Telegram::email::keduanya",
 "Perlu halaman status publik (cek node hidup)?::perlu::tidak",
 "Perlu dokumentasi user/help center di v1?::perlu::tidak::nanti",
 "Perlu changelog publik?::perlu::tidak",
 "Backup & restore drill berapa sering?::harian::mingguan::bulanan",
]),
("R", "Roadmap & Masa Depan", "🚀", [
 "Fitur apa yang kamu bayangkan ada 6 bulan lagi?",
 "Cuda mau jadi SaaS publik atau tetap personal tool?::SaaS::personal::dua-duanya",
 "Kalau sukses, buka versi untuk tim/kantor (Cuda Teams)?::ya::tidak::mungkin",
 "Perlu versi enterprise/on-premise?::perlu::tidak",
 "Perlu mobile app native?::perlu::PWA cukup",
 "Perlu marketplace playbook/tool dari komunitas?::perlu::tidak",
 "Perlu Cuda belajar dari percakapan lama kamu (fine-tune/RAG personal)?::perlu::tidak",
 "Perlu multi-agent kolaborasi (beberapa agent kerja bareng di satu misi)?::perlu::tidak::nanti",
 "Perlu agent bisa jual jasa (agent-as-a-service ke klien)?::perlu::tidak",
 "Milestone 3 bulan / 6 bulan / 1 tahun?",
 "Ada fitur besar lain yang mau kamu tambahkan sekarang?",
 "Ada hal yang HARAM dilakukan Cuda (batasan keras dari kamu)?",
]),
]

# ---------- flatten ----------
flat = []
n = 0
for code, title, emoji, qs in SECTIONS:
    for q in qs:
        n += 1
        parts = q.split("::")
        flat.append({"n": n, "sec": code, "q": parts[0], "opts": parts[1:]})
TOTAL = n

data = [{"code": c, "title": t, "emoji": e, "items": [x for x in flat if x["sec"] == c]}
        for c, t, e, _ in SECTIONS]

# ---------- markdown + csv ----------
md = ["# Cuda — Kuesioner Penyempurnaan Produk", "",
      f"Total: **{TOTAL} pertanyaan** dalam {len(SECTIONS)} bagian.", "",
      "Cara pakai: isi jawaban setelah tanda `→`. Kalau tidak punya preferensi, tulis `default`.",
      "", "---", ""]
for s in data:
    md += [f"## {s['code']}. {s['title']}", ""]
    for it in s["items"]:
        md.append(f"**{it['n']}.** {it['q']}")
        if it["opts"]:
            md.append("   opsi: " + " | ".join(it["opts"]))
        md.append("   → ")
        md.append("")
open(f"{OUT}/QUESTIONS.md", "w").write("\n".join(md))

with open(f"{OUT}/questions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["no", "bagian", "pertanyaan", "opsi", "jawaban"])
    for it in flat:
        w.writerow([it["n"], it["sec"], it["q"], " | ".join(it["opts"]), ""])

# ---------- interactive html ----------
JS = r"""
const DATA = __DATA__;
const KEY = 'cuda-questionnaire-v1';
let answers = {};
try { answers = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) { answers = {}; }
const $ = s => document.querySelector(s);
const total = DATA.reduce((a,s)=>a+s.items.length,0);

function save(){ localStorage.setItem(KEY, JSON.stringify(answers)); }
function answeredCount(){ return Object.values(answers).filter(v=>v && v.trim()).length; }

function render(){
  const root = $('#qroot'); root.innerHTML='';
  DATA.forEach(sec=>{
    const s = document.createElement('section');
    s.className='sec'; s.id='sec-'+sec.code;
    s.innerHTML = `<div class="sechead"><span class="code">${sec.code}</span>
      <h2>${sec.emoji} ${sec.title}</h2>
      <span class="seccount" data-c="${sec.code}"></span></div>`;
    sec.items.forEach(it=>{
      const row = document.createElement('div');
      row.className='row'; row.dataset.n = it.n;
      const val = answers[it.n] || '';
      let chips = '';
      if(it.opts.length){
        chips = '<div class="chips">' + it.opts.map(o=>`<button type="button" class="chip${val===o?' on':''}" data-n="${it.n}" data-o="${o.replace(/"/g,'&quot;')}">${o}</button>`).join('') + '</div>';
      }
      row.innerHTML = `<div class="qhead"><span class="num">${it.n}</span><p class="qtext">${it.q}</p></div>
        ${chips}
        <textarea rows="1" data-n="${it.n}" placeholder="tulis jawaban…">${val}</textarea>`;
      if(val.trim()) row.classList.add('filled');
      s.appendChild(row);
    });
    root.appendChild(s);
  });
  root.querySelectorAll('textarea').forEach(t=>{
    autoGrow(t);
    t.addEventListener('input', e=>{
      answers[e.target.dataset.n] = e.target.value; save(); autoGrow(e.target);
      updateProgress(); syncChips(e.target.dataset.n);
      const r = e.target.closest('.row'); if(r) r.classList.toggle('filled', !!e.target.value.trim());
    });
  });
  root.querySelectorAll('.chip').forEach(c=>{
    c.addEventListener('click', ()=>{
      const n = c.dataset.n, o = c.dataset.o;
      answers[n] = (answers[n]===o) ? '' : o; save();
      const ta = root.querySelector(`textarea[data-n="${n}"]`); if(ta) ta.value = answers[n]||'';
      syncChips(n); updateProgress();
    });
  });
  updateProgress();
}
function syncChips(n){
  document.querySelectorAll(`.chip[data-n="${n}"]`).forEach(c=>{
    c.classList.toggle('on', answers[n]===c.dataset.o);
  });
}
function autoGrow(t){ t.style.height='auto'; t.style.height = Math.min(t.scrollHeight, 320) + 'px'; }
function updateProgress(){
  const done = answeredCount();
  $('#bar').style.width = (done/total*100).toFixed(1)+'%';
  $('#prog').textContent = `${done} / ${total} terjawab`;
  DATA.forEach(sec=>{
    const el = document.querySelector(`[data-c="${sec.code}"]`);
    if(el){ const d = sec.items.filter(i=>answers[i.n]&&answers[i.n].trim()).length; el.textContent = `${d}/${sec.items.length}`; }
  });
}
function exportText(){
  let out = `CUDA — JAWABAN KUESIONER (${answeredCount()}/${total})\n`;
  out += `Tanggal: ${new Date().toLocaleString('id-ID')}\n\n`;
  DATA.forEach(sec=>{
    out += `## ${sec.code}. ${sec.title}\n`;
    sec.items.forEach(it=>{
      const a = (answers[it.n]||'').trim();
      out += `${it.n}. ${it.q} → ${a || '(belum dijawab)'}\n`;
    });
    out += `\n`;
  });
  return out;
}
function download(name, text, type){
  const b = new Blob([text], {type: type||'text/plain;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b); a.download = name; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
}
function toast(msg){
  const t = $('#toast'); t.textContent = msg; t.classList.add('on');
  setTimeout(()=>t.classList.remove('on'), 2200);
}
document.addEventListener('click', e=>{
  const id = e.target.id;
  if(id==='copy'){
    const txt = exportText();
    navigator.clipboard.writeText(txt).then(()=>toast('Semua jawaban di-copy ✓ tinggal paste ke chat'),
      ()=>{ const ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); toast('Jawaban di-copy ✓'); });
  }
  if(id==='dl-md'){ download('cuda-jawaban.md', exportText(), 'text/markdown;charset=utf-8'); toast('cuda-jawaban.md diunduh'); }
  if(id==='dl-json'){ download('cuda-jawaban.json', JSON.stringify({answered:answeredCount(),total,answers},null,1), 'application/json'); toast('cuda-jawaban.json diunduh'); }
  if(id==='skip-empty'){
    DATA.forEach(sec=>sec.items.forEach(it=>{ if(!(answers[it.n]||'').trim()) answers[it.n]='default'; }));
    save(); render(); toast('Yang kosong diisi "default" — tinggal edit yang mau diubah');
  }
  if(id==='reset'){ if(confirm('Hapus semua jawaban?')){ answers={}; save(); render(); toast('Reset ✓'); } }
  if(id==='toggle-done'){
    document.body.classList.toggle('hide-done');
    e.target.textContent = document.body.classList.contains('hide-done') ? 'Tampilkan semua' : 'Sembunyikan yang sudah dijawab';
  }
});
render();
"""

HTML = r"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cuda — Kuesioner 262 Pertanyaan</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0d10;--surface:#15171b;--surface2:#1b1e23;--border:#2a2e35;--text:#e6e8eb;--dim:#9aa3af;--mute:#6b7280;
--accent:#5e6ad2;--violet:#8b5cf6;--ok:#22c55e;--mono:"JetBrains Mono",ui-monospace,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 Inter,system-ui,sans-serif}
a{color:#4f8cff;text-decoration:none}
header{position:sticky;top:0;z-index:20;background:#0d0f13ee;backdrop-filter:blur(10px);border-bottom:1px solid var(--border);padding:14px 18px}
.hrow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;max-width:1000px;margin:0 auto}
.mark{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,var(--accent),var(--violet));display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff}
h1{font-size:17px;margin:0;letter-spacing:-.2px}
h1 span{display:block;font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.08em;font-weight:500}
.pbar{flex:1;min-width:140px;height:6px;background:var(--surface2);border-radius:20px;overflow:hidden}
#bar{height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--violet));transition:width .25s}
#prog{font-size:12px;color:var(--dim);font-family:var(--mono);white-space:nowrap}
.btns{display:flex;gap:8px;flex-wrap:wrap}
button{font:inherit;font-size:13px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text);
padding:7px 13px;cursor:pointer;transition:.15s}
button:hover{background:var(--surface2);border-color:#3a4150}
button.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
button.primary:hover{background:#6b76dd}
button.ghost{background:transparent;color:var(--dim)}
main{max-width:1000px;margin:0 auto;padding:22px 18px 140px}
.intro{background:linear-gradient(180deg,#141821,#0e1116);border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:24px}
.intro h2{margin:0 0 8px;font-size:16px}
.intro p{margin:6px 0;color:var(--dim);font-size:14px}
.intro code{font-family:var(--mono);font-size:12px;background:#0f1216;border:1px solid var(--border);padding:1px 5px;border-radius:4px}
.sec{margin:34px 0}
.sechead{display:flex;align-items:center;gap:10px;padding-bottom:10px;border-bottom:1px solid var(--border);position:sticky;top:64px;background:var(--bg);z-index:10}
.code{font-family:var(--mono);font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:2px 7px;color:var(--violet)}
.sechead h2{font-size:16px;margin:0;flex:1}
.seccount{font-size:11.5px;color:var(--mute);font-family:var(--mono)}
.row{padding:16px 0;border-bottom:1px solid #1c2027}
.row.filled{opacity:.55}
body.hide-done .row.filled{display:none}
.qhead{display:flex;gap:10px;align-items:flex-start}
.num{font-family:var(--mono);font-size:12px;color:var(--mute);min-width:34px;padding-top:3px}
.qtext{margin:0;font-size:14.5px;font-weight:500;flex:1}
.chips{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0 0 44px}
.chip{font-size:12.5px;padding:5px 11px;border-radius:20px;background:var(--surface);border:1px solid var(--border);color:var(--dim)}
.chip.on{background:#241d3d;border-color:var(--violet);color:#c4a6ff}
textarea{width:100%;margin:10px 0 0 44px;max-width:calc(100% - 44px);background:#0f1216;border:1px solid var(--border);border-radius:9px;
color:var(--text);font:14px/1.55 Inter,sans-serif;padding:10px 13px;resize:vertical;min-height:42px}
textarea:focus{outline:none;border-color:var(--accent);background:#111419}
footer{border-top:1px solid var(--border);margin-top:50px;padding-top:18px;color:var(--mute);font-size:12.5px}
#toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,20px);background:#1b1e23;border:1px solid var(--border);
border-radius:10px;padding:11px 18px;font-size:13.5px;opacity:0;pointer-events:none;transition:.25s;z-index:50;max-width:90vw;text-align:center}
#toast.on{opacity:1;transform:translate(-50%,0)}
@media(max-width:640px){.chips,textarea{margin-left:0;max-width:100%}.sechead{top:96px}h1{font-size:15px}}
</style></head><body>
<header><div class="hrow">
<div class="mark">C</div>
<h1>Cuda — Kuesioner Penyempurnaan<span>__TOTAL__ pertanyaan · __SECTIONS__ bagian</span></h1>
<div class="pbar"><div id="bar"></div></div>
<div id="prog">0 / 0</div>
</div>
<div class="hrow" style="margin-top:12px">
<div class="btns">
<button class="primary" id="copy">📋 Copy semua jawaban</button>
<button id="dl-md">⬇︎ .md</button>
<button id="dl-json">⬇︎ .json</button>
<button class="ghost" id="skip-empty">Isi "default" yang kosong</button>
<button class="ghost" id="toggle-done">Sembunyikan yang sudah dijawab</button>
<button class="ghost" id="reset">Reset</button>
</div>
</div></header>
<main>
<div class="intro">
<h2>Kenapa kuesioner ini ada</h2>
<p>Jawaban lo di sini yang nentuin bentuk akhir Cuda — bukan asumsi gue. Semua <strong>auto-save</strong> di browser (aman kalau HP ke-refresh).</p>
<p><strong>Cara paling cepat:</strong> klik <code>Isi "default" yang kosong</code> → semua pertanyaan keisi "default" (artinya: pakai rekomendasi gue) → terus edit cuma yang lo mau beda. Habis itu klik <code>Copy semua jawaban</code> dan paste ke chat.</p>
<p>Ada <code>::opsi::</code> di bawah pertanyaan? Itu pilihan cepat — tinggal tap. Kalau mau jawaban bebas, tulis aja di kotak.</p>
</div>
<div id="qroot"></div>
<footer>File ini offline — tidak ada data yang dikirim ke server. Jawaban tersimpan di browser lo sendiri.</footer>
</main>
<div id="toast"></div>
<script>__JS__</script></body></html>
"""

html = (HTML.replace("__TOTAL__", str(TOTAL))
            .replace("__SECTIONS__", str(len(SECTIONS)))
            .replace("__JS__", JS.replace("__DATA__", json.dumps(data, ensure_ascii=False))))
open(f"{OUT}/index.html", "w").write(html)

# extract JS for syntax check
os.makedirs("/tmp/cudachk", exist_ok=True)
open("/tmp/cudachk/app.js", "w").write(JS.replace("__DATA__", json.dumps(data, ensure_ascii=False)))

print(f"TOTAL QUESTIONS: {TOTAL} in {len(SECTIONS)} sections")
print("wrote:", sorted(os.listdir(OUT)))
