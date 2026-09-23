# CUDA — SATU FILE LENGKAP (prompt + semua dokumen)

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


---
---

# ════ BAGIAN 3 · SETUP ENVIRONMENT (WAJIB — WSL2 + Node 22 + gh) ════

> _Sumber asli: `docs/SETUP_LAPTOP.md` di repo_

# SETUP LAPTOP — environment buat ngembangin Cuda

Target: laptop Windows user (`zie`). **Wajib pakai WSL2** — Cuda Agent butuh shell Linux, git, Playwright, dan `bash`. Di PowerShell native, tool `shell`/`python` bakal bermasalah.

---

## A. Wajib: WSL2 + Ubuntu

Buka **PowerShell as Administrator**:

```powershell
wsl --install -d Ubuntu
# restart kalau diminta, lalu buka Ubuntu dari Start Menu, bikin username + password
```

Di dalam Ubuntu (WSL):

```bash
sudo apt update && sudo apt install -y build-essential git curl ripgrep ffmpeg \
  python3 python3-pip unzip
```

**Node 22** (jangan pakai Node bawaan apt — terlalu tua):

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v   # harus >= v22
npm i -g npm@latest
```

**GitHub CLI:**

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
gh auth login    # pilih GitHub.com → HTTPS → login via browser/token (akun Xiaochown)
gh auth status
```

**Clone repo:**

```bash
cd ~ && git clone https://github.com/Xiaochown/cuda.git && cd cuda
```

> Tip: taruh project di filesystem WSL (`~/cuda`), **bukan** di `/mnt/c/...` — jauh lebih cepat dan tidak bikin masalah permission/symlink.

---

## B. Opsional tapi disarankan

**Playwright (tool browser Cuda Agent):**

```bash
npx playwright install --with-deps chromium
```

**pm2 (biar agent-node jalan terus):**

```bash
sudo npm i -g pm2
```

**Tailscale (biar HP user bisa akses app dari luar rumah):**

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip -4      # catat IP-nya, dipakai buat akses dari HP
```

**Akses folder Windows dari WSL** (kalau file ada di `C:\`): `cd /mnt/c/Users/zie/...`

---

## C. Env untuk Cuda

Bikin `.env` di root repo (**jangan di-commit** — sudah masuk `.gitignore`):

```bash
cat > .env <<'EOF'
# Provider untuk testing (BYOE — pakai key milik user)
TEST_PROVIDER_LABEL=TeamORouter
TEST_PROVIDER_BASE_URL=https://api.teamorouter.com/v1
TEST_PROVIDER_API_KEY=sk-xxxxx

# Secret untuk enkripsi kredensial user (AES-256-GCM) — generate:
#   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
CUDA_SECRET_KEY=isi-64-hex-char

# Agent node
AGENT_NODE_PORT=9400
AGENT_NODE_HMAC_SECRET=ganti-dengan-random-string
EOF
chmod 600 .env
```

**Minta user** kasih satu `base_url` + `api_key` OpenAI-compatible untuk testing (bisa dari provider apa pun yang dia punya).

---

## D. Jalankan

```bash
npm install                 # dari root (npm workspaces)
npm run dev                 # web  → http://localhost:3000
npm run dev:agent           # agent-node → http://localhost:9400
```

Kalau mau HP bisa akses (mis. buat uji mobile):

```bash
npm run dev -- --hostname 0.0.0.0
# lalu dari HP buka http://<tailscale-ip>:3000
```

---

## E. Verifikasi setup

```bash
node -v                 # >= v22
git -v
gh auth status          # logged in
npm -v                  # 10+
npx playwright --version
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9400/health   # 200 setelah agent-node jalan
```

---

## F. Pitfall yang sudah diketahui (hemat waktu)

1. **Jangan install project di `/mnt/c/...`** — `npm install` lambat dan symlink rusak. Pakai `~/cuda`.
2. **Node < 22 bikin gagal build Next.js 16** — pakai NodeSource 22 seperti di atas.
3. **`npm audit fix --force` jangan dijalankan** — merusak dependency tree.
4. **Playwright di WSL butuh `--with-deps`** untuk library sistem (kalau tidak, Chromium gagal start).
5. **Port < 1024 butuh root** di WSL — pakai 3000 (web) dan 9400 (agent-node).
6. **Kalau `gh` belum login**, clone repo private akan gagal dengan "repository not found" (pesan menyesatkan — itu masalah auth, bukan repo hilang).
7. **Windows Firewall** bisa memblok akses dari HP ke port WSL — pakai Tailscale (cara paling gampang) atau tambahkan rule inbound.
8. **Deploy Vercel** butuh login sendiri: `npx vercel login` lalu `npx vercel --prod` dari `apps/web`. Repo GitHub sudah connect-able untuk auto-deploy.


---
---

# ════ BAGIAN 4 · CHECKLIST 38 TASK (INI PEKERJAANMU) ════

> _Sumber asli: `TASKS.md` di repo_

# TASKS — Cuda MVP (38 task, 14 hari)

> 38 task ini konsolidasi dari 40 langkah di `PLAN.md §11`.
> Update checkbox jadi `[x]` tiap task selesai. Satu task = satu commit.
> Objective + acceptance criteria ada di tiap task. Kalau ada penyimpangan, tulis catatan di bawah task.

**Legenda:** `[ ]` belum · `[~]` sedang dikerjakan · `[x]` selesai · `[!]` diblokir (tulis alasannya)

---

## P0 — Fondasi (Hari 1–2)

### [ ] P0-1 · Bootstrap monorepo
**Objective:** repo jalan dengan struktur npm workspaces.
**Files:** `package.json`, `tsconfig.base.json`, `.editorconfig`, `.gitignore`, `apps/`, `packages/`
**Acceptance:** `npm install` sukses dari root; `packages/core` bisa di-import dari `apps/web`; `npm run build` jalan (walau kosong).
**Commit:** `chore: bootstrap monorepo`

### [ ] P0-2 · Kontrak event agent (`packages/core/src/events.ts`)
**Objective:** union type `AgentEvent` (lihat `PLAN.md §5`) + validator Zod.
**Acceptance:** test unit memvalidasi **setiap varian** event (valid lolos, field kurang ditolak). Tulis test dulu (RED) baru implementasi (GREEN).
**Commit:** `feat(core): agent event protocol + zod schemas`

### [ ] P0-3 · Tool registry (`packages/core/src/tools.ts`)
**Objective:** registry tool: nama, deskripsi, skema argumen (Zod), permission default (always/ask/never).
**Acceptance:** 18 tool dari `PLAN.md §9` terdaftar; test memastikan tiap tool punya skema + permission valid.
**Commit:** `feat(core): tool registry`

### [ ] P0-4 · LLM router BYOE (`packages/core/src/router.ts`)
**Objective:** panggil provider milik user (`base_url` + `api_key`), streaming, fallback chain.
**Acceptance:** test dengan mock fetch: 200 → stream normal; 400 → fallback ke provider berikutnya; 429 → fallback; timeout → fallback; semua gagal → error yang jelas. **Tidak ada key hardcoded.**
**Commit:** `feat(core): user-provider router with fallback chain`

### [ ] P0-5 · Skill engine (`packages/core/src/skills.ts`)
**Objective:** parser `SKILL.md` (frontmatter: name, description, triggers, tools, version) + matcher trigger + renderer untuk slash command.
**Acceptance:** test: parse skill valid, tolak frontmatter rusak, match trigger dari deskripsi, skill dengan tools terdaftar otomatis minta permission.
**Commit:** `feat(core): skill engine`

### [ ] P0-6 · Prisma schema + migration
**Objective:** model di `PLAN.md §6` (User, Provider, SearchCfg, Workspace, Thread, Folder, Message, Artifact, ArtifactVer, MemoryFact, Skill, Mission, MissionStep, AgentEventRow, Permission, ToolPerm, Checkpoint, Receipt, Secret, Schedule, Webhook).
**Acceptance:** `prisma migrate dev` sukses di SQLite; index `AgentEventRow(missionId, seq)` ada; FTS5 untuk thread + memory dibuat via raw SQL migration.
**Commit:** `feat(db): schema v2 + migration init`

### [ ] P0-7 · Seed 6 skill bawaan
**Objective:** `deep-research`, `scrape-to-dataset`, `build-and-deploy-site`, `monitor-and-alert`, `osint-dossier`, `doc-pipeline`.
**Acceptance:** `npm run seed` mengisi tabel Skill; skill bisa dibaca & dipanggil dari core.
**Commit:** `feat(core): seed default skills`

---

## P1 — Cuda AI (Hari 3–6)

### [ ] P1-1 · Shell UI + design token
**Objective:** layout sidebar + area thread, token dari `PLAN.md §2`, i18n (EN default + switch ID), tema ikut sistem + light mode.
**Acceptance:** halaman `/ai` render; ganti tema jalan; teks ikut bahasa yang dipilih.
**Commit:** `feat(ai): app shell + design tokens + i18n`

### [ ] P1-2 · `/api/chat` SSE
**Objective:** route handler streaming ke provider user (pakai router P0-4).
**Acceptance:** `curl -N` ke `/api/chat` mengeluarkan token bertahap; stop request memutus stream; error provider tampil rapi.
**Commit:** `feat(ai): streaming chat endpoint`

### [ ] P1-3 · Thread UI
**Objective:** render streaming, markdown + syntax highlight + tabel + Mermaid, stop, regenerate, continue, rating 👍👎, edit → fork cabang + navigasi versi.
**Acceptance:** pesan panjang ter-render benar; fork menghasilkan cabang baru yang bisa dinavigasi `‹ 2/3 ›`.
**Commit:** `feat(ai): message rendering + branching`

### [ ] P1-4 · Sidebar & persistensi thread
**Objective:** list thread + grup waktu (Today/7 days/30 days/Older), folder, pin, arsip, hapus massal, rename, search FTS5 + semantik.
**Acceptance:** refresh halaman → data tetap; search menemukan thread lama; bulk delete jalan.
**Commit:** `feat(ai): thread sidebar + persistence + search`

### [ ] P1-5 · Projects / Ruang Kerja
**Objective:** project dengan custom instruction permanen + file knowledge + scope memory.
**Acceptance:** thread di dalam project memakai instruksi project; file project bisa dirujuk.
**Commit:** `feat(ai): projects with custom instructions`

### [ ] P1-6 · Composer lengkap
**Objective:** attach (gambar/PDF/DOCX/XLSX/CSV/kode ≤50MB) + OCR, model picker dari provider user, slash `/` skill, persona chips, toggle Web Search (multi-engine) / Deep Research / Image Gen / STT / TTS.
**Acceptance:** upload PDF scan → teks terbaca (OCR); slash command memunculkan daftar skill; STT & TTS bahasa Indonesia jalan.
**Commit:** `feat(ai): composer with attachments, skills, voice`

### [ ] P1-7 · Settings provider & keamanan
**Objective:** CRUD provider (base_url/key/model, test koneksi), fallback chain, search engine config, tema, bahasa, matriks permission, keamanan (sudo toggle + peringatan).
**Acceptance:** tombol "Test connection" mengembalikan daftar model dari `/models`; key disimpan terenkripsi dan **tidak pernah** tampil plaintext setelah disimpan.
**Commit:** `feat(settings): providers, permissions, security`

### [ ] P1-8 · Skills UI
**Objective:** halaman `/skills`: list, edit, buat baru, enable/disable, versioning + rollback, generate dari template.
**Acceptance:** bikin skill baru → langsung bisa dipanggil `/` di composer.
**Commit:** `feat(skills): manager UI`

### [ ] P1-9 · Artifacts
**Objective:** entitas artifact + versioning tak terbatas, deteksi blok besar → **tanya dulu** sebelum dibuka, render sandboxed iframe (postMessage bridge), targeted edit, edit manual, download, publish `/share/a/[slug]` + cabut, halaman galeri.
**Acceptance:** artifact ter-render di iframe `sandbox="allow-scripts"` tanpa akses cookie/origin; publish → link publik jalan; cabut → 404.
**Commit:** `feat(ai): artifacts with versioning + publish`

### [ ] P1-10 · Memory
**Objective:** extractor fakta otomatis, halaman `/memory` CRUD, scope gabungan (global/workspace/thread), penjelasan "kenapa diingat" + sumber, tanpa kadaluwarsa otomatis, import riwayat dari ChatGPT/Hermes.
**Acceptance:** fakta baru muncul di `/memory` dengan sumbernya; hapus fakta → tidak dipakai lagi di konteks; import file export ChatGPT berhasil.
**Commit:** `feat(ai): transparent memory + history import`

### [ ] P1-11 · Export & share
**Objective:** export PDF berbrand + MD + JSON, share thread (harus klik Publish), meter token/biaya per thread, keyboard shortcuts + halaman cheat sheet, onboarding wizard.
**Acceptance:** PDF hasil export rapi; share link hanya aktif setelah Publish.
**Commit:** `feat(ai): export, sharing, cost meter, onboarding`

---

## P2 — Cuda Agent (Hari 7–11)

### [ ] P2-1 · Service agent-node
**Objective:** Fastify + `ws`, auth HMAC dari web, `/health`, direktori `workspaces/`.
**Acceptance:** `curl /health` balas ok; koneksi WS tanpa token valid ditolak.
**Commit:** `feat(agent): node service skeleton`

### [ ] P2-2 · Orchestrator
**Objective:** goal → planner (output JSON tervalidasi Zod) → executor per step → replan kalau gagal (retry 3x → eskalasi).
**Acceptance:** test dengan mock LLM: plan dibuat, langkah dieksekusi berurutan, kegagalan memicu replan lalu eskalasi.
**Commit:** `feat(agent): orchestrator plan/execute/replan`

### [ ] P2-3 · Event bus + replay
**Objective:** semua event append-only ke `AgentEventRow`, broadcast via WS, endpoint replay, **fork misi dari langkah N**.
**Acceptance:** misi selesai → event bisa di-replay urut; fork dari langkah N membuat misi baru yang melanjutkan dari state itu.
**Commit:** `feat(agent): append-only event bus + replay + fork`

### [ ] P2-4 · Sandbox (WAJIB lolos test negatif)
**Objective:** workspace per-misi, path-traversal guard, command allowlist, timeout, rlimit, output cap, env bersih.
**Acceptance:** test negatif **semua ditolak**: `../../etc/passwd`, `cat /etc/shadow`, `ls; rm -rf x`, `` `whoami` ``, symlink keluar workspace, `yes > /dev/full`, fork bomb. Test positif: perintah normal di workspace jalan.
**Commit:** `feat(agent): workspace sandbox + guards`

### [ ] P2-5 · Tool v1
**Objective:** `fs`, `shell`, `python`, `web_search` (multi-engine), `web_fetch`, `browser` (Playwright), `document`, `data`, `sql`, `rag`, `git`, `notify`, `monitor`, `osint`.
**Acceptance:** tiap tool punya test unit; tool yang butuh izin memicu permission request; hasil tool tervalidasi sebelum dipakai langkah berikutnya.
**Commit:** `feat(agent): tool implementations`

### [ ] P2-6 · Permission engine
**Objective:** request/response, auto-pause 5 menit, deny → agent tanya alternatif, matriks per tool (always/ask/never), mode paranoid, mode gas, sudo guard (default OFF), konfirmasi kedua untuk command berbahaya.
**Acceptance:** test: izin ditolak → agent menawarkan alternatif (bukan berhenti diam); mode paranoid → semua aksi tanya; sudo tanpa opt-in → ditolak + tercatat.
**Commit:** `feat(agent): permission engine + approval gates`

### [ ] P2-7 · Budget, limits, kill switch
**Objective:** hitung langkah (150) & aksi (100), warning 80%, auto-pause kalau 5 menit tanpa progres, ringkasan biaya token, tombol Stop yang benar-benar membatalkan tool in-flight + membuang antrean + menyimpan checkpoint.
**Acceptance:** test: budget 80% memicu warning; Stop menghentikan proses anak yang sedang jalan (tidak ada zombie).
**Commit:** `feat(agent): budget guards + kill switch`

### [ ] P2-8 · Checkpoint + Receipt + Undo
**Objective:** git init per workspace, commit per langkah (simpan 20, auto-prune), restore, receipt untuk tiap aksi (diff + izin + undoable), tombol Undo.
**Acceptance:** test: restore mengembalikan file ke state checkpoint; undo membalikkan satu aksi dan tercatat.
**Commit:** `feat(agent): checkpoints, receipts, undo`

### [ ] P2-9 · Skill generator
**Objective:** setelah misi sukses, Cuda mengusulkan `SKILL.md` baru (dari langkah yang dikerjakan) → event `skill.learned` → bisa langsung dipanggil `/`.
**Acceptance:** misi sukses menghasilkan usulan skill; setelah diterima, skill muncul di `/skills` dan bisa dipanggil.
**Commit:** `feat(agent): self-extending skills`

### [ ] P2-10 · Schedule, webhook, monitoring
**Objective:** cron misi, trigger webhook masuk, tool monitoring uptime + change detection + alert (notify Telegram/WA/webhook).
**Acceptance:** misi terjadwal jalan sesuai cron; webhook memicu misi; perubahan halaman terdeteksi → alert terkirim.
**Commit:** `feat(agent): scheduling, webhooks, monitoring`

---

## P3 — UI Agent + polish + deploy (Hari 12–14)

### [ ] P3-1 · Console 3-pane
**Objective:** Missions list + Activity + Workspace, status bar (Run/Pause/Stop, autonomy Suggest/Draft/Execute, meter `18/100`).
**Acceptance:** layout tidak overflow di layar 1280px dan di HP; status bar selalu terlihat.
**Commit:** `feat(agent-ui): three-pane console`

### [ ] P3-2 · Activity timeline
**Objective:** render **semua** varian `AgentEvent` jadi kartu: step, tool call (expandable args+hasil), thought, receipt+undo, permission, escalation, skill.learned; current step pinned; filter severity/tipe.
**Acceptance:** setiap varian event punya komponen sendiri (test snapshot); pinned step ikut saat scroll.
**Commit:** `feat(agent-ui): activity timeline`

### [ ] P3-3 · Permission card
**Objective:** kartu "PERMISSION NEEDED" dengan dampak + tingkat risiko + countdown 5 menit + tombol Setujui/Edit/Tolak.
**Acceptance:** countdown jalan; lewat 5 menit → misi auto-pause; Tolak → agent menawarkan alternatif.
**Commit:** `feat(agent-ui): permission card`

### [ ] P3-4 · Workspace viewer
**Objective:** file tree, CodeMirror editor, diff view, live preview iframe, terminal xterm.js (attach PTY), browser view (screenshot stream).
**Acceptance:** file yang diubah agent muncul di tree; diff menampilkan perubahan; terminal bisa kirim perintah dan melihat output.
**Commit:** `feat(agent-ui): workspace viewer`

### [ ] P3-5 · Board, plan compare, fork, mode diskusi
**Objective:** Board (kanban) misi, banding 2 rencana dengan tombol pilih, fork misi dari langkah N, mode diskusi (ngobrol tanpa eksekusi).
**Acceptance:** semua empat fitur bisa dipakai dan tercatat di event.
**Commit:** `feat(agent-ui): board, plan compare, fork, discussion mode`

### [ ] P3-6 · Deliverables + audit export
**Objective:** daftar serahan dengan tombol download / kirim Telegram / kirim WA / publish; export audit trail JSON + PDF.
**Acceptance:** file terkirim benar; audit PDF memuat semua aksi + izin + waktu.
**Commit:** `feat(agent-ui): deliverables + audit export`

### [ ] P3-7 · Mobile + PWA
**Objective:** Cuda Agent tab bar (Missions/Activity/Workspace/Deliverables) + sheet permission; Cuda AI 1 kolom + sheet artifact; PWA installable; offline read riwayat; mode lanskap.
**Acceptance:** installable di Android (Lighthouse PWA pass); tanpa internet riwayat masih terbaca.
**Commit:** `feat(pwa): mobile layouts + offline`

### [ ] P3-8 · Polish
**Objective:** light mode rapi, empty/error/loading state di semua layar, ilustrasi custom, suara notifikasi misi selesai, push browser, keyboard shortcut + cheat sheet.
**Acceptance:** tidak ada layar tanpa empty state; tidak ada error mentah yang bocor ke UI.
**Commit:** `polish: states, sounds, notifications, shortcuts`

### [ ] P3-9 · Deploy + CI/CD
**Objective:** web → Vercel (project `cuda`, auto-deploy dari GitHub); agent-node → jalan di laptop (pm2/systemd) port 9400; staging environment; GitHub Actions (lint+test+build); halaman status; help center; changelog.
**Acceptance:** URL Vercel hidup dan bisa dipakai dari HP; `/health` agent-node balas ok; CI hijau di PR.
**Commit:** `chore: deploy, CI/CD, docs`

### [ ] P3-10 · Load test + hardening
**Objective:** 10 misi paralel, rate limit internal, redaction log diverifikasi, smoke test end-to-end.
**Acceptance:** 10 misi jalan tanpa crash; tidak ada API key muncul di log/event/audit (grep bersih).
**Commit:** `test: load + hardening pass`

---

## Catatan penyimpangan

_(tulis di sini kalau ada task yang diubah/ditunda beserta alasannya)_


---
---

# ════ BAGIAN 5 · KEPUTUSAN PRODUK LOCKED — sumber kebenaran (262 jawaban) ════

> _Sumber asli: `docs/DECISIONS.md` di repo_

# CUDA — Decision Record (dari kuesioner 262 pertanyaan)

Sumber: `docs/ANSWERS.md` (jawaban mentah user, 262/262 terjawab, 23 Sep 2026).
Dokumen ini = hasil ekstraksi keputusan + flag konflik + capability map. **Plan v2 mengikuti dokumen ini.**

---

## 1. Lima pivot besar (ini yang mengubah arah project)

### Pivot #1 — Cuda itu **local-first client**, bukan SaaS gateway
Jawaban #191, #192, #200, #201, #165–#172: **gratis by default, user bawa base_url + API key sendiri (BYOE — Bring Your Own Everything)**.
Tidak ada model bawaan, tidak ada markup, tidak ada kuota, tidak ada rate limit dari sisi Cuda.
→ Konsekuensi: Cuda = *shell* (UI + agent engine + tools), bukan penyedia token. Infra biaya ≈ Rp0. Onboarding wajib punya **preset provider** + wizard input key.

### Pivot #2 — **Desktop-first**, mobile PWA, nanti jadi software
#219, #220, #228, #255, #57: desktop nomor 1, PWA di v1, target akhir = **software desktop + mobile app**.
→ Konsekuensi: arsitektur harus bisa dibungkus (Tauri/Electron) nanti. Storage **dua-duanya** (server SQLite + browser IndexedDB) karena #182 minta lokal + server.

### Pivot #3 — **Skills menggantikan Prompt Library**
#78, #80, #257, #163, #164: tidak ada prompt library; gantinya **skill yang dipanggil dengan `/`**, plus plugin & marketplace, dan **Cuda boleh bikin skill sendiri**.
→ Konsekuensi: butuh **Skill Engine** (SKILL.md + tool grants + trigger + versioning) sejak v1, bukan sekadar template prompt.

### Pivot #4 — **English-first, bilingual**
#7, #8, #12: bahasa utama Inggris, switch ke Indonesia; istilah UI pakai Inggris (Mission/Step/Permission/Receipt/Deliverables); tanpa footer/credit biar profesional; fokus app ke Cuda Agent.

### Pivot #5 — **Satu accent midnight-blue ala ChatGPT**, bukan dua warna
#6: hitam + biru midnight, "linear khas ChatGPT", **icon berwarna** (model/brand icons colorful).
→ Token diperbarui di §4. Skema dua-accent (biru/violet) dibatalkan.

---

## 2. Keputusan per bagian

**A. Brand** — Cuda (induk), Cuda AI + Cuda Agent. Tagline: *"Cuda for Simple Work. Cuda Agent for Deep Work, Autonomous."* Domain nanti (Vercel dulu). Logo monogram C. Maskot: nanti. Brand berdiri sendiri.

**B. Positioning** — publik (mahasiswa, remaja, pekerja, vibe coder, programmer, umum). Komersial + personal nanti. Target 1.000 user / 3 bulan. Pricing: nanti. Mode team/multi-user: **v1**. Offline/privasi khusus: tidak perlu.

**C. Scope** — P0–P4 dulu, **Cuda AI diselesaikan dulu** baru Agent. **MVP ≈ 2 minggu.** Deep Research: v1. STT+TTS: v1. Multi-sesi agent paralel: v1. Cron misi: v1. MCP: v2. Compare mode: tidak perlu. Playbook: terserah gue (kalau berguna). "3 fitur wajib" diserahkan ke gue (lihat §5).

**D. Stack** — Next.js 16, Tailwind 4 + komponen sendiri, ORM/state/monorepo/runtime: gue pilih (→ Prisma, Zustand+React Query, npm workspaces, Fastify). Chat SSE + Agent WebSocket. Zod: oke. Vitest + Playwright: oke. API publik OpenAI-compatible: **tidak**. Multi-tenant: nanti. i18n: framework. Monorepo **berdiri sendiri** (tidak gabung Meridian). Dev runtime: box ini.

**E. Infra** — Web → **Vercel**. Agent-node → box ini (lokal). DB → SQLite. Storage → lokal. Backup → GitHub. Budget → **$0**. Node down → tampil error. Queue → in-memory dulu, Redis menyusul. Monitoring → **log saja**. Log 30 hari. Disk → pakai drive lain (bukan rootfs 99%). Build → box ini.

**F. Cuda AI** — sidebar mengikuti mockup, jawaban **polos** (Claude-style), Projects/Ruang Kerja v1 + custom instruction, organisasi **folder**, search **full-text + semantik**, pin/arsip/hapus massal semua, Enter=kirim, draft sync, **skills via `/`**, persona chips generik (gue generate), attach semua tipe ≤50MB, **OCR perlu**, web search **multi-engine gratis (DuckDuckGo/Brave/Firecrawl) & user-configurable**, default ON, image gen via custom key (sunburst/flare/gpt-image-2.0), TTS+STT Indonesia, branching penting, continue-generating, rating, export PDF berbrand, share **harus klik Publish**, tanpa mode sementara.

**G. Artifact & Memory** — artifact **selalu tanya** sebelum dibuka, tipe bebas, JS sandbox bebas, **versioning tak terbatas**, targeted edit v1, publish link bisa dicabut, bisa diedit manual, **halaman galeri artifact**, memory boleh mengingat **semua**, halaman Memory CRUD, scope **gabungan** (global+workspace+thread), penjelasan "kenapa diingat" perlu, **tanpa kadaluwarsa otomatis**, **import riwayat ChatGPT/Hermes perlu**.

**H. Agent flow** — mulai misi dari form **atau** dari chat, **wajib tampilkan Rencana + approval**, setelah approve tetap tanya per aksi berisiko, **Board (kanban) perlu**, timeline **terbuka**, current-step pinned, estimasi **waktu saja**, retry **3x lalu eskalasi**, batas **150 langkah / 100 aksi / tanpa batas waktu / tanpa batas biaya**, agent **sangat boleh** bertanya balik, mode diskusi perlu, fork misi perlu, banding 2 rencana **perlu (dengan tombol)**, format serahan bebas, kirim hasil ke Telegram/WA boleh.

**I. Kontrol & Keamanan** — autonomy tergantung permission yang dikasih user; izin wajib untuk **hal sensitif saja**; **matriks izin per tool** perlu; izin **selalu tanya ulang** (tidak diingat); mode paranoid perlu; mode gas perlu; izin ditolak → agent **tanya alternatif**; kartu izin auto-pause **5 menit**; akses folder **boleh lebih luas bila perlu**; internet **bebas**; **sudo: BOLEH (flag risiko)**; command berbahaya → **tanya dulu**; log **diredact**; audit trail **exportable**; undo **git-based**; checkpoint: bebas; simpan **20 checkpoint**; network namespace per misi (saat ada Docker) perlu; data misi **permanen**; credential **boleh disimpan, terenkripsi, hanya user yang bisa lihat**.

**J. Tools** — sebanyak yang bisa dibuat. v1: browser Playwright, Firecrawl scraping, image gen, PDF/DOCX/XLSX, git + auto-push, deploy Vercel/GH Pages, kirim email/WA/Telegram, query SQL, RAG workspace, olah CSV/XLSX besar, convert file, monitoring uptime + alert, **OSINT (scam-hunt)**, simpan Playbook dari misi sukses, jalankan skrip/plugin custom, marketplace plugin. **Tidak**: scrape IG/TikTok.

**K. Model** — **semua dari base_url + key user** (tidak ada default provider, tidak ada urutan prioritas dari Cuda); user atur fallback sendiri; pesan error bebas; tanpa limit token; **BYO key wajib**; tidak expose API OpenAI-compatible; markup 10% *(hanya relevan kalau nanti jual token)*; tanpa model lokal; prompt caching opsional, **default off**.

**L. Data & Auth** — login bebas: Telegram/email/OAuth semua opsi (tidak ada yang wajib), **mode tamu perlu**, multi-device sync perlu, storage server+lokal, export semua data, hapus akun self-service, role admin, **tanpa batas gratis**, training/evaluasi → **tanya dulu**, enkripsi at-rest perlu, tanpa 2FA/timeout, share slug acak.

**M. Billing** — **gratis by default** (karena user bawa key sendiri). Tidak ada paket, invoice, referral, trial, rate limit. Kuota agent+chat digabung. (→ tidak ada pekerjaan billing di v1.)

**N. Desain** — tema **ikut sistem**, light mode v1, Inter + JetBrains Mono, density AI lega / Agent padat, animasi halus, suara notifikasi misi selesai, push browser, Lucide, ilustrasi/empty state custom, **onboarding wizard**, landing **lengkap + demo interaktif**, WCAG "seadanya", keyboard shortcut + cheat sheet, accent bisa diganti user, referensi visual bebas (ambil dari chatbot/web bagus).

**O. Mobile** — desktop prioritas #1 (dua-duanya), PWA v1, offline baca riwayat, tab bar Agent di HP (setuju), notif Telegram, tanpa swipe, font kecil, mode lanskap perlu, quick-share perlu, PWA cukup (native nanti).

**P. Integrasi** — tidak ada yang wajib, semua opsional. Meridian: belum. Migrasi masbraw-chat: tidak. Bot Telegram: perlu. WhatsApp: perlu. Kalender/Todoist: perlu. Webhook keluar: perlu. API key Cuda: perlu. **Cuda jadi tool Hermes**: perlu. MCP: beberapa yang berguna dulu. Pembayaran: nanti. Email laporan: tidak.

**Q. Ops** — maintainer: gue + user. CI/CD perlu. Staging perlu. Coverage "seadanya". Load test 10 misi paralel. Bug notif → Telegram. Halaman status perlu. Help center perlu. Changelog perlu. Backup harian.

**R. Roadmap** — 6 bulan: semua fitur AI terbaru. SaaS + personal. Cuda Teams: ya. Enterprise: belum. Desktop+mobile app: nanti. Marketplace: perlu. Belajar dari riwayat + bikin skill sendiri: perlu. **Multi-agent collaboration: SANGAT perlu**. Agent-as-a-service: belum paham (nanti dijelaskan). Milestone **2–3 bulan**. Batasan keras (haram): belum ada.

---

## 3. Flag: konflik & hal yang perlu gue putuskan/dikonfirmasi

| # | Isu | Kenyataan | Usul gue |
|---|---|---|---|
| F1 | **sudo boleh** (#137) + command berbahaya "tanya dulu" (#138) + akses folder lebih luas (#135) | Kombinasi ini berbahaya: agent bisa mengubah sistem user | Default **sudo OFF** + wajib nyalakan sadar di Settings (dengan peringatan), command berbahaya butuh **konfirmasi kedua** (ketik ulang), semua sudo masuk audit log. Tetap hormati pilihan user, tapi ada guard. |
| F2 | **150 langkah / 100 aksi / tanpa batas waktu & biaya** (#117–#120) | Misi bisa jalan lama & nyangkut | Tetap seperti diminta, tapi: warning di 80% budget aksi, tombol "lanjutkan" eksplisit, auto-pause kalau 5 menit tidak ada progres (bukan batas keras). |
| F3 | **"box ini"** (#53, #56, #68) vs **"drive C"** (#67) | Ambiguitas: box Linux (tempat gue jalan sekarang) atau laptop Windows | Bangun di **box Linux ini** (bisa langsung kerja), kode cross-platform, nanti di-package jadi software desktop (Tauri) yang jalan di Windows. Kalau mau di laptop Windows, butuh sesi Hermes di mesin itu. |
| F4 | **Gratis total + BYO key** (#191, #200) tapi **markup 10%** (#176) | Konflik | Baca sebagai: v1 gratis total; markup 10% hanya kalau nanti Cuda jual token sendiri. Tidak ada pekerjaan billing di v1. |
| F5 | **Tidak expose API OpenAI-compatible** (#49) tapi **perlu API key Cuda untuk app lain** (#236) | Konflik | API internal Cuda (untuk bot Telegram/WA/webhook/plugin), bukan endpoint publik multi-provider. |
| F6 | **Disk rootfs 99% penuh** (#67: "pakai drive C aja dulu") | Kalau build di box ini, butuh ruang | Bersihkan/relokasi: pindahkan artefak besar ke `/sdcard` (drive HP) atau hapus project lama; atau build di laptop. Butuh ~5 GB. |
| F7 | **Target 1.000 user / 3 bulan** + **tanpa model bawaan** | User baru harus punya API key sendiri → friksi tinggi | Onboarding wizard + **preset provider** (OpenAI/Anthropic/Gemini/OpenRouter/TeamORouter/Ldrcloud/Ollama) + mode tamu untuk coba UI dulu. |
| F8 | **Multi-agent "sangat perlu"** (#258) tapi MVP 2 minggu | Scope besar | Fondasi v1: event protocol + shared workspace + role model disiapkan; swarm penuh di v2. |

---

## 4. Design token (revisi sesuai #6)

```css
/* base — hitam netral + midnight blue, idiom ChatGPT */
--bg:#0d0d0d;          /* canvas */
--bg-elev:#141517;     /* panel */
--surface:#1a1c1f;     /* kartu */
--surface-2:#22252a;   /* input / hover */
--border:#2b2f36; --border-strong:#3a3f47;
--text:#ececf1; --text-dim:#a0a6b0; --text-mute:#6e747e;
/* accent tunggal */
--accent:#2563eb; --accent-hover:#3b82f6; --accent-soft:#1e293b;
/* status (agent) */
--run:#f5a524; --ok:#22c55e; --err:#ef4444; --wait:#38bdf8; --idle:#6b7280;
/* ikon berwarna: model/brand icon full-color (bukan monokrom) */
--r-sm:6px; --r:10px; --r-lg:14px;
--font:Inter; --mono:"JetBrains Mono",ui-monospace;
```
Aturan: light mode = `#ffffff / #f7f7f8 / #e5e5e5` dengan accent sama. Tema ikut sistem (#203).

---

## 5. Capability map — distilasi daftar fitur #17

Jawaban #17 isinya ~500 capability. Gue kelompokkan jadi 16 grup dan tempatkan per fase biar realistis (MVP 2 minggu → jangan janji semuanya sekaligus).

**Grup 1 — Planning & Reasoning:** Autonomous Task Planning · Multi-Step Execution · Goal Decomposition · Prioritization · Dynamic Replanning · Self-Reflection · Self-Correction · Structured/Hierarchical Planning · ReAct & Planner-Executor architecture.
→ **V1** (planner+executor+replan). V2: reflection loop, hierarchical.

**Grup 2 — Memory:** Short/Long/Episodic/Semantic/Working · Retrieval · Summarization · Consolidation · User-preference · Agent state · Persistent profiles · Relevance scoring · Duplicate detection · Importance scoring.
→ **V1**: working+long-term+preference+retrieval+summarize. **V2**: episodic/semantic graph, consolidation, importance scoring.

**Grup 3 — Tool use:** Discovery · Dynamic selection · Chaining · Parallel/Sequential/Conditional · Result validation · Failure detection · Retry logic · Caching.
→ **V1** (registry + chain + validate + retry). V2: discovery/MCP-driven, caching.

**Grup 4 — Code & Repo:** Code gen · Execution · Debugging · Refactoring · Review · Repo analysis · Git/GitHub/GitLab · Commit & PR generation · Issue/branch management · Tests (unit/integration) · CI/CD.
→ **V1**: gen+exec+debug+git+commit/PR+repo analysis. V2: auto-refactor, test generation, CI/CD, GitLab.

**Grup 5 — Data & Dokumen:** Web scraping · Extraction · Cleaning · Transformation · Analysis · Spreadsheet/CSV/JSON/XML/Markdown · PDF read/generate · Document parsing · OCR · Database querying · SQL gen · Vector DB · Embeddings · Semantic search · RAG · Knowledge base · Knowledge graphs.
→ **V1**: scrape, CSV/JSON, PDF, OCR, SQL, RAG ringan. V2: vector DB penuh, knowledge graph, NL-DB search.

**Grup 6 — Web & Browser:** Search · Browsing · Page reading/summarization · Navigation · Browser automation · Form filling · Upload/Download · Screenshot · DOM inspection · Accessibility tree · Mouse/Keyboard automation · Multi-browser · Headless.
→ **V1**: search, read, screenshot, automation dasar. V2: form filling, DOM/accessibility, desktop automation.

**Grup 7 — Media:** Image understanding · Generation · Editing · Screenshot analysis · Computer vision · Voice input · STT · TTS · Voice conversation.
→ **V1**: STT+TTS (Indonesia), image understanding, gen via custom key. V2: image editing, vision pipeline, voice call mode.

**Grup 8 — Kontrol & Keamanan:** HITL approval · Action confirmation · Sensitive action detection · Audit logs · Execution logs · Sandboxing · Permission boundaries · Risk scoring · Approval gates · Escalation · Emergency stop / kill switch · Quotas · Safe/Read-only/Restricted/Autonomous mode.
→ **V1**: approval gates, risk scoring, audit log, kill switch, permission matrix, mode set.

**Grup 9 — Observability:** Activity timeline · Cost/token tracking · Latency & performance monitoring · Agent analytics · Trace replay · Failure replay · Time-travel debugging · OpenTelemetry · Log export · Debug/verbose/dry-run/simulation mode · Decision logs · Explainable execution.
→ **V1**: timeline, token/cost, trace replay, decision log, dry-run. V2: OTEL, analytics, time-travel debug console.

**Grup 10 — Model & Prompt:** Model routing · Multi-model · Fallback · Selection · Temperature · Structured output/JSON schema · Function calling · Streaming tool results · Response validation · Hallucination detection · Fact verification · Source citation · Confidence scoring · Prompt management/optimization · Prompt caching.
→ **V1**: BYO provider routing + fallback + structured output + citations + confidence. V2: hallucination detection, prompt optimization, semantic cache.

**Grup 11 — Scheduling & Triggers:** Background/scheduled/recurring/event-driven tasks · Webhook & conditional triggers · Cron · Autonomous monitoring · Change detection · Alerts.
→ **V1**: cron misi, webhook, monitoring+alert. V2: event-driven graph, conditional triggers.

**Grup 12 — Multi-Agent:** Collaboration · A2A messaging · Delegation · Specialist/Supervisor/Worker/Planner/Research/Coding/Browser/Data/Writer/Reviewer/QA/Memory/Orchestrator agents · Handoff · Swarm · Shared memory/workspace · Conflict resolution · Consensus · Voting · Parallel research · Source comparison & ranking.
→ **V1**: fondasi (role model, shared workspace, A2A event). **V2**: swarm + consensus + specialist agents.

**Grup 13 — Skills & Ekstensi:** Agent skills · Skill discovery/generation/evaluation/versioning/sharing · Slash commands · Custom commands · Plugin system (discovery/install/permissions/sandboxing) · Marketplace · MCP (server/tool discovery/resource access) · Custom connectors/webhooks/automations.
→ **V1**: Skill Engine + slash command + plugin loader lokal. **V2**: MCP, marketplace, skill sharing.

**Grup 14 — Workspace & Kolaborasi:** Multi-project · Workspace isolation · Env vars · Config files · Presets · Project rules · Team collaboration · Shared agents · Agent/workflow/config versioning · A/B agents · Multi-tenant.
→ **V1**: multi-project + isolation + presets + project rules. V2: teams, versioning, A/B.

**Grup 15 — Output & Deliverables:** Report/dashboard/chart/presentation generation · Website/UI generation · UI testing · Screenshot-to-code · Design-to-code · Figma · Full-stack project gen · Docs/README/changelog/release notes · SEO · Content/blog/social generation · Marketing automation.
→ **V1**: report, chart, website/UI gen, docs/README/changelog. V2: design-to-code, Figma, full-stack scaffold, marketing suite.

**Grup 16 — Domain packs (template misi):** Research & Deep Research · Competitive/market/technical research · Literature review · Fact checking · Education (learning path, quiz, flashcard, homework) · Personal productivity (journal, second brain, file organization) · DevOps (server monitoring, deployment, IaC, k8s, docker) · Security (vuln scan, secret leak, license) · Business (CRM, lead research, invoice/receipt, meeting notes).
→ **V1**: 6 playbook (riset, scrape→dataset, bangun situs→deploy, monitoring→alert, OSINT, olah dokumen). V2: sisanya sebagai paket domain.

---

## 6. Terobosan yang gue usulkan (jawaban #30: "kamu pikirkan sendiri, terobosan gila")

Lima hal yang bikin Cuda bukan "wrapper ChatGPT lagi":

1. **Self-Extending Skills** — setelah misi sukses, Cuda **menulis skill baru** (`SKILL.md` + tool grants + contoh) dari apa yang barusan dia kerjakan, langsung bisa dipanggil `/`. Makin dipakai, makin pintar — tanpa training. (#78, #257, #162)
2. **Time-Travel Missions** — semua langkah = event append-only, jadi: replay misi dari langkah mana pun, **fork dari langkah N**, dan **banding 2 rencana side-by-side** dengan tombol. Debugging & trust level yang belum ada di ChatGPT/Claude. (#123, #124, #113)
3. **Universal Receipt + Undo** — setiap aksi (file, terminal, git, deploy, kirim pesan) menghasilkan struk: apa berubah, diff, izin yang dipakai, **tombol Undo** (git-based). "What did it do?" selalu bisa dijawab. (#140, #141)
4. **Zero-Cost by Design (BYOE)** — semua model/search/image/tool pakai key user; Cuda jadi shell gratis + preset provider. Ini yang bikin 1.000 user realistis tanpa biaya infra. (#174, #191)
5. **Personal Brain yang transparan** — memory gabungan (global/workspace/thread) yang bisa dilihat, diedit, dijelaskan asalnya ("kenapa ini diingat"), plus import riwayat ChatGPT/Hermes. Bukan black-box RAG. (#103–#108)

Plus dua fondasi yang disiapkan diam-diam di v1 tapi baru "kelihatan" di v2: **Agent Swarm** (#258) dan **Cuda as Hermes Tool** (#237).

---

## 7. Yang berubah dari plan v1 → v2

- Billing/kredit/admin-pricing → **dihapus dari v1** (gratis + BYOE).
- Prompt Library → **Skill Engine + slash command**.
- Dua accent warna → **satu midnight blue + ikon berwarna**.
- Istilah Indonesia → **Inggris** (Mission/Step/Permission/Receipt/Deliverables) + i18n EN/ID.
- API publik OpenAI-compatible → **tidak ada** (API internal saja).
- Storage: SQLite server + IndexedDB browser **dua-duanya**.
- Target: **MVP 2 minggu**, desktop-first, PWA v1, packaging desktop nanti.
- Ditambah: cron misi, webhook, monitoring+alert, import riwayat, skill generator, Board view, mode diskusi, fork misi, banding rencana, 20 checkpoint, audit export, notif Telegram.
- Ditunda ke v2: MCP, marketplace plugin, multi-agent swarm, multi-tenant/teams, desktop packaging, vector DB penuh, OTEL/analytics.


---
---

# ════ BAGIAN 6 · RENCANA TEKNIS LENGKAP (arsitektur, event protocol, data model, token desain, route) ════

> _Sumber asli: `PLAN.md` di repo_

# CUDA — Implementation Plan v2.0

> **Untuk Hermes:** plan ini dieksekusi task-by-task. Semua keputusan produk sudah dikunci di `docs/DECISIONS.md` (dari kuesioner 262 pertanyaan). Jangan tanya ulang hal yang sudah ada di sana.
> **Status:** keputusan produk LOCKED · menunggu "gas" untuk mulai P0.
> **Target MVP:** 2 minggu (desktop-first, Cuda AI diselesaikan dulu, lalu Cuda Agent).

**Goal:** Bangun **Cuda** — aplikasi AI **local-first** dengan dua room terpisah:
- **Cuda AI** (`/ai`) — workspace chat biasa (ngobrol, tanya-jawab, dokumen, artifact, riset).
- **Cuda Agent** (`/agent`) — console agentic (kasih goal → plan → eksekusi dengan tools → deliverable nyata).

**Prinsip produk yang mengunci semua keputusan:**
1. **BYOE (Bring Your Own Everything)** — gratis by default; semua model/search/image/tool pakai base_url + API key milik user. Cuda tidak menyediakan token, tidak ada markup, tidak ada kuota.
2. **Local-first, desktop-first** — data di SQLite lokal + IndexedDB browser; PWA di v1; nanti di-package jadi software desktop.
3. **Skills, bukan prompt library** — kemampuan dipanggil dengan `/` dan Cuda bisa **menulis skill sendiri** setelah misi sukses.
4. **Pisahkan conversation stream dari activity stream** (keputusan riset) — Cuda Agent = 3-pane, bukan chat.
5. **Setiap aksi punya struk + undo** — trust dibangun dari transparansi, bukan dari output yang kelihatan pintar.

**Tech Stack (final):** Next.js 16 (App Router) · TypeScript · Tailwind 4 + komponen sendiri (Radix primitives) · Prisma + SQLite · Zustand + TanStack Query · Zod (kontrak event) · Fastify + `ws` (agent-node) · CodeMirror 6 · xterm.js · sandboxed iframe + postMessage (artifact) · Playwright (browser tool) · i18n (EN default, ID switch) · Vitest + Playwright (test) · npm workspaces (monorepo).

---

## 1. Arsitektur v2

```
┌──────────────────────────────────────────────────────────────────────┐
│  apps/web  (Next.js 16)  →  Vercel                                   │
│  /  (landing + demo)   /ai  (Cuda AI)   /agent  (Cuda Agent)         │
│  /settings  /skills  /memory  /missions  /share/*                    │
│  /api/chat (SSE)  /api/agent/* (proxy + WS)  /api/upload             │
└───────────┬──────────────────────────────────────┬───────────────────┘
            │ SSE (chat)                            │ WS (agent events)
            ▼                                       ▼
┌───────────────────────────┐        ┌──────────────────────────────────┐
│  LLM Router (core)        │        │  apps/agent-node (Fastify + ws)  │
│  provider dari USER:      │◀───────│  • Orchestrator (plan/exec/replan)│
│  base_url + api_key       │        │  • Tool registry + sandbox        │
│  fallback chain (user)    │        │  • Event bus (Zod, append-only)   │
│  prompt cache (opt, off)  │        │  • Checkpoint (git) + receipt     │
└───────────────────────────┘        └───────┬──────────────────────────┘
                                             │
                        ┌────────────────────┴─────────────────┐
                        ▼                                      ▼
              workspaces/<mission-id>/                 SQLite (Prisma)
              (files, git repo, artifacts)      users, providers, keys,
                                                threads, artifacts, memory,
                                                missions, events, skills
```

**Deployment v1:** `apps/web` → Vercel (project `cuda`) · `apps/agent-node` → **box dev ini** (port 9400, pm2) · DB → SQLite · storage → lokal · backup → GitHub (repo private `Xiaochown/cuda`).
**Kalau agent-node mati:** Cuda AI tetap jalan penuh (chat tidak butuh node), Cuda Agent menampilkan status "agent node offline" + tombol retry. *(#63)*

---

## 2. Design token (final, sesuai jawaban #6)

```css
:root[data-theme="dark"]{
  --bg:#0d0d0d; --bg-elev:#141517; --surface:#1a1c1f; --surface-2:#22252a;
  --border:#2b2f36; --border-strong:#3a3f47;
  --text:#ececf1; --text-dim:#a0a6b0; --text-mute:#6e747e;
  --accent:#2563eb; --accent-hover:#3b82f6; --accent-soft:#1e293b;
  --run:#f5a524; --ok:#22c55e; --err:#ef4444; --wait:#38bdf8; --idle:#6b7280;
}
:root[data-theme="light"]{
  --bg:#ffffff; --bg-elev:#f7f7f8; --surface:#ffffff; --surface-2:#f0f0f2;
  --border:#e3e3e6; --border-strong:#cfcfd4;
  --text:#0d0d0d; --text-dim:#5b6068; --text-mute:#8b9099;
  --accent:#2563eb; --accent-hover:#1d4ed8; --accent-soft:#eef2ff;
}
--r-sm:6px; --r:10px; --r-lg:14px; --font:Inter; --mono:"JetBrains Mono",ui-monospace;
```
- Tema **ikut sistem** + toggle manual + light mode di v1 (#203, #204).
- **Satu accent midnight blue**, bukan dua warna. **Ikon model/brand full-color** (devicon/simple-icons).
- Cuda AI: density lega, jawaban AI polos (bukan bubble). Cuda Agent: density padat, mono untuk log/aksi, badge status warna.

---

## 3. Cuda AI — spec v1 (`/ai`)

**Layout:** sidebar (Percakapan + Ruang Kerja/Projects + Skills + Memory) · thread · panel kanan **Artifacts** (collapsible; mobile = bottom sheet).

**Wajib v1:**
- Thread: list + grup waktu, search **full-text + semantik**, pin, arsip, hapus massal, rename.
- **Projects/Ruang Kerja**: custom instruction permanen + file knowledge + scope memory sendiri.
- **Folder** untuk organisasi percakapan.
- Composer: attach semua tipe (≤50MB) + **OCR** untuk PDF scan/gambar, Enter=kirim, draft auto-save (server+lokal), persona chips generik, **slash command `/` = skills + help + plugin**.
- Toggle: 🔎 Web Search (**multi-engine gratis**: DuckDuckGo/Brave/Firecrawl — user pilih engine, default ON) · 🧠 Deep Research · 🖼 Image Gen (via custom key: sunburst/flare/gpt-image-2.0) · 🎙 STT Indonesia · 🔊 TTS Indonesia.
- Model picker: **provider milik user** (base_url + key + model list diambil dari `/models`), fallback chain diatur user, label "served by <provider>" di bawah jawaban.
- Pesan: streaming, stop, regenerate, **edit → fork cabang**, continue-generating, rating 👍👎, sitasi bernomor, markdown+tabel+kode+Mermaid+LaTeX.
- **Artifacts**: auto-**tanya** dulu sebelum dibuka (#95), versioning **tak terbatas**, targeted edit (highlight → ubah), edit manual, download, **Publish → `/share/a/<slug>`** (bisa dicabut), halaman **galeri artifact**, render di sandboxed iframe.
- **Memory**: halaman CRUD, scope gabungan (global/workspace/thread), penjelasan "kenapa diingat" + sumber, **tanpa kadaluwarsa otomatis**, **import riwayat dari ChatGPT/Hermes**.
- Export PDF berbrand + MD/JSON, share thread (harus klik Publish), token/cost meter, keyboard shortcuts + cheat sheet, onboarding wizard, i18n EN/ID.

**Tidak ada di v1:** compare mode (#32), mode sementara (#94), prompt library (#78 → skills), API publik OpenAI-compatible (#49).

---

## 4. Cuda Agent — spec v1 (`/agent`)

**Layout 3-pane** (bukan chat):
```
┌──────────────┬────────────────────────────────┬─────────────────────────┐
│ MISSIONS     │ ACTIVITY                       │ WORKSPACE               │
│ + New Mission│ ┌ Brief & steering (chat)      │ [Files][Editor][Preview]│
│ ────────     │ ├ Plan (checklist + approve)   │ [Terminal][Browser]     │
│ ● Research…  │ ├ Timeline (kartu terbuka)     │ [Deliverables]          │
│ ● Scrape…    │ │  ✓ step · ⏳ tool call       │                         │
│ ○ Build…     │ │  ⛔ PERMISSION NEEDED        │ workspace/              │
│ Board view   │ ├ Evidence (sources+rationale) │  report.md · data.csv   │
│              │ └ Deliverables + Receipts      │  preview/index.html     │
├──────────────┴────────────────────────────────┴─────────────────────────┤
│ ▶ Run │ ⏸ Pause │ ⏹ Stop │ Autonomy: [Suggest|Draft|Execute] │ 18/100    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Wajib v1 (semua sudah dikonfirmasi user):**
1. Mission dari **form goal** atau naik dari chat biasa (#109).
2. **Plan wajib + approval** sebelum eksekusi (#110); setelah approve, aksi berisiko tetap minta izin (#111).
3. **Board (kanban)** + **timeline kartu terbuka** + **current step pinned** (#112–#114).
4. Estimasi **waktu** sebelum jalan (#115).
5. Retry **3x → eskalasi** (#116); agent **sangat boleh** bertanya balik (#121).
6. Batas: **150 langkah · 100 aksi · tanpa batas waktu · tanpa batas biaya** (#117–#120) + guard di §7 F2.
7. **Mode diskusi** (ngobrol tanpa eksekusi) (#122), **fork misi** (#123), **banding 2 rencana dengan tombol** (#124).
8. **Permission matrix per tool** (always/ask/never) yang bisa diubah user (#129), izin **selalu tanya ulang** (#130), **mode paranoid** & **mode gas** (#131, #132), izin ditolak → **tanya alternatif** (#133), kartu izin **auto-pause 5 menit** (#134).
9. **Autonomy**: Suggest / Draft / Execute, mengikuti permission yang diberikan user (#127). Aksi sensitif yang wajib izin: deploy, hapus, kirim keluar, bayar, network keluar, tulis file di luar workspace (#128).
10. **Receipt + Undo** (git-based) untuk setiap aksi (#140, #141), **checkpoint** (simpan 20, auto-prune) (#142, #143).
11. **Audit trail exportable** JSON/PDF (#140), log **diredact** (API key/token otomatis disensor) (#139).
12. **Credential vault**: user boleh simpan API key untuk tool — **terenkripsi, hanya user yang bisa lihat** (#146).
13. **Multi-sesi paralel** (#35), **cron/scheduled missions** (#37), **webhook trigger**, **monitoring + alert** (#159).
14. **Deliverables**: format bebas (#125), bisa dikirim ke **Telegram/WA** (#126).
15. Workspace viewer: file tree, CodeMirror editor, diff, live preview, terminal xterm.js, browser (screenshot stream).
16. **Skills**: Cuda boleh **menyimpan playbook/skill dari misi sukses** (#162) dan menjalankan skrip/plugin custom (#163).

---

## 5. Agent Event Protocol (kontrak inti — tidak berubah)

```ts
type AgentEvent =
  | { t:'mission.started'; id:string; goal:string; model:string; autonomy:Autonomy; limits:Limits }
  | { t:'plan.created';   steps:Step[] }
  | { t:'plan.updated';   stepId:string; status:StepStatus; note?:string }
  | { t:'plan.compared';  a:string; b:string; chosen?:'a'|'b' }         // fitur banding rencana
  | { t:'step.started';   stepId:string; title:string; startedAt:number }
  | { t:'thought';        stepId:string; summary:string }               // ringkas, bukan CoT mentah
  | { t:'tool.call';      stepId:string; callId:string; tool:string; args:unknown; preview:string }
  | { t:'tool.result';    callId:string; ok:boolean; ms:number; result:unknown; error?:string }
  | { t:'artifact.new';   artifactId:string; kind:ArtifactKind; name:string; url:string; bytes:number }
  | { t:'artifact.diff';  artifactId:string; from:string; to:string; patch:string }
  | { t:'permission.req'; id:string; action:string; risk:'low'|'med'|'high'; impact:string; options:string[] }
  | { t:'permission.res'; id:string; decision:'allow'|'deny'|'edit'; payload?:unknown }
  | { t:'checkpoint';     id:string; label:string; gitSha:string }
  | { t:'receipt';        actionId:string; summary:string; changed:string[]; permission:string; undoable:boolean }
  | { t:'budget.tick';    steps:number; stepsMax:number; actions:number; actionsMax:number; msElapsed:number }
  | { t:'escalation';     question:string; options:string[] }
  | { t:'skill.learned';  skillId:string; name:string; fromMission:string }   // self-extending skills
  | { t:'mission.paused'|'mission.resumed'|'mission.done'|'mission.failed'; id:string; summary?:string }
```
Sifat: **append-only, idempotent, replayable** → semua event disimpan di `AgentEventRow` sehingga timeline bisa di-replay, misi bisa di-fork, dan debugging time-travel mungkin.

---

## 6. Data model (Prisma, v2)

```prisma
model User        { id, email?, handle?, avatarUrl?, createdAt }
model Provider    { id, userId, label, baseUrl, apiKeyEnc, kind:"openai"|"anthropic"|"gemini"|"custom", models Json, isDefault }
model SearchCfg   { id, userId, engine:"ddg"|"brave"|"firecrawl", apiKeyEnc?, enabled }
model Workspace   { id, userId, name, kind:"ai"|"agent", instructions, rules Json }
model Thread      { id, userId, workspaceId?, folderId?, title, model, pinned, archived, createdAt }
model Folder      { id, userId, name, parentId? }
model Message     { id, threadId, parentId?, role, content, model, providerId?, tokensIn, tokensOut, branchIndex, createdAt }
model Artifact    { id, userId, threadId?, missionId?, name, kind, currentVersionId, publicSlug?, published }
model ArtifactVer { id, artifactId, seq, content, lang, createdAt }
model MemoryFact  { id, userId, workspaceId?, threadId?, subject, predicate, object, sourceType, sourceRef, createdAt }  // no expiry
model Skill       { id, userId, name, slug, description, body, tools Json, trigger Json, version, source:"user"|"generated"|"marketplace", enabled }
model Mission     { id, userId, workspaceId, goal, status, autonomy, providerId?, model, stepsMax, actionsMax,
                    stepsUsed, actionsUsed, startedAt, endedAt, gitDir, forkOf?, forkedAtStep? }
model MissionStep { id, missionId, idx, title, status, startedAt, endedAt, note }
model AgentEventRow { id, missionId, seq, type, payload Json, createdAt }
model Permission  { id, missionId, action, risk, impact, decision, decidedAt, payload Json, autoPaused:Boolean }
model ToolPerm    { id, userId, tool, mode:"always"|"ask"|"never" }
model Checkpoint  { id, missionId, label, gitSha, createdAt }
model Receipt     { id, missionId, actionId, summary, changed Json, permission, undoable, undoneAt? }
model Secret      { id, userId, label, valueEnc, iv, scope }   // AES-256-GCM, key dari env server
model Schedule    { id, userId, missionId?, goalTemplate, cron, nextRunAt, enabled }
model Webhook     { id, userId, url, secret, events Json, enabled }
```
Index: `AgentEventRow(missionId, seq)` · `Message(threadId, createdAt)` · FTS5 untuk thread + memory.

---

## 7. Keamanan & permission (dengan guard dari flag F1)

- **Sandbox v1 (tanpa Docker):** workspace per-misi, path-traversal guard, command **allowlist**, timeout per aksi, rlimit (CPU/mem), output cap, env bersih.
- **Akses folder:** default workspace misi; boleh lebih luas **hanya bila user setujui** (per-misi, tercatat di audit) (#135).
- **sudo (#137):** **default OFF**. Untuk menyalakan: Settings → Security → toggle "Allow sudo" dengan peringatan eksplisit + konfirmasi ketik ulang. Semua pemakaian sudo dicatat di audit log + muncul di timeline sebagai kartu merah.
- **Command berbahaya (#138):** `rm -rf /`, `dd`, `curl|bash`, `chmod 777`, `mkfs`, fork bomb → **konfirmasi kedua** (user harus ketik ulang perintahnya), bukan auto-block.
- **Mode gas (#132):** boleh, tapi wajib banner merah "FULL AUTO — no confirmations" + kill switch selalu terlihat.
- **Secret:** AES-256-GCM at-rest, key dari env server, **tidak pernah** dikirim ke frontend dalam bentuk plaintext, diredact otomatis di log/event/audit (#139, #146).
- **Kill switch** global (⏹ Stop) → membatalkan tool in-flight, membuang antrean, menyimpan checkpoint terakhir.
- **Guard budget (#117–#120):** karena tanpa batas waktu/biaya, tambahkan: warning di 80% aksi, auto-pause kalau **5 menit tanpa progres** (bukan batas keras, bisa dilanjut), dan ringkasan biaya token di akhir misi.

---

## 8. Skill Engine (pengganti prompt library)

- **Format:** `SKILL.md` (frontmatter: name, description, triggers, tools, version) + folder `references/` & `scripts/`.
- **Pemanggilan:** `/skill-name` di composer (AI maupun Agent), atau trigger otomatis dari deskripsi.
- **Sumber skill:** (a) bawaan (6 playbook v1), (b) **digenerate Cuda** setelah misi sukses (`skill.learned` event + kartu "simpan jadi skill?"), (c) user bikin sendiri di `/skills`, (d) marketplace (v2).
- **Tool grants:** skill mendeklarasikan tool yang dibutuhkan; saat dijalankan, permission diminta sekali per skill (tetap bisa di-override per misi).
- **Versioning + rollback** + enable/disable per skill.
- **6 skill bawaan v1:** `deep-research` · `scrape-to-dataset` · `build-and-deploy-site` · `monitor-and-alert` · `osint-dossier` (pakai scam-hunt) · `doc-pipeline` (PDF/DOCX/XLSX/convert).

---

## 9. Tool layer v1

| Tool | Fungsi | Default permission |
|---|---|---|
| `fs` | read/write/patch/glob/grep di workspace | read=always, write=ask |
| `shell` | bash (allowlist, timeout, rlimit) | ask |
| `python` | eksekusi skrip di workspace | ask |
| `web_search` | multi-engine (DDG/Brave/Firecrawl), user-configurable | always |
| `web_fetch` | scrape → markdown (Firecrawl) | always |
| `browser` | Playwright: open, click, fill, screenshot, extract | ask |
| `image_gen` | via provider user (sunburst/flare/gpt-image-2.0) | always |
| `document` | PDF/DOCX/XLSX + convert (pandoc/libreoffice) | always |
| `data` | CSV/JSON/XML/XLSX olah besar (100k baris) | always |
| `sql` | query SQLite lokal + NL→SQL | ask |
| `rag` | tanya-jawab atas file workspace (index ringan) | always |
| `git` | init/commit/branch/diff/restore (+auto-push opsional) | always (lokal), ask (push) |
| `deploy` | Vercel / GitHub Pages | ask |
| `notify` | Telegram / WhatsApp / webhook | ask |
| `monitor` | uptime check + change detection + alert | always |
| `osint` | scam-hunt pipeline | ask |
| `mcp` | MCP client (v2) | ask |
| `http` | request API eksternal | ask |

Tidak dibuat: scraper IG/TikTok (#160).

---

## 10. Route map v2

```
/                     landing lengkap + demo interaktif
/ai                   Cuda AI  · /ai/c/[threadId] · /ai/a/[artifactId]
/agent                Cuda Agent · /agent/m/[missionId] (3-pane console)
/agent/board          Board view (kanban misi)
/missions             riwayat misi + replay + biaya
/skills               skill manager (list, edit, generate, versioning)
/memory               memory CRUD + "kenapa diingat"
/settings             provider & key, search engine, permissions, tema, bahasa, keamanan (sudo/dangerous)
/share/c/[slug]       thread publik   ·  /share/a/[slug]  artifact publik
/api/chat             SSE proxy → provider user (fallback chain)
/api/agent/*          proxy + WS ke agent-node (HMAC)
/api/upload           upload file
/api/import           import riwayat ChatGPT/Hermes
```

---

## 11. Rencana 14 hari (bite-sized, commit tiap task)

### Hari 1–2 · P0 Fondasi
1. `gh repo create Xiaochown/cuda --private`, init monorepo npm workspaces (`apps/*`, `packages/*`), tsconfig base, eslint/prettier, `.gitignore`.
2. `packages/core`: `events.ts` (union `AgentEvent`) + test Zod tiap varian (**RED→GREEN**).
3. `packages/core`: `tools.ts` (registry + skema argumen + default permission) + test.
4. `packages/core`: `router.ts` — provider dari user (base_url/key), fallback chain, streaming; test dengan mock fetch (200/400/429/timeout).
5. `packages/core`: `skills.ts` — parser SKILL.md + matcher trigger + test.
6. Prisma schema v2 + migration `init` (SQLite) + seed 6 skill bawaan.
7. Commit: `chore: bootstrap monorepo + core contracts`.

### Hari 3–6 · P1 Cuda AI (inti)
8. `apps/web` Next.js 16 + Tailwind 4 + token §2 + layout sidebar/thread + i18n (EN default).
9. `/api/chat` SSE route → router (provider user) — verifikasi curl streaming.
10. Thread UI: streaming, markdown/highlight/tabel/Mermaid, stop, regenerate, continue, rating, fork cabang.
11. Sidebar: list + grup waktu + folder + pin/arsip/hapus massal + search FTS5.
12. Projects/Ruang Kerja + custom instruction.
13. Composer: attach (≤50MB) + OCR, model picker (dari provider user), slash `/` skills, persona chips, toggles (search/deep-research/image/STT/TTS).
14. Settings: provider CRUD + test koneksi + fallback chain + search engine + tema + bahasa.
15. **Skills UI**: `/skills` list/edit/generate + slash command runner.
16. Artifacts: entitas + versioning + sandbox iframe + targeted edit + publish `/share/a/[slug]` + galeri.
17. Memory: extractor + halaman CRUD + "kenapa diingat" + import riwayat.
18. Export PDF/MD/JSON + share thread + token/cost meter + onboarding wizard.
19. Commit per fitur + verifikasi curl semua route.

### Hari 7–11 · P2 Cuda Agent
20. `apps/agent-node`: Fastify + ws + auth HMAC + healthcheck + `workspaces/`.
21. Orchestrator: goal → planner (JSON tervalidasi Zod) → executor → replan; test mock LLM.
22. Event bus append-only + persist + endpoint replay + fork misi.
23. Sandbox: workspace per-misi, traversal guard, allowlist, timeout, rlimit, output cap; **test negatif** (`../../etc/passwd`, `;`, backtick, symlink escape, fork bomb).
24. Tools v1 (fs, shell, python, web_search, web_fetch, browser, document, data, git, rag) + test tiap tool.
25. Permission engine: request/response, auto-pause 5 menit, deny→alternatif, matriks per tool, mode paranoid/gas, sudo guard, konfirmasi kedua.
26. Budget/limits + warning 80% + auto-pause tanpa progres + kill switch.
27. Checkpoint (git per langkah, simpan 20) + restore + **Receipt + Undo**.
28. **Skill generator**: setelah misi sukses → usul skill baru (`skill.learned`).
29. Cron/schedule + webhook trigger + monitoring/alert tool.
30. Commit.

### Hari 12–14 · P3 UI Agent + polish + deploy
31. Layout 3-pane + Missions list + Board (kanban) + status bar (Run/Pause/Stop, autonomy, meter).
32. Activity timeline: semua varian event → kartu (step, tool call expandable, thought, receipt+undo, permission, escalation, skill.learned) + current step pinned + filter.
33. Kartu **PERMISSION NEEDED** (dampak + risiko + Setujui/Edit/Tolak + countdown 5 menit).
34. Workspace viewer: file tree, CodeMirror, diff, live preview, terminal xterm.js, browser view.
35. Plan compare (banding 2 rencana) + fork misi UI + mode diskusi.
36. Deliverables + tombol kirim Telegram/WA + audit export (JSON/PDF).
37. Mobile: Cuda Agent tab bar (Missions/Activity/Workspace/Deliverables) + sheet permission; Cuda AI 1 kolom; PWA installable + offline read.
38. Light mode polish, empty/error/loading state, ilustrasi custom, suara notifikasi, push browser, shortcut + cheat sheet.
39. Deploy: web → Vercel; agent-node → pm2 di box + tunnel/port; smoke test end-to-end.
40. Load test 10 misi paralel + CI/CD GitHub Actions + staging + help center + changelog + halaman status.

**Buffer:** kalau mepet, yang boleh digeser ke minggu ke-3: cron/webhook, import riwayat, monitoring tool, Board view, skill generator (semua non-blocker inti).

---

## 12. Verifikasi

- Unit: Vitest untuk `packages/core` (events, router fallback, skills parser) + `agent-node` (orchestrator, permission, budget, sandbox).
- **Sandbox security test wajib lulus:** traversal, injection, symlink, resource bomb, egress tanpa izin, sudo tanpa opt-in.
- E2E: chat streaming, artifact render+publish, misi end-to-end menghasilkan file nyata, pause/stop/resume, permission ditolak → alternatif, restore checkpoint, fork misi, replay misi, skill baru terpakai.
- Semua route + aset `curl -o /dev/null -w '%{http_code}'` = 200 sebelum klaim selesai.
- Uji nyata di HP (user akses via Telegram) untuk Cuda AI & Cuda Agent mobile.

---

## 13. Risiko

| Risiko | Mitigasi |
|---|---|
| **Disk rootfs 99% penuh (2.6 GB)** | Butuh ~5 GB: relokasi artefak ke `/sdcard`, hapus project lama, atau build di laptop. **Ini prasyarat P0.** |
| Tanpa Docker → sandbox lebih lemah | Process-level + allowlist + rlimit v1; Docker/E2B di v2 (fondasi network namespace sudah disiapkan) |
| sudo + mode gas (permintaan user) | Default OFF + opt-in sadar + konfirmasi kedua + audit log + kill switch |
| BYO key → user baru bingung | Onboarding wizard + preset provider + mode tamu + halaman bantuan |
| Target 1.000 user/3 bulan tanpa model bawaan | Fokus landing + demo interaktif + template skill siap pakai |
| 150 langkah/100 aksi tanpa batas waktu | Warning 80%, auto-pause tanpa progres, ringkasan biaya |
| Scope agent sangat luas (500+ capability di #17) | Capability map bertahap (DECISIONS §5): v1 = 16 grup inti, sisanya v2/v3 |
| Multi-agent "sangat perlu" tapi MVP 2 minggu | Fondasi role/A2A/shared-workspace di v1, swarm penuh v2 |

---

## 14. Perlu konfirmasi singkat (bukan blocker kalau dijawab "default")

- **F1** sudo: oke default OFF + opt-in sadar? *(rekomendasi gue: ya)*
- **F3** mesin agent-node: **box Linux ini** (bisa langsung kerja) atau laptop Windows (butuh sesi Hermes di mesin itu)?
- **F4** markup 10% ditunda sampai Cuda jual token — oke?
- **F6** disk: boleh gue relokasi/bersihkan supaya ada ~5 GB ruang?

Kalau jawabannya "default semua" → gue mulai P0 hari 1 sekarang.


---
---

# ════ BAGIAN 7 · BRIEF LENGKAP (guardrail + definition of done detail) ════

> _Sumber asli: `AGENT_BRIEF.md` di repo_

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
5. `TASKS.md` — **checklist 38 task yang harus kamu kerjakan** (update checkbox-nya sambil jalan)
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


---
---

# ════ BAGIAN 8 · RISET (referensi — kenapa desainnya begini) ════

> _Sumber asli: `docs/RESEARCH.md` di repo_

# CUDA — Riset & Sumber (Firecrawl, 23 Sep 2026)

Riset dijalankan dengan Firecrawl API v2 (`/search` + `/scrape`), 15 query, ~40 halaman.
Data mentah: `raw_search.json`, `pages.json`, `github.json` (di `/root/cuda-research/`).

## 1. Agent UX — kenapa chat-first gagal

**Sumber utama:**
- Fuselab Creative — *Agent UX: designing UI for AI agents in 2026* — https://fuselabcreative.com/ui-design-for-ai-agents/
- Hatchworks — *Agent UX Patterns: Chat-First UX Fails* — https://hatchworks.com/blog/ai-agents/agent-ux-patterns/
- AI UX Playground — *Agents patterns* — https://aiuxplayground.com/patterns/agents
- The Skins Factory — *AI Agent UX Design* — https://www.theskinsfactory.com/uiux-design-blog/ai-agent-ux-design

**Temuan kunci (dipakai sebagai keputusan arsitektur Cuda):**

1. > *"The architectural fix is separating the conversation from the activity stream. The conversation thread is where the user sets goals and provides input. A dedicated activity panel shows the agent's autonomous work in progress. Combining both into one stream produces an interface that fails as both a conversation and an activity tracker."*
   → **Cuda Agent = 3-pane: Misic(chat/brief) | Aktivitas(timeline) | Workspace.**

2. Perbedaan kelas produk: *chatbot* = thread + input + formatting; *assistant* = + dialog konfirmasi; *agent* = + **plan visibility layer, real-time progress tracking, intervention points, audit trail**. Membangun UI agent dari template chatbot = gagal karena cadence request-response dilanggar agent (4 aksi otonom terjadi antara dua pesan user).

3. Empat prinsip wajib: **transparency** (alasan di level keputusan, bukan cuma output — "fait accompli" confirmation screen tidak cukup), **user control** (pause/override/redirect per-step tanpa restart; NASA mission dashboard: step-level intervention = fitur paling dihargai), **proactive status** (diam = anxiety tercepat; "comparing 14 options" mengubah 30 detik dari "rusak?" jadi "sedang kerja"), **structured error recovery** (apa yang gagal + kenapa + langkah berikutnya — bukan tombol retry generik).

4. Kegagalan chat-first yang paling umum: invisible actions, unclear state, no controls, no recovery path, no accountability trail, no way to pause, no "kenapa begitu".

5. **12 pattern produksi** (hatchworks): Taskboard+Outcomes · Activity Timeline · Start/Stop/Pause/Resume · Autonomy Levels (Suggest→Draft→Execute) · Two-Phase Actions (Plan→Validate→Execute) · Action Receipts (diff + rollback hook) · Evidence Panel (sumber + rasional, **bukan** chain-of-thought dump) · Human Checkpoint Gates · Autonomy Budget · Per-Action Autonomy (autonomy per kapabilitas, bukan per app) · Checkpoints & Restore · Escalation.
   → Semua 12 dipetakan jadi fitur konkret di `PLAN.md §5.2`.

6. Gartner: 40% enterprise apps punya task-specific AI agent akhir 2026 (dari <5% di 2025) — interface layer-nya belum ada satu tahun lalu.

## 2. Artifact / Canvas — artifact harus jadi OBJEK

**Sumber:** instapods — *ChatGPT Artifacts vs Claude Artifacts: Is Canvas the Same? (2026)* — https://instapods.com/blog/claude-artifacts-vs-chatgpt-canvas/

- Claude Artifacts: side panel, **disimpan sebagai objek bernama**, punya **version history**, tombol **Publish** → URL publik. Bisa dipakai di Free/Pro/Max.
- ChatGPT Canvas: preview pane bagus (HTML/React/SVG/Mermaid/Vega) + Python in-browser + targeted edit (highlight → "pendekin ini"), tapi **bloknya mati di dalam thread**; Canvas dihentikan dari GPT-5.5 (Mei 2026) dan dilebur jadi inline blocks.
- **Kesimpulan untuk Cuda AI:** artifact wajib punya versioning + share link sendiri (`/share/a/<slug>`) + targeted edit. Render di **sandboxed iframe** + postMessage.

## 3. Referensi produk & repo (data GitHub, 23 Sep 2026)

**Chat UI (acuan Cuda AI):**
- open-webui/open-webui ⭐152.9k (Python, MCP) — RAG dokumen, user mgmt, **conversation branching**
- lobehub/lobehub ⭐82.8k — paling polished; plugin 100+, TTS/STT, knowledge base, mobile bagus
- danny-avila/LibreChat ⭐44.7k (MIT) — **artifacts, agents, MCP, skills**, multi-provider, granular permissions
- chatboxai/chatbox ⭐41.8k · vercel/chatbot ⭐21.0k (Next.js + Redis + shadcn) · enricoros/big-AGI ⭐7.1k (**Beam multi-model chat** = acuan compare mode) · Cinnamon/kotaemon ⭐25.8k (RAG)
- Pelajaran pasar (Elestio): UI ChatGPT sudah jadi *table stakes*; diferensiasi pindah ke workflow/agent/RAG/privasi.

**Agent workspace (acuan Cuda Agent):**
- kortix-ai/suna ⭐20.2k — open-source Manus/Cowork alternative; sandbox baca/tulis file, browser
- OpenHands/OpenHands ⭐89.0k (MIT) — agent workspace: terminal + browser + editor
- browser-use/browser-use ⭐116.0k (MIT) — tool browser
- cline/cline ⭐69.1k (Apache-2.0) — acuan **approval gate before every action**
- e2b-dev/E2B ⭐13.9k · daytonaio/daytona ⭐71.7k — sandbox code execution
- modelcontextprotocol/servers ⭐90.6k — MCP (tool eksternal)
- mem0ai/mem0 ⭐65.9k · getzep/graphiti ⭐31.1k — memory layer
- langgenius/dify ⭐156.9k · n8n-io/n8n ⭐205.8k — workflow/agent builder (acuan Playbook)
- firecrawl/firecrawl ⭐183.6k — search/scrape (sudah dipakai user)

**Agent harness 2026 (nimbalyst.com):** Claude Code = paling kuat untuk refactor; OpenCode = open-source terbaik; Cline = approval gate; Aider = commit per turn; **"workspace di atas agent" = lapisan yang masalahnya belum selesai** → peluang Cuda Agent.

## 4. Sandbox — pilihan teknis

**Sumber:** Northflank — *Daytona vs E2B in 2026* — https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes

- **E2B**: Firecracker microVM, kernel terpisah per sesi (isolasi hardware), cold start tercepat, SDK TypeScript bersih, model sesi (bukan persist). Managed → kode dikirim ke infra mereka.
- **Daytona**: workspace persisten, container (shared kernel); produksi closed-source sejak Juni 2026.
- **WebContainer**: jalan di browser, bagus untuk preview tapi tidak untuk tool native (shell/browser).
- **Box ini tidak punya Docker** → MVP pakai *process-level sandbox* (workspace per-run + path-traversal guard + allowlist command + timeout + rlimit + output cap). Naik kelas: E2B free tier atau node terpisah.

## 5. Memory — vector saja tidak cukup

**Sumber:** Mem0 *State of AI Agent Memory 2026* — https://mem0.ai/blog/state-of-ai-agent-memory-2026 · vectorize.io — https://vectorize.io/articles/best-ai-agent-memory-systems · Atlan — https://atlan.com/know/mem0-alternatives/

- Mem0: dual-store vector + knowledge graph (Qdrant/Chroma/pgvector/Redis).
- Zep/Graphiti (arXiv 2501.13956): tiap node/edge punya `valid_at` + `invalid_at` → **temporal retrieval 91% vs mem0 49%**.
- "Just use a bigger context window" = jebakan.
- **Keputusan Cuda:** SQLite FTS5 + embedding lokal + tabel fakta bertimestamp (`MemoryFact`) — murah, tanpa layanan eksternal, tetap bisa jawab "fakta ini masih berlaku?".

## 6. Catatan lingkungan (hasil cek box)

- Node v22.23.2, npm 10.9.8 ✅ (Next.js 16 aman)
- **Docker: TIDAK ADA** ❌ → sandbox process-level dulu
- Disk `/` **99% penuh — sisa 2.6 GB** ⚠️ → build berat sebaiknya di VPS/STB atau bersihkan dulu
- gh CLI: login sebagai `Xiaochown` ✅ (bisa `gh repo create`)
- cloudflared: `/root/.9router/bin/cloudflared` ✅ (tunnel pakai script, `--protocol http2`)
- Port bebas: 9090–9095, 9400, 9999, 3000 ✅
- Kandidat ruang disk: `/root/meridian` 1.2G · `nuxt-neobrutalism` 735M · `masbraw-router-v2` 710M · `belajar-ai-neo-brutal` 546M · `ai-belajar` 486M (≈3.7 GB bisa diarsipkan)


---
---

# ════ BAGIAN 9 · JAWABAN MENTAH 262 PERTANYAAN (referensi ground-truth) ════

> _Sumber asli: `docs/ANSWERS.md` di repo_

CUDA — JAWABAN KUESIONER (262/262)
Tanggal: 23/9/2026, 18.49.03

## A. Brand & Identitas
1. Nama brand induk final: "Cuda" — atau ada alternatif? → Cuda
2. Nama dua produk: "Cuda AI" & "Cuda Agent" — fix atau mau ganti? → fix
3. Tagline landing: "Cuda AI buat mikir. Cuda Agent buat ngerjain." — oke atau mau versi lain? → Cuda For Simple Work , Cuda Agent for Deep Work Autonomus
4. Domain yang mau dipakai (mis. cuda.my.id / cudai.app)? Sudah punya domain apa saja? → nanti aja kita pakai vercel dulu
5. Logo: monogram huruf C (rounded-square/hexagon), atau mau dibikin dari nol dengan konsep lain? → Monogram C
6. Accent dua room: biru #4f8cff (AI) + violet #8b5cf6 (Agent) — setuju? → warna hitamdan biru Midnight  linear khas Chatgpt saja dengan tampilan icon dl yang berwarna
7. Bahasa UI default: Indonesia, Inggris, atau dua-duanya (switch)? → dua-duanya dengan inggris sebagai bahasa utama
8. Istilah Indonesia (Misi/Langkah/Izin/Struk/Serahan) dipertahankan atau campur Inggris? → Inggris
9. Agent kalau "ngomong" pakai nama siapa? → Cuda
10. Perlu maskot/karakter visual? → ya Nanti Kita bikin Maskot
11. Cuda jadi bagian keluarga brand Masbraw/ZieDev, atau brand berdiri sendiri? → berdiri sendiri
12. Credit/footer: "Cuda by ..." mau ditulis apa? → tanpa keterangan agar lebih profesional dan tanpa footer kita fokuskan aplikasi CUda Agent

## B. Positioning & Target User
13. User utama v1: kamu sendiri, teman kampus, atau publik luas? → publik, mahasiswa, remaja, pekerja, vibe coding ,proggramer, dan lainnya
14. Cuda mau jadi produk komersial (dijual) atau alat pribadi dulu? → nanti kita keduanyaa kalau berbayar nanti dia beli token dari aku basicnya gratis karna kita menerapkan bebas custom api
15. Kalau dijual: target pasar utama? → semuanya tidak hanya mahasiswa bahkan orang biasa sampai developer pun
16. Satu kalimat: "Cuda beda dari ChatGPT karena ____" → AI agent bisa mengubah kode langsung dari Cuda bisa liat log terminal editor preview dan lainnya bahkan history timeleinekita ambil referensi sebagian dari ai agent yang lainnya juga, tapi bedakan juga itu hanya untuk Cuda Agent kalau cuda Ai dia chat biasa
17. Fitur mana yang jadi pembunuh utama (bikin orang pindah ke Cuda)? → Feature Seperti hermes ini datanya saya kirimkan tapi filter aja soalnya ini juga hasil generate ai = Autonomous Task Planning, Multi-Step Task Execution, Goal Decomposition, Task Prioritization, Task Scheduling, Dynamic Replanning, Self-Reflection, Self-Correction, Retry Failed Tasks, Error Recovery, Context Management, Long-Term Memory, Short-Term Memory, Episodic Memory, Semantic Memory, Working Memory, Memory Retrieval, Memory Summarization, Memory Consolidation, User Preference Memory, Conversation History, Persistent Agent State, Agent Profiles, Multiple Agent Personas, Tool Calling, Tool Discovery, Dynamic Tool Selection, Tool Chaining, Parallel Tool Execution, Sequential Tool Execution, Conditional Tool Execution, Tool Result Validation, Tool Failure Detection, Tool Retry Logic, API Integration, REST API Calls, GraphQL Integration, Web Search, Web Browsing, Web Page Reading, Web Page Summarization, Website Navigation, Browser Automation, Form Filling, File Uploading, File Downloading, File Management, PDF Reading, PDF Generation, Document Parsing, OCR, Image Understanding, Image Generation, Image Editing, Screenshot Analysis, Computer Vision, Voice Input, Speech-to-Text, Text-to-Speech, Voice Conversation, Streaming Responses, Real-Time Interaction, Code Generation, Code Execution, Code Debugging, Code Refactoring, Code Review, Repository Analysis, Git Integration, GitHub Integration, GitLab Integration, Commit Generation, Pull Request Generation, Issue Management, Branch Management, Automated Testing, Unit Test Generation, Integration Test Generation, Test Result Analysis, CI/CD Integration, Shell Command Execution, Terminal Automation, Docker Integration, Database Querying, SQL Generation, Database Schema Analysis, CRUD Automation, Vector Database Integration, Embedding Generation, Semantic Search, RAG, Knowledge Base Integration, Document Indexing, Knowledge Graphs, Web Scraping, Data Extraction, Data Cleaning, Data Transformation, Data Analysis, Spreadsheet Analysis, CSV Processing, JSON Processing, XML Processing, Markdown Processing, Email Reading, Email Drafting, Email Sending, Calendar Integration, Calendar Scheduling, Reminder Creation, Notification System, Slack Integration, Discord Integration, Telegram Integration, WhatsApp Integration, Trello Integration, Notion Integration, Google Drive Integration, Google Sheets Integration, Authentication Handling, OAuth Integration, API Key Management, Secret Management, Permission Management, Role-Based Access Control, Human-in-the-Loop Approval, Action Confirmation, Sensitive Action Detection, Audit Logs, Execution Logs, Agent Activity Timeline, Cost Tracking, Token Usage Tracking, Latency Monitoring, Performance Monitoring, Agent Analytics, Prompt Management, System Prompt Templates, Dynamic Prompt Generation, Prompt Optimization, Model Routing, Multi-Model Support, LLM Fallback, Model Selection, Temperature Control, Structured Output, JSON Schema Output, Function Calling, Streaming Tool Results, Response Validation, Hallucination Detection, Fact Verification, Source Citation, Confidence Scoring, Uncertainty Detection, Safety Filters, Content Moderation, Rate Limiting, Budget Limits, Token Limits, Execution Time Limits, Task Cancellation, Background Tasks, Scheduled Tasks, Recurring Tasks, Event-Driven Tasks, Webhook Triggers, Cron Jobs, Conditional Triggers, Autonomous Monitoring, Website Monitoring, Price Monitoring, Status Monitoring, Change Detection, Alert Generation, Multi-Agent Collaboration, Agent-to-Agent Messaging, Agent Delegation, Specialist Agents, Supervisor Agent, Worker Agents, Planner Agent, Research Agent, Coding Agent, Browser Agent, Data Analyst Agent, Writer Agent, Reviewer Agent, QA Agent, Memory Agent, Orchestrator Agent, Agent Handoff, Agent Swarm, Shared Memory, Shared Workspace, Conflict Resolution Between Agents, Consensus Generation, Agent Voting, Parallel Research, Research Source Comparison, Automatic Source Ranking, Research Summarization, Fact Extraction, Entity Extraction, Sentiment Analysis, Intent Detection, Language Detection, Multilingual Support, Translation, Text Classification, Document Classification, Information Extraction, Keyword Extraction, Topic Modeling, Personal Assistant Mode, Research Assistant Mode, Coding Assistant Mode, Project Manager Mode, Customer Support Mode, Automation Mode, Learning Mode, Study Assistant Mode, Custom Agent Workflows, Workflow Templates, Visual Workflow Builder, Drag-and-Drop Agent Builder, Agent Configuration Dashboard, Tool Permission Dashboard, Memory Dashboard, Execution History, Task History, Conversation Search, Project Workspace, Multi-Project Support, Workspace Isolation, Environment Variables, Configuration Files, Agent Presets, Custom Commands, Slash Commands, Agent Skills, Skill Marketplace, Plugin System, Plugin Discovery, Plugin Installation, Plugin Permissions, Plugin Sandboxing, MCP Support, MCP Server Integration, MCP Tool Discovery, MCP Resource Access, Local Tool Integration, Remote Tool Integration, Local File System Access, Cloud File System Access, Browser Profile Management, Multi-Browser Support, Headless Browser Mode, Screenshot Capture, DOM Inspection, Accessibility Tree Analysis, Mouse Automation, Keyboard Automation, Clipboard Automation, Desktop Automation, Process Management, Background Process Monitoring, Resource Monitoring, CPU Monitoring, Memory Monitoring, Network Monitoring, Automatic Backup, State Recovery, Checkpointing, Task Snapshots, Session Recovery, Offline Mode, Local LLM Support, Cloud LLM Support, Hybrid LLM Mode, Model Failover, Prompt Caching, Response Caching, Tool Result Caching, Semantic Cache, Batch Processing, Queue Management, Priority Queue, Job Scheduling, Distributed Execution, Worker Pool, Rate-Aware Execution, Retry Backoff, Circuit Breaker, Observability, Debug Mode, Verbose Execution Mode, Dry Run Mode, Simulation Mode, Explainable Execution, Step-by-Step Execution Trace, Agent Reasoning Summary, Decision Logs, Custom System Rules, User Rules, Project Rules, Context Injection, Dynamic Context Loading, Context Compression, Automatic Context Pruning, Token Budget Optimization, Prompt Compression, Retrieval Optimization, Memory Relevance Scoring, Duplicate Memory Detection, Automatic Memory Expiration, Memory Importance Scoring, User Feedback Learning, Reinforcement From Feedback, Preference Learning, Adaptive Behavior, Personalized Responses, Automatic Task Suggestions, Proactive Assistance, Proactive Notifications, Daily Briefing, Weekly Summary, Progress Tracking, Goal Tracking, Habit Tracking, Project Progress Reports, Automated Reports, Dashboard Generation, Chart Generation, Presentation Generation, Website Generation, UI Generation, UI Testing, Screenshot-to-Code, Design-to-Code, Figma Integration, Frontend Code Generation, Backend Code Generation, Full-Stack Project Generation, API Documentation Generation, README Generation, Technical Documentation, Changelog Generation, Release Notes Generation, Dependency Analysis, Vulnerability Scanning, Code Security Analysis, Secret Leak Detection, License Detection, Dependency Updates, Automated Refactoring, Performance Optimization, Database Optimization, SEO Analysis, Content Generation, Blog Generation, Social Media Generation, Content Scheduling, Marketing Automation, Lead Research, CRM Integration, Customer Data Analysis, Support Ticket Classification, Automated Ticket Responses, Knowledge Base Search, FAQ Generation, Meeting Transcription, Meeting Summarization, Action Item Extraction, Meeting Follow-Up Generation, Email Follow-Up Automation, Document Comparison, Version Comparison, Contract Data Extraction, Invoice Processing, Receipt Processing, Form Processing, Resume Parsing, Job Search Automation, Job Application Assistance, Interview Preparation, Learning Path Generation, Quiz Generation, Flashcard Generation, Homework Assistance, Research Paper Assistance, Citation Management, Experiment Planning, Personal Knowledge Base, Second Brain, Daily Journal Processing, Personal Productivity Assistant, Automated File Organization, Smart Folder Creation, Duplicate File Detection, File Naming Automation, Backup Verification, System Health Checks, Autonomous DevOps, Server Monitoring, Server Deployment, Cloud Deployment, Infrastructure Automation, Log Analysis, Incident Detection, Incident Response, Automated Rollback, Health Checks, Service Restart Automation, Environment Provisioning, Cloud Resource Management, Infrastructure-as-Code Generation, Kubernetes Assistance, Docker Compose Generation, Security Policy Enforcement, Agent Sandboxing, Permission Boundaries, Action Risk Scoring, Approval Gates, Human Escalation, Emergency Stop, Kill Switch, Agent Quotas, Multi-Tenant Support, Workspace Permissions, Team Collaboration, Shared Agents, Agent Templates, Agent Versioning, Agent Rollback, Workflow Versioning, Configuration Versioning, A/B Testing Agents, Evaluation Benchmarks, Automated Agent Evaluation, Task Success Scoring, Tool Success Scoring, Response Quality Scoring, Regression Testing, Prompt Regression Testing, Synthetic Test Generation, Agent Simulation, Environment Simulation, Benchmark Dataset Management, Trace Replay, Failure Replay, Agent Debugging, Interactive Debug Console, Execution Replay, Time-Travel Debugging, Custom Metrics, OpenTelemetry Integration, Logging Export, Monitoring Webhooks, External Event Triggers, Agent API, Agent-as-a-Service, REST Agent Endpoint, WebSocket Agent Endpoint, Streaming API, SDK Generation, CLI Interface, Web Interface, Mobile Interface, Desktop Interface, Custom Agent UI, Chat UI, Command Center UI, Agent Control Panel, Real-Time Task Visualization, Live Execution Graph, Tool Execution Timeline, Agent Status Indicators, Task Progress Bars, Multi-Conversation Support, Conversation Branching, Conversation Forking, Conversation Export, Data Export, JSON Import Export, Project Backup Export, Agent Configuration Export, Custom Knowledge Upload, Knowledge Source Connectors, Website Knowledge Sync, Automatic Knowledge Refresh, Scheduled Knowledge Crawling, Source Change Alerts, Citation Tracking, Source Provenance, Data Lineage, Enterprise Search, Cross-Source Search, Federated Search, Semantic Document Search, Natural Language Database Search, Natural Language File Search, Natural Language API Search, Autonomous Research Pipelines, Deep Research Mode, Competitive Analysis, Market Research, Technical Research, Literature Review, Multi-Source Fact Checking, Claim Verification, Contradiction Detection, Evidence Collection, Research Brief Generation, Executive Summary Generation, Decision Support Reports, Scenario Analysis, What-If Analysis, Simulation Workflows, Optimization Workflows, Constraint Solving, Rule-Based Reasoning, Knowledge-Based Reasoning, Hybrid Symbolic-AI Reasoning, Planning Graphs, State Machines, Finite-State Workflows, Event-Based State Transitions, Goal-Oriented Agents, Reactive Agents, Proactive Agents, Long-Horizon Agents, Persistent Autonomous Agents, Self-Improving Workflows, Automatic Skill Discovery, Skill Generation, Skill Evaluation, Skill Versioning, Skill Sharing, Agent Marketplace, Community Tools, Community Skills, Custom MCP Servers, Custom Plugins, Custom Connectors, Custom Webhooks, Custom Automations, Agent Memory Search, Cross-Agent Memory, Agent Knowledge Sharing, Multi-Agent Research Teams, Multi-Agent Coding Teams, Multi-Agent Debate, Peer Review Agents, Manager-Worker Architecture, Planner-Executor Architecture, Router-Worker Architecture, Reflection Architecture, ReAct Architecture, Chain-of-Thought-Free Tool Planning, Structured Planning, Hierarchical Planning, Goal Monitoring, Deadline Monitoring, Automatic Escalation, Failure Prediction, Task Risk Prediction, Action Impact Analysis, Safe Mode, Read-Only Mode, Restricted Mode, Autonomous Mode, Full-Auto Mode, Human Approval Mode, Sandbox Mode, Development Mode, Production Mode
18. Target realistis Cuda AI vs ChatGPT/Gemini/Claude? → Yess
19. Target segmen Cuda Agent vs Manus/Claude Cowork? → tidak ada
20. Perlu mode "lokal/offline" (data tidak keluar dari device)? → tidak perlu
21. Ada kebutuhan privasi khusus (data kampus, data klien)? → tidak ada
22. Pesaing lokal Indonesia yang perlu diperhatikan? → tidak ada
23. Cuda mau dipakai untuk jualan jasa (agent-as-a-service)? → mungkin nanti
24. Target jumlah user 3 bulan pertama? → 1000 user
25. Perlu halaman pricing publik sejak v1? → nanti
26. Perlu mode team/kantor (multi-user satu workspace)? → v1

## C. Scope & Prioritas MVP
27. Kerjakan P0–P4 dulu (AI + Agent inti), P5–P7 nyusul — setuju? → setuju
28. Pilih satu: Cuda AI dulu sampai sempurna, atau dua-duanya jalan bareng? → AI dulu baru lanjut agent
29. Target kapan MVP harus jadi (tanggal/perkiraan)? → kisaran 2 minggu dari sekarang
30. 3 fitur WAJIB ada di v1? → kamu pikirkan sendiri intinya terobosan gila
31. Fitur yang boleh ditunda / tidak perlu sama sekali? → belum kepikiran
32. Compare mode (2 model jawab bareng) prioritas atau nice-to-have? → tidak perlu
33. Deep Research mode (riset multi-step otomatis) masuk v1? → ya
34. Voice input (STT) & read aloud (TTS) masuk v1? → dua-duanya
35. Multi-sesi agent paralel masuk v1? → v1
36. Berapa template Playbook yang wajib ada di v1? → kurang paham konsepnya jika berguna tambahkan saja
37. Jadwal/cron misi otomatis masuk v1? → v1
38. MCP connector masuk v1 atau v2? → v2

## D. Stack & Arsitektur
39. Frontend: Next.js 16 atau Nuxt 4? → Next.js 16
40. TypeScript strict mode? → bebas
41. Styling: Tailwind 4 + komponen sendiri, atau pakai UI kit jadi? → Tailwind + komponen sendiri
42. ORM: Prisma atau Drizzle? → terserah kamu
43. State management frontend: Zustand, Jotai, atau React Query + context? → terserah kamu
44. Streaming: chat pakai SSE dan agent pakai WebSocket — setuju? → setuju
45. Monorepo: npm workspaces atau pnpm/turborepo? → terserah kamu
46. Paket packages/ui terpisah atau komponen langsung di apps/web? → bebas yang bagus saja
47. Agent runtime: Node/Fastify, atau Python/FastAPI (ekosistem tool lebih kaya)? → terserah kamu
48. Validasi event pakai Zod di dua sisi — setuju? → bebas
49. Perlu API publik Cuda (REST / OpenAI-compatible)? → tidak
50. Perlu multi-tenant sejak awal (untuk dijual nanti)? → nanti
51. Perlu framework i18n atau switch bahasa manual? → framework
52. Testing: Vitest + Playwright — oke? → oke
53. Box ini tidak ada Docker. Dev agent-node di VPS atau tetap di box ini? → box ini  jika bagus
54. Monorepo Cuda digabung dengan Meridian (pakai gateway-nya) atau berdiri sendiri? → berdiri sendiri

## E. Hosting, Infra & Biaya
55. Web deploy ke Vercel (project baru "cuda") atau self-host? → Vercel
56. Agent-node jalan di mana? → box ini
57. Kalau STB: sanggup nyala 24/7? Resource masih cukup (sekarang ada AdGuard + bot)? → pakai lapto ini aja dulu soalnya nanti kita bikin dia jadi software
58. TLS/domain: Caddy otomatis, Cloudflare Tunnel permanen, atau pakai domain Vercel? → domain Vercel
59. Database produksi: Neon free, Supabase free, atau SQLite di VPS? → SQLite VPS
60. Storage file (upload + artifact): lokal VPS, Cloudflare R2, atau Supabase Storage? → lokal VPS
61. Backup otomatis ke mana? → GitHub
62. Budget infra bulanan yang wajar (Rp)? → kurang tau kalau ini saya mau yang 0$ soalnya
63. Kalau agent-node down: fallback tampil error, atau Cuda AI tetap jalan penuh? → error saja
64. Perlu queue (Redis/BullMQ) atau cukup in-memory dulu? → semuanyaa
65. Monitoring v1: Sentry, Uptime Kuma, atau cukup log? → log saja
66. Log retention berapa lama? → 30 hari
67. Disk box ini 99% penuh (sisa 2.6GB). Boleh gue bersihkan project lama? mana yang aman dihapus? → pakai Drive C aja dulu
68. Build berat boleh dijalankan di VPS (SSH) biar tidak makan disk box ini? → box ini saja

## F. Cuda AI — UX & Fitur Chat
69. Layout default: sidebar terbuka atau collapsed? → kurang tauuu sesuai gambar tadi yang bagusss
70. Jawaban AI: gaya polos (Claude) atau bubble (ChatGPT)? → polos
71. Perlu Projects/Ruang Kerja sejak v1? → ya
72. Instruksi permanen per Ruang Kerja (custom instruction) perlu? → perlu
73. Organisasi percakapan: folder bertingkat, tag, atau cuma list? → folder
74. Search percakapan: full-text saja atau + semantik? → +semantik
75. Perlu pin / arsip / hapus massal? → semua
76. Composer: Enter = kirim, atau Shift+Enter = kirim? → Enter
77. Draft auto-save lintas device? → perlu
78. Prompt library (Resep) dengan variabel + berapa resep bawaan? → tidak ada prompt libary adanya skill yang bisa dipanggil denfgan /
79. Persona chips bawaan: mau apa saja? → kamu generate beberapa saja yang sesuai dengan beberapa kondisi, bukan spesifik
80. Slash command yang kamu mau ada? → skill command help dan banyak lainnya plugin juga dll
81. Tipe file attach wajib: gambar/PDF/DOCX/XLSX/CSV/kode — pilih semua yang wajib → gass bisa semua
82. Batas ukuran file upload? → 50MB
83. Perlu OCR untuk PDF scan & gambar? → perlu
84. Web search: pakai Firecrawl (key sudah ada) atau tambah engine lain? → lain tapi gratis nanti usernya download sendiri kaya di hermes itu masuknya apaa ya bebas dah pokonya mau ada duckduckgo firecawl brave atau yg laen asal gratis bro
85. Default toggle web search: on atau off? → on
86. Image generation: model mana & kuota per hari? → image generation sementara kosong tapi bisa ditambahkan lewat custom apikey seperti mode2 biasa kaya sunburst flare image 2.0 dll
87. Read aloud (TTS): perlu suara bahasa Indonesia? → perlu
88. STT bahasa Indonesia untuk voice input? → perlu
89. Branching (edit pesan → fork cabang): seberapa penting? → penting
90. Perlu fitur "lanjutkan jawaban" (continue generating)? → perlu
91. Rating jawaban (👍👎 + alasan) perlu? → perlu
92. Export PDF rapi dengan header/brand Cuda? → perlu
93. Share thread publik: langsung publik atau harus klik Publish? → harus Publish
94. Perlu mode sementara (percakapan tidak disimpan)? → tidak

## G. Cuda AI — Artifact & Memory
95. Artifact otomatis dibuka kalau kode lebih dari berapa baris? → selalu tanya
96. Tipe artifact wajib: HTML/React/SVG/Mermaid/chart/dokumen — pilih yang wajib → bebas
97. Artifact boleh menjalankan JS sendiri di sandbox iframe? → bebas
98. Berapa versi history artifact yang disimpan? → tak terbatas
99. Targeted edit (highlight → "pendekin ini") masuk v1? → v1
100. Publish artifact → link publik yang bisa dicabut? → ya
101. Artifact bisa diedit manual oleh kamu (bukan cuma AI)? → ya
102. Perlu halaman galeri semua artifact? → perlu
103. Apa yang boleh diingat otomatis? (nama, preferensi, project, jadwal, data sensitif?) → boleh semua
104. Perlu halaman Memory yang bisa dilihat/diedit/dihapus? → perlu
105. Scope memory: global / per Ruang Kerja / per percakapan? → gabungan
106. Perlu penjelasan "kenapa ini diingat?" (sumber fakta)? → perlu
107. Fakta lama otomatis jadi kadaluwarsa (valid_at/invalid_at)? → tidak
108. Perlu import riwayat dari ChatGPT/Hermes ke Cuda? → perlu

## H. Cuda Agent — Model Mental & Alur Misi
109. Mulai misi: form goal khusus, atau dari chat biasa lalu naik jadi misi? → dua-duanya
110. Agent wajib tampilkan Rencana dulu & minta persetujuan sebelum jalan? → ya
111. Setelah plan di-approve, agent boleh eksekusi semua langkah tanpa tanya lagi? → tetap tanya per aksi berisiko
112. Perlu tampilan Board (kanban) selain timeline? → perlu
113. Timeline default: kartu terbuka semua atau collapsed? → terbuka
114. "Current step" selalu di-pin di atas? → ya
115. Perlu estimasi waktu & biaya sebelum misi jalan? → waktu saja
116. Kalau agent nyangkut: langsung eskalasi atau coba ulang dulu? → coba 3x lalu eskalasi
117. Batas maksimal langkah per misi (default)? → 150
118. Batas aksi/tool call per misi (default)? → 100
119. Batas waktu per misi (default)? → tanpa batas
120. Batas biaya per misi (Rp, default)? → tidak ada
121. Agent boleh bertanya balik ke kamu di tengah misi? → sangat boleh
122. Perlu mode "diskusi" (agent cuma ngobrol, tidak eksekusi) di room agent? → perlu
123. Perlu "fork misi" (ulang dari langkah tertentu)? → perlu
124. Perlu bandingkan 2 rencana lalu pilih? → perlu tapi ada tombol
125. Format Serahan (hasil akhir) yang wajib: md/pdf/zip/link/gambar? → bebass inimah
126. Agent boleh kirim hasil otomatis ke Telegram/WA? → boleh

## I. Cuda Agent — Kontrol, Izin & Keamanan
127. Default autonomy level: Sarankan, Draf, atau Eksekusi? → Sarankan,draf,eksekusi terantung permission ang dikasih user
128. Aksi apa saja yang WAJIB minta izin? (deploy/hapus/kirim/bayar/network/tulis file) → hal yang sensitif saja
129. Perlu matriks izin per tool (selalu/tanya/tidak) yang bisa diubah user? → perlu
130. Izin bisa "ingat pilihan ini untuk misi ini"? → selalu tanya ulang
131. Perlu mode paranoid (semua aksi tanya)? → perlu
132. Perlu mode gas (semua aksi otomatis, tanpa tanya)? → perlu
133. Kalau izin ditolak, agent harus ngapain? → tanya alternatif
134. Kartu izin auto-pause kalau tidak dijawab berapa lama? → 5 menit
135. Agent hanya boleh akses folder workspace misi? → boleh lebih luas jika diperlukan saja
136. Akses internet agent: bebas atau whitelist domain? → bebas
137. Agent boleh jalankan sudo? → boleh (bahaya)
138. Command berbahaya (rm -rf, dd, curl|bash) diblok total? → tanya dulu
139. Log diredact (API key/token disembunyikan otomatis)? → ya
140. Audit trail bisa diekspor (JSON/PDF)? → perlu
141. Undo aksi file: cukup git-based, atau perlu trash bin juga? → git saja
142. Checkpoint otomatis tiap langkah atau tiap N langkah? → bebas secocoknyaa
143. Berapa checkpoint disimpan sebelum auto-prune? → 20
144. Kalau nanti ada Docker: perlu network namespace terpisah per misi? → perlu
145. Data misi disimpan berapa lama sebelum dihapus otomatis? → permanen
146. Cuda boleh simpan credential/API key user untuk tool? Bagaimana enkripsinya? → bowlehhh enskripsi hanya bisa dilihat user sendiri tidak bisa dilihat orang laen bahkan saya yang punya

## J. Cuda Agent — Tool & Kemampuan
147. Tool prioritas v1 (pilih 6–8 dari daftar di plan §5.3)? → sebanyakn apapun yg bisa kamu buat
148. Tool browser (Playwright) masuk v1? → v1
149. Tool scraping Firecrawl langsung jadi tool agent? → ya
150. Tool generate gambar untuk agent? → perlu
151. Tool bikin PDF/DOCX/XLSX? → perlu
152. Tool git (commit/branch/push) + auto-push ke GitHub? → perlu+auto push
153. Tool deploy (Vercel/GitHub Pages) di v1? → v1
154. Tool kirim email/WhatsApp/Telegram? → perlu
155. Tool query database lokal (SQL)? → perlu
156. Tool RAG atas file workspace (tanya-jawab dokumen misi)? → perlu
157. Tool olah CSV/XLSX besar (100k baris)? → perlu
158. Tool convert file (docx→pdf, img→webp, dll)? → perlu
159. Tool monitoring uptime situs + alert? → perlu
160. Tool scrape sosmed (IG/TikTok) — sadar batasan ToS, tetap mau? → tidak
161. Tool OSINT (pakai scam-hunt yang sudah ada)? → perlu
162. Agent bisa simpan Playbook dari misi sukses (belajar sendiri)? → boleh
163. Tool jalankan skrip/plugin custom buatan user? → perlu
164. Perlu marketplace tool/plugin dari orang lain? → perlu

## K. Model, Provider & Routing
165. Urutan prioritas provider: TeamORouter, Ldrcloud, Meridian, Genspark — tulis urutannya → tidak ada urutan karna dimasukkan oleh user sendiri 2 nantinyya
166. Model default Cuda AI (cepat & murah)? → pake model default dari base url yg ditambahkan user sendiri
167. Model default Cuda Agent planner (reasoning kuat)? → pake model default dari base url yg ditambahkan user sendiri
168. Model untuk executor (murah & cepat)? → pake model default dari base url yg ditambahkan user sendiri
169. Model untuk summarizer/compressor? → pake model default dari base url yg ditambahkan user sendiri
170. User boleh ganti model per percakapan/misi? → boleh
171. Berapa model dalam rantai fallback sebelum menyerah? → diatur sendiri oleh user
172. Kalau semua provider down: pesan/aksi apa yang muncul? → bebas
173. Perlu limit token per user per hari? → tidak
174. Perlu BYO key (user bawa API key sendiri)? → perlu
175. Perlu expose endpoint OpenAI-compatible dari Cuda? → tidak
176. Markup billing Rupiah per token berapa persen? → 10%
177. Perlu model lokal (llama.cpp di STB) sebagai opsi offline? → tidak
178. Perlu prompt caching untuk hemat biaya? → opsionla bisa diaktifkan tapi default nonaktif

## L. Data, Akun & Auth
179. Metode login: email+password, magic link, Google OAuth, Telegram login? → tidak ada semuanya bebas bisa telegram email biasa dll nanti juga bisa kita update
180. Perlu mode tamu (tanpa login) di v1? → perlu
181. Perlu multi-device sync? → perlu
182. Data percakapan disimpan di server, lokal browser, atau dua-duanya? → dua-duanya
183. Perlu export semua data (GDPR-style)? → perlu
184. Perlu hapus akun self-service? → perlu
185. Perlu role admin terpisah? → perlu
186. Batas percakapan/misi untuk user gratis? → tidak ada karna basicnya ini juga gratis
187. Data user boleh dipakai untuk training/evaluasi? → tanya dulu
188. Perlu enkripsi at-rest untuk isi percakapan? → perlu
189. Perlu session timeout / 2FA? → tidak
190. Username publik untuk link share (mis. /share/c/ziee)? → slug acak saja

## M. Billing & Monetisasi
191. Model bisnis: gratis total, freemium, atau berbayar? → gratis by default
192. Kalau freemium: batas gratisnya apa (pesan/hari, misi/bulan)? → tidak ada karna basicnya tidak ada model yang tersedia untuk sekarang ser harus menambahkan model ia sendiri
193. Harga paket bulanan yang wajar (Rp)? → tidak ada
194. Metode bayar: QRIS, transfer bank, Midtrans, crypto? → belum ada
195. Pakai kredit (credit system) atau langganan flat? → belum ada
196. Perlu halaman invoice/riwayat pembayaran? → belum ada
197. Kuota agent dipisah dari kuota chat? → digabung
198. Perlu referral/affiliate? → tidak
199. Perlu free trial? → tidak
200. Biaya API upstream ditanggung siapa (kamu atau user)? → gak ada kaya ginian
201. Rate limit anti-abuse: berapa per menit? → tanpa limit tergantung token yg dikasukkan user maksud saya base url dan apikey dia
202. Perlu paket khusus mahasiswa? → tidak

## N. Desain Visual & Bahasa
203. Tema default: dark, light, atau ikut sistem? → ikut sistem
204. Light mode masuk v1? → v1
205. Font Inter + JetBrains Mono — oke? → oke
206. Density: Cuda AI lega, Cuda Agent padat — setuju? → setuju
207. Animasi/transisi: halus banyak, atau minim & cepat? → halus
208. Suara notifikasi saat misi selesai? → perlu
209. Notifikasi push browser? → perlu
210. Icon set Lucide — oke? → oke
211. Perlu ilustrasi/empty state custom (dibuatkan)? → perlu
212. Onboarding: wizard 3 langkah atau langsung pakai? → wizard
213. Landing marketing lengkap atau cuma redirect ke app? → lengkap
214. Perlu demo interaktif di landing? → perlu
215. Target aksesibilitas WCAG AA? → seadanya
216. Perlu keyboard shortcut lengkap + halaman cheat sheet? → perlu
217. User boleh ganti warna accent sendiri? → boleh
218. Ada referensi visual/situs yang kamu suka untuk jadi acuan? (kirim link) → bebasss kamu pakai referensi dari chatbot atau web bagus lainnya saja

## O. Mobile & PWA
219. Prioritas: desktop dulu atau mobile dulu? → dua-duanya tapi dekstop number 1
220. PWA installable di v1? → v1
221. Offline mode (baca riwayat tanpa internet)? → perlu
222. Cuda Agent di HP pakai tab bar (Misi/Aktivitas/Workspace/Serahan) — setuju? → setuju
223. Notifikasi HP saat misi selesai via bot Telegram? → perlu
224. Swipe gesture (arsip/hapus) di mobile? → tidak
225. Ukuran font default di HP? → kecil
226. Mode lanskap untuk lihat timeline + workspace bareng? → perlu
227. Perlu quick action share-ke-Cuda dari app lain? → perlu
228. App Android native nanti, atau PWA cukup? → PWA cukup

## P. Integrasi & Ekosistem
229. Integrasi wajib: GitHub, Telegram, Google Drive, Notion — pilih yang wajib v1 → bebas tidak ada integrasi wajib adanya opsiional
230. Perlu integrasi dengan project kamu yang lain (Meridian, masbraw-chat lama)? → belum sih sementara
231. Migrasi data dari masbraw-chat lama perlu? → tidak
232. Perlu bot Telegram sebagai front-end Cuda (chat lewat TG)? → perlu
233. Perlu integrasi WhatsApp? → perlu
234. Perlu integrasi kalender/tugas (Google Calendar, Todoist)? → perlu
235. Perlu webhook keluar (hasil misi dikirim ke endpoint kamu)? → perlu
236. Perlu API key Cuda untuk dipakai app lain? → perlu
237. Perlu integrasi Hermes (Cuda jadi tool Hermes, atau sebaliknya)? → Cuda jadi tool
238. MCP server mana yang mau dipasang dulu? → bebas brooo uang berguna aja dulu beberapa
239. Perlu integrasi pembayaran di v1? → nanti
240. Perlu kirim laporan via email? → tidak

## Q. Operasional, Monitoring & QA
241. Siapa yang maintain setelah jadi? → kamu + gue
242. Perlu CI/CD GitHub Actions untuk deploy otomatis? → perlu
243. Perlu staging environment terpisah? → perlu
244. Target test coverage? → seadanya
245. Load test: berapa misi paralel harus kuat? → 10
246. Kalau ada bug produksi, notif ke mana? → Telegram
247. Perlu halaman status publik (cek node hidup)? → perlu
248. Perlu dokumentasi user/help center di v1? → perlu
249. Perlu changelog publik? → perlu
250. Backup & restore drill berapa sering? → harian

## R. Roadmap & Masa Depan
251. Fitur apa yang kamu bayangkan ada 6 bulan lagi? → semua feature ai terbaru
252. Cuda mau jadi SaaS publik atau tetap personal tool? → dua-duanya
253. Kalau sukses, buka versi untuk tim/kantor (Cuda Teams)? → ya
254. Perlu versi enterprise/on-premise? → belum
255. Perlu mobile app native? → nanti jai software dekstop dan mobile aps
256. Perlu marketplace playbook/tool dari komunitas? → perlu
257. Perlu Cuda belajar dari percakapan lama kamu (fine-tune/RAG personal)? → perlu dan bisa buat skill sendiri mupun save memory
258. Perlu multi-agent kolaborasi (beberapa agent kerja bareng di satu misi)? → sangatt perlu
259. Perlu agent bisa jual jasa (agent-as-a-service ke klien)? → kurang mengerti
260. Milestone 3 bulan / 6 bulan / 1 tahun? → 2-3 bulan
261. Ada fitur besar lain yang mau kamu tambahkan sekarang? → masih bingung kalau kamu mau menambahkan bisa ajaaaa
262. Ada hal yang HARAM dilakukan Cuda (batasan keras dari kamu)? → belum ada sebenernya


---
---

# ════ SELESAI ════

Semua yang kamu butuhkan sudah ada di file ini + repo `https://github.com/Xiaochown/cuda`.

**Langkah pertamamu sekarang:** `git clone https://github.com/Xiaochown/cuda.git && cd cuda`

Lalu kerjakan **TASKS P0-1** (lihat Bagian 4). Satu task = satu commit.
Lapor ke user dalam Bahasa Indonesia casual tiap phase selesai.
