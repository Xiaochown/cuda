#!/usr/bin/env python3
"""Assemble ONE self-contained file: prompt + all docs, for handing to an AI agent."""
import pathlib, datetime

SRC = pathlib.Path("/root/cuda-ai")
OUT = SRC / "CUDA-COMPLETE.md"

HEADER = """# CUDA — SATU FILE LENGKAP (prompt + semua dokumen)

> **Untuk pemilik project:** kirim file ini ke AI agent kamu (Hermes / Claude Code / Codex / Cursor),
> lalu bilang: **"kerjakan file ini"**. Nggak perlu ngapa-ngapain lagi — semua instruksi, URL,
> aturan, dan checklist sudah ada di dalam file ini.

---

# ════ BAGIAN 0 · INSTRUKSI UNTUK AGENT (BACA INI DULU) ════

**Kamu adalah agent yang akan mengeksekusi project "Cuda" dari nol sampai MVP jalan.**
Kamu tidak punya konteks percakapan sebelumnya. File ini berisi SEMUA yang kamu butuhkan.
Baca Bagian 0 ini sampai habis, lalu Bagian 3 (setup), lalu Bagian 4 (checklist task), lalu mulai kerja.

## 0.1 Repo

```
https://github.com/Xiaochown/cuda        (PUBLIC — bisa diakses tanpa auth)
```

**Aksi pertama — ambil repo:**

```bash
git clone https://github.com/Xiaochown/cuda.git && cd cuda
```

Kalau `git clone` tidak bisa (tidak ada terminal), ambil dokumennya lewat raw URL ini:

```
https://raw.githubusercontent.com/Xiaochown/cuda/master/README.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/AGENT_BRIEF.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/PLAN.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/TASKS.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/DECISIONS.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/RESEARCH.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/SETUP_LAPTOP.md
https://raw.githubusercontent.com/Xiaochown/cuda/master/docs/ANSWERS.md
```

Kalau kamu tidak punya terminal sama sekali (agent web/chat): kamu **tidak bisa** membangun project ini —
kamu hanya bisa me-review. Laporkan itu ke user dan berhenti.

## 0.2 Urutan baca

1. **Bagian 2** (aturan keras) — wajib, jangan dilanggar
2. **Bagian 3** (setup environment) — kerjakan perintahnya
3. **Bagian 4** (checklist 38 task) — ini pekerjaanmu, kerjakan berurutan
4. **Bagian 5** (keputusan produk LOCKED) — sumber kebenaran kalau ada keraguan
5. **Bagian 6** (rencana teknis lengkap) — arsitektur, event protocol, data model, token desain, route
6. **Bagian 7** (brief lengkap) — guardrail keamanan & definition of done
7. **Bagian 8–9** — riset & jawaban mentah (referensi saja, jangan diubah)

## 0.3 Aturan keras (ringkasan — detail di Bagian 2)

1. **BYOE** — Cuda TIDAK menyediakan model. Semua LLM/search/image pakai `base_url` + `api_key` milik user.
   **Jangan** bikin billing, kredit, markup, kuota, atau rate limit. **Jangan** hardcode API key apa pun.
2. **Local-first + desktop-first** — SQLite lokal + IndexedDB browser, PWA, nanti di-package jadi software desktop.
3. **Skills via `/`** — kemampuan = file `SKILL.md` dipanggil `/nama-skill`. **BUKAN** prompt library.
   Cuda boleh menulis skill baru sendiri setelah misi sukses.
4. **Cuda Agent = console 3-pane (Missions | Activity | Workspace), BUKAN chat.**
   Pisahkan *conversation stream* dari *activity stream*.
5. **Setiap aksi agent punya Receipt + Undo** (apa berubah + diff + izin yang dipakai + Undo git-based).

## 0.4 Cara kerja

- **Autonomi tinggi.** User ini gaya "gas" — dia tidak mau ditanya tiap langkah. Kalau ada keputusan kecil,
  pilih default yang paling sesuai **Bagian 5 (DECISIONS)** dan catat pilihanmu di commit message.
- **Tanya HANYA kalau:** (a) butuh kredensial/API key, (b) ada konflik nyata antar dokumen,
  (c) mau menghapus/mengubah data user, (d) mau deploy ke akun milik user.
- **Satu task = satu commit.** Centang checkbox di `TASKS.md` tiap task selesai.
- **Commit message:** Conventional Commits (`feat(ai): ...`, `fix(agent): ...`, `chore: ...`).
- **Bahasa:** kode/komentar/UI **Inggris**; laporan ke user **Bahasa Indonesia casual**.
- **Jangan klaim "sudah jalan" tanpa bukti.** Jalankan test / `curl -o /dev/null -w '%{http_code}'` / screenshot.
  Kalau gagal, laporkan apa adanya — jangan mengarang hasil.

## 0.5 Yang dibutuhkan dari user (tanya sekali di awal)

1. **Satu `base_url` + `api_key`** OpenAI-compatible untuk testing → simpan di `.env` (**JANGAN commit**).
2. **Login Vercel** (`npx vercel login`) — hanya saat mau deploy web. Kalau belum ada, tunda deploy.
3. Konfirmasi kalau mau pakai **WSL2** (sangat disarankan, lihat Bagian 3).

## 0.6 Definition of Done

**Per task:** kode jalan + test lulus (kalau ada logika) + checkbox `TASKS.md` dicentang + commit.

**Per phase (P0–P3):**
- `npm run build` bersih, `npm run test` hijau
- Semua route di Bagian 6 §10 balas 200 (curl)
- Cuda AI: chat streaming dengan provider user, thread tersimpan, artifact bisa di-publish
- Cuda Agent: satu misi end-to-end menghasilkan **file nyata** di `workspaces/<mission-id>/`,
  timeline terisi, permission card muncul, receipt + undo jalan
- **Test keamanan sandbox WAJIB lulus:** path traversal (`../../etc/passwd`), command injection
  (`;`, `&&`, backtick), symlink escape, resource bomb → semua ditolak/di-cap
- Layout tidak overflow di layar HP

## 0.7 Urutan fase

```
P0 (Hari 1–2)   Fondasi: monorepo, packages/core (events, tools, router, skills), Prisma schema, seed skills
P1 (Hari 3–6)   Cuda AI: shell UI, streaming, thread, projects, composer, skills UI, artifacts, memory, export
P2 (Hari 7–11)  Cuda Agent: agent-node, orchestrator, event bus, sandbox, tools, permission, budget, checkpoint, receipt, skill generator, cron
P3 (Hari 12–14) UI console 3-pane, timeline, permission card, workspace viewer, plan compare, mobile/PWA, deploy
```

User memutuskan: **Cuda AI diselesaikan dulu**, baru Cuda Agent. Target MVP **2 minggu**.

## 0.8 Mulai sekarang

1. `git clone https://github.com/Xiaochown/cuda.git && cd cuda`
2. Setup environment (Bagian 3)
3. Minta `base_url` + `api_key` ke user → `.env`
4. Kerjakan **TASKS P0-1** → commit → P0-2 → dst (Bagian 4)
5. Setelah P1 selesai: lapor user dengan cara menjalankannya (`npm run dev`, URL lokal, apa yang bisa dicoba)

**Jangan berhenti di tengah untuk minta izin** kecuali kondisi di §0.4 terpenuhi.

---
---

# ════ BAGIAN 1 · REPO & URL ════

| Item | URL |
|---|---|
| Repo (public) | https://github.com/Xiaochown/cuda |
| Prompt agent | https://github.com/Xiaochown/cuda/blob/master/PROMPT.md |
| Prompt AI web | https://github.com/Xiaochown/cuda/blob/master/PROMPT-PUBLIC.md |
| Brief | https://github.com/Xiaochown/cuda/blob/master/AGENT_BRIEF.md |
| Checklist task | https://github.com/Xiaochown/cuda/blob/master/TASKS.md |
| Plan v2 | https://github.com/Xiaochown/cuda/blob/master/PLAN.md |
| Keputusan (262 jawaban) | https://github.com/Xiaochown/cuda/blob/master/docs/DECISIONS.md |
| Riset | https://github.com/Xiaochown/cuda/blob/master/docs/RESEARCH.md |
| Setup laptop | https://github.com/Xiaochown/cuda/blob/master/docs/SETUP_LAPTOP.md |
| Mockup | `mockups/` di repo (3 gambar) |

---
---

# ════ BAGIAN 2 · ATURAN KERAS (jangan dilanggar) ════

1. **BYOE — Bring Your Own Everything.** Cuda **tidak menyediakan model**. Semua LLM/search/image
   lewat `base_url` + `api_key` milik user. **Jangan** bikin billing, kredit, markup, kuota, atau
   rate limit. **Jangan** hardcode API key apa pun ke repo.
2. **Local-first + desktop-first.** Data di SQLite lokal + IndexedDB browser. PWA installable.
   Nanti di-package jadi software desktop — jangan pakai fitur yang cuma jalan di cloud/Vercel.
3. **Skills, BUKAN prompt library.** Kemampuan dipanggil dengan `/nama-skill`. Skill = `SKILL.md`
   (frontmatter: name, description, triggers, tools, version + body). Cuda boleh **menulis skill baru
   sendiri** setelah misi sukses.
4. **Pisahkan conversation stream dari activity stream.** Cuda Agent = **console 3-pane**, BUKAN chat.
5. **Setiap aksi punya Receipt + Undo.** Aksi agent (tulis file, terminal, git, deploy, kirim pesan)
   wajib menghasilkan struk: apa berubah + diff + izin yang dipakai + tombol Undo (git-based).

## Yang JANGAN dikerjakan (user sudah bilang tidak perlu)

- Billing / kredit / langganan / markup / rate limit
- Prompt library (diganti skills)
- Endpoint publik OpenAI-compatible (API internal saja)
- Scraper Instagram / TikTok (user menolak)
- Mode sementara, compare mode 2 model, multi-tenant (ditunda)
- MCP, marketplace plugin, multi-agent swarm → **v2** (tapi siapkan fondasi: role model +
  shared workspace + A2A event)
- Migrasi data dari `masbraw-chat` lama (user bilang tidak perlu)
- Footer/credit "Cuda by ..." di UI (user minta tanpa keterangan)

## Guardrail keamanan (wajib diimplementasi)

- **Sandbox v1 tanpa Docker:** workspace per-misi (`workspaces/<id>/`), path-traversal guard,
  command allowlist, timeout per aksi, rlimit (CPU/mem), output cap, env bersih.
- **Akses folder:** default hanya workspace misi; lebih luas **hanya** kalau user setujui per-misi
  (tercatat di audit).
- **`sudo`: default OFF.** Bisa dinyalakan di Settings → Security dengan peringatan eksplisit +
  konfirmasi ketik ulang. Semua pemakaian sudo masuk audit log + muncul sebagai kartu merah di timeline.
- **Command berbahaya** (`rm -rf /`, `dd`, `curl|bash`, `chmod 777`, `mkfs`, fork bomb):
  **konfirmasi kedua** (user ketik ulang perintahnya), bukan auto-block.
- **Mode gas (full auto):** boleh, tapi wajib banner merah + kill switch selalu terlihat.
- **Secret:** AES-256-GCM at-rest, key dari env server, **tidak pernah** dikirim ke frontend sebagai
  plaintext, otomatis diredact di log/event/audit.
- **Budget guard:** meski user bilang tanpa batas waktu/biaya, tambahkan warning di 80% aksi +
  auto-pause kalau 5 menit tanpa progres (bukan batas keras) + ringkasan biaya token di akhir misi.

---
"""

FOOTER = """
---
---

# ════ SELESAI ════

Semua yang kamu butuhkan sudah ada di file ini + repo `https://github.com/Xiaochown/cuda`.

**Langkah pertamamu sekarang:** `git clone https://github.com/Xiaochown/cuda.git && cd cuda`

Lalu kerjakan **TASKS P0-1** (lihat Bagian 4). Satu task = satu commit.
Lapor ke user dalam Bahasa Indonesia casual tiap phase selesai.
"""

SECTIONS = [
    ("BAGIAN 3 · SETUP ENVIRONMENT (WAJIB — WSL2 + Node 22 + gh)", "docs/SETUP_LAPTOP.md"),
    ("BAGIAN 4 · CHECKLIST 38 TASK (INI PEKERJAANMU)", "TASKS.md"),
    ("BAGIAN 5 · KEPUTUSAN PRODUK LOCKED — sumber kebenaran (262 jawaban)", "docs/DECISIONS.md"),
    ("BAGIAN 6 · RENCANA TEKNIS LENGKAP (arsitektur, event protocol, data model, token desain, route)", "PLAN.md"),
    ("BAGIAN 7 · BRIEF LENGKAP (guardrail + definition of done detail)", "AGENT_BRIEF.md"),
    ("BAGIAN 8 · RISET (referensi — kenapa desainnya begini)", "docs/RESEARCH.md"),
    ("BAGIAN 9 · JAWABAN MENTAH 262 PERTANYAAN (referensi ground-truth)", "docs/ANSWERS.md"),
]

parts = [HEADER]
for title, rel in SECTIONS:
    p = SRC / rel
    body = p.read_text().strip()
    parts.append(f"\n---\n---\n\n# ════ {title} ════\n\n> _Sumber asli: `{rel}` di repo_\n\n{body}\n")

parts.append(FOOTER)
content = "\n".join(parts)
OUT.write_text(content)

n_lines = content.count("\n") + 1
print(f"wrote {OUT}")
print(f"  size   : {len(content)/1024:.1f} KB")
print(f"  lines  : {n_lines}")
print(f"  est tok: ~{len(content)//4} tokens")
