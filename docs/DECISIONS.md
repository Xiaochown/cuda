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
