#!/usr/bin/env python3
"""Generate the Kouzia-styled SVG cards used in README.md.

Run from the repo root:  python3 scripts/build_cards.py
Edit the CONTENT section below, then re-run and commit assets/.
"""
import base64
import io
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
FONTS = OUT / "fonts"

# ── Theme (from kouzia.com) ──────────────────────────────────────────────
BG, SURFACE, SURFACE2 = "#0b1020", "#121a2e", "#19233c"
TEXT, MUTED, LABEL = "#e8eaf8", "#9aa1bf", "#c0c5dc"
LINE, LINE_STRONG = "#232d47", "#3a4566"
ACCENT, INDIGO = "#fe9a00", "#8b93ff"
UI = "'Exo 2',system-ui,'Segoe UI',Roboto,sans-serif"
MONO = "'Share Tech Mono',ui-monospace,Menlo,Consolas,monospace"

# ── CONTENT ──────────────────────────────────────────────────────────────
BANNER = {
    "tagline": "Custom websites and software that work for you.",
    "meta": "INDEPENDENT WEB DEVELOPER · HUELGOAT · BRITTANY, FRANCE",
}

ABOUT = {
    "label": "ABOUT",
    "title": "Hi, I'm Alexandre.",
    "text": (
        "From Huelgoat, in the heart of Brittany's Monts d'Arrée, I build websites "
        "and custom software for local non-profits, public bodies and businesses. "
        "Simple, fast and accessible tools, built without relying on Big Tech whenever possible."
    ),
    "stack": ["TypeScript", "React", "Astro", "Tailwind", "Node.js", "Fastify",
              "PHP", "Go", "PostgreSQL", "Electron", "Tauri", "Linux"],
}

FEATURED = [
    {"file": "vigie-bot", "label": "DISCORD BOT", "title": "Vigie Bot",
     "text": "A free Discord bot for streamers: Twitch & YouTube live alerts, clips, schedule, moderation and temporary voice channels.",
     "tags": ["Twitch", "YouTube", "Discord"], "link": "vigiebot.kouzia.com"},
    {"file": "capsuleos", "label": "WEB APP", "title": "CapsuleOS",
     "text": "Try out desktop environments in your browser, learn them by playing and find the one that suits you.",
     "tags": ["JavaScript", "PHP", "MySQL"], "link": "os.lacapsule.org"},
    {"file": "tracebay", "label": "DESKTOP SOFTWARE", "title": "Tracebay",
     "text": "IT hardware traceability software, used daily by La Capsule's refurbishing workshop in Morlaix.",
     "tags": ["Electron", "Fastify", "PostgreSQL"], "link": "tracebay.kouzia.com"},
    {"file": "gobox", "label": "DIAGNOSTIC TOOL", "title": "GoBox",
     "text": "A hardware diagnostic tool built for La Capsule's computer refurbishing workshop.",
     "tags": ["Go", "Fyne"], "link": "demo-gobox.kouzia.com"},
]

SIDE = [
    {"file": "kouziaconverter", "label": "OPEN SOURCE", "title": "KouziaConverter",
     "text": "Convert videos, images and icons locally, without uploading anything.",
     "tags": ["Local-first", "Privacy"], "link": "github.com/k0uzia/KouziaConverter"},
    {"file": "safenet", "label": "OPEN SOURCE", "title": "Safenet",
     "text": "A fake \"hacker\" terminal for cybersecurity awareness escape games aimed at young people.",
     "tags": ["JavaScript", "Education"], "link": "github.com/k0uzia/Safenet"},
]

SITES = {
    "label": "ON THE WEB",
    "title": "Websites I've built",
    "link": "kouzia.com/realisations",
    "sites": ["ESS29", "La Capsule", "Morlaix Communauté", "ULAMIR CPIE", "SSA Pays de Morlaix"],
}

CONTACT = {
    "title": "Got a project in mind?",
    "text": "Free quote, no strings attached. Reply within 24 to 48 hours.",
    "cta": "contact@kouzia.com",
}

# ── Rendering helpers ────────────────────────────────────────────────────
try:
    from fontTools import subset as _subset
    from fontTools.ttLib import TTFont
except ImportError:  # fonts are embedded whole without fontTools
    _subset = None


def font_data(path: Path, chars: str) -> str:
    raw = path.read_bytes()
    if _subset:
        try:
            font = TTFont(io.BytesIO(raw))
            opts = _subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["*"]
            sub = _subset.Subsetter(opts)
            sub.populate(text=chars + " ")
            sub.subset(font)
            buf = io.BytesIO()
            font.flavor = "woff2"
            font.save(buf)
            raw = buf.getvalue()
        except Exception:
            pass
    return base64.b64encode(raw).decode()


def wrap(text: str, size: float, width: float, ratio: float = 0.5) -> list[str]:
    max_chars = int(width / (size * ratio))
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > max_chars:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def chips(items, x, y, max_x, size=15, gap=10, h=32, color=LABEL, mono=False):
    out, cx, cy = [], x, y
    ratio = 0.56 if mono else 0.55
    for item in items:
        w = len(item) * size * ratio + 28
        if cx + w > max_x:
            cx, cy = x, cy + h + gap
        out.append(
            f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="{h}" rx="{h/2}" '
            f'fill="{SURFACE2}" stroke="{LINE_STRONG}"/>'
            f'<text x="{cx + w/2:.0f}" y="{cy + h/2 + size*0.36:.1f}" text-anchor="middle" '
            f'class="{"chipm" if mono else "chip"}" fill="{color}">{escape(item)}</text>'
        )
        cx += w + gap
    return "".join(out), cy + h


def svg(width, height, body, chars, label="Kouzia"):
    exo = font_data(FONTS / "exo2-latin.woff2", chars)
    stm = font_data(FONTS / "share-tech-mono-latin.woff2", chars)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">
<defs>
<style>
@font-face {{ font-family:'Exo 2'; font-weight:400 700; src:url(data:font/woff2;base64,{exo}) format('woff2'); }}
@font-face {{ font-family:'Share Tech Mono'; src:url(data:font/woff2;base64,{stm}) format('woff2'); }}
.label {{ font:15px {MONO}; letter-spacing:.14em; fill:{ACCENT}; }}
.title {{ font:700 30px {UI}; fill:{TEXT}; }}
.body  {{ font:400 18px {UI}; fill:{MUTED}; }}
.chip  {{ font:600 15px {UI}; }}
.chipm {{ font:15px {MONO}; }}
.link  {{ font:17px {MONO}; fill:{ACCENT}; }}
.logo  {{ font:84px {MONO}; letter-spacing:.06em; }}
.sub   {{ font:600 28px {UI}; fill:{TEXT}; }}
.meta  {{ font:600 17px {UI}; fill:{MUTED}; letter-spacing:.12em; }}
.cursor {{ animation:blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity:0; }} }}
</style>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb900"/><stop offset=".55" stop-color="#fe9a00"/><stop offset="1" stop-color="#f07800"/></linearGradient>
<radialGradient id="gi" cx=".85" cy=".1" r=".6"><stop offset="0" stop-color="#615fff" stop-opacity=".2"/><stop offset="1" stop-color="#615fff" stop-opacity="0"/></radialGradient>
<radialGradient id="ga" cx=".05" cy=".3" r=".5"><stop offset="0" stop-color="#fe9a00" stop-opacity=".14"/><stop offset="1" stop-color="#fe9a00" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-opacity=".5"/></pattern>
<clipPath id="card"><rect width="{width}" height="{height}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{width}" height="{height}" fill="{BG}"/>
<rect width="{width}" height="{height}" fill="url(#grid)"/>
<rect width="{width}" height="{height}" fill="url(#gi)"/>
<rect width="{width}" height="{height}" fill="url(#ga)"/>
</g>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="22" fill="none" stroke="{LINE}"/>
{body}
</svg>
'''


def write(name, content):
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"assets/{name}.svg  {len(content) // 1024} KiB")


# ── Cards ────────────────────────────────────────────────────────────────
def banner():
    body = (
        f'<text x="80" y="138" class="logo"><tspan fill="{ACCENT}">&lt;</tspan>'
        f'<tspan fill="{TEXT}">Kouzia</tspan><tspan fill="{ACCENT}">/&gt;</tspan>'
        f'<tspan fill="{ACCENT}" class="cursor">_</tspan></text>'
        f'<rect x="80" y="164" width="96" height="4" rx="2" fill="url(#accent)"/>'
        f'<text x="80" y="214" class="sub">{escape(BANNER["tagline"])}</text>'
        f'<text x="80" y="254" class="meta">{escape(BANNER["meta"])}</text>'
    )
    chars = "<Kouzia/>_" + BANNER["tagline"] + BANNER["meta"]
    write("kouzia-banner", svg(1200, 300, body, chars, "Kouzia — " + BANNER["tagline"]))


def about():
    W, P = 1200, 64
    lines = wrap(ABOUT["text"], 20, W - 2 * P, 0.43)
    y = 150
    text = "".join(
        f'<text x="{P}" y="{y + i * 32}" class="body" style="font-size:20px">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    sy = y + len(lines) * 32 + 20
    stack, end = chips(ABOUT["stack"], P, sy, W - P, gap=8, mono=True)
    H = end + 56
    body = (
        f'<text x="{P}" y="76" class="label">{ABOUT["label"]}</text>'
        f'<text x="{P}" y="118" class="title" style="font-size:34px">{escape(ABOUT["title"])}</text>'
        + text + stack
    )
    chars = ABOUT["label"] + ABOUT["title"] + ABOUT["text"] + "".join(ABOUT["stack"])
    write("about", svg(W, H, body, chars, ABOUT["title"] + " " + ABOUT["text"]))


def project(p, H=300):
    W, P = 600, 40
    lines = wrap(p["text"], 18, W - 2 * P, 0.46)
    desc = "".join(
        f'<text x="{P}" y="{136 + i * 28}" class="body">{escape(l)}</text>' for i, l in enumerate(lines)
    )
    tags, _ = chips(p["tags"], P, H - 96, W - P)
    body = (
        f'<rect x="{P}" y="40" width="40" height="4" rx="2" fill="url(#accent)"/>'
        f'<text x="{P}" y="72" class="label">{escape(p["label"])}</text>'
        f'<text x="{P}" y="108" class="title">{escape(p["title"])}</text>'
        + desc + tags
        + f'<text x="{P}" y="{H - 30}" class="link">{escape(p["link"])} →</text>'
    )
    chars = p["label"] + p["title"] + p["text"] + "".join(p["tags"]) + p["link"] + "→"
    write(f"card-{p['file']}", svg(W, H, body, chars, f'{p["title"]} — {p["text"]}'))


def sites():
    W, P = 1200, 64
    row, end = chips(SITES["sites"], P, 132, W - P, size=18, h=42, gap=14, color=TEXT)
    body = (
        f'<text x="{P}" y="76" class="label">{SITES["label"]}</text>'
        f'<text x="{P}" y="112" class="title">{escape(SITES["title"])}</text>'
        f'<style>.chip{{font-size:18px}}</style>' + row
        + f'<text x="{P}" y="{end + 46}" class="link">{SITES["link"]} →</text>'
    )
    chars = SITES["label"] + SITES["title"] + "".join(SITES["sites"]) + SITES["link"] + "→"
    write("sites", svg(W, end + 84, body, chars, SITES["title"] + ": " + ", ".join(SITES["sites"])))


def contact():
    W, H = 1200, 220
    cta = CONTACT["cta"]
    bw = len(cta) * 19 * 0.56 + 56
    body = (
        f'<text x="{W/2}" y="82" text-anchor="middle" class="title" style="font-size:34px">{escape(CONTACT["title"])}</text>'
        f'<text x="{W/2}" y="118" text-anchor="middle" class="body">{escape(CONTACT["text"])}</text>'
        f'<rect x="{(W - bw)/2:.0f}" y="142" width="{bw:.0f}" height="48" rx="24" fill="url(#accent)"/>'
        f'<text x="{W/2}" y="173" text-anchor="middle" style="font:19px {MONO};fill:#1a1103">{escape(cta)}</text>'
    )
    chars = CONTACT["title"] + CONTACT["text"] + cta
    write("contact", svg(W, H, body, chars, CONTACT["title"] + " " + cta))


if __name__ == "__main__":
    banner()
    about()
    for p in FEATURED + SIDE:
        project(p)
    sites()
    contact()
