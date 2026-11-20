"""Builds the profile README graphics (assets/*.svg) from the brand files.

    pip install pillow
    python tools/build.py

Brand colours come from each product's own theme:
  Sellora Tech  - E:/Sellora src/app/globals.css (--ink, --accent, ...)
  Bikroyee      - frontend/src/app/globals.css (--brand-*, --accent-*)
  Amar Restora  - src/app/globals.css (--color-ink, --color-paper, saffron dot)
Logos are embedded as data URIs because GitHub blocks external files inside SVGs.
"""
import base64
import io
import re
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "tools" / "brand"
OUT = ROOT / "assets"

SANS = "'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'SF Mono', Menlo, 'Courier New', monospace"

SELLORA = dict(ink="#07080a", soft="#0d0f13", raised="#13161c", muted="#8e97a4",
               accent="#0062e0", hover="#0a6bf0", light="#35b4fd", dark="#003593")
BIKROYEE = dict(b950="#061c49", b900="#0a2d78", b700="#0041b5", b600="#1f42f2",
                b500="#3765fc", b300="#91b6ff", lime="#93d207", lime4="#a3e024", lime2="#d7f791")
RESTORA = dict(ink="#1b1916", paper="#f6f3ec", saffron="#e8a66a", accent="#c2621b",
               night="#141311", night2="#1d1b18", night3="#27241f", line="#34302a", muted="#8f887c")


def png_uri(name, size):
    """Trim transparent edges, square it, downscale, return a PNG data URI."""
    im = Image.open(BRAND / name).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    w, h = im.size
    s = max(w, h)
    sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sq.paste(im, ((s - w) // 2, (s - h) // 2))
    buf = io.BytesIO()
    sq.resize((size, size), Image.LANCZOS).save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def inline_svg(name, x, y, height):
    """Place an SVG logo (outlined paths) inside another SVG at a given height."""
    src = (BRAND / name).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    vw, vh = (float(v) for v in vb.split()[2:])
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    width = vw * height / vh
    return f'<svg x="{x}" y="{y}" width="{width:.1f}" height="{height}" viewBox="{vb}">{inner}</svg>', width


SELLORA_LOGO = png_uri("sellora-logo.png", 160)
BIKROYEE_LOGO = png_uri("bikroyee-logo.png", 112)
BIKROYEE_LOGO_SM = png_uri("bikroyee-logo.png", 40)


# --------------------------------------------------------------------- banner

def banner():
    S, K = SELLORA, BIKROYEE
    tx = 232                                    # left edge of the text column
    w1, w2, w3 = 576, 560, 560                  # typed line widths (textLength)
    cur = lambda w: tx + w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-label="Sellora Tech: AI sales agents, restaurant systems and open-source tools, built in Bangladesh">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{S['ink']}"/><stop offset="1" stop-color="{S['soft']}"/></linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="{S['light']}"/><stop offset="1" stop-color="{S['accent']}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.25 0;0.25 0;-0.25 0" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="ai" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{K['b600']}"/><stop offset="1" stop-color="{K['b500']}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{S['light']}" stop-opacity="0.7"/><stop offset="1" stop-color="{S['accent']}" stop-opacity="0.15"/></linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{S['light']}" stroke-opacity="0.06"/></pattern>
    <clipPath id="frame"><rect width="1200" height="340" rx="24"/></clipPath>
    <clipPath id="screen"><rect x="905" y="52" width="190" height="236" rx="18"/></clipPath>
    <clipPath id="t1"><rect x="{tx}" y="196" height="40" width="0"><animate attributeName="width" dur="12s" repeatCount="indefinite" values="0;{w1};{w1};0;0" keyTimes="0;0.12;0.29;0.33;1"/></rect></clipPath>
    <clipPath id="t2"><rect x="{tx}" y="196" height="40" width="0"><animate attributeName="width" dur="12s" repeatCount="indefinite" values="0;0;{w2};{w2};0;0" keyTimes="0;0.333;0.453;0.623;0.663;1"/></rect></clipPath>
    <clipPath id="t3"><rect x="{tx}" y="196" height="40" width="0"><animate attributeName="width" dur="12s" repeatCount="indefinite" values="0;0;{w3};{w3};0;0" keyTimes="0;0.666;0.786;0.956;0.996;1"/></rect></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1200" height="340" fill="url(#bg)"/>
    <rect width="1200" height="340" fill="url(#grid)"/>
    <g filter="url(#blur)" opacity="0.6">
      <circle cx="140" cy="140" r="150" fill="{S['accent']}"><animateTransform attributeName="transform" type="translate" values="0 0;80 40;0 0" dur="14s" repeatCount="indefinite"/></circle>
      <circle cx="760" cy="320" r="170" fill="{S['dark']}"><animateTransform attributeName="transform" type="translate" values="0 0;-110 -40;0 0" dur="18s" repeatCount="indefinite"/></circle>
      <circle cx="1060" cy="30" r="120" fill="{S['light']}" opacity="0.7"><animateTransform attributeName="transform" type="translate" values="0 0;-60 70;0 0" dur="16s" repeatCount="indefinite"/></circle>
    </g>

    <image href="{SELLORA_LOGO}" x="66" y="66" width="148" height="148">
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="6s" repeatCount="indefinite"/>
    </image>

    <text x="{tx + 2}" y="96" font-family="{MONO}" font-size="15" letter-spacing="4" fill="{S['muted']}">HELLO WORLD, WE ARE</text>
    <text x="{tx - 2}" y="170" font-family="{SANS}" font-size="80" font-weight="800" fill="url(#title)" filter="url(#glow)">Sellora Tech</text>

    <g font-family="{MONO}" font-size="27" fill="#e2e8f0">
      <text x="{tx}" y="226" textLength="{w1}" lengthAdjust="spacingAndGlyphs" clip-path="url(#t1)"><tspan fill="{S['light']}">&gt;</tspan> AI sales agents for online sellers</text>
      <text x="{tx}" y="226" textLength="{w2}" lengthAdjust="spacingAndGlyphs" clip-path="url(#t2)"><tspan fill="{S['light']}">&gt;</tspan> Restaurant systems for Bangladesh</text>
      <text x="{tx}" y="226" textLength="{w3}" lengthAdjust="spacingAndGlyphs" clip-path="url(#t3)"><tspan fill="{S['light']}">&gt;</tspan> Open-source tools for low-end PCs</text>
    </g>
    <rect y="203" width="13" height="28" fill="{S['light']}" x="{tx + 4}">
      <animate attributeName="x" dur="12s" repeatCount="indefinite"
        values="{tx + 4};{cur(w1)};{cur(w1)};{tx + 4};{tx + 4};{cur(w2)};{cur(w2)};{tx + 4};{tx + 4};{cur(w3)};{cur(w3)};{tx + 4};{tx + 4}"
        keyTimes="0;0.12;0.29;0.33;0.333;0.453;0.623;0.663;0.666;0.786;0.956;0.996;1"/>
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
    </rect>

    <g font-family="{SANS}" font-size="16" fill="#cbd5e1">
      <rect x="{tx}" y="262" width="150" height="34" rx="17" fill="{S['light']}" fill-opacity="0.07" stroke="{S['light']}" stroke-opacity="0.25"/>
      <circle cx="{tx + 20}" cy="279" r="5" fill="{S['light']}"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="{tx + 34}" y="284">Bangladesh</text>
      <rect x="{tx + 162}" y="262" width="210" height="34" rx="17" fill="{S['light']}" fill-opacity="0.07" stroke="{S['light']}" stroke-opacity="0.25"/>
      <text x="{tx + 182}" y="284">AI · SaaS · Dev tools</text>
    </g>

    <!-- phone: a Bikroyee chat in Bikroyee colours -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="6s" repeatCount="indefinite"/>
      <rect x="893" y="36" width="214" height="268" rx="30" fill="{S['raised']}" stroke="url(#edge)" stroke-width="2"/>
      <rect x="975" y="44" width="50" height="6" rx="3" fill="#1e293b"/>
      <g clip-path="url(#screen)">
        <rect x="905" y="52" width="190" height="236" fill="{S['soft']}"/>
        <rect x="905" y="52" width="190" height="36" fill="{K['b950']}"/>
        <circle cx="927" cy="70" r="12" fill="#ffffff"/>
        <image href="{BIKROYEE_LOGO_SM}" x="918" y="61" width="18" height="18"/>
        <text x="946" y="68" font-family="{SANS}" font-size="11" font-weight="700" fill="#ffffff">Bikroyee AI</text>
        <circle cx="949" cy="79" r="3" fill="{K['lime']}"/>
        <text x="956" y="82" font-family="{SANS}" font-size="9" fill="{K['lime2']}">online</text>

        <g opacity="0"><animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;0.05;0.9;1"/>
          <rect x="915" y="100" width="110" height="30" rx="12" fill="#1e293b"/><rect x="926" y="111" width="80" height="8" rx="4" fill="#94a3b8"/></g>
        <g opacity="0"><animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;0.12;0.15;0.28;0.3;1"/>
          <rect x="1035" y="140" width="50" height="24" rx="12" fill="{K['b900']}"/>
          <circle cx="1049" cy="152" r="3" fill="{K['b300']}"><animate attributeName="cy" values="152;148;152" dur="0.6s" repeatCount="indefinite"/></circle>
          <circle cx="1060" cy="152" r="3" fill="{K['b300']}"><animate attributeName="cy" values="152;148;152" dur="0.6s" begin="0.15s" repeatCount="indefinite"/></circle>
          <circle cx="1071" cy="152" r="3" fill="{K['b300']}"><animate attributeName="cy" values="152;148;152" dur="0.6s" begin="0.3s" repeatCount="indefinite"/></circle></g>
        <g opacity="0"><animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;0.3;0.33;0.9;1"/>
          <rect x="975" y="140" width="110" height="42" rx="12" fill="url(#ai)"/>
          <rect x="986" y="150" width="88" height="7" rx="3.5" fill="#ffffff" fill-opacity="0.9"/><rect x="986" y="164" width="60" height="7" rx="3.5" fill="#ffffff" fill-opacity="0.7"/></g>
        <g opacity="0"><animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;0.48;0.51;0.9;1"/>
          <rect x="915" y="192" width="80" height="30" rx="12" fill="#1e293b"/><rect x="926" y="203" width="52" height="8" rx="4" fill="#94a3b8"/></g>
        <g opacity="0"><animate attributeName="opacity" dur="8s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;0.62;0.65;0.9;1"/>
          <rect x="965" y="232" width="120" height="46" rx="12" fill="url(#ai)"/>
          <rect x="976" y="243" width="72" height="7" rx="3.5" fill="#ffffff" fill-opacity="0.9"/>
          <rect x="976" y="256" width="64" height="14" rx="7" fill="{K['lime']}"/>
          <text x="1008" y="266.5" text-anchor="middle" font-family="{SANS}" font-size="9" font-weight="700" fill="{K['b950']}">ORDER ✓</text></g>
      </g>
    </g>
  </g>
  <rect x="0.5" y="0.5" width="1199" height="339" rx="24" fill="none" stroke="{S['light']}" stroke-opacity="0.15"/>
</svg>
'''


# ---------------------------------------------------------------------- cards

def card(*, title, subtitle, lines, chips, status, logo, theme, title_svg=None, title_w=0):
    t = theme
    W, H = 500, 250
    label, scolor, pulse = status
    sw = 30 + len(label) * 8.6
    sx = W - 24 - sw

    if title_svg:      # official lockup replaces logo + text title
        head = f'{title_svg}<text x="28" y="98" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{escape(subtitle)}</text>'
    else:
        head = (f'{logo}<text x="108" y="54" font-family="{SANS}" font-size="26" font-weight="700" fill="{t["title"]}">{escape(title)}</text>'
                f'<text x="108" y="80" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{escape(subtitle)}</text>')

    ring = (f'<circle cx="{sx + 15:.0f}" cy="38" r="5" fill="{scolor}"><animate attributeName="r" values="5;11;5" dur="2s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/></circle>') if pulse else ""
    desc = "".join(f'<text x="28" y="{148 + i * 25}">{escape(l)}</text>' for i, l in enumerate(lines))
    chip_svg, cx = [], 28
    for c in chips:
        w = 18 + len(c) * 8.4
        chip_svg.append(f'<rect x="{cx:.0f}" y="200" width="{w:.0f}" height="26" rx="13" fill="{t["chip"]}" fill-opacity="0.1" stroke="{t["chip"]}" stroke-opacity="0.35"/>'
                        f'<text x="{cx + w / 2:.0f}" y="218" text-anchor="middle">{escape(c)}</text>')
        cx += w + 8

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}: {escape(' '.join(lines))}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['edge1']}" stop-opacity="0.8"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.05"/><stop offset="1" stop-color="{t['edge2']}" stop-opacity="0.6"/></linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <clipPath id="clip"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <circle cx="{W - 40}" cy="{H + 10}" r="110" fill="{t['glow']}" opacity="0.35" filter="url(#blur)">
      <animateTransform attributeName="transform" type="translate" values="0 0;-60 -30;0 0" dur="12s" repeatCount="indefinite"/>
    </circle>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" fill="none" stroke="url(#edge)" stroke-width="2"/>
  {head}
  <rect x="{sx:.0f}" y="25" width="{sw:.0f}" height="26" rx="13" fill="{scolor}" fill-opacity="0.12" stroke="{scolor}" stroke-opacity="0.55"/>
  {ring}<circle cx="{sx + 15:.0f}" cy="38" r="4" fill="{scolor}"/>
  <text x="{sx + 26:.0f}" y="43" font-family="{SANS}" font-size="13.5" font-weight="600" fill="{scolor}">{escape(label)}</text>
  <g font-family="{SANS}" font-size="18" fill="{t['text']}">{desc}</g>
  <g font-family="{MONO}" font-size="13" fill="{t['chiptext']}">{"".join(chip_svg)}</g>
</svg>
'''


def footer():
    S = SELLORA
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-label="Built in Bangladesh. Thanks for visiting.">
  <defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{S['dark']}"/><stop offset="0.5" stop-color="{S['accent']}"/><stop offset="1" stop-color="{S['light']}"/></linearGradient></defs>
  <path fill="url(#w)" opacity="0.3"><animate attributeName="d" dur="10s" repeatCount="indefinite" values="M0 60 C200 20 400 100 600 60 C800 20 1000 100 1200 60 V120 H0Z;M0 60 C200 100 400 20 600 60 C800 100 1000 20 1200 60 V120 H0Z;M0 60 C200 20 400 100 600 60 C800 20 1000 100 1200 60 V120 H0Z"/></path>
  <path fill="url(#w)" opacity="0.55"><animate attributeName="d" dur="7s" repeatCount="indefinite" values="M0 80 C250 50 450 110 600 80 C750 50 950 110 1200 80 V120 H0Z;M0 80 C250 110 450 50 600 80 C750 110 950 50 1200 80 V120 H0Z;M0 80 C250 50 450 110 600 80 C750 50 950 110 1200 80 V120 H0Z"/></path>
  <text x="600" y="36" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="3" fill="{S['muted']}">BUILT IN BANGLADESH · THANKS FOR VISITING</text>
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    S, K, R = SELLORA, BIKROYEE, RESTORA
    (OUT / "banner.svg").write_text(banner(), encoding="utf-8")
    (OUT / "footer.svg").write_text(footer(), encoding="utf-8")

    (OUT / "card-bikroyee.svg").write_text(card(
        title="Bikroyee", subtitle="AI sales agent",
        lines=["Replies to customers 24/7, takes orders", "and flags likely fraud, for online sellers."],
        chips=["FastAPI", "Celery", "PostgreSQL", "Next.js"],
        status=("Live", K["lime4"], True),
        logo=f'<rect x="28" y="26" width="64" height="64" rx="16" fill="#ffffff"/><image href="{BIKROYEE_LOGO}" x="34" y="32" width="52" height="52"/>',
        theme=dict(bg1=K["b950"], bg2="#03102c", edge1=K["b500"], edge2=K["lime"], glow=K["b600"],
                   title="#ffffff", muted=K["b300"], text="#dbe6ff", chip=K["b300"], chiptext="#eff4ff"),
    ), encoding="utf-8")

    lockup, _ = inline_svg("amar-restora-lockup-ondark.svg", 28, 32, 40)
    (OUT / "card-amar-restora.svg").write_text(card(
        title="Amar Restora", subtitle="Amar Restora · restaurant system",
        lines=["POS, QR ordering, kitchen screen, pagers", "and automatic bKash/Nagad checks."],
        chips=["Next.js", "React", "Drizzle", "PostgreSQL"],
        status=("In development", R["saffron"], False), logo="", title_svg=lockup,
        theme=dict(bg1=R["night2"], bg2=R["night"], edge1=R["saffron"], edge2=R["line"], glow=R["accent"],
                   title=R["paper"], muted=R["muted"], text="#e5dfd3", chip=R["saffron"], chiptext=R["paper"]),
    ), encoding="utf-8")

    (OUT / "card-emulator.svg").write_text(card(
        title="Sellora Emulator", subtitle="android emulator",
        lines=["Lightweight Android for low-end Windows", "PCs. One click, no Android Studio."],
        chips=["PowerShell", "QEMU", "Android"],
        status=("Open source", S["light"], False),
        logo=f'<image href="{SELLORA_LOGO}" x="22" y="20" width="76" height="76"/>',
        theme=dict(bg1=S["raised"], bg2=S["ink"], edge1=S["light"], edge2=S["accent"], glow=S["accent"],
                   title="#ffffff", muted=S["muted"], text="#cbd5e1", chip=S["light"], chiptext="#e2e8f0"),
    ), encoding="utf-8")

    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:24} {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
