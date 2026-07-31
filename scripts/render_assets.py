"""Regenerate organization profile assets.

Run from the repository root:
    python scripts/render_assets.py
"""

from pathlib import Path
import json
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile"
ASSETS = PROFILE / "assets"
CONTENT = json.loads((PROFILE / "content.json").read_text(encoding="utf-8"))

FONT_REG_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/malgun.ttf",
]
FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "C:/Windows/Fonts/malgunbd.ttf",
]

def find_font(candidates):
    for item in candidates:
        p = Path(item)
        if p.exists():
            return str(p)
    raise FileNotFoundError("Install Noto Sans CJK or use Windows Malgun Gothic.")

FONT_REG = find_font(FONT_REG_CANDIDATES)
FONT_BOLD = find_font(FONT_BOLD_CANDIDATES)

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)

def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def gradient_bg(size, c1, c2):
    w, h = size
    im = Image.new("RGB", size)
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x / max(1, w-1)) * 0.65 + (y / max(1, h-1)) * 0.35
            px[x, y] = tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))
    return im

def save_gif(frames, path, duration):
    """Save a GitHub-optimized GIF while preserving the original loop time."""
    max_width = 1000
    max_frames = 22
    palette_colors = 80

    original_count = len(frames)
    total_duration = original_count * duration

    if original_count > max_frames:
        indices = sorted({
            round(i * (original_count - 1) / (max_frames - 1))
            for i in range(max_frames)
        })
        frames = [frames[index] for index in indices]

    frames = [frame.convert("RGB") for frame in frames]

    if frames[0].width > max_width:
        target_height = round(
            frames[0].height * max_width / frames[0].width
        )
        frames = [
            frame.resize(
                (max_width, target_height),
                Image.Resampling.LANCZOS,
            )
            for frame in frames
        ]

    optimized_duration = max(
        20,
        round((total_duration / len(frames)) / 10) * 10,
    )

    thumb_width = 160
    thumbnails = []
    for frame in frames:
        thumb_height = round(
            frame.height * thumb_width / frame.width
        )
        thumbnails.append(
            frame.resize(
                (thumb_width, thumb_height),
                Image.Resampling.BILINEAR,
            )
        )

    columns = min(6, len(thumbnails))
    rows = math.ceil(len(thumbnails) / columns)
    thumb_height = thumbnails[0].height
    montage = Image.new(
        "RGB",
        (columns * thumb_width, rows * thumb_height),
        (0, 0, 0),
    )
    for index, thumbnail in enumerate(thumbnails):
        montage.paste(
            thumbnail,
            (
                (index % columns) * thumb_width,
                (index // columns) * thumb_height,
            ),
        )

    shared_palette = montage.quantize(
        colors=palette_colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    pal = [
        frame.quantize(
            palette=shared_palette,
            dither=Image.Dither.NONE,
        )
        for frame in frames
    ]
    pal[0].save(
        path,
        save_all=True,
        append_images=pal[1:],
        duration=optimized_duration,
        loop=0,
        optimize=True,
        disposal=2,
    )





def render_layout_helpers():
    spacer_svg = """<svg xmlns="http://www.w3.org/2000/svg"
width="1200" height="54" viewBox="0 0 1200 54">
<defs>
<linearGradient id="left" x1="0" x2="1">
<stop offset="0" stop-color="#dce9e1" stop-opacity="0"/>
<stop offset="1" stop-color="#8eb59f" stop-opacity=".72"/>
</linearGradient>
<linearGradient id="right" x1="0" x2="1">
<stop offset="0" stop-color="#8eb59f" stop-opacity=".72"/>
<stop offset="1" stop-color="#dce9e1" stop-opacity="0"/>
</linearGradient>
</defs>
<line x1="80" y1="27" x2="548" y2="27"
stroke="url(#left)" stroke-width="2"/>
<line x1="652" y1="27" x2="1120" y2="27"
stroke="url(#right)" stroke-width="2"/>
<circle cx="578" cy="27" r="5" fill="#73a88e"/>
<circle cx="600" cy="27" r="7" fill="#d5a72f"/>
<circle cx="622" cy="27" r="5" fill="#73a88e"/>
</svg>"""
    (ASSETS / "section-spacer.svg").write_text(
        spacer_svg,
        encoding="utf-8",
    )

def render_brand_footer():
    W, H = 1200, 235
    frames = []

    for frame_index in range(36):
        image = Image.new("RGBA", (W, H), (12, 49, 40, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((48, 30), "THIS IS STRESS",
                  font=font(30, True),
                  fill=(255, 255, 255, 255))
        draw.text((48, 72), "Health Data × Reproducible ML",
                  font=font(16, True),
                  fill=(235, 197, 81, 255))
        draw.text(
            (48, 103),
            "Small, controlled experiments. Shared evidence. Better predictions.",
            font=font(14),
            fill=(190, 217, 203, 242),
        )

        draw.ellipse((48, 147, 62, 161),
                     fill=(83, 197, 143, 255))
        draw.text((76, 143), "RESEARCH PROFILE ACTIVE",
                  font=font(12, True),
                  fill=(208, 232, 220, 245))

        cards = [
            ("BASELINE", "V1"),
            ("PUBLIC MAE", CONTENT.get("public_mae", "N/A")),
            ("MODEL", CONTENT.get("model", "ExtraTrees × 1,200").upper()),
            ("TEAM", f"{len(CONTENT.get('team', []))} RESEARCHERS"),
        ]
        card_x = 565
        for index, (label, value) in enumerate(cards):
            x = card_x + (index % 2) * 300
            y = 28 + (index // 2) * 82
            active = index == (frame_index // 9) % 4

            rounded(
                draw,
                (x, y, x + 267, y + 62),
                21,
                (255, 255, 255, 30 if active else 18),
                (218, 170, 48, 210)
                if active else (156, 191, 172, 75),
                2 if active else 1,
            )
            draw.text((x + 18, y + 12), label,
                      font=font(10, True),
                      fill=(167, 203, 184, 240))
            value_size = 17 if label == "PUBLIC MAE" else 19
            draw.text(
                (x + 18, y + 30),
                value,
                font=font(value_size, True),
                fill=(242, 203, 91, 255)
                if active else (255, 255, 255, 248),
            )

        rail_y = 204
        draw.line((48, rail_y, 1152, rail_y),
                  fill=(142, 183, 162, 80), width=2)
        rail_progress = (frame_index / 35) * 1104
        draw.line((48, rail_y, 48 + rail_progress, rail_y),
                  fill=(220, 173, 48, 230), width=3)
        packet_x = 48 + rail_progress
        draw.ellipse((packet_x - 6, rail_y - 6,
                      packet_x + 6, rail_y + 6),
                     fill=(241, 205, 94, 255))

        draw.text(
            (48, 213),
            "PUBLIC PROFILE · NO RAW DATA · NO SUBMISSION CSV · REPRODUCIBLE METHODS ONLY",
            font=font(10, True),
            fill=(167, 200, 183, 220),
        )

        frames.append(image.convert("RGB"))

    save_gif(
        frames,
        ASSETS / "brand-footer.gif",
        105,
    )
    frames[0].save(
        ASSETS / "brand-footer-preview.png",
        optimize=True,
    )


def render_section_headers():
    team_text = " · ".join(CONTENT.get("team", []))
    snapshot_date = CONTENT.get("experiment_status", {}).get(
        "snapshot_date",
        "Not dated",
    )
    sections = [
        ("research", "01", "RESEARCH", "What we are building",
         "Health signals · Reproducible ML · Shared evidence"),
        ("baseline", "02", "BASELINE V1", "Current reproducible benchmark",
         f"{CONTENT.get('baseline', 'Weighted Quantile ExtraTrees')} · "
         f"Public MAE {CONTENT.get('public_mae', 'N/A')}"),
        ("workflow", "03", "WORKFLOW", "From data to validated evidence",
         "Train-only · Controlled change · Multi-seed validation"),
        ("principles", "04", "PRINCIPLES", "Rules that protect reproducibility",
         "No leakage · One hypothesis · Public-safe"),
        ("team", "05", "TEAM", "Three researchers, one shared baseline",
         team_text),
        ("repositories", "06", "REPOSITORIES", "Research workspace map",
         "Private now · public after official release"),
        ("status", "07", "EXPERIMENT STATUS", "Current research snapshot",
         f"Snapshot · {snapshot_date}"),
    ]

    for slug, number, title, subtitle, detail in sections:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="1200" height="118" viewBox="0 0 1200 118">
<defs>
<linearGradient id="line" x1="0" x2="1">
<stop offset="0" stop-color="#d5a72f"/>
<stop offset=".45" stop-color="#73a88e"/>
<stop offset="1" stop-color="#dce9e1" stop-opacity=".15"/>
</linearGradient>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
<feDropShadow dx="0" dy="5" stdDeviation="6"
flood-color="#0b2e25" flood-opacity=".12"/>
</filter>
</defs>
<rect x="8" y="8" width="1184" height="102" rx="28"
fill="#f8fbf9" stroke="#d9e7df" stroke-width="2"/>
<g filter="url(#shadow)">
<rect x="34" y="27" width="72" height="64" rx="22"
fill="#123f33" stroke="#d5a72f" stroke-width="2"/>
<text x="70" y="67" text-anchor="middle"
font-family="Inter, Noto Sans KR, sans-serif"
font-size="23" font-weight="850" fill="#f1c957">{number}</text>
</g>
<text x="132" y="46"
font-family="Inter, Noto Sans KR, sans-serif"
font-size="15" font-weight="800" fill="#52816d"
letter-spacing="1.8">{title}</text>
<text x="132" y="76"
font-family="Inter, Noto Sans KR, sans-serif"
font-size="25" font-weight="850" fill="#123f33">{subtitle}</text>
<text x="724" y="67"
font-family="Inter, Noto Sans KR, sans-serif"
font-size="14" font-weight="650" fill="#708d80">{detail}</text>
<line x1="132" y1="94" x2="1155" y2="94"
stroke="url(#line)" stroke-width="3" stroke-linecap="round"/>
<circle cx="1100" cy="33" r="5" fill="#d5a72f"/>
<circle cx="1126" cy="33" r="4" fill="#5b987b"/>
<circle cx="1149" cy="33" r="3" fill="#a9c7b7"/>
</svg>"""
        (ASSETS / f"section-{slug}.svg").write_text(
            svg,
            encoding="utf-8",
        )


def render_navigation():
    items = [
        ("overview", "OVERVIEW", "home"),
        ("research", "RESEARCH", "nodes"),
        ("baseline", "BASELINE", "tree"),
        ("workflow", "WORKFLOW", "flow"),
        ("principles", "PRINCIPLES", "shield"),
        ("team", "TEAM", "people"),
        ("repositories", "REPOS", "repo"),
        ("status", "STATUS", "status"),
    ]

    paths = {
        "home": '<path d="M20 22 L32 12 L44 22 V39 H35 V29 H29 V39 H20 Z" fill="none" stroke="{c}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>',
        "nodes": '<path d="M32 14 V24 M22 30 L29 25 M42 30 L35 25" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/><circle cx="32" cy="11" r="4" fill="{c}"/><circle cx="19" cy="33" r="4" fill="{c}"/><circle cx="45" cy="33" r="4" fill="{c}"/>',
        "tree": '<path d="M32 11 V21 M32 21 L20 31 M32 21 L44 31" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/><circle cx="32" cy="10" r="4" fill="{c}"/><circle cx="19" cy="33" r="4" fill="{c}"/><circle cx="45" cy="33" r="4" fill="{c}"/>',
        "flow": '<rect x="16" y="17" width="12" height="12" rx="3" fill="none" stroke="{c}" stroke-width="2.4"/><rect x="38" y="17" width="12" height="12" rx="3" fill="none" stroke="{c}" stroke-width="2.4"/><path d="M28 23 H38 M34 19 L38 23 L34 27" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
        "shield": '<path d="M32 10 L45 16 V27 C45 35 40 40 32 44 C24 40 19 35 19 27 V16 Z" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/><path d="M26 27 L30 31 L38 22" fill="none" stroke="{c}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>',
        "people": '<circle cx="26" cy="18" r="5" fill="none" stroke="{c}" stroke-width="2.4"/><circle cx="40" cy="18" r="5" fill="none" stroke="{c}" stroke-width="2.4"/><path d="M16 38 C17 29 23 26 28 26 M48 38 C47 29 41 26 36 26 M24 39 C25 31 29 28 33 28 C37 28 41 31 42 39" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>',
        "repo": '<rect x="17" y="15" width="30" height="25" rx="5" fill="none" stroke="{c}" stroke-width="2.4"/><path d="M22 20 H37 M22 26 H42 M22 32 H35" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>',
        "status": '<path d="M17 35 H25 L30 22 L36 38 L42 27 H49" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="35" r="3" fill="{c}"/><circle cx="49" cy="27" r="3" fill="{c}"/>',
    }

    for slug, label, icon in items:
        active = slug == "overview"
        stroke = "#d5a72f" if active else "#cfe2d6"
        text = "#ffffff" if active else "#103f33"
        icon_color = "#d5a72f" if active else "#4f9074"
        rect_fill = "url(#active)" if active else "#ffffff"
        icon_markup = paths[icon].format(c=icon_color)

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="174" height="52" viewBox="0 0 174 52">'
            '<defs><filter id="shadow" x="-20%" y="-40%" width="140%" height="180%">'
            '<feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#0b2e25" flood-opacity=".12"/>'
            '</filter><linearGradient id="active" x1="0" x2="1">'
            '<stop offset="0" stop-color="#103f33"/><stop offset="1" stop-color="#1c5b48"/>'
            '</linearGradient></defs>'
            f'<rect x="4" y="4" width="166" height="44" rx="18" fill="{rect_fill}" '
            f'stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>'
            f'{icon_markup}'
            f'<text x="59" y="31" font-family="Inter, Noto Sans KR, sans-serif" '
            f'font-size="13" font-weight="800" fill="{text}" letter-spacing=".4">{label}</text>'
            '</svg>'
        )
        (ASSETS / f"nav-{slug}.svg").write_text(svg, encoding="utf-8")

def render_hero():
    W, H = 1200, 420
    frames = []
    random.seed(2026)
    particles = [
        (
            random.randint(665, 1140),
            random.randint(52, 370),
            random.uniform(0, math.tau),
            random.randint(2, 4),
        )
        for _ in range(26)
    ]

    tree_nodes = [
        (850, 122), (778, 200), (922, 200),
        (738, 284), (815, 284), (885, 284), (960, 284),
    ]
    tree_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

    def moving_background(frame_index):
        base = Image.new("RGBA", (W, H), (7, 31, 26, 255))
        pixels = base.load()
        phase = frame_index * 0.09

        for y in range(H):
            ny = y / max(H - 1, 1)
            for x in range(W):
                nx = x / max(W - 1, 1)
                wave = 0.5 + 0.5 * math.sin(nx * 5.2 + ny * 2.5 + phase)
                glow = math.exp(-((nx - 0.79) ** 2 + (ny - 0.48) ** 2) / 0.15)
                green = 39 + int(40 * nx + 21 * wave + 48 * glow)
                blue = 32 + int(20 * nx + 12 * wave + 24 * glow)
                red = 7 + int(12 * nx + 7 * glow)
                pixels[x, y] = (red, min(green, 112), min(blue, 84), 255)

        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay, "RGBA")
        shift = 18 * math.sin(frame_index * 0.16)
        od.ellipse((650 + shift, -120, 1290 + shift, 530), fill=(87, 173, 137, 32))
        od.ellipse((860 - shift, 30, 1290 - shift, 500), fill=(230, 183, 58, 17))
        overlay = overlay.filter(ImageFilter.GaussianBlur(42))
        return Image.alpha_composite(base, overlay)

    for frame_index in range(30):
        image = moving_background(frame_index)
        d = ImageDraw.Draw(image, "RGBA")

        for gx in range(690, 1170, 30):
            for gy in range(55, 380, 30):
                alpha = 22 + int(
                    23 * (
                        0.5 + 0.5 * math.sin(
                            frame_index * 0.20 + gx * 0.013 + gy * 0.017
                        )
                    )
                )
                d.ellipse((gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6),
                          fill=(205, 234, 219, alpha))

        for px, py, phase, radius in particles:
            x = px + 7 * math.sin(frame_index * 0.16 + phase)
            y = py + 5 * math.cos(frame_index * 0.13 + phase)
            alpha = 65 + int(
                50 * (0.5 + 0.5 * math.sin(frame_index * 0.23 + phase))
            )
            d.ellipse((x - radius, y - radius, x + radius, y + radius),
                      fill=(239, 193, 67, alpha))

        rounded(d, (62, 48, 289, 88), 20, (255, 255, 255, 19),
                (255, 255, 255, 48), 1)
        d.text((84, 59), "PUBLIC RESEARCH PROFILE",
               font=font(15, True), fill=(238, 207, 106, 255))

        d.text((61, 112), CONTENT["title"],
               font=font(57, True), fill=(255, 255, 255, 255))
        d.text((63, 187), CONTENT["subtitle"],
               font=font(26, True), fill=(239, 196, 77, 255))
        d.text((64, 235), CONTENT["tagline_ko"],
               font=font(23), fill=(226, 241, 233, 248))
        d.text((64, 283),
               "Tabular ML  ·  Controlled Experiments  ·  Shared Evidence",
               font=font(16), fill=(171, 206, 190, 235))
        d.ellipse((65, 333, 77, 345), fill=(92, 197, 145, 255))
        d.text((88, 325), "BASELINE V1  /  ACTIVE RESEARCH",
               font=font(14, True), fill=(204, 226, 215, 242))

        d.arc((691, 34, 1152, 400), 198, 520,
              fill=(229, 179, 52, 145), width=3)
        angle = frame_index / 30 * math.tau
        orbit_x = 921 + 225 * math.cos(angle)
        orbit_y = 217 + 181 * math.sin(angle)
        d.ellipse((orbit_x - 7, orbit_y - 7, orbit_x + 7, orbit_y + 7),
                  fill=(247, 207, 88, 255),
                  outline=(255, 237, 174, 230), width=2)

        active_node = frame_index % len(tree_nodes)
        for start_node, end_node in tree_edges:
            d.line((tree_nodes[start_node], tree_nodes[end_node]),
                   fill=(208, 236, 222, 165), width=4)

        for index, (x, y) in enumerate(tree_nodes):
            radius = 14 if index == 0 else 11
            if index == active_node:
                fill = (241, 188, 53, 255)
                d.ellipse(
                    (x - radius - 6, y - radius - 6,
                     x + radius + 6, y + radius + 6),
                    fill=(242, 190, 57, 34),
                )
            else:
                fill = (
                    (217, 240, 227, 255)
                    if index % 2
                    else (103, 180, 145, 255)
                )
            d.ellipse((x - radius, y - radius, x + radius, y + radius),
                      fill=fill, outline=(255, 255, 255, 145), width=2)

        rounded(d, (955, 68, 1142, 135), 20, (4, 27, 23, 178),
                (225, 181, 62, 155), 2)
        d.text((976, 82), "PUBLIC MAE", font=font(12, True),
               fill=(173, 209, 190, 255))
        d.text((976, 104), CONTENT["public_mae"], font=font(18, True),
               fill=(247, 209, 91, 255))

        rounded(d, (744, 321, 1118, 385), 18, (255, 255, 255, 17),
                (255, 255, 255, 43), 1)
        points = []
        for point_index in range(14):
            x = 766 + point_index * 25
            value = (
                0.38
                + 0.10 * math.sin((point_index + frame_index * 0.16) * 0.95)
                + 0.031 * point_index
            )
            y = 374 - int(value * 61)
            points.append((x, y))

        d.line(points, fill=(239, 190, 59, 255), width=4)
        for point_index, (x, y) in enumerate(points):
            active = point_index == frame_index % len(points)
            radius = 4.5 if active else 3
            d.ellipse((x - radius, y - radius, x + radius, y + radius),
                      fill=(247, 211, 102, 255 if active else 190))

        frames.append(image.convert("RGB"))

    save_gif(frames, ASSETS / "hero.gif", 95)
    frames[0].save(ASSETS / "hero-preview.png", optimize=True)



def render_research_cards():
    W, H = 1200, 350
    cards = [
        {
            "title": "HEALTH SIGNALS",
            "subtitle": "의미 있는 건강 변수",
            "body": "BMI · 혈압 · 대사 지표 · 근무시간",
            "accent": (76, 142, 111),
            "icon": "health",
        },
        {
            "title": "REPRODUCIBLE ML",
            "subtitle": "같은 조건의 반복 검증",
            "body": "Train-only · Multi-seed · Registry",
            "accent": (205, 160, 48),
            "icon": "model",
        },
        {
            "title": "SHARED EVIDENCE",
            "subtitle": "팀 의사결정으로 연결",
            "body": "Baseline · Pull Request · Learning",
            "accent": (47, 107, 84),
            "icon": "network",
        },
    ]
    positions = [(35, 78), (410, 78), (785, 78)]
    card_w, card_h = 340, 220

    def draw_icon(draw, cx, cy, kind, color, active):
        alpha = 255 if active else 210
        line = color + (alpha,)

        if kind == "health":
            draw.arc((cx - 27, cy - 20, cx + 2, cy + 15),
                     205, 520, fill=line, width=4)
            draw.arc((cx - 2, cy - 20, cx + 27, cy + 15),
                     20, 335, fill=line, width=4)
            draw.line(
                [
                    (cx - 31, cy + 10), (cx - 14, cy + 10),
                    (cx - 7, cy - 2), (cx + 1, cy + 20),
                    (cx + 10, cy + 3), (cx + 17, cy + 10),
                    (cx + 31, cy + 10),
                ],
                fill=line,
                width=3,
            )
        elif kind == "model":
            nodes = [
                (cx, cy - 25), (cx - 24, cy), (cx + 24, cy),
                (cx - 36, cy + 27), (cx - 12, cy + 27),
                (cx + 12, cy + 27), (cx + 36, cy + 27),
            ]
            for a, b in [(0, 1), (0, 2), (1, 3),
                         (1, 4), (2, 5), (2, 6)]:
                draw.line((nodes[a], nodes[b]), fill=line, width=3)
            for index, (x, y) in enumerate(nodes):
                r = 6 if index == 0 else 5
                draw.ellipse((x-r, y-r, x+r, y+r),
                             fill=color + (255,))
        else:
            nodes = [
                (cx - 27, cy - 10), (cx + 27, cy - 10),
                (cx, cy + 25), (cx, cy - 30),
            ]
            for a, b in [(0, 1), (0, 2), (1, 2), (3, 0), (3, 1)]:
                draw.line((nodes[a], nodes[b]), fill=line, width=3)
            for index, (x, y) in enumerate(nodes):
                r = 7 if index == 2 else 5
                fill = (
                    (225, 177, 52, 255)
                    if index == 2
                    else color + (255,)
                )
                draw.ellipse((x-r, y-r, x+r, y+r), fill=fill)

    frames = []
    for frame_index in range(36):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((42, 23), "WHAT WE ARE BUILDING",
                  font=font(16, True), fill=(59, 113, 91, 255))
        draw.text((42, 48),
                  "Three capabilities, one reproducible research loop",
                  font=font(14), fill=(108, 138, 123, 235))

        active = (frame_index // 12) % 3
        active_progress = (frame_index % 12) / 11
        centers = [
            (x + card_w / 2, y + card_h / 2)
            for x, y in positions
        ]

        for i in range(2):
            start_x = centers[i][0] + card_w / 2 - 20
            end_x = centers[i + 1][0] - card_w / 2 + 20
            y = 189
            draw.line((start_x, y, end_x, y),
                      fill=(177, 202, 188, 170), width=4)

        path_t = frame_index / 35
        start_x = positions[0][0] + 50
        end_x = positions[-1][0] + card_w - 50
        packet_x = start_x + (end_x - start_x) * path_t
        packet_y = 189
        for offset, alpha, radius in [
            (0, 255, 7), (-16, 145, 5), (-30, 70, 4)
        ]:
            x = packet_x + offset
            draw.ellipse((x-radius, packet_y-radius,
                          x+radius, packet_y+radius),
                         fill=(225, 175, 47, alpha))

        for index, card in enumerate(cards):
            x, y = positions[index]
            is_active = index == active
            is_complete = index < active
            lift = (
                int(7 * math.sin(active_progress * math.pi))
                if is_active else 0
            )
            card_y = y - lift

            if index == 1:
                fill = (
                    (16, 61, 49, 250)
                    if is_active
                    else (23, 76, 61, 246)
                )
                outline = card["accent"] + (
                    240 if is_active else 150,
                )
                label_color = (238, 205, 102, 255)
                title_color = (255, 255, 255, 255)
                subtitle_color = (207, 230, 217, 245)
                body_color = (183, 211, 196, 230)
            else:
                fill = (255, 255, 255, 246)
                outline = card["accent"] + (
                    235 if is_active else 130,
                )
                label_color = card["accent"] + (255,)
                title_color = (20, 64, 51, 255)
                subtitle_color = (70, 113, 94, 255)
                body_color = (108, 137, 123, 230)

            rounded(draw,
                    (x, card_y, x + card_w, card_y + card_h),
                    28, fill, outline, 3 if is_active else 2)

            draw.ellipse(
                (x + 24, card_y + 23, x + 54, card_y + 53),
                fill=card["accent"] + (255,),
            )
            status = (
                "ACTIVE"
                if is_active
                else ("READY" if is_complete else "NEXT")
            )
            draw.text((x + 66, card_y + 29), status,
                      font=font(11, True), fill=label_color)

            draw_icon(draw, x + card_w - 65, card_y + 65,
                      card["icon"], card["accent"], is_active)

            draw.text((x + 24, card_y + 76), card["title"],
                      font=font(21, True), fill=title_color)
            draw.text((x + 24, card_y + 116), card["subtitle"],
                      font=font(16, True), fill=subtitle_color)
            draw.text((x + 24, card_y + 151), card["body"],
                      font=font(13), fill=body_color)

            rail_x = x + 24
            rail_y = card_y + 193
            rail_w = card_w - 48
            draw.rounded_rectangle(
                (rail_x, rail_y, rail_x + rail_w, rail_y + 7),
                radius=4,
                fill=(
                    (220, 231, 224, 155)
                    if index != 1
                    else (255, 255, 255, 30)
                ),
            )
            fill_ratio = (
                1.0
                if is_complete
                else (active_progress if is_active else 0.0)
            )
            if fill_ratio > 0:
                draw.rounded_rectangle(
                    (
                        rail_x, rail_y,
                        rail_x + rail_w * fill_ratio,
                        rail_y + 7,
                    ),
                    radius=4,
                    fill=card["accent"] + (255,),
                )

        rounded(draw, (42, 316, 1158, 340), 12,
                (255, 255, 255, 175),
                (194, 216, 203, 120), 1)
        draw.text((60, 320),
                  "Health signals  →  controlled modeling  →  shared evidence",
                  font=font(12, True), fill=(53, 103, 82, 255))
        draw.text((954, 320), "REPEATABLE",
                  font=font(11, True), fill=(205, 160, 48, 255))

        frames.append(image.convert("RGB"))

    save_gif(frames, ASSETS / "research-cards.gif", 100)
    frames[0].save(
        ASSETS / "research-cards-preview.png",
        optimize=True,
    )

def render_metrics():
    W, H = 1200, 230
    cards = [
        {"label": "BASELINE", "value": "V1",
         "caption": "current team baseline", "accent": (219, 170, 45)},
        {"label": "MODEL", "value": "1,200",
         "caption": "ExtraTrees estimators", "accent": (75, 143, 112)},
        {"label": "AGGREGATION", "value": "51%",
         "caption": "tree prediction quantile", "accent": (107, 177, 146)},
        {"label": "PUBLIC MAE", "value": CONTENT["public_mae"],
         "caption": "lower is better", "accent": (219, 170, 45)},
    ]

    def count_text(target, progress):
        if target == "V1":
            return "V1"
        if target == "1,200":
            return f"{int(1200 * progress):,}"
        if target == "51%":
            return f"{int(round(51 * progress))}%"
        if target == CONTENT["public_mae"]:
            start_value = 0.24944
            target_value = float(target)
            current = start_value + (target_value - start_value) * progress
            return f"{current:.10f}"
        return target

    frames = []
    for frame_index in range(36):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        d = ImageDraw.Draw(image, "RGBA")

        rail_y = 20
        d.line((44, rail_y, 1156, rail_y), fill=(195, 215, 204, 150), width=3)
        active_card = (frame_index // 9) % 4
        progress_in_card = (frame_index % 9) / 8

        for index in range(4):
            cx = 175 + index * 290
            node_fill = cards[index]["accent"] if index <= active_card else (205, 219, 211)
            radius = 7 if index == active_card else 5
            d.ellipse((cx - radius, rail_y - radius,
                       cx + radius, rail_y + radius),
                      fill=node_fill + (255,))

        line_end = 175 + active_card * 290
        if active_card < 3:
            line_end += int(290 * progress_in_card)
        d.line((44, rail_y, min(line_end, 1156), rail_y),
               fill=(80, 141, 112, 230), width=4)

        for index, card in enumerate(cards):
            x = 30 + index * 290
            y = 42
            w = 270
            h = 160
            is_active = index == active_card
            already_seen = index < active_card

            if index == 0:
                fill = (14, 58, 47, 255)
                outline = (219, 170, 45, 220)
                label_color = (190, 218, 204, 255)
                value_color = (242, 202, 87, 255)
                caption_color = (183, 207, 196, 235)
            else:
                fill = (255, 255, 255, 245)
                outline = card["accent"] + ((230 if is_active else 110),)
                label_color = (82, 120, 104, 255)
                value_color = (19, 63, 51, 255)
                caption_color = (112, 137, 124, 235)

            rounded(d, (x, y, x + w, y + h), 24,
                    fill, outline, 2)

            d.ellipse((x + 22, y + 22, x + 32, y + 32),
                      fill=card["accent"] + (255,))
            status = "verified" if already_seen else ("active" if is_active else "queued")
            d.text((x + 37, y + 17), status,
                   font=font(12, True), fill=label_color)
            d.text((x + 22, y + 50), card["label"],
                   font=font(15, True), fill=label_color)

            if already_seen:
                progress = 1.0
            elif is_active:
                progress = min(1.0, (frame_index % 9 + 1) / 9)
            else:
                progress = 0.0

            value = count_text(card["value"], progress)
            value_size = 21 if index == 3 else (28 if index == 1 else 29)

            d.text((x + 22, y + 82), value,
                   font=font(value_size, True), fill=value_color)
            d.text((x + 22, y + 124), card["caption"],
                   font=font(13), fill=caption_color)

            bar_x = x + 22
            bar_y = y + 148
            bar_w = 220
            d.rounded_rectangle(
                (bar_x, bar_y, bar_x + bar_w, bar_y + 6),
                radius=3,
                fill=(221, 231, 225, 180) if index else (255, 255, 255, 32),
            )
            fill_w = int(bar_w * progress)
            if fill_w > 0:
                d.rounded_rectangle(
                    (bar_x, bar_y, bar_x + fill_w, bar_y + 6),
                    radius=3,
                    fill=card["accent"] + (255,),
                )

        frames.append(image.convert("RGB"))

    save_gif(frames, ASSETS / "metrics.gif", 100)
    frames[0].save(ASSETS / "metrics-preview.png", optimize=True)






def render_experiment_status():
    W, H = 1200, 430
    status_data = CONTENT.get("experiment_status", {})
    snapshot_date = status_data.get("snapshot_date", "Not dated")
    items = []
    for raw_item in status_data.get("items", []):
        item = dict(raw_item)
        item["accent"] = tuple(item.get("accent", (92, 160, 126)))
        items.append(item)
    if not items:
        raise ValueError("content.json experiment_status.items must not be empty.")
    frames = []

    for frame_index in range(len(items) * 9):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        draw = ImageDraw.Draw(image, "RGBA")
        draw.text((42, 24), "EXPERIMENT REGISTRY",
                  font=font(16, True), fill=(57, 111, 89, 255))
        draw.text((42, 51), "Promote evidence, not lucky scores",
                  font=font(24, True), fill=(18, 63, 51, 255))
        draw.text((995, 30), "SNAPSHOT",
                  font=font(10, True), fill=(106, 137, 122, 255))
        draw.text((995, 49), snapshot_date,
                  font=font(13, True), fill=(35, 83, 65, 255))

        active = (frame_index // 9) % len(items)
        local_progress = (frame_index % 9) / 8
        rail_x = 80
        first_y = 112
        row_gap = 57
        last_y = first_y + row_gap * (len(items) - 1)
        draw.line((rail_x, first_y, rail_x, last_y),
                  fill=(190, 211, 199, 170), width=5)

        if active < len(items) - 1:
            completed_y = first_y + row_gap * active + row_gap * local_progress
        else:
            completed_y = last_y
        draw.line((rail_x, first_y, rail_x, completed_y),
                  fill=(53, 119, 91, 235), width=6)

        for index, item in enumerate(items):
            y = 88 + index * row_gap
            accent = item["accent"]
            is_active = index == active
            is_complete = index < active

            node_r = 10 if is_active else 7
            node_fill = accent + (255,) if index <= active else (176, 201, 188, 210)
            draw.ellipse((rail_x-node_r, y+17-node_r,
                          rail_x+node_r, y+17+node_r), fill=node_fill)

            fill = (17, 65, 51, 250) if is_active else (255, 255, 255, 244)
            outline = accent + (235 if is_active else 115,)
            rounded(draw, (106, y-5, 1158, y+49), 19,
                    fill, outline, 2)

            title_fill = (255,255,255,255) if is_active else (19,64,51,255)
            secondary = (197,223,210,245) if is_active else (102,135,119,235)
            status_fill = (242,204,92,255) if is_active else accent + (255,)

            draw.text((128, y+5), f"0{index+1}",
                      font=font(10, True), fill=status_fill)
            draw.text((170, y+2), item["title"],
                      font=font(15, True), fill=title_fill)
            draw.text((405, y+9), item["status"],
                      font=font(9, True), fill=status_fill)
            draw.text((530, y+2), item["detail"],
                      font=font(12, True), fill=title_fill)
            draw.text((530, y+24), item["evidence"],
                      font=font(10), fill=secondary)

            bar_x = 970
            bar_y = y + 19
            bar_w = 155
            draw.rounded_rectangle((bar_x, bar_y,
                                    bar_x+bar_w, bar_y+7),
                                   radius=4,
                                   fill=(220,231,224,150))
            ratio = 1.0 if is_complete else (local_progress if is_active else 0.0)
            if ratio > 0:
                draw.rounded_rectangle((bar_x, bar_y,
                                        bar_x+bar_w*ratio, bar_y+7),
                                       radius=4,
                                       fill=accent + (255,))

        rounded(draw, (42, 382, 1158, 416), 16,
                (15, 60, 48, 247), (211, 163, 45, 175), 1)
        draw.text((62, 391), "PROMOTION RULE",
                  font=font(10, True), fill=(239, 201, 88, 255))
        draw.text((184, 389),
                  "A model moves to UNIFIED only when improvement survives repeated validation.",
                  font=font(12, True), fill=(220, 238, 228, 245))
        draw.text((1064, 391), "GATED",
                  font=font(10, True), fill=(239, 201, 88, 255))

        frames.append(image.convert("RGB"))

    save_gif(frames, ASSETS / "experiment-status.gif", 100)
    frames[0].save(
        ASSETS / "experiment-status-preview.png",
        optimize=True,
    )

def render_repository_map():
    W, H = 1200, 390
    repository_map = CONTENT.get("repository_map", [])
    if len(repository_map) != 4:
        raise ValueError("content.json repository_map must contain four repositories.")
    nodes = [
        {"name": repository_map[0]["name"], "owner": "JH",
         "role": "INDIVIDUAL NODE", "x": 46, "y": 104,
         "accent": (78, 148, 115)},
        {"name": repository_map[1]["name"], "owner": "BS",
         "role": "INDIVIDUAL NODE", "x": 330, "y": 104,
         "accent": (109, 174, 143)},
        {"name": repository_map[2]["name"], "owner": "SK",
         "role": "INDIVIDUAL NODE", "x": 614, "y": 104,
         "accent": (49, 110, 85)},
    ]
    hub = {
        "name": repository_map[3]["name"],
        "owner": "V1",
        "role": "SHARED BASELINE HUB",
        "x": 898,
        "y": 88,
        "accent": (211, 163, 45),
    }
    card_w = 252
    card_h = 194
    frames = []

    for frame_index in range(42):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((42, 23), "RESEARCH REPOSITORY MAP",
                  font=font(16, True),
                  fill=(57, 111, 89, 255))
        draw.text(
            (42, 49),
            "Private research nodes now · public showcase after official release",
            font=font(14),
            fill=(106, 138, 123, 235),
        )

        active = (frame_index // 10) % 4
        local_progress = (frame_index % 10) / 9
        hub_center = (
            hub["x"] + card_w / 2,
            hub["y"] + card_h / 2,
        )

        for index, node in enumerate(nodes):
            start = (
                node["x"] + card_w,
                node["y"] + card_h / 2,
            )
            end = hub_center
            ratio = (
                1.0
                if index < active
                else (local_progress if index == active else 0.0)
            )
            draw.line((start[0], start[1],
                       end[0], end[1]),
                      fill=(189, 211, 199, 100),
                      width=3)
            if ratio > 0:
                px = start[0] + (end[0] - start[0]) * ratio
                py = start[1] + (end[1] - start[1]) * ratio
                draw.line((start[0], start[1], px, py),
                          fill=node["accent"] + (225,),
                          width=5)

        for index, node in enumerate(nodes):
            x = node["x"]
            y = node["y"]
            is_active = index == active
            is_connected = index < active

            fill = (
                (18, 66, 52, 248)
                if is_active
                else (255, 255, 255, 246)
            )
            outline = node["accent"] + (
                240 if is_active else 140,
            )
            main = (
                (255, 255, 255, 255)
                if is_active
                else (18, 63, 51, 255)
            )
            secondary = (
                (198, 224, 211, 242)
                if is_active
                else (103, 136, 120, 235)
            )

            rounded(
                draw,
                (x, y, x + card_w, y + card_h),
                26,
                fill,
                outline,
                3 if is_active else 2,
            )

            draw.ellipse(
                (x + 20, y + 20, x + 64, y + 64),
                fill=node["accent"] + (255,),
            )
            draw.text(
                (x + 29, y + 31),
                node["owner"],
                font=font(16, True),
                fill=(255, 255, 255, 255),
            )

            status = (
                "CONNECTED"
                if is_connected
                else ("SYNCING" if is_active else "LOCKED")
            )
            draw.text((x + 78, y + 25), status,
                      font=font(10, True),
                      fill=node["accent"] + (255,))
            draw.text((x + 78, y + 45), node["role"],
                      font=font(10, True),
                      fill=secondary)
            draw.text((x + 20, y + 86), node["name"],
                      font=font(16, True),
                      fill=main)
            draw.text((x + 20, y + 117),
                      "Private research workspace",
                      font=font(12),
                      fill=secondary)

            rounded(
                draw,
                (x + 20, y + 151,
                 x + 132, y + 176),
                12,
                node["accent"] + (
                    60 if is_active else 35,
                ),
                node["accent"] + (100,),
                1,
            )
            draw.text((x + 48, y + 157), "PRIVATE",
                      font=font(10, True),
                      fill=main)

        x = hub["x"]
        y = hub["y"]
        rounded(
            draw,
            (x, y, x + card_w, y + card_h),
            28,
            (16, 61, 49, 252),
            hub["accent"] + (245,),
            3,
        )
        draw.ellipse(
            (x + 20, y + 20, x + 68, y + 68),
            fill=hub["accent"] + (255,),
        )
        draw.text((x + 35, y + 34), "V1",
                  font=font(16, True),
                  fill=(255, 255, 255, 255))
        draw.text((x + 82, y + 23), "SHARED HUB",
                  font=font(11, True),
                  fill=(242, 205, 98, 255))
        draw.text((x + 20, y + 88),
                  hub["name"],
                  font=font(16, True),
                  fill=(255, 255, 255, 255))
        draw.text((x + 20, y + 119),
                  "Promotion gate for team experiments",
                  font=font(11),
                  fill=(193, 220, 207, 240))

        rounded(
            draw,
            (42, 328, 1158, 372),
            18,
            (255, 255, 255, 190),
            (197, 218, 206, 135),
            1,
        )
        draw.text((62, 340), "CURRENT STATUS",
                  font=font(10, True),
                  fill=(96, 132, 114, 255))
        draw.text((180, 337), "4 PRIVATE REPOSITORIES",
                  font=font(13, True),
                  fill=(22, 67, 53, 255))
        draw.text((456, 337),
                  "PUBLIC SHOWCASE AFTER OFFICIAL RELEASE",
                  font=font(13, True),
                  fill=(72, 119, 98, 255))

        frames.append(image.convert("RGB"))

    save_gif(
        frames,
        ASSETS / "repository-map.gif",
        100,
    )
    frames[0].save(
        ASSETS / "repository-map-preview.png",
        optimize=True,
    )

def render_team_network():
    W, H = 1200, 350
    team = CONTENT.get("team", ["김지현", "박빛샘", "안상균"])
    if len(team) != 3:
        raise ValueError("content.json team must contain exactly three names.")
    members = [
        {"initials": "JH", "name": team[0],
         "node": "RESEARCH NODE 01", "accent": (80, 149, 116)},
        {"initials": "BS", "name": team[1],
         "node": "RESEARCH NODE 02", "accent": (210, 164, 47)},
        {"initials": "SK", "name": team[2],
         "node": "RESEARCH NODE 03", "accent": (47, 108, 84)},
    ]
    positions = [(55, 92), (430, 92), (805, 92)]
    card_w, card_h = 340, 185
    hub = (600, 307)

    frames = []
    for frame_index in range(42):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((42, 23), "TEAM NETWORK",
                  font=font(16, True), fill=(58, 112, 90, 255))
        draw.text((42, 49),
                  "Individual experiments become shared evidence",
                  font=font(14), fill=(106, 137, 122, 235))

        active = (frame_index // 14) % 3
        local_progress = (frame_index % 14) / 13

        centers = [
            (x + card_w / 2, y + card_h / 2)
            for x, y in positions
        ]

        for index, center in enumerate(centers):
            is_complete = index < active
            is_active = index == active
            ratio = (
                1.0 if is_complete
                else (local_progress if is_active else 0.0)
            )

            start_x = center[0]
            start_y = positions[index][1] + card_h
            end_x, end_y = hub
            partial_x = start_x + (end_x - start_x) * ratio
            partial_y = start_y + (end_y - start_y) * ratio

            draw.line((start_x, start_y, end_x, end_y),
                      fill=(191, 211, 200, 110), width=3)
            if ratio > 0:
                draw.line((start_x, start_y,
                           partial_x, partial_y),
                          fill=members[index]["accent"] + (235,),
                          width=5)

        for index, member in enumerate(members):
            x, y = positions[index]
            is_active = index == active
            is_complete = index < active
            lift = (
                int(8 * math.sin(local_progress * math.pi))
                if is_active else 0
            )
            card_y = y - lift

            if is_active:
                fill = (18, 66, 52, 250)
                outline = member["accent"] + (245,)
                name_color = (255, 255, 255, 255)
                secondary = (197, 224, 211, 245)
                status_color = (238, 204, 101, 255)
            else:
                fill = (255, 255, 255, 246)
                outline = member["accent"] + (145,)
                name_color = (20, 64, 51, 255)
                secondary = (104, 136, 120, 235)
                status_color = member["accent"] + (255,)

            rounded(
                draw,
                (x, card_y, x + card_w, card_y + card_h),
                28,
                fill,
                outline,
                3 if is_active else 2,
            )

            avatar_cx = x + 72
            avatar_cy = card_y + 72
            draw.ellipse(
                (
                    avatar_cx - 42, avatar_cy - 42,
                    avatar_cx + 42, avatar_cy + 42,
                ),
                fill=member["accent"] + (255,),
            )

            initials_box = draw.textbbox(
                (0, 0),
                member["initials"],
                font=font(26, True),
            )
            initials_w = initials_box[2] - initials_box[0]
            draw.text(
                (avatar_cx - initials_w / 2, avatar_cy - 20),
                member["initials"],
                font=font(26, True),
                fill=(255, 255, 255, 255),
            )

            status = (
                "SYNCED"
                if is_complete
                else ("CONNECTING" if is_active else "READY")
            )
            draw.text((x + 132, card_y + 34), status,
                      font=font(11, True), fill=status_color)
            draw.text((x + 132, card_y + 60), member["name"],
                      font=font(23, True), fill=name_color)
            draw.text((x + 132, card_y + 98), member["node"],
                      font=font(12, True), fill=secondary)

            chips = ["MODEL", "REVIEW", "LEARNING"]
            chip_x = x + 28
            for chip in chips:
                chip_w = 78 if chip != "LEARNING" else 92
                rounded(
                    draw,
                    (
                        chip_x, card_y + 140,
                        chip_x + chip_w, card_y + 165,
                    ),
                    12,
                    member["accent"] + (
                        55 if is_active else 30,
                    ),
                    member["accent"] + (90,),
                    1,
                )
                draw.text((chip_x + 13, card_y + 146),
                          chip, font=font(9, True),
                          fill=status_color)
                chip_x += chip_w + 10

        rounded(
            draw,
            (hub[0] - 74, hub[1] - 25,
             hub[0] + 74, hub[1] + 25),
            22,
            (15, 60, 48, 250),
            (219, 171, 47, 235),
            2,
        )
        draw.text((hub[0] - 48, hub[1] - 13),
                  "SHARED V1",
                  font=font(14, True),
                  fill=(242, 204, 91, 255))

        draw.text((42, 320), "3 RESEARCHERS",
                  font=font(11, True),
                  fill=(60, 112, 91, 255))
        draw.text((190, 320), "1 BASELINE",
                  font=font(11, True),
                  fill=(60, 112, 91, 255))
        draw.text((315, 320), "SHARED EVIDENCE",
                  font=font(11, True),
                  fill=(60, 112, 91, 255))
        draw.text((1020, 320), "2거 스트레스조",
                  font=font(12, True),
                  fill=(45, 97, 77, 255))

        frames.append(image.convert("RGB"))

    save_gif(
        frames,
        ASSETS / "team-network.gif",
        100,
    )
    frames[0].save(
        ASSETS / "team-network-preview.png",
        optimize=True,
    )

def render_principles():
    W, H = 1200, 310
    principles = [
        {
            "number": "01",
            "title": "TRAIN-ONLY",
            "subtitle": "전처리 기준은 Train에서만 학습",
            "accent": (218, 169, 47),
            "icon": "lock",
        },
        {
            "number": "02",
            "title": "ONE HYPOTHESIS",
            "subtitle": "한 실험에서는 핵심 변경 하나만",
            "accent": (84, 151, 118),
            "icon": "target",
        },
        {
            "number": "03",
            "title": "MULTI-SEED",
            "subtitle": "분할 운보다 반복 검증을 우선",
            "accent": (112, 177, 145),
            "icon": "seeds",
        },
        {
            "number": "04",
            "title": "PUBLIC-SAFE",
            "subtitle": "원본 데이터와 제출물은 공개 금지",
            "accent": (46, 111, 84),
            "icon": "shield",
        },
    ]
    positions = [(35 + i * 290, 92) for i in range(4)]
    card_w, card_h = 270, 170

    def draw_icon(draw, cx, cy, kind, color, active):
        line = color + (255 if active else 220,)
        pale = (234, 244, 238, 235)

        if kind == "lock":
            draw.arc((cx - 20, cy - 28, cx + 20, cy + 10),
                     190, 350, fill=line, width=4)
            draw.rounded_rectangle(
                (cx - 25, cy - 4, cx + 25, cy + 34),
                radius=8, fill=pale, outline=line, width=3,
            )
            draw.ellipse((cx - 4, cy + 8, cx + 4, cy + 16),
                         fill=line)
            draw.rectangle((cx - 2, cy + 15,
                            cx + 2, cy + 25), fill=line)
        elif kind == "target":
            for radius in [28, 18, 9]:
                draw.ellipse((cx-radius, cy-radius,
                              cx+radius, cy+radius),
                             outline=line, width=3)
            draw.line((cx + 10, cy - 10,
                       cx + 34, cy - 34),
                      fill=(232, 183, 54, 255), width=4)
        elif kind == "seeds":
            nodes = [
                (cx, cy - 27), (cx - 28, cy + 3),
                (cx + 28, cy + 3),
                (cx - 14, cy + 29), (cx + 14, cy + 29),
            ]
            for a, b in [
                (0, 1), (0, 2), (1, 3),
                (1, 4), (2, 3), (2, 4),
            ]:
                draw.line((nodes[a], nodes[b]),
                          fill=line, width=3)
            for index, (x, y) in enumerate(nodes):
                radius = 7 if index == 0 else 6
                fill = (
                    (232, 183, 54, 255)
                    if index == 0
                    else pale
                )
                draw.ellipse((x-radius, y-radius,
                              x+radius, y+radius),
                             fill=fill, outline=line, width=2)
        else:
            shield = [
                (cx, cy - 32), (cx + 29, cy - 19),
                (cx + 23, cy + 15), (cx, cy + 36),
                (cx - 23, cy + 15), (cx - 29, cy - 19),
            ]
            draw.polygon(shield, fill=pale, outline=line)
            draw.line((cx - 12, cy + 1,
                       cx - 3, cy + 11),
                      fill=line, width=5)
            draw.line((cx - 3, cy + 11,
                       cx + 15, cy - 11),
                      fill=line, width=5)

    frames = []
    for frame_index in range(40):
        image = Image.new("RGBA", (W, H), (13, 55, 44, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((40, 24), "RESEARCH PRINCIPLES",
                  font=font(16, True),
                  fill=(235, 202, 100, 255))
        draw.text((40, 51),
                  "점수보다 재현 가능한 개선 과정을 남깁니다.",
                  font=font(24, True),
                  fill=(255, 255, 255, 255))

        active = (frame_index // 10) % 4
        local_progress = (frame_index % 10) / 9
        timeline_y = 84

        draw.line((70, timeline_y, 1130, timeline_y),
                  fill=(149, 190, 168, 110), width=3)

        completed_x = 70 + int((1060 / 3) * active)
        if active < 3:
            completed_x += int(
                (1060 / 3) * local_progress
            )
        else:
            completed_x = 1130

        draw.line((70, timeline_y,
                   completed_x, timeline_y),
                  fill=(229, 181, 55, 230), width=4)

        for index, principle in enumerate(principles):
            x, y = positions[index]
            is_active = index == active
            is_complete = index < active

            fill = (
                (20, 73, 58, 245)
                if is_active
                else (255, 255, 255, 16)
            )
            outline = principle["accent"] + (
                235 if is_active else 85,
            )

            rounded(
                draw,
                (x, y, x + card_w, y + card_h),
                26, fill, outline,
                3 if is_active else 2,
            )

            draw.ellipse(
                (x + 20, y + 20, x + 52, y + 52),
                fill=principle["accent"] + (255,),
            )
            draw.text((x + 25, y + 27),
                      principle["number"],
                      font=font(11, True),
                      fill=(255, 255, 255, 255))

            status = (
                "LOCKED"
                if is_complete
                else ("VERIFYING" if is_active else "PENDING")
            )
            draw.text(
                (x + 63, y + 28),
                status,
                font=font(10, True),
                fill=(
                    (235, 203, 101, 255)
                    if is_active
                    else (179, 207, 193, 225)
                ),
            )

            icon_color = (
                (237, 205, 104)
                if is_active
                else principle["accent"]
            )
            draw_icon(
                draw,
                x + card_w - 58,
                y + 60,
                principle["icon"],
                icon_color,
                is_active,
            )

            draw.text((x + 22, y + 76),
                      principle["title"],
                      font=font(18, True),
                      fill=(255, 255, 255, 255))
            draw.text((x + 22, y + 111),
                      principle["subtitle"],
                      font=font(12),
                      fill=(194, 220, 207, 238))

            px = x + 22
            py = y + 148
            bar_w = card_w - 44
            draw.rounded_rectangle(
                (px, py, px + bar_w, py + 7),
                radius=4,
                fill=(255, 255, 255, 27),
            )
            ratio = (
                1.0
                if is_complete
                else (local_progress if is_active else 0)
            )
            if ratio > 0:
                draw.rounded_rectangle(
                    (px, py,
                     px + bar_w * ratio, py + 7),
                    radius=4,
                    fill=principle["accent"] + (255,),
                )

        rounded(
            draw,
            (40, 274, 1160, 300),
            13,
            (255, 255, 255, 15),
            (171, 204, 187, 70),
            1,
        )
        draw.text(
            (58, 279),
            "NO TEST LEAKAGE  ·  ONE CHANGE  ·  REPEATED VALIDATION  ·  NO RAW DATA",
            font=font(11, True),
            fill=(190, 216, 203, 240),
        )
        draw.text((1034, 279), "SAFE",
                  font=font(11, True),
                  fill=(235, 199, 91, 255))

        frames.append(image.convert("RGB"))

    save_gif(
        frames,
        ASSETS / "principles.gif",
        100,
    )
    frames[0].save(
        ASSETS / "principles-preview.png",
        optimize=True,
    )

def render_baseline_architecture():
    W, H = 1200, 360
    stages = [
        {"title": "INPUT", "subtitle": "17 health & lifestyle columns",
         "accent": (62, 125, 98), "kind": "input"},
        {"title": "FEATURES", "subtitle": "BMI · MAP · ratios · missing",
         "accent": (88, 151, 119), "kind": "features"},
        {"title": "EXTRATREES", "subtitle": "1,200 randomized trees",
         "accent": (36, 92, 72), "kind": "forest"},
        {"title": "Q51", "subtitle": "51% tree-prediction quantile",
         "accent": (208, 162, 46), "kind": "quantile"},
        {"title": "OUTPUT", "subtitle": "stress_score · clipped 0–1",
         "accent": (50, 115, 88), "kind": "output"},
    ]
    centers = [(100 + i * 250, 170) for i in range(5)]
    card_w, card_h = 184, 190

    def draw_icon(draw, cx, cy, kind, color, active):
        line = color + (255 if active else 220,)
        pale = (236, 245, 239, 245)

        if kind == "input":
            draw.rounded_rectangle(
                (cx - 31, cy - 28, cx + 31, cy + 28),
                radius=8, outline=line, width=3,
                fill=(255, 255, 255, 12),
            )
            for dx in [-10, 10]:
                draw.line((cx + dx, cy - 28, cx + dx, cy + 28),
                          fill=line, width=2)
            for dy in [-9, 9]:
                draw.line((cx - 31, cy + dy, cx + 31, cy + dy),
                          fill=line, width=2)
        elif kind == "features":
            nodes = [
                (cx, cy - 26), (cx - 26, cy),
                (cx + 26, cy), (cx, cy + 27),
            ]
            for a, b in [(0, 1), (0, 2), (1, 3), (2, 3)]:
                draw.line((nodes[a], nodes[b]), fill=line, width=3)
            for i, (x, y) in enumerate(nodes):
                r = 7 if i in (0, 3) else 6
                fill = (231, 188, 71, 255) if i == 3 else pale
                draw.ellipse((x-r, y-r, x+r, y+r),
                             fill=fill, outline=line, width=2)
        elif kind == "forest":
            for ox in [-24, 0, 24]:
                root = (cx + ox, cy - 22)
                left = (cx + ox - 10, cy + 4)
                right = (cx + ox + 10, cy + 4)
                draw.line((root, left), fill=line, width=2)
                draw.line((root, right), fill=line, width=2)
                for x, y in [root, left, right]:
                    draw.ellipse((x-4, y-4, x+4, y+4),
                                 fill=color + (255,))
        elif kind == "quantile":
            for i in range(11):
                x = cx - 40 + i * 8
                height = 7 + int(
                    25 * math.exp(-((i - 5) ** 2) / 9)
                )
                draw.rounded_rectangle(
                    (x - 3, cy + 24 - height, x + 3, cy + 26),
                    radius=2, fill=line,
                )
            marker_x = cx + 2
            draw.line((marker_x, cy - 30, marker_x, cy + 28),
                      fill=(234, 184, 53, 255), width=4)
            draw.ellipse((marker_x-6, cy-36,
                          marker_x+6, cy-24),
                         fill=(244, 204, 89, 255))
        else:
            draw.arc((cx - 33, cy - 20, cx + 33, cy + 46),
                     190, 350, fill=line, width=5)
            angle = math.radians(250)
            ex = cx + 25 * math.cos(angle)
            ey = cy + 13 + 25 * math.sin(angle)
            draw.line((cx, cy + 13, ex, ey),
                      fill=(224, 176, 45, 255), width=4)
            draw.ellipse((cx-5, cy+8, cx+5, cy+18),
                         fill=(224, 176, 45, 255))

    frames = []
    for frame_index in range(40):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((42, 24), "BASELINE V1 ARCHITECTURE",
                  font=font(16, True), fill=(57, 111, 89, 255))
        draw.text(
            (42, 50),
            "Weighted Quantile ExtraTrees · one controlled inference path",
            font=font(14), fill=(107, 138, 123, 235),
        )

        active = (frame_index // 8) % 5
        local_progress = (frame_index % 8) / 7
        rail_y = 170
        draw.line((centers[0][0], rail_y,
                   centers[-1][0], rail_y),
                  fill=(188, 210, 198, 175), width=6)

        if active < 4:
            completed_x = centers[active][0] + int(
                (centers[active + 1][0] - centers[active][0])
                * local_progress
            )
        else:
            completed_x = centers[-1][0]
        draw.line((centers[0][0], rail_y,
                   completed_x, rail_y),
                  fill=(51, 117, 90, 238), width=7)

        path_pos = (frame_index / 39) * 4
        idx = min(3, int(path_pos))
        frac = path_pos - idx
        packet_x = centers[idx][0] + (
            centers[idx + 1][0] - centers[idx][0]
        ) * frac

        for offset, alpha, radius in [
            (0, 255, 7), (-15, 150, 5), (-29, 75, 4)
        ]:
            x = packet_x + offset
            draw.ellipse((x-radius, rail_y-radius,
                          x+radius, rail_y+radius),
                         fill=(226, 177, 48, alpha))

        for index, stage in enumerate(stages):
            cx, cy = centers[index]
            x = cx - card_w / 2
            y = cy - card_h / 2
            is_active = index == active
            is_complete = index < active

            if is_active:
                fill = (18, 66, 52, 250)
                outline = stage["accent"] + (245,)
                title_color = (255, 255, 255, 255)
                sub_color = (198, 225, 211, 245)
                code_color = (240, 200, 91, 255)
            else:
                fill = (255, 255, 255, 246)
                outline = stage["accent"] + (145,)
                title_color = (20, 64, 51, 255)
                sub_color = (105, 136, 121, 235)
                code_color = stage["accent"] + (255,)

            rounded(draw,
                    (x, y, x + card_w, y + card_h),
                    25, fill, outline, 3 if is_active else 2)

            draw.text((x + 17, y + 16), f"0{index + 1}",
                      font=font(11, True), fill=code_color)

            icon_color = (
                (237, 203, 99)
                if is_active
                else stage["accent"]
            )
            draw_icon(draw, cx, cy - 20,
                      stage["kind"], icon_color, is_active)

            title_box = draw.textbbox(
                (0, 0), stage["title"],
                font=font(15, True),
            )
            title_w = title_box[2] - title_box[0]
            draw.text((cx - title_w / 2, cy + 39),
                      stage["title"],
                      font=font(15, True),
                      fill=title_color)

            sub_box = draw.textbbox(
                (0, 0), stage["subtitle"],
                font=font(10),
            )
            sub_w = sub_box[2] - sub_box[0]
            draw.text((cx - sub_w / 2, cy + 65),
                      stage["subtitle"],
                      font=font(10),
                      fill=sub_color)

            px1 = x + 18
            py = y + card_h - 17
            rail_w = card_w - 36
            draw.rounded_rectangle(
                (px1, py, px1 + rail_w, py + 6),
                radius=3,
                fill=(
                    (220, 231, 224, 160)
                    if not is_active
                    else (255, 255, 255, 32)
                ),
            )
            ratio = (
                1.0
                if is_complete
                else (local_progress if is_active else 0.0)
            )
            if ratio > 0:
                draw.rounded_rectangle(
                    (px1, py,
                     px1 + rail_w * ratio, py + 6),
                    radius=3,
                    fill=stage["accent"] + (255,),
                )

        rounded(draw, (42, 315, 1158, 344), 14,
                (255, 255, 255, 182),
                (195, 216, 204, 125), 1)
        metadata = [
            ("TREES", "1,200"),
            ("MAX FEATURES", "1"),
            ("LEAF", "1"),
            ("QUANTILE", "0.51"),
            ("PUBLIC MAE", CONTENT.get("public_mae", "N/A")),
        ]
        cursor = 64
        for index, (label, value) in enumerate(metadata):
            draw.text((cursor, 321), label,
                      font=font(10, True),
                      fill=(101, 134, 118, 255))
            cursor += (
                draw.textbbox(
                    (0, 0), label,
                    font=font(10, True)
                )[2] + 8
            )
            draw.text((cursor, 320), value,
                      font=font(11, True),
                      fill=(23, 69, 55, 255))
            cursor += (
                draw.textbbox(
                    (0, 0), value,
                    font=font(11, True)
                )[2] + 24
            )

        frames.append(image.convert("RGB"))

    save_gif(
        frames,
        ASSETS / "baseline-architecture.gif",
        95,
    )
    frames[0].save(
        ASSETS / "baseline-architecture-preview.png",
        optimize=True,
    )

def render_pipeline():
    W, H = 1200, 250
    stages = [
        {"code": "01", "label": "DATA", "sub": "Train-only", "accent": (48, 112, 88)},
        {"code": "02", "label": "FEATURES", "sub": "Health signals", "accent": (76, 142, 111)},
        {"code": "03", "label": "MODEL", "sub": "1,200 trees", "accent": (107, 174, 144)},
        {"code": "04", "label": "Q51", "sub": "51% quantile", "accent": (205, 160, 48)},
        {"code": "05", "label": "VALIDATE", "sub": "Multi-seed", "accent": (34, 92, 71)},
    ]
    centers = [(120 + i * 240, 104) for i in range(5)]

    def draw_stage_icon(draw, cx, cy, stage_index, color, active):
        alpha = 255 if active else 210
        line = color + (alpha,)
        pale = (236, 245, 239, alpha)

        if stage_index == 0:
            draw.ellipse((cx - 18, cy - 15, cx + 18, cy - 3), outline=line, width=3)
            draw.rectangle((cx - 18, cy - 9, cx + 18, cy + 15), outline=line, width=3)
            draw.arc((cx - 18, cy + 3, cx + 18, cy + 16), 0, 180, fill=line, width=3)
        elif stage_index == 1:
            nodes = [(cx, cy - 18), (cx - 18, cy + 14), (cx + 18, cy + 14)]
            draw.line((nodes[0], nodes[1]), fill=line, width=3)
            draw.line((nodes[0], nodes[2]), fill=line, width=3)
            for x, y in nodes:
                draw.ellipse((x - 6, y - 6, x + 6, y + 6),
                             fill=pale, outline=line, width=2)
        elif stage_index == 2:
            lines = [
                (cx, cy - 20, cx - 18, cy + 13),
                (cx, cy - 20, cx + 18, cy + 13),
                (cx - 18, cy + 13, cx - 28, cy + 25),
                (cx - 18, cy + 13, cx - 8, cy + 25),
                (cx + 18, cy + 13, cx + 8, cy + 25),
                (cx + 18, cy + 13, cx + 28, cy + 25),
            ]
            for line_coords in lines:
                draw.line(line_coords, fill=line, width=3)
            for x, y in [
                (cx, cy - 20), (cx - 18, cy + 13), (cx + 18, cy + 13),
                (cx - 28, cy + 25), (cx - 8, cy + 25),
                (cx + 8, cy + 25), (cx + 28, cy + 25),
            ]:
                draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color + (255,))
        elif stage_index == 3:
            for i in range(9):
                x = cx - 32 + i * 8
                height = 5 + int(18 * math.exp(-((i - 4) ** 2) / 7))
                draw.ellipse((x - 3, cy + 14 - height,
                              x + 3, cy + 20 - height), fill=line)
            marker_x = cx + 3
            draw.line((marker_x, cy - 22, marker_x, cy + 23),
                      fill=(232, 184, 57, 255), width=3)
            draw.ellipse((marker_x - 5, cy - 27,
                          marker_x + 5, cy - 17),
                         fill=(239, 191, 61, 255))
        else:
            shield = [
                (cx, cy - 24), (cx + 22, cy - 14), (cx + 17, cy + 12),
                (cx, cy + 27), (cx - 17, cy + 12), (cx - 22, cy - 14),
            ]
            draw.polygon(shield, fill=(232, 242, 236, alpha), outline=line)
            draw.line((cx - 9, cy + 2, cx - 1, cy + 10), fill=line, width=4)
            draw.line((cx - 1, cy + 10, cx + 12, cy - 6), fill=line, width=4)

    frames = []
    for frame_index in range(40):
        image = Image.new("RGBA", (W, H), (247, 250, 248, 255))
        wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        wd = ImageDraw.Draw(wash, "RGBA")
        shift = 18 * math.sin(frame_index * 0.15)
        wd.ellipse((650 + shift, -110, 1280 + shift, 330),
                   fill=(88, 166, 132, 23))
        wd.ellipse((-140 - shift, 90, 420 - shift, 350),
                   fill=(216, 166, 43, 12))
        wash = wash.filter(ImageFilter.GaussianBlur(32))
        image = Image.alpha_composite(image, wash)
        draw = ImageDraw.Draw(image, "RGBA")

        draw.text((40, 24), "RESEARCH WORKFLOW",
                  font=font(15, True), fill=(62, 116, 94, 255))
        draw.text((40, 47), "From raw signals to validated evidence",
                  font=font(14), fill=(104, 137, 122, 235))

        active_stage = (frame_index // 8) % 5
        stage_progress = (frame_index % 8) / 7
        rail_y = 104
        draw.line((centers[0][0], rail_y, centers[-1][0], rail_y),
                  fill=(190, 211, 199, 180), width=6)

        if active_stage < 4:
            completed_x = centers[active_stage][0] + int(
                (centers[active_stage + 1][0] - centers[active_stage][0])
                * stage_progress
            )
        else:
            completed_x = centers[-1][0]
        draw.line((centers[0][0], rail_y, completed_x, rail_y),
                  fill=(54, 118, 91, 235), width=7)

        travel_position = (frame_index / 39) * 4
        packet_index = min(3, int(travel_position))
        packet_fraction = travel_position - packet_index
        packet_x = centers[packet_index][0] + (
            centers[packet_index + 1][0] - centers[packet_index][0]
        ) * packet_fraction
        for offset, alpha, radius in [(0, 255, 7), (-18, 150, 5), (-34, 75, 4)]:
            x = packet_x + offset
            draw.ellipse((x - radius, rail_y - radius,
                          x + radius, rail_y + radius),
                         fill=(229, 179, 49, alpha))

        for index, stage in enumerate(stages):
            cx, cy = centers[index]
            is_active = index == active_stage
            is_complete = index < active_stage

            fill = (21, 69, 55, 255) if is_active else (255, 255, 255, 246)
            outline = stage["accent"] + ((240 if is_active else 140),)
            rounded(draw, (cx - 78, cy - 59, cx + 78, cy + 59),
                    26, fill, outline, 3)

            draw.text((cx - 58, cy - 48), stage["code"],
                      font=font(11, True),
                      fill=(229, 187, 74, 255)
                      if is_active else (106, 143, 126, 235))

            icon_color = (236, 205, 108) if is_active else stage["accent"]
            draw_stage_icon(draw, cx, cy - 5, index, icon_color, is_active)

            label_fill = (255, 255, 255, 255) if is_active else (22, 66, 53, 255)
            sub_fill = (196, 222, 208, 245) if is_active else (108, 137, 123, 235)

            label_box = draw.textbbox((0, 0), stage["label"], font=font(14, True))
            label_width = label_box[2] - label_box[0]
            draw.text((cx - label_width / 2, cy + 30),
                      stage["label"], font=font(14, True), fill=label_fill)

            sub_box = draw.textbbox((0, 0), stage["sub"], font=font(11))
            sub_width = sub_box[2] - sub_box[0]
            draw.text((cx - sub_width / 2, cy + 48),
                      stage["sub"], font=font(11), fill=sub_fill)

            if is_complete:
                draw.ellipse((cx + 53, cy - 50, cx + 73, cy - 30),
                             fill=(64, 139, 104, 255))
                draw.line((cx + 58, cy - 40, cx + 62, cy - 35),
                          fill=(255, 255, 255, 255), width=3)
                draw.line((cx + 62, cy - 35, cx + 69, cy - 44),
                          fill=(255, 255, 255, 255), width=3)

        rounded(draw, (40, 190, 1160, 232), 18,
                (255, 255, 255, 190), (199, 219, 207, 140), 1)
        draw.text((60, 200), "V1 baseline",
                  font=font(13, True), fill=(25, 70, 56, 255))
        draw.text((162, 200), "→",
                  font=font(16, True), fill=(213, 165, 43, 255))
        draw.text((195, 200), "controlled change",
                  font=font(13, True), fill=(72, 119, 98, 255))
        draw.text((340, 200), "→",
                  font=font(16, True), fill=(213, 165, 43, 255))
        draw.text((373, 200), "multi-seed validation",
                  font=font(13, True), fill=(72, 119, 98, 255))
        draw.text((547, 200), "→",
                  font=font(16, True), fill=(213, 165, 43, 255))
        draw.text((580, 200), "shared evidence",
                  font=font(13, True), fill=(72, 119, 98, 255))
        draw.text((962, 200), "LOWER MAE",
                  font=font(12, True), fill=(213, 165, 43, 255))

        frames.append(image.convert("RGB"))

    save_gif(frames, ASSETS / "pipeline.gif", 95)
    frames[0].save(ASSETS / "pipeline-preview.png", optimize=True)

if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    render_layout_helpers()
    render_brand_footer()
    render_section_headers()
    render_navigation()
    render_hero()
    render_research_cards()
    render_metrics()
    render_experiment_status()
    render_repository_map()
    render_team_network()
    render_principles()
    render_baseline_architecture()
    render_pipeline()
    print("Profile assets regenerated.")
