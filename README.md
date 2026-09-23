# CUDA — dokumen produk & rencana

Repo ini berisi **rencana, riset, keputusan produk, mockup, dan kuesioner** untuk project **Cuda**.

## Isi
- `PLAN.md` — Implementation Plan v2 (14 hari, 40 task bite-sized)
- `docs/RESEARCH.md` — riset Firecrawl (15 query, ~40 halaman) + temuan lingkungan
- `docs/DECISIONS.md` — decision record dari kuesioner 262 pertanyaan (5 pivot, 8 flag, capability map 16 grup, 5 terobosan)
- `docs/ANSWERS.md` — jawaban mentah 262/262
- `mockups/` — 3 mockup visual (Cuda Agent desktop/mobile, Cuda AI desktop)
- `questionnaire/` — builder kuesioner 262 pertanyaan (HTML interaktif + MD + CSV)
- `site/` — SSG-lite yang bikin halaman HTML plan/riset/keputusan/mockup (port 9400)

## Produk dalam satu paragraf
**Cuda** adalah aplikasi AI local-first dengan dua room terpisah: **Cuda AI** (workspace chat biasa) dan **Cuda Agent** (agentic console: goal → plan → eksekusi dengan tools → deliverable). Prinsipnya: **BYOE** (user bawa base_url + API key sendiri, Cuda gratis), **local-first/desktop-first**, **Skills via `/`** (Cuda bisa menulis skill sendiri), dan **setiap aksi punya receipt + undo**.

## Status
- Keputusan produk: **LOCKED** (dari 262 jawaban)
- Target MVP: **2 minggu**
- Menunggu keputusan hosting (VPS / laptop / STB) sebelum P0 dieksekusi
