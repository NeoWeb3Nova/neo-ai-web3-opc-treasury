from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "demo-cover.png"
W, H = 1920, 1080
S = 2  # supersample for crisp edges

# Project palette from web/src/index.css
BG = (18, 16, 12)
PAPER = (253, 252, 250)
INK = (232, 230, 227)
TEXT_DARK = (44, 41, 37)
MUTED = (154, 149, 142)
RULE = (232, 230, 227, 42)
GOLD = (224, 184, 90)
GOLD_DEEP = (176, 138, 48)
PATINA = (106, 191, 168)
PATINA_DEEP = (77, 154, 130)
VERMILION = (201, 110, 96)
PURPLE = (111, 90, 168)
PURPLE_DEEP = (76, 39, 170)

FONT_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_LATIN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


def font(size: int, bold: bool = False, cjk: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_CJK if cjk else (FONT_LATIN_BOLD if bold else FONT_LATIN)
    return ImageFont.truetype(path, size * S)


def sc(v):
    if isinstance(v, tuple):
        return tuple(int(x * S) for x in v)
    return int(v * S)


def rounded(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(sc(x) for x in xy), radius=sc(r), fill=fill, outline=outline, width=sc(width))


def line(draw, xy, fill, width=1):
    draw.line([sc(p) for p in xy], fill=fill, width=sc(width))


def text(draw, xy, s, fnt, fill, anchor=None, spacing=4, align="left"):
    draw.text(sc(xy), s, font=fnt, fill=fill, anchor=anchor, spacing=sc(spacing), align=align)


def glow(base: Image.Image, bbox, color, radius=36, alpha=160):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(tuple(sc(x) for x in bbox), radius=sc(28), fill=(*color[:3], alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(sc(radius)))
    base.alpha_composite(layer)


def draw_background(img: Image.Image):
    px = img.load()
    for y in range(H * S):
        for x in range(W * S):
            nx = x / (W * S)
            ny = y / (H * S)
            vignette = 1 - 0.55 * math.hypot(nx - 0.55, ny - 0.48)
            purple = max(0, 1 - math.hypot(nx - 0.82, ny - 0.22) * 2.0)
            teal = max(0, 1 - math.hypot(nx - 0.28, ny - 0.75) * 2.3)
            r = int((BG[0] + purple * 34 + teal * 8) * vignette)
            g = int((BG[1] + purple * 16 + teal * 30) * vignette)
            b = int((BG[2] + purple * 60 + teal * 24) * vignette)
            px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), 255)

    d = ImageDraw.Draw(img)
    # subtle grid
    for x in range(0, W + 1, 80):
        line(d, [(x, 0), (x, H)], (255, 255, 255, 12), 1)
    for y in range(0, H + 1, 80):
        line(d, [(0, y), (W, y)], (255, 255, 255, 9), 1)

    # orbit arcs / policy rails
    for i, color in enumerate([(224,184,90,46), (106,191,168,42), (111,90,168,58)]):
        box = (880 - i * 80, 80 + i * 40, 2050 - i * 30, 1080 + i * 95)
        d.arc(tuple(sc(v) for v in box), 196, 326, fill=color, width=sc(3))


def draw_card(draw: ImageDraw.ImageDraw, xy, wh, title, subtitle, amount, accent, status="ACTIVE"):
    x, y = xy
    w, h = wh
    # shadow
    rounded(draw, (x + 14, y + 18, x + w + 14, y + h + 18), 26, (0, 0, 0, 75))
    rounded(draw, (x, y, x + w, y + h), 26, (*PAPER, 246), outline=(255,255,255,70), width=2)
    rounded(draw, (x + 28, y + 26, x + 28 + 96, y + 26 + 96), 18, (*accent, 34), outline=(*accent, 140), width=2)
    # pixel avatar
    px0, py0, unit = x + 48, y + 44, 10
    blocks = [
        (2,0,4,1,(32,28,26)), (1,1,6,2,(32,28,26)), (1,3,6,4,(232,185,148)),
        (2,4,1,1,(32,28,26)), (5,4,1,1,(32,28,26)), (3,5,2,1,(120,76,70)),
        (0,7,8,3,accent), (2,7,4,2,(248,244,235)), (3,9,2,2,GOLD),
    ]
    for bx, by, bw, bh, col in blocks:
        draw.rectangle((sc(px0 + bx*unit), sc(py0 + by*unit), sc(px0 + (bx+bw)*unit), sc(py0 + (by+bh)*unit)), fill=(*col, 255))
    text(draw, (x + 150, y + 34), title, font(26, bold=True), TEXT_DARK)
    text(draw, (x + 150, y + 72), subtitle, font(18), (107, 101, 88))
    rounded(draw, (x + w - 142, y + 32, x + w - 34, y + 68), 18, (*PATINA, 120), outline=(*PATINA_DEEP, 220), width=2)
    text(draw, (x + w - 88, y + 50), status, font(16, bold=True), (30, 91, 76), anchor="mm")
    text(draw, (x + 34, y + 148), "Monthly Budget", font(18), (107,101,88))
    text(draw, (x + 34, y + 174), amount, font(44, bold=True), TEXT_DARK)
    # policy chips
    chips = ["$40 / tx", "Vendor allowlist", "Cooldown", "Audit"]
    cx, cy = x + 34, y + h - 72
    for chip in chips:
        tw = draw.textbbox((0, 0), chip, font=font(16))[2] / S + 28
        rounded(draw, (cx, cy, cx + tw, cy + 38), 19, (245, 242, 237, 255), outline=(61,58,54,45), width=1)
        text(draw, (cx + 14, cy + 9), chip, font(16), TEXT_DARK)
        cx += tw + 12


def draw_flow(draw: ImageDraw.ImageDraw):
    # central lock / pact shield
    cx, cy = 1165, 520
    glow(img, (cx - 120, cy - 120, cx + 120, cy + 120), GOLD, radius=54, alpha=110)
    pts = [(cx, cy-115), (cx+100, cy-70), (cx+82, cy+82), (cx, cy+132), (cx-82, cy+82), (cx-100, cy-70)]
    draw.polygon([sc(p) for p in pts], fill=(*GOLD, 245), outline=(*GOLD_DEEP, 255))
    # lock
    rounded(draw, (cx - 46, cy - 10, cx + 46, cy + 64), 12, (30, 25, 18, 255))
    draw.arc(tuple(sc(v) for v in (cx-34, cy-56, cx+34, cy+34)), 200, -20, fill=(30,25,18,255), width=sc(12))
    text(draw, (cx, cy + 98), "CAW PACT", font(24, bold=True), (40, 31, 15), anchor="mm")

    # approved path
    line(draw, [(780, 420), (980, 420), (1062, 485)], (*PATINA, 230), 7)
    line(draw, [(1270, 560), (1430, 630), (1580, 630)], (*PATINA, 230), 7)
    # denied path
    line(draw, [(770, 635), (960, 670), (1060, 585)], (*VERMILION, 220), 7)
    line(draw, [(1270, 485), (1445, 395), (1600, 400)], (*VERMILION, 220), 7)

    rounded(draw, (1455, 332, 1740, 460), 22, (18, 16, 12, 210), outline=(*VERMILION, 180), width=2)
    text(draw, (1486, 364), "Prompt Injection", font(24, bold=True), INK)
    text(draw, (1486, 406), "DENIED: scope / limit", font(20, bold=True), VERMILION)

    rounded(draw, (1448, 594, 1748, 728), 22, (18, 16, 12, 210), outline=(*PATINA, 180), width=2)
    text(draw, (1480, 626), "x402 API Payment", font(24, bold=True), INK)
    text(draw, (1480, 668), "APPROVED + audited", font(20, bold=True), PATINA)


def draw_layered_cube(draw: ImageDraw.ImageDraw, x=1290, y=150):
    # inspired by existing hero image: floating square layers
    top = [(x, y), (x+250, y+135), (x+45, y+250), (x-205, y+115)]
    mid = [(x-5, y+85), (x+245, y+220), (x+40, y+335), (x-210, y+200)]
    low = [(x-18, y+170), (x+232, y+305), (x+27, y+420), (x-223, y+285)]
    draw.polygon([sc(p) for p in low], fill=(*PURPLE_DEEP, 210), outline=(186,160,255,140))
    draw.polygon([sc(p) for p in mid], fill=(0,0,0,190), outline=(232,230,227,130))
    draw.polygon([sc(p) for p in top], fill=(5,5,5,232), outline=(232,230,227,170))
    for dx in range(-190, 220, 42):
        line(draw, [(x+dx, y+270), (x+dx+35, y+292)], (186,160,255,54), 2)


img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 255))
draw_background(img)
d = ImageDraw.Draw(img)

# top labels
rounded(d, (90, 80, 352, 126), 23, (255,255,255,20), outline=RULE, width=1)
text(d, (116, 94), "DEMO VIDEO COVER", font(18, bold=True), GOLD)
rounded(d, (374, 80, 580, 126), 23, (255,255,255,16), outline=RULE, width=1)
text(d, (400, 94), "Cobo CAW Track", font(18, bold=True), TEXT_DARK)

# main title
text(d, (90, 184), "OPC Agent\nTreasury", font(92, bold=True), INK, spacing=-6)
text(d, (94, 410), "AI 员工的可编程支出卡", font(44, cjk=True), (240, 217, 160))
text(d, (96, 478), "Scoped · Revocable · Auditable finance permissions\nfor agent-native payments.", font(31), (202, 198, 194), spacing=10)

# cards and flow
rounded(d, (90, 680, 555, 814), 22, (18,16,12,210), outline=(255,255,255,70), width=1)
text(d, (124, 714), "Problem", font(23, bold=True), VERMILION)
text(d, (124, 758), "Private key to Agent = unbounded blast radius", font(22), INK)
rounded(d, (90, 840, 555, 974), 22, (18,16,12,210), outline=(255,255,255,70), width=1)
text(d, (124, 874), "Solution", font(23, bold=True), PATINA)
text(d, (124, 918), "Pact-scoped card: budget, vendors, audit", font(22), INK)

draw_layered_cube(d)
draw_card(d, (700, 665), (610, 305), "VEGA Research Agent", "Programmable CAW spending card", "300 USDC", PURPLE)
draw_flow(d)

# audit strip bottom right
rounded(d, (1318, 780, 1818, 958), 26, (253,252,250,238), outline=(255,255,255,80), width=2)
text(d, (1352, 812), "Audit Report", font(28, bold=True), TEXT_DARK)
rows = [("approved", "BlockRun AI Gateway", PATINA_DEEP), ("denied", "attacker address", VERMILION), ("denied", "per_tx_exceeded", VERMILION)]
for i, (st, vendor, col) in enumerate(rows):
    yy = 858 + i * 34
    rounded(d, (1352, yy, 1442, yy+24), 12, (*col, 35), outline=(*col, 155), width=1)
    text(d, (1397, yy+12), st.upper(), font(11, bold=True), col, anchor="mm")
    text(d, (1460, yy+3), vendor, font(17), TEXT_DARK)

# footer
text(d, (90, 1018), "Cobo Agentic Wallet × x402 × One-Person Company", font(22), MUTED)
text(d, (1830, 1018), "Mock runnable · Real CAW verified", font(22), MUTED, anchor="ra")

img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, quality=95)
print(OUT)
print(f"{W}x{H}")
