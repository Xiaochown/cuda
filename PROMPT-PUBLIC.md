# PROMPT — versi PUBLIC (untuk AI tanpa terminal / AI web)

Repo Cuda sekarang **public**, jadi dokumennya bisa dibaca langsung lewat URL oleh AI apa pun yang punya akses web (ChatGPT, Claude, Gemini, Grok, Perplexity, dll) — **tanpa perlu clone**.

**Batasnya:** AI yang nggak punya terminal/eksekusi kode cuma bisa **review, kritik, atau bantu desain** — nggak bisa nulis file & commit. Untuk **membangun**, tetap butuh agent yang punya shell (Hermes/Claude Code/Codex/Cursor di laptop) → pakai `PROMPT.md`.

---

## Raw URL (semua dokumen)

```
https://raw.githubusercontent.com/Xiaochown/cuda/master/README.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/AGENT_BRIEF.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/PLAN.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/TASKS.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/PROMPT.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/DECISIONS.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/RESEARCH.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/SETUP_LAPTOP.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/ANSWERS.md
```

Halaman repo: https://github.com/Xiaochown/cuda

---

## Prompt A — buat AI web yang bisa browsing (review/kritik)

```
Baca dokumen project "Cuda" di repo public ini (fetch satu per satu, jangan skip):

  https://raw.githubusercontent.com/Xiaochown/cuda/master/AGENT_BRIEF.md
  https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/DECISIONS.md
  https://raw.githubusercontent.com/Xiaochown/cuda/master/PLAN.md
  https://raw.githubusercontent.com/Xiaochown/cuda/master/TASKS.md

Cuda = aplikasi AI local-first dua room: "Cuda AI" (workspace chat) dan "Cuda Agent"
(agentic console 3-pane: goal -> plan -> eksekusi pakai tools -> deliverable).

Tugas kamu: jadi REVIEWER kritis, bukan penulis ulang.
1. Baca semua dokumen di atas sampai habis.
2. Laporkan: (a) 5 kelemahan terbesar di arsitektur/rencananya, (b) 3 hal yang
   berpotensi bikin gagal di 2 minggu pertama, (c) 3 ide perbaikan konkret yang
   belum ada di dokumen, (d) bagian mana yang masih ambigu dan harus diklarifikasi user.
3. Jangan mengarang fakta tentang repo. Kalau ada yang belum kebaca, bilang belum kebaca.
4. Bahasa Indonesia casual. Ringkas, poin-poin, tanpa basa-basi.
```

## Prompt B — buat AI web yang mau bantu detail teknis

```
Baca dokumen project "Cuda" (repo public):
  https://raw.githubusercontent.com/Xiaochown/cuda/master/AGENT_BRIEF.md
  https://raw.githubusercontent.com/Xiaochown/cuda/master/PLAN.md

Cuda = aplikasi AI local-first (Next.js 16 + Fastify agent-node + SQLite/Prisma).
Dua room: Cuda AI (chat workspace) & Cuda Agent (agentic console 3-pane).
Prinsip keras: BYOE (user bawa base_url+api_key sendiri, tanpa billing), local-first,
skills via "/" (bukan prompt library), pisahkan conversation stream dari activity stream,
setiap aksi agent punya Receipt + Undo.

Tugas kamu: bantu aku merancang [ISI DI SINI — misal: "skema Prisma untuk event
append-only + replay", "arsitektur permission engine", "cara sandbox process-level
tanpa Docker"].
Syarat: ikuti aturan keras di AGENT_BRIEF.md. Jangan tambahkan fitur yang sudah
diputuskan user TIDAK perlu (billing, prompt library, scraper IG/TikTok, MCP di v1).
Output: kode/skema konkret + alasannya, bukan teori umum. Bahasa Indonesia casual.
```

## Prompt C — buat AI lain yang punya terminal (clone & kerjakan)

Sama seperti `PROMPT.md`, tapi tanpa perlu `gh auth login` (repo sudah public):

```
Clone repo public ini dan kerjakan project-nya:
  git clone https://github.com/Xiaochown/cuda.git && cd cuda

Baca berurutan: AGENT_BRIEF.md -> docs/DECISIONS.md -> PLAN.md -> TASKS.md -> docs/SETUP_LAPTOP.md.
Lalu kerjakan TASKS.md dari P0-1 sampai P3-10 (satu task = satu commit, centang checkbox).
Aturan keras lengkap ada di AGENT_BRIEF.md — baca sampai habis sebelum menulis kode.
```

---

## Catatan

- **Repo sudah public** — siapa pun dengan link bisa baca. Kalau nanti mau private lagi: `gh repo edit Xiaochown/cuda --visibility private --accept-visibility-change-consequences`.
- **Jangan pernah taruh API key / secret di repo ini** — sudah public. Semua kredensial lewat `.env` (sudah masuk `.gitignore`).
- Kalau agent lain menghasilkan perubahan kode, kirim lewat **Pull Request** (branch baru) supaya bisa di-review dulu, jangan push langsung ke `master`.
