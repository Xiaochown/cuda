#!/usr/bin/env python3
"""Build dark-Linear HTML pages for the CUDA plan (index.html + research.html)."""
import html, os, re, shutil

SRC = "/root/cuda-ai"
OUT = "/root/cuda-ai/site"
os.makedirs(f"{OUT}/mockups", exist_ok=True)

CSS = """
:root{--bg:#0b0d10;--surface:#15171b;--surface2:#1b1e23;--border:#2a2e35;--border2:#343941;
--text:#e6e8eb;--dim:#9aa3af;--mute:#6b7280;--accent:#5e6ad2;--accent2:#8b5cf6;--blue:#4f8cff;
--ok:#22c55e;--warn:#f5a524;--err:#ef4444;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.7 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.wrap{display:flex;max-width:1400px;margin:0 auto;gap:0}
nav{position:sticky;top:0;align-self:flex-start;width:290px;flex:0 0 290px;height:100vh;overflow-y:auto;
padding:26px 18px 60px;border-right:1px solid var(--border);background:#0d0f13}
nav .brand{display:flex;align-items:center;gap:10px;margin-bottom:22px}
nav .mark{width:26px;height:26px;border-radius:7px;background:linear-gradient(135deg,var(--accent),var(--accent2));
display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#fff}
nav .brand b{font-size:15px;letter-spacing:-.2px}
nav .brand span{display:block;font-size:11px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
nav a{display:block;color:var(--dim);font-size:13px;padding:4px 8px;border-radius:6px;margin:1px 0}
nav a:hover{background:var(--surface);color:var(--text);text-decoration:none}
nav .sec{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:16px 8px 6px}
main{flex:1;min-width:0;padding:44px 46px 120px;max-width:1000px}
.kicker{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:600}
h1{font-size:34px;line-height:1.2;letter-spacing:-.7px;margin:10px 0 6px}
h2{font-size:21px;letter-spacing:-.35px;margin:52px 0 12px;padding-top:20px;border-top:1px solid var(--border)}
h3{font-size:16.5px;margin:30px 0 8px}
h4{font-size:14.5px;margin:22px 0 6px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em}
p{margin:11px 0}
ul,ol{margin:11px 0;padding-left:22px}li{margin:5px 0}
code{font-family:var(--mono);font-size:12.5px;background:var(--surface2);border:1px solid var(--border);
padding:1.5px 5px;border-radius:5px;color:#c9d1d9}
pre{background:#0f1216;border:1px solid var(--border);border-radius:10px;padding:16px 18px;overflow-x:auto;margin:16px 0}
pre code{background:none;border:0;padding:0;font-size:12.5px;line-height:1.6;color:#c9d1d9;white-space:pre}
blockquote{margin:16px 0;padding:12px 18px;border-left:2px solid var(--accent2);background:#12141a;
border-radius:0 8px 8px 0;color:#cfd4dc}
blockquote p{margin:4px 0}
hr{border:0;border-top:1px solid var(--border);margin:34px 0}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.5px}
th,td{border:1px solid var(--border);padding:8px 11px;text-align:left;vertical-align:top}
th{background:var(--surface);color:var(--dim);font-size:11.5px;letter-spacing:.05em;text-transform:uppercase}
tr:nth-child(even) td{background:#101216}
strong{color:#fff;font-weight:600}
.hero{background:linear-gradient(180deg,#141821,#0e1116);border:1px solid var(--border);border-radius:14px;
padding:26px 28px;margin:0 0 30px}
.hero .sub{color:var(--dim);font-size:15px;margin:8px 0 0}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.badge{font-size:11.5px;padding:4px 10px;border-radius:20px;border:1px solid var(--border2);color:var(--dim);
background:#12151b}
.badge.b{border-color:#2a4a7a;color:#8ab4f8}.badge.v{border-color:#4a3170;color:#c4a6ff}
.badge.g{border-color:#1f5136;color:#7ee2a8}.badge.a{border-color:#5c4318;color:#f3c078}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:20px 0}
figure{margin:0;border:1px solid var(--border);border-radius:12px;overflow:hidden;background:var(--surface)}
figure img{width:100%;display:block}
figcaption{padding:10px 14px;font-size:12.5px;color:var(--dim);border-top:1px solid var(--border)}
.note{border:1px solid #4a3170;background:#161226;border-radius:10px;padding:14px 18px;margin:20px 0}
.note b{color:#c4a6ff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.card{border:1px solid var(--border);background:var(--surface);border-radius:12px;padding:16px 18px}
.card h3{margin:0 0 8px;font-size:15px}
.card ul{margin:8px 0 0;padding-left:18px;font-size:13.5px}
footer{color:var(--mute);font-size:12.5px;border-top:1px solid var(--border);margin-top:60px;padding-top:20px}
@media(max-width:960px){nav{display:none}main{padding:26px 18px 90px}h1{font-size:26px}.grid2{grid-template-columns:1fr}}
"""


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"(?<![\"=>])(https?://[^\s<)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    return t


def md_to_html(md):
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + esc("\n".join(buf)) + "</code></pre>")
            continue
        if re.match(r"^\|.*\|$", ln) and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1]):
            head = [c.strip() for c in ln.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and re.match(r"^\|.*\|$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
            t = ["<table><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1)); txt = m.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")[:60]
            out.append(f'<h{lvl} id="{anchor}">{inline(txt)}</h{lvl}>')
            i += 1
            continue
        if re.match(r"^[-*]\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                buf.append(re.sub(r"^[-*]\s+", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\d+\.\s+", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ol>")
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip()); i += 1
            out.append("<blockquote>" + "".join(f"<p>{inline(b)}</p>" for b in buf if b) + "</blockquote>")
            continue
        if ln.strip() == "---":
            out.append("<hr>"); i += 1; continue
        if ln.strip() == "":
            i += 1; continue
        out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "\n".join(out)


def toc(md):
    items = []
    for m in re.finditer(r"^(#{2,3})\s+(.*)$", md, re.M):
        lvl, txt = len(m.group(1)), m.group(2)
        anchor = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")[:60]
        items.append((lvl, txt, anchor))
    return items


def page(title, kicker, md, nav_extra="", hero=""):
    nav = [f'<div class="brand"><div class="mark">C</div><div><b>Cuda</b><span>plan &amp; riset</span></div></div>',
           '<a href="decisions.html">✅ Keputusan Terkunci</a>',
           '<a href="index.html">📋 Plan Implementasi v2</a>',
           '<a href="research.html">🔎 Riset &amp; Sumber</a>',
           '<a href="mockups.html">🎨 Mockup</a>',
           '<a href="questionnaire/">📝 Kuesioner 262 Pertanyaan</a>',
           '<div class="sec">Isi halaman</div>']
    for lvl, txt, anchor in toc(md):
        pad = "padding-left:8px" if lvl == 2 else "padding-left:20px;font-size:12.5px"
        nav.append(f'<a href="#{anchor}" style="{pad}">{esc(txt[:52])}</a>')
    body = md_to_html(md)
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — Cuda</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<nav>{''.join(nav)}</nav>
<main><div class="kicker">{esc(kicker)}</div>{hero}{body}
<footer>Cuda — plan v1.0 · dibuat 23 Sep 2026 · sumber riset: Firecrawl (lihat <a href="research.html">Riset &amp; Sumber</a>)</footer>
</main></div></body></html>"""


hero = """<h1>Cuda — Implementation Plan</h1>
<div class="hero"><p class="sub">Dua produk, dua page, dua mental model: <strong>Cuda AI</strong> (workspace chat biasa)
dan <strong>Cuda Agent</strong> (agentic console). Dibangun dari nol dengan fondasi riset 2026.</p>
<div class="badges"><span class="badge b">Next.js 16 + TS + Tailwind 4</span>
<span class="badge v">Fastify agent-node + WS</span><span class="badge g">SQLite/Postgres + Prisma</span>
<span class="badge a">12 Agent UX patterns</span><span class="badge">Estimasi 10–16 hari</span>
<span class="badge">Status: menunggu approval</span></div></div>"""

plan = open(f"{SRC}/PLAN.md").read()
# strip the top H1 (replaced by hero) and the leading quote line for cleanliness
plan = re.sub(r"^# CUDA.*?\n", "", plan, count=1)
research = open(f"{SRC}/docs/RESEARCH.md").read()
research = re.sub(r"^# CUDA.*?\n", "", research, count=1)

open(f"{OUT}/index.html", "w").write(page("Implementation Plan v2", "cuda · plan implementasi v2", plan, hero=hero))
decisions = open(f"{SRC}/docs/DECISIONS.md").read()
decisions = re.sub(r"^# CUDA.*?\n", "", decisions, count=1)
open(f"{OUT}/decisions.html", "w").write(
    page("Keputusan Terkunci", "cuda · decision record", decisions,
         hero='<h1>Keputusan Terkunci</h1><div class="hero"><p class="sub">Hasil ekstraksi 262 jawaban kuesioner: '
              '5 pivot besar, keputusan per bagian, 8 flag konflik, capability map 16 grup, dan 5 terobosan.</p>'
              '<div class="badges"><span class="badge b">262/262 terjawab</span>'
              '<span class="badge g">MVP 2 minggu</span><span class="badge v">Desktop-first</span>'
              '<span class="badge a">BYOE · gratis</span></div></div>'))
open(f"{OUT}/research.html", "w").write(
    page("Riset & Sumber", "cuda · riset", research,
         hero='<h1>Riset &amp; Sumber</h1><div class="hero"><p class="sub">15 query Firecrawl + ~40 halaman '
              'dibaca. Semua keputusan arsitektur di plan punya rujukan di sini.</p></div>'))

for f in os.listdir(f"{SRC}/mockups"):
    shutil.copy(f"{SRC}/mockups/{f}", f"{OUT}/mockups/{f}")

gal = """<h1>Mockup Visual</h1><div class="hero"><p class="sub">Tiga arah tampilan yang digenerate dengan
<code>gpt-image-2.5-sunburst</code>. Ini acuan visual untuk build nyata — token warna, layout, dan komponen
akan diambil dari sini.</p></div>
<h2>1 · Cuda Agent — Desktop (console 3-pane)</h2>
<p>Perhatikan: <strong>activity timeline terpisah dari chat</strong> (keputusan arsitektur utama), kartu
<strong>BUTUH IZIN</strong> dengan tombol Setujui/Edit/Tolak, kartu <strong>Struk aksi</strong> dengan diff +
Undo, kontrol Jalan/Jeda/Stop, slider otonomi, dan meter budget.</p>
<figure><img src="mockups/cuda-agent-desktop.jpg" alt="Cuda Agent desktop console">
<figcaption>Cuda Agent · desktop · accent violet #8b5cf6 · timeline + workspace + approval + receipt</figcaption></figure>
<h2>2 · Cuda Agent — Mobile</h2>
<p>Tab bar (Misi/Aktivitas/Workspace/Akun), kartu timeline versi mobile, sheet izin dengan tiga tombol
full-width, dan meter budget menempel di atas tab bar.</p>
<figure><img src="mockups/cuda-agent-mobile.jpg" alt="Cuda Agent mobile">
<figcaption>Cuda Agent · mobile · timeline + kartu izin + tab bar</figcaption></figure>
<h2>3 · Cuda AI — Desktop (workspace chat)</h2>
<p>Idiom ChatGPT/Claude: sidebar percakapan + Ruang Kerja, jawaban AI polos (bukan bubble), tabel markdown,
sitasi bernomor, composer pill mengambang dengan chip model &amp; toggle konteks 1M, dan panel kanan
<strong>Hasil</strong> berisi artifact dengan version strip v1/v2/v3 + tombol Publish.</p>
<figure><img src="mockups/cuda-ai-desktop.jpg" alt="Cuda AI desktop">
<figcaption>Cuda AI · desktop · accent biru #4f8cff · chat + artifact panel</figcaption></figure>
<h2>Yang perlu lo putuskan dari mockup ini</h2>
<ul>
<li>Accent dua room (biru vs violet) — setuju, atau mau satu warna brand aja?</li>
<li>Density Cuda Agent (padat, banyak info) vs Cuda AI (lega) — pas?</li>
<li>Istilah Indonesia (Misi / Langkah / Izin / Struk / Serahan) — pakai, atau campur Inggris?</li>
<li>Layout mobile Cuda Agent pakai tab bar — oke?</li>
</ul>
<div class="note"><b>Catatan:</b> mockup ini menjawab pertanyaan <em>"bentuknya udah bener belum"</em>, bukan
<em>"fungsinya jalan"</em>. Interaksi nyata (streaming, pause, rollback) baru ada di build.</div>
"""
open(f"{OUT}/mockups.html", "w").write(page("Mockup", "cuda · arah visual", gal))
print("built:", os.listdir(OUT))
