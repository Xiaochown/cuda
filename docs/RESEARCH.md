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
