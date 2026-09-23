# CUDA

Rencana, riset, keputusan produk, mockup, dan **brief eksekusi** untuk project **Cuda** — aplikasi AI local-first dengan dua room terpisah: **Cuda AI** (workspace chat) dan **Cuda Agent** (agentic console).

## 🚀 Kalau kamu AI agent yang mau mengeksekusi project ini

Baca berurutan:
1. **`AGENT_BRIEF.md`** — brief utama (aturan keras, stack, cara kerja, definition of done)
2. **`docs/DECISIONS.md`** — 262 keputusan produk yang sudah LOCKED (sumber kebenaran)
3. **`PLAN.md`** — arsitektur, spec tiap room, event protocol, data model, rencana 14 hari
4. **`TASKS.md`** — checklist 38 task yang harus dikerjakan (update checkbox-nya)
5. **`docs/SETUP_LAPTOP.md`** — setup environment (WSL2 + Node 22 + gh)
6. **`docs/RESEARCH.md`** — dasar riset desain

Prompt siap-paste: **`PROMPT.md`**

## Isi repo

| File | Isi |
|---|---|
| `AGENT_BRIEF.md` | Brief eksekusi untuk AI agent (aturan keras, guardrail, DoD) |
| `PROMPT.md` | Prompt siap-paste ke agent |
| `TASKS.md` | 38 task (P0–P3) dengan acceptance criteria + checkbox |
| `PLAN.md` | Implementation Plan v2 (14 hari) |
| `docs/DECISIONS.md` | Decision record: 5 pivot, 8 flag, capability map 16 grup, 5 terobosan |
| `docs/RESEARCH.md` | Riset Firecrawl (15 query, ~40 halaman) + temuan lingkungan |
| `docs/ANSWERS.md` | Jawaban mentah kuesioner 262/262 |
| `docs/SETUP_LAPTOP.md` | Setup WSL2/Node 22/gh/Playwright + pitfall |
| `mockups/` | 3 mockup visual (Cuda Agent desktop/mobile, Cuda AI desktop) |
| `questionnaire/` | Builder kuesioner 262 pertanyaan (HTML interaktif + MD + CSV) |
| `site/` | SSG-lite halaman dokumen (plan/riset/keputusan/mockup), serve port 9400 |

## Produk dalam satu paragraf

**Cuda** = aplikasi AI **local-first** dengan dua room: **Cuda AI** (chat workspace: percakapan, projects, artifacts, memory, skills) dan **Cuda Agent** (console 3-pane: goal → plan → eksekusi dengan tools → deliverable nyata, dengan permission gate, receipt+undo, checkpoint, dan budget guard).

Prinsip yang mengunci semua keputusan:
- **BYOE** — user bawa `base_url` + `api_key` sendiri; Cuda gratis, tanpa billing/kuota/rate limit
- **Local-first & desktop-first** — SQLite + IndexedDB, PWA, nanti di-package jadi software desktop
- **Skills via `/`** — bukan prompt library; Cuda bisa menulis skill sendiri dari misi sukses
- **Pisahkan conversation stream dari activity stream** — Cuda Agent console, bukan chat
- **Setiap aksi punya Receipt + Undo** — trust dari transparansi

## Status

- Keputusan produk: **LOCKED** (dari 262 jawaban kuesioner)
- Target MVP: **2 minggu** · Cuda AI dulu, baru Cuda Agent
- Hosting: web → Vercel · agent-node → laptop (dev) / STB Armbian (24/7)
