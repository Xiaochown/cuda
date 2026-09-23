# AGENT BRIEF — Eksekusi Project CUDA

> **Untuk AI agent (Hermes/Claude Code/Codex/Cursor) yang jalan di laptop user.**
> Kamu TIDAK punya konteks percakapan sebelumnya. Semua yang kamu butuh ada di repo ini + dokumen ini.
> Baca dokumen ini SAMPAI HABIS sebelum menulis kode pertama.

---

## 0. Ringkasan satu menit

**Cuda** = aplikasi AI **local-first** dengan **dua room terpisah**:

| Room | Path | Apa itu |
|---|---|---|
| **Cuda AI** | `/ai` | Workspace chat biasa (setara ChatGPT/Claude): ngobrol, dokumen, artifact, riset, memory |
| **Cuda Agent** | `/agent` | Agentic console (setara Manus/Claude Cowork): kasih goal → plan → eksekusi pakai tools → deliverable nyata |

Brand: **Cuda** (induk), produk **Cuda AI** + **Cuda Agent**. Tagline: *"Cuda for Simple Work. Cuda Agent for Deep Work, Autonomous."*
Repo: `https://github.com/Xiaochown/cuda` (private). Pemilik: **Faa** (GitHub: Xiaochown, brand ZieeRoute/ZieDev).

---

## 1. Lima aturan yang TIDAK BOLEH dilanggar

1. **BYOE — Bring Your Own Everything.** Cuda **tidak menyediakan model**. Semua LLM/search/image lewat `base_url` + `api_key` milik user. **Jangan** bikin billing, kredit, markup, kuota, atau rate limit. **Jangan** hardcode API key apa pun ke repo.
2. **Local-first + desktop-first.** Data di SQLite lokal + IndexedDB browser. PWA installable. Nanti di-package jadi software desktop — jadi **jangan** pakai fitur yang cuma jalan di Vercel/cloud.
3. **Skills, BUKAN prompt library.** Kemampuan dipanggil dengan `/nama-skill`. Skill = file `SKILL.md` (frontmatter + body). Cuda boleh **menulis skill baru sendiri** setelah misi sukses.
4. **Pisahkan conversation stream dari activity stream.** Cuda Agent itu **console 3-pane**, BUKAN chat. Chat-first UX untuk agent = kegagalan desain yang sudah diteliti (lihat `docs/RESEARCH.md` §1).
5. **Setiap aksi punya Receipt + Undo.** Aksi agent (tulis file, jalankan terminal, git, deploy, kirim pesan) wajib menghasilkan struk: apa berubah + diff + izin yang dipakai + tombol Undo (git-based).

Detail lengkap keputusan produk (262 pertanyaan dijawab user) ada di **`docs/DECISIONS.md`** — itu sumber kebenaran. Kalau ada konflik antara dokumen lain dan `DECISIONS.md`, **`DECISIONS.md` menang**.

---

## 2. Baca dokumen ini berurutan

1. `README.md` — ringkas isi repo
2. `docs/DECISIONS.md` — **keputusan produk LOCKED** (5 pivot, keputusan per bagian, 8 flag, capability map 16 grup, 5 terobosan)
3. `PLAN.md` — **Implementation Plan v2**: arsitektur, design token, spec tiap room, event protocol, data model, tool layer, route map, **rencana 14 hari (§11)**, verifikasi, risiko
4. `docs/RESEARCH.md` — riset 2026 (kenapa agent UX harus 3-pane, sandbox, memory, artifact)
5. `TASKS.md` — **checklist 40 task yang harus kamu kerjakan** (update checkbox-nya sambil jalan)
6. `docs/SETUP_LAPTOP.md` — cara setup environment di laptop user
7. `mockups/` — 3 mockup visual (acuan tampilan akhir)

---

## 3. Stack (sudah diputuskan — jangan ganti tanpa alasan kuat)

- **Web:** Next.js 16 (App Router) + TypeScript + Tailwind 4 + komponen sendiri (Radix primitives)
- **State:** Zustand + TanStack Query · **ORM:** Prisma + SQLite · **Validasi:** Zod (dipakai di dua sisi)
- **Agent runtime:** Node 22 + Fastify + `ws` (service terpisah, `apps/agent-node`)
- **Editor/terminal/preview:** CodeMirror 6 · xterm.js · sandboxed iframe + postMessage
- **Tool browser:** Playwright · **Monorepo:** npm workspaces (`apps/*`, `packages/*`)
- **Test:** Vitest (unit) + Playwright (e2e) · **i18n:** EN default, ID switch
- **Deploy web:** Vercel (dari GitHub, auto) · **agent-node:** jalan lokal di laptop (port **9400**)

Token desain lengkap ada di `PLAN.md §2`. Ringkasnya: bg `#0d0d0d`, surface `#1a1c1f`, border `#2b2f36`, teks `#ececf1`, **satu accent midnight blue `#2563eb`**, status `run #f5a524 / ok #22c55e / err #ef4444 / wait #38bdf8`, font Inter + JetBrains Mono, radius 6/10/14px, tema ikut sistem + light mode, **ikon model/brand full-color**.

---

## 4. Urutan kerja (jangan diacak)

User memutuskan: **Cuda AI diselesaikan dulu**, baru Cuda Agent. Target MVP **2 minggu**.

```
P0 (Hari 1–2)   Fondasi: repo, monorepo, packages/core (events, tools, router, skills), Prisma schema
P1 (Hari 3–6)   Cuda AI: shell UI, streaming chat, thread, projects, composer, skills UI, artifacts, memory, export
P2 (Hari 7–11)  Cuda Agent: agent-node, orchestrator, event bus, sandbox, tools, permission, budget, checkpoint, receipt, skill generator, cron
P3 (Hari 12–14) UI console 3-pane, timeline, permission card, workspace viewer, plan compare, mobile/PWA, deploy
```

Detail tiap task (objective + file + acceptance criteria) ada di **`TASKS.md`**. Kerjakan **satu task = satu commit**.

---

## 5. Cara kerja yang diharapkan

- **Autonomi tinggi.** User ini gaya "gas" — dia nggak mau ditanya tiap langkah. Kalau ada keputusan kecil, pilih default yang paling sesuai `docs/DECISIONS.md` dan **catat pilihanmu di commit message**.
- **Tanya HANYA kalau:** (a) butuh API key/kredensial, (b) ada konflik nyata antar dokumen, (c) mau menghapus/mengubah data user, (d) mau deploy ke akun milik user.
- **Update `TASKS.md`** — centang `[x]` tiap task selesai, tulis catatan singkat kalau ada penyimpangan.
- **Commit message** gaya Conventional Commits: `feat(ai): streaming chat SSE`, `fix(agent): sandbox path traversal`, `chore: bootstrap monorepo`.
- **Bahasa laporan ke user:** Bahasa Indonesia casual (user pakai slang "gas", "cukk"). Kode/komentar/UI **Bahasa Inggris** (keputusan #7 & #8).
- **Verifikasi sebelum bilang selesai.** Jangan klaim "sudah jalan" tanpa bukti: jalankan test, `curl -o /dev/null -w '%{http_code}'` untuk tiap route, atau screenshot. Kalau gagal, laporkan apa adanya — jangan mengarang hasil.

---

## 6. Definition of Done

**Per task:** kode jalan + test lulus (kalau ada logika) + `TASKS.md` dicentang + commit.

**Per phase (P0–P3):**
- `npm run build` bersih tanpa error, `npm run test` hijau
- Semua route di `PLAN.md §10` balas 200 (curl)
- Cuda AI: bisa chat streaming dengan provider user, thread tersimpan, artifact bisa di-publish
- Cuda Agent: satu misi end-to-end menghasilkan **file nyata** di `workspaces/<mission-id>/`, timeline terisi, permission card muncul, receipt + undo jalan
- **Test keamanan sandbox WAJIB lulus:** path traversal (`../../etc/passwd`), command injection (`;`, `&&`, backtick), symlink escape, resource bomb → semua harus ditolak/di-cap
- Jalan di layar HP (user akses dari HP) — layout mobile tidak overflow

---

## 7. Guardrail keamanan (wajib diimplementasi)

- **Sandbox v1 tanpa Docker:** workspace per-misi (`workspaces/<id>/`), path-traversal guard, command allowlist, timeout per aksi, rlimit (CPU/mem), output cap, env bersih.
- **Akses folder:** default hanya workspace misi; lebih luas **hanya** kalau user setujui per-misi (tercatat di audit).
- **`sudo`: default OFF.** Bisa dinyalakan di Settings → Security dengan peringatan eksplisit + konfirmasi ketik ulang. Semua pemakaian sudo masuk audit log + muncul sebagai kartu merah di timeline.
- **Command berbahaya** (`rm -rf /`, `dd`, `curl|bash`, `chmod 777`, `mkfs`, fork bomb): **konfirmasi kedua** (user ketik ulang perintahnya), bukan auto-block.
- **Mode gas (full auto):** boleh, tapi wajib banner merah + kill switch selalu terlihat.
- **Secret:** AES-256-GCM at-rest, key dari env server, **tidak pernah** dikirim ke frontend sebagai plaintext, otomatis diredact di log/event/audit.
- **Budget guard:** meski user bilang tanpa batas waktu/biaya, tambahkan warning di 80% aksi + auto-pause kalau 5 menit tanpa progres (bukan batas keras) + ringkasan biaya token di akhir misi.

---

## 8. Yang JANGAN dikerjakan (sudah diputuskan user = tidak perlu)

- Billing/kredit/langganan/markup/rate limit (Cuda gratis, BYOE)
- Prompt library (diganti skills)
- Endpoint publik OpenAI-compatible (API internal saja)
- Scraper Instagram/TikTok (user menolak)
- Mode sementara / compare mode 2 model / multi-tenant (ditunda)
- MCP, marketplace plugin, multi-agent swarm → **v2**, jangan di v1 (tapi siapkan fondasi: role model + shared workspace + A2A event)
- Jangan migrasi data dari `masbraw-chat` lama (user bilang tidak perlu)
- Jangan pakai footer/credit "Cuda by ..." di UI (user minta tanpa keterangan, fokus ke aplikasi)

---

## 9. Aset yang SUDAH ada (jangan dibuat ulang)

- `mockups/cuda-agent-desktop.jpg`, `cuda-agent-mobile.jpg`, `cuda-ai-desktop.jpg` — acuan visual final
- `docs/DECISIONS.md` — 262 keputusan produk
- `questionnaire/` — kuesioner interaktif (kalau user mau tanya lagi, pakai ini)
- `site/` — SSG-lite halaman dokumen (plan/riset/keputusan/mockup), serve port 9400

---

## 10. Mulai dari mana (aksi pertama kamu)

1. `git clone https://github.com/Xiaochown/cuda.git && cd cuda`
2. Baca 7 dokumen di §2 (boleh paralel)
3. Setup environment sesuai `docs/SETUP_LAPTOP.md` (Node 22, git, gh, Playwright; **WSL2 sangat disarankan**)
4. Minta ke user **satu** `base_url` + `api_key` OpenAI-compatible untuk testing → simpan di `.env` (jangan commit)
5. Kerjakan **TASKS.md P0-1** sampai selesai, commit, lanjut P0-2, dst.
6. Setelah P1 selesai → lapor user dengan cara jalaninnya (`npm run dev`, URL lokal, apa yang bisa dicoba)

**Jangan berhenti di tengah untuk minta izin** kecuali salah satu kondisi di §5 terpenuhi.
