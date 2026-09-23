# PROMPT — paste ini ke AI agent di laptop

Salin seluruh blok di bawah ke agent (Hermes / Claude Code / Codex / Cursor) yang jalan di laptop.

---

```
Kamu akan mengeksekusi project "Cuda" dari nol sampai MVP jalan. Kamu tidak punya konteks
sebelumnya — semua konteks ada di repo GitHub private ini:

  https://github.com/Xiaochown/cuda

LANGKAH 1 — Ambil repo:
  git clone https://github.com/Xiaochown/cuda.git && cd cuda

LANGKAH 2 — Baca dokumen ini berurutan (jangan skip):
  1. AGENT_BRIEF.md        <- brief utama, baca SAMPAI HABIS dulu
  2. docs/DECISIONS.md     <- 262 keputusan produk yang sudah LOCKED (sumber kebenaran)
  3. PLAN.md               <- arsitektur, spec tiap room, event protocol, data model, rencana 14 hari
  4. TASKS.md              <- checklist 40 task yang harus kamu kerjakan
  5. docs/SETUP_LAPTOP.md  <- setup environment
  6. docs/RESEARCH.md      <- riset 2026 yang jadi dasar desain

LANGKAH 3 — Setup environment sesuai docs/SETUP_LAPTOP.md (Node 22, git, gh, Playwright).
  Sangat disarankan pakai WSL2 Ubuntu. Verifikasi: node -v (>=22), git -v, gh auth status.

LANGKAH 4 — Minta ke user SATU base_url + api_key OpenAI-compatible untuk testing,
  taruh di .env (JANGAN commit). Cuda tidak menyediakan model — semua lewat key user (BYOE).

LANGKAH 5 — Kerjakan TASKS.md berurutan dari P0-1 sampai P3 selesai.
  Aturan: satu task = satu commit. Centang checkbox di TASKS.md tiap task selesai.
  Jangan lompat ke phase berikutnya sebelum Definition of Done phase sebelumnya terpenuhi.

ATURAN KERAS (dari AGENT_BRIEF.md, jangan dilanggar):
  - Cuda = local-first + BYOE. TIDAK ADA billing, kredit, markup, kuota, rate limit.
  - Skills (file SKILL.md dipanggil dengan /nama-skill) — BUKAN prompt library.
  - Cuda Agent = console 3-pane (Missions | Activity | Workspace), BUKAN chat.
    Pisahkan conversation stream dari activity stream.
  - Setiap aksi agent wajib punya Receipt (apa berubah + diff + izin + Undo git-based).
  - Permission matrix per tool + approval gate untuk aksi sensitif + kill switch.
  - sudo default OFF; command berbahaya butuh konfirmasi kedua (user ketik ulang).
  - Secret: AES-256-GCM at-rest, tidak pernah plaintext ke frontend, diredact di log.
  - UI Bahasa Inggris, laporan ke user Bahasa Indonesia casual.
  - Satu accent warna: midnight blue #2563eb. Ikon model/brand full-color. Tema ikut sistem.
  - Test keamanan sandbox WAJIB lulus: path traversal, command injection, symlink escape,
    resource bomb -> semua harus ditolak/di-cap.

CARA KERJA:
  - Autonomi tinggi. User ini gaya "gas" — jangan minta konfirmasi tiap langkah.
  - Tanya HANYA kalau: butuh kredensial, ada konflik nyata antar dokumen, mau hapus data user,
    atau mau deploy ke akun user.
  - Kalau keputusan kecil ambigu: pilih default paling sesuai docs/DECISIONS.md, catat di commit.
  - Jangan klaim "sudah jalan" tanpa bukti. Jalankan test / curl route / screenshot.
    Kalau gagal, lapor apa adanya.

MULAI SEKARANG dari LANGKAH 1. Setelah P1 (Cuda AI) selesai, lapor user dengan cara
menjalankannya + apa yang bisa dicoba.
```

---

## Catatan untuk user

- Ganti `Xiaochown` kalau lo pakai akun GitHub lain. Repo-nya **private**, jadi agent perlu akses (`gh auth login` atau PAT).
- Kalau agent di laptop itu bukan Hermes (mis. Claude Code / Codex / Cursor), prompt di atas tetap jalan — semuanya cuma butuh akses file + terminal.
- Kalau laptop belum ada Node 22 / git / gh, ikuti `docs/SETUP_LAPTOP.md` (5–10 menit).
- Prompt versi pendek (kalau agent-nya sudah bisa baca repo sendiri):
  *"Clone https://github.com/Xiaochown/cuda, baca AGENT_BRIEF.md + docs/DECISIONS.md + PLAN.md + TASKS.md, lalu kerjakan TASKS.md dari P0 sampai P3 selesai. Aturan lengkap ada di AGENT_BRIEF.md."*
