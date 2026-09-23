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
