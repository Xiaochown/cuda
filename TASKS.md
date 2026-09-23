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
