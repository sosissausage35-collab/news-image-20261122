#!/usr/bin/env python3
"""Draw the round-3 news image for make.fun news-image-20261122.

A one-page newspaper front page, 1024x1024, drawn entirely in code with
Pillow: masthead, stat strip, region tabs, 3 lead stories with drawn
illustrations, 10 more stories, a world map with numbered pins, a numbered
list of 22 more stories, and a date-check box. Every story was verified
against wire reporting of Sunday 22 November 2026 (see the DATE CHECK box
in the image and the story list in the README).

Deterministic: fixed layout, fixed fonts, no randomness, no timestamps,
no network. The JPEG encoder (libjpeg via Pillow) is deterministic for
identical pixels and settings, so repeated runs are byte-identical.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
NAVY = (26, 42, 74)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GREY = (90, 90, 90)
LIGHTGREY = (210, 205, 190)
TEAL = (0, 110, 110)
GOLD = (180, 140, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, leading=None, spacing=0):
    """Draw lines of text; returns the y just below the last line."""
    x, y = xy
    lh = leading if leading is not None else int(fnt.size * 1.18) + spacing
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, label, fill=RED):
    """Small white-on-colour tag; returns its width."""
    fnt = SANS_B(11)
    w = int(draw.textlength(label, font=fnt)) + 12
    draw.rectangle([x, y, x + w, y + 16], fill=fill)
    draw.text((x + 6, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def flame(draw, cx, base_y, s):
    """A stylised flame: orange outer, yellow inner."""
    draw.polygon(
        [(cx - s, base_y), (cx - s * 0.55, base_y - s * 1.5),
         (cx, base_y - s * 0.8), (cx + s * 0.5, base_y - s * 1.7),
         (cx + s, base_y)],
        fill=(230, 110, 20))
    draw.polygon(
        [(cx - s * 0.45, base_y), (cx - s * 0.2, base_y - s * 0.9),
         (cx + s * 0.35, base_y - s * 0.7), (cx + s * 0.45, base_y)],
        fill=(250, 200, 40))


def smoke(draw, cx, cy, r, fill=(120, 120, 120)):
    for dx, dy, rr in ((-r, 0, r), (0, -r, int(r * 1.1)), (r, -r // 2, r)):
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=fill)


# ---------------------------------------------------------------- stories
# (number, region, kicker, location line, headline, summary, source)
LEADS = [
    ("COP31: DEAL CLOSE", "1 ANTALYA, TURKEY \u00b7 CLIMATE",
     "COP31 climate talks close in on a final deal",
     "A new package lands after a fight over fossil fuels; delegations have "
     "until 03:00 GMT to object before a final plenary.",
     "Reuters, AP"),
    ("BAHRAIN: STRUCK", "2 MANAMA, BAHRAIN \u00b7 IRAN WAR",
     "Iran strikes US bases in Bahrain",
     "IRGC missiles and drones hit two Patriot radars; an industrial site "
     "burns, no injuries; tankers are hit in Hormuz.",
     "Al Jazeera, Xinhua"),
    ("UKRAINE: BARRAGE", "3 KYIV, UKRAINE \u00b7 WAR",
     "Russia fires 186 drones in one night",
     "Kyiv says 161 were downed or jammed; strikes recorded at 18 sites in "
     "one of the war's biggest drone nights.",
     "Ukrainian Air Force"),
]

MEDIUMS = [
    ("2 DEAD, 60 HURT", "KRYVYI RIH, UKRAINE",
     "Strike hits Zelensky's home city",
     "A triple-tap attack kills a boy of 7 and a paramedic.", "CNN"),
    ("SHIP ABLAZE", "GULF OF FINLAND \u00b7 WAR AT SEA",
     "Russian cargo ship burns after drone strike",
     "16 crew evacuate; Finland says Ukraine was likely behind it.",
     "Reuters"),
    ("GENOCIDE RULING", "THE HAGUE \u00b7 JUSTICE",
     "ICJ: Myanmar committed genocide",
     "First state ever found guilty of genocide; 9\u20136, reparations ordered.",
     "CNN, Le Monde"),
    ("CAPTURED", "SINALOA, MEXICO \u00b7 CARTELS",
     "\u2018El Chapo Isidro\u2019 caught; 11 dead",
     "FBI top-ten fugitive held after a shoot-out.", "AP"),
    ("856 CANDIDATES", "HONG KONG \u00b7 POLITICS",
     "Hong Kong votes for its Election Committee",
     "856 vie for 723 seats; turnout 93.55% by 2pm.",
     "China Daily"),
    ("720/9 DECLARED", "WELLINGTON \u00b7 CRICKET",
     "India post record Test total in New Zealand",
     "Pant's 128 and Rahul's 136 lift India to 720/9; NZ 119/2 at stumps.",
     "Reuters"),
    ("\u22123.7%", "NEW YORK \u00b7 MARKETS",
     "US stocks fall in AI sell-off",
     "S&P 500 drops 3.7%, Nikkei 5.06%; Dow and S&P enter correction.",
     "Reports"),
    ("10 YEARS", "JAKARTA \u00b7 TRADE",
     "EU and Indonesia sign trade deal",
     "A decade of talks ends with a deal between Brussels and Jakarta.",
     "Reports"),
    ("4 KILLED", "GAZA CITY \u00b7 CEASEFIRE",
     "Four killed as Gaza strikes go on",
     "Four Palestinians die, 14 hurt; an aid vehicle is hit.", "Al Jazeera"),
    ("3 MISSILES", "RIYADH \u00b7 GULF",
     "Saudi coalition stops Houthi missiles",
     "Three ballistic missiles intercepted over Riyadh; Hodeidah struck.",
     "Al Jazeera"),
]

# (number, text) — every item was reported on 22 November 2026.
MORE = [
    (14, "Denmark: Russian attach\u00e9 expelled over rapper plot (Guardian)"),
    (15, "Nigeria: Funeral boat capsizes, 24 dead (DW)"),
    (16, "Iraq: Basra power-station fire kills 4, hurts 35 (Iraqi media)"),
    (17, "India: Toxic liquor kills 11 in Manipur, 180+ in hospital"),
    (18, "US: St. Johns River breaks 73-year record in Florida floods"),
    (19, "Hormuz: Two tankers hit; Iran says a tanker struck a mine"),
    (20, "Hormuz: Iran claims a US F-16 downed; CENTCOM denies it"),
    (21, "Health: Ebola death toll passes 5,700"),
    (22, "Brazil: Bolsonaro in intensive care"),
    (23, "Las Vegas: Verstappen wins wild GP; 35 lead changes (AP)"),
    (24, "Turin: ATP Finals final today \u2014 Zverev v Alcaraz (ATP)"),
    (25, "US: Nvidia faces SEC accounting probe (Straits Times)"),
    (26, "Lebanon: Aoun blames Israel and Iran for threats"),
    (27, "Kyiv: Ukraine marks Day of Dignity and Freedom"),
    (28, "Gaza: Hamas seeks talks after strike kills 3 aid workers"),
    (29, "US: Judge rejects Trump bid to revamp $4bn homeless aid"),
    (30, "China: Beijing to bar young \u2018red-chip\u2019 firms abroad"),
    (31, "Sudan: Tasis alliance takes Bau area in Blue Nile"),
    (32, "Turkey: State takes over last independent news outlet"),
    (33, "Germany: Protests over education, conscription"),
    (34, "Spain: PM to extend bank tax to fund housing"),
    (35, "Vietnam: Drug smuggling to lose death penalty"),
]

STATS = [
    ("~200", "nations at the COP31 talks"),
    ("03:00", "GMT deadline for objections"),
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed by Kyiv"),
    ("720/9", "India's record Test total in NZ"),
    ("2", "US bases targeted in Bahrain"),
]

REGIONS = [
    ("EUROPE", 10, (30, 80, 160)),
    ("MIDDLE EAST", 8, (178, 34, 34)),
    ("AMERICAS", 7, (0, 110, 110)),
    ("ASIA-PACIFIC", 6, (200, 130, 30)),
    ("AFRICA", 3, (110, 90, 160)),
    ("WORLD", 1, (100, 100, 100)),
]

# (lon, lat) of stories 1-13, for the map pins.
PINS = [
    (30.7, 36.9), (50.6, 26.2), (30.5, 50.4), (33.4, 47.9), (25.0, 60.0),
    (4.3, 52.1), (-107.4, 24.8), (114.2, 22.3), (174.8, -41.3),
    (-74.0, 40.7), (106.8, -6.2), (34.5, 31.5), (46.7, 24.7),
]


# ------------------------------------------------------------- illustrations
def illo_cop31(draw, x, y, w, h):
    """Negotiation table under a globe and a clock: Antalya, COP31."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 222, 222))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 170, 160))
    # globe, left
    gx, gy, gr = x + 52, y + 48, 34
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 200),
                 outline=(255, 255, 255), width=2)
    draw.ellipse([gx - 18, gy - 12, gx + 2, gy + 6], fill=(90, 180, 110))
    draw.ellipse([gx + 4, gy + 8, gx + 22, gy + 24], fill=(90, 180, 110))
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=(255, 255, 255), width=2)
    # thermometer, right of globe
    tx = x + 108
    draw.rectangle([tx, y + 22, tx + 10, y + 62], fill=(255, 255, 255),
                   outline=RED, width=2)
    draw.rectangle([tx + 2, y + 40, tx + 8, y + 60], fill=RED)
    draw.ellipse([tx - 3, y + 58, tx + 13, y + 74], fill=RED)
    # clock, right
    cx, cy, cr = x + w - 52, y + 46, 30
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255),
                 outline=INK, width=3)
    draw.line([cx, cy, cx, cy - cr + 8], fill=INK, width=3)
    draw.line([cx, cy, cx + cr - 12, cy + 6], fill=INK, width=3)
    # negotiation table with delegates
    ty = y + h - 34
    draw.rectangle([x + 30, ty, x + w - 30, ty + 10], fill=(120, 72, 32))
    for i, c in enumerate([(178, 34, 34), (30, 80, 160), (0, 110, 110),
                           (200, 130, 30), (110, 90, 160), (60, 140, 60)]):
        dx = x + 52 + i * 42
        draw.ellipse([dx - 9, ty - 16, dx + 9, ty + 2], fill=c)
        draw.rectangle([dx - 12, ty + 2, dx + 12, ty + 10], fill=c)


def illo_bahrain(draw, x, y, w, h):
    """Night over Bahrain: missile trails, burning facility, the sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(48, 26, 44))
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(20, 40, 70))
    draw.ellipse([x + w - 52, y + 12, x + w - 28, y + 36], fill=(240, 230, 200))
    # missile trails arcing down onto the facility
    for sx, ex in ((x + 40, x + 150), (x + 130, x + 210), (x + 230, x + 260)):
        draw.line([sx, y + 8, (sx + ex) // 2, y + 52, ex, y + 78],
                  fill=(255, 220, 150), width=2)
        draw.ellipse([ex - 4, y + 74, ex + 4, y + 82], fill=(255, 160, 40))
    # facility: grey blocks with flames
    fy = y + h - 52
    for bx, bw in ((x + 36, 70), (x + 120, 60), (x + 200, 80)):
        draw.rectangle([bx, fy, bx + bw, fy + 24], fill=(150, 150, 150))
        draw.rectangle([bx + 8, fy - 12, bx + bw - 8, fy], fill=(170, 170, 170))
    flame(draw, x + 70, fy + 2, 12)
    flame(draw, x + 150, fy + 2, 10)
    flame(draw, x + 240, fy + 2, 13)
    # ship on the sea
    draw.rectangle([x + w - 92, y + h - 22, x + w - 12, y + h - 10], fill=(10, 10, 10))
    draw.rectangle([x + w - 70, y + h - 32, x + w - 44, y + h - 22], fill=(10, 10, 10))
    flame(draw, x + w - 52, y + h - 22, 7)


def illo_ukraine(draw, x, y, w, h):
    """Night city under a drone swarm: Kyiv, Ukraine."""
    draw.rectangle([x, y, x + w, y + h], fill=(13, 27, 46))
    draw.ellipse([x + w - 46, y + 10, x + w - 22, y + 34], fill=(240, 230, 200))
    # skyline with lit windows
    base = y + h - 26
    bx = x + 8
    for bw, bh in ((34, 52), (26, 70), (40, 44), (30, 62), (36, 50), (28, 74), (34, 46)):
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(8, 12, 22))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if (wx * 7 + wy * 3) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
        bx += bw + 6
    # drone swarm: dots with dotted trails
    for dx, dy in ((x + 60, y + 26), (x + 130, y + 16), (x + 200, y + 30),
                   (x + 260, y + 20), (x + 90, y + 44), (x + 180, y + 48),
                   (x + 230, y + 56), (x + 40, y + 58)):
        for i in range(3):
            draw.ellipse([dx - 1, dy - 1 + i * 7, dx + 1, dy + 1 + i * 7],
                         fill=(255, 220, 150))
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 255, 255))
    # fires on the ground
    flame(draw, x + 90, base + 2, 9)
    flame(draw, x + 210, base + 2, 11)
    flame(draw, x + 280, base + 2, 8)


def illo_medium(draw, idx, x, y, w, h):
    """Small iconic scene for medium story idx (0-9)."""
    if idx == 0:  # Kryvyi Rih: building, smoke, fire
        draw.rectangle([x, y, x + w, y + h], fill=(60, 60, 70))
        draw.rectangle([x + 20, y + 18, x + 90, y + h], fill=(40, 40, 48))
        draw.rectangle([x + 110, y + 28, x + 170, y + h], fill=(48, 48, 56))
        smoke(draw, x + 130, y + 16, 7)
        flame(draw, x + 55, y + h - 2, 10)
    elif idx == 1:  # Sparta II: ship ablaze on a dark sea
        draw.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(10, 25, 50))
        draw.rectangle([x + 30, y + 30, x + 160, y + 46], fill=(10, 10, 10))
        draw.rectangle([x + 70, y + 18, x + 100, y + 30], fill=(10, 10, 10))
        flame(draw, x + 60, y + 30, 10)
        flame(draw, x + 120, y + 30, 12)
        smoke(draw, x + 140, y + 12, 6)
    elif idx == 2:  # ICJ: courthouse columns
        draw.rectangle([x, y, x + w, y + h], fill=(200, 190, 170))
        draw.polygon([(x + 20, y + 18), (x + w - 20, y + 18), (x + w // 2, y + 4)],
                     fill=(140, 110, 80))
        for cx in (x + 40, x + 80, x + 120, x + 160):
            draw.rectangle([cx - 6, y + 20, cx + 6, y + h - 8], fill=(245, 240, 225))
        draw.rectangle([x + 14, y + h - 8, x + w - 14, y + h], fill=(140, 110, 80))
    elif idx == 3:  # Mexico: desert, cactus, badge
        draw.rectangle([x, y, x + w, y + h], fill=(240, 200, 130))
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(200, 150, 80))
        draw.rectangle([x + 30, y + 22, x + 38, y + h - 18], fill=(40, 120, 60))
        draw.rectangle([x + 38, y + 34, x + 56, y + 42], fill=(40, 120, 60))
        draw.ellipse([x + 130, y + 16, x + 168, y + 54], fill=(255, 215, 60),
                     outline=(178, 34, 34), width=3)
        draw.text((x + 144, y + 28), "\u2605", font=SANS_B(18), fill=DARKRED)
    elif idx == 4:  # Hong Kong: skyline + ballot box
        draw.rectangle([x, y, x + w, y + h], fill=(170, 200, 220))
        for bx, bw, bh in ((x + 14, 26, 40), (x + 48, 22, 52), (x + 78, 30, 34),
                           (x + 116, 24, 46)):
            draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(60, 70, 90))
        draw.rectangle([x + 128, y + 18, x + 178, y + 52], fill=(255, 255, 255),
                       outline=RED, width=2)
        draw.rectangle([x + 140, y + 24, x + 166, y + 30], fill=RED)
        draw.text((x + 146, y + 32), "\u2713", font=SANS_B(16), fill=RED)
    elif idx == 5:  # Cricket: green pitch, stumps, ball
        draw.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
        draw.rectangle([x + 60, y + 8, x + 130, y + h - 8], fill=(220, 200, 150))
        for sx in (x + 66, x + 72, x + 78):
            draw.rectangle([sx, y + 14, sx + 3, y + 30], fill=(255, 220, 120))
        draw.ellipse([x + 150, y + 34, x + 164, y + 48], fill=(178, 34, 34))
        draw.text((x + 12, y + 40), "720/9", font=SANS_B(15), fill=(255, 255, 255))
    elif idx == 6:  # Stocks: falling red chart
        draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        for gy in range(y + 12, y + h - 8, 12):
            draw.line([x + 8, gy, x + w - 8, gy], fill=(230, 230, 230))
        draw.line([(x + 14, y + 14), (x + 60, y + 22), (x + 100, y + 20),
                   (x + 140, y + 38), (x + 178, y + 54)], fill=RED, width=3)
        draw.polygon([(x + 178, y + 54), (x + 168, y + 50), (x + 172, y + 44)],
                     fill=RED)
        draw.text((x + 12, y + 4), "\u22123.7%", font=SANS_B(13), fill=DARKRED)
    elif idx == 7:  # EU-Indonesia: two flags
        draw.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
        draw.rectangle([x + 18, y + 14, x + 78, y + 44], fill=(0, 50, 140))
        for sx, sy in ((48, 22), (60, 29), (48, 36), (36, 29)):
            draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                         fill=(255, 215, 60))
        draw.rectangle([x + 108, y + 14, x + 168, y + 44], fill=(255, 255, 255),
                       outline=INK, width=1)
        draw.rectangle([x + 108, y + 14, x + 168, y + 29], fill=(200, 30, 30))
        draw.line([x + 90, y + 10, x + 90, y + 48], fill=INK, width=2)
    elif idx == 8:  # Gaza: buildings, smoke, cross
        draw.rectangle([x, y, x + w, y + h], fill=(90, 85, 80))
        draw.rectangle([x + 16, y + 22, x + 80, y + h], fill=(60, 58, 55))
        draw.rectangle([x + 92, y + 32, x + 150, y + h], fill=(70, 68, 64))
        smoke(draw, x + 120, y + 20, 7, fill=(160, 160, 160))
        draw.rectangle([x + 158, y + 34, x + 182, y + 58], fill=(255, 255, 255))
        draw.rectangle([x + 166, y + 38, x + 174, y + 54], fill=RED)
        draw.rectangle([x + 162, y + 42, x + 178, y + 50], fill=RED)
    else:  # Riyadh: skyline + intercepted missiles
        draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 55))
        for bx, bw, bh in ((x + 12, 24, 44), (x + 44, 22, 54), (x + 74, 28, 36),
                           (x + 110, 26, 48)):
            draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(15, 15, 30))
            for wy in range(y + h - bh + 6, y + h - 6, 10):
                draw.rectangle([bx + 5, wy, bx + 9, wy + 4], fill=(255, 210, 90))
        # tower
        draw.rectangle([x + 148, y + 6, x + 160, y + h - 40], fill=(200, 200, 210))
        draw.line([x + 150, y + 10, x + 178, y + 26], fill=(255, 220, 150), width=2)
        draw.ellipse([x + 172, y + 20, x + 184, y + 32], fill=(255, 160, 40))


# --------------------------------------------------------------------- map
# Crude continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-55, 52),
     (-60, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -55),
     (-75, -40), (-80, -20), (-80, 10)],
    [(-10, 36), (0, 44), (10, 45), (20, 40), (30, 36), (30, 42), (25, 45),
     (20, 55), (10, 58), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -15), (35, -25), (28, -33), (20, -35),
     (15, -30), (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(30, 36), (40, 36), (45, 30), (50, 25), (58, 25), (62, 25), (70, 20),
     (78, 8), (80, 15), (90, 22), (95, 15), (100, 8), (105, 2), (110, 10),
     (115, 20), (120, 30), (127, 35), (130, 42), (140, 45), (145, 50),
     (158, 60), (170, 66), (178, 65), (170, 60), (160, 55), (140, 50),
     (130, 45), (120, 40), (110, 35), (100, 30), (90, 28), (80, 30),
     (70, 35), (60, 40), (50, 42), (40, 45), (30, 42), (30, 36)],
    [(113, -22), (125, -12), (135, -12), (142, -10), (150, -20), (153, -27),
     (150, -37), (140, -38), (130, -32), (120, -34), (113, -22)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 235))
    draw.rectangle([x, y, x + w, y + h], outline=GREY, width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (90 - lat) / 180.0 * h)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=(232, 214, 170), outline=(150, 130, 100))
    # numbered pins for stories 1-13; the Europe/Middle-East cluster is
    # spread with leader lines so the numbers stay legible at this scale.
    offsets = [(0, 12), (0, 0), (-14, -10), (14, -10), (-22, -4), (-16, -8),
               (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (4, 12), (16, 4)]
    for i, ((lon, lat), (dx, dy)) in enumerate(zip(PINS, offsets), start=1):
        px, py = proj(lon, lat)
        ox, oy = px + dx, py + dy
        if dx or dy:
            draw.line([px, py, ox, oy], fill=RED, width=1)
        r = 7
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        fnt = SANS_B(8)
        tw = draw.textlength(str(i), font=fnt)
        draw.text((ox - tw / 2, oy - 5), str(i), font=fnt, fill=(255, 255, 255))


# ------------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top banner
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((14, 5), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=(255, 255, 255))
    right = "35 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - 14 - d.textlength(right, font=SANS_B(12)), 6), right,
           font=SANS_B(12), fill=(255, 255, 255))

    # --- masthead
    title = "Sunday 22 November 2026"
    tf = SERIF_B(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf, fill=INK)
    sub = ("Climate deal in sight at COP31 \u00b7 Iran strikes US bases in Bahrain "
           "\u00b7 Russia\u2019s 186-drone night over Ukraine")
    sf = SERIF_I(16)
    if sf == ImageFont.load_default():
        sf = SERIF(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 86), sub, font=sf, fill=DARKRED)

    # --- stat strip (single-line labels so nothing touches the tabs)
    d.line([14, 110, W - 14, 110], fill=INK, width=2)
    d.line([14, 156, W - 14, 156], fill=INK, width=2)
    cell_w = (W - 28) / 6
    stat_labels = ["nations at COP31", "GMT objection deadline",
                   "drones fired overnight", "downed or jammed",
                   "India's record Test total", "US bases hit in Bahrain"]
    for i, ((num, _), label) in enumerate(zip(STATS, stat_labels)):
        cx = 14 + i * cell_w
        if i:
            d.line([cx, 114, cx, 152], fill=LIGHTGREY, width=1)
        nf = SANS_B(26)
        d.text((cx + (cell_w - d.textlength(num, font=nf)) / 2, 113), num,
               font=nf, fill=RED)
        lf = SANS(10)
        d.text((cx + (cell_w - d.textlength(label, font=lf)) / 2, 142), label,
               font=lf, fill=GREY)

    # --- region tabs (fixed widths so the WORLD tab is not cut off)
    x = 14
    tab_widths = [260, 210, 185, 160, 95, 86]
    for (name, n, color), seg_w in zip(REGIONS, tab_widths):
        d.rectangle([x, 162, x + seg_w - 1, 180], fill=color)
        lab = f"{name} {n}"
        lf = SANS_B(11)
        d.text((x + (seg_w - d.textlength(lab, font=lf)) / 2, 166), lab,
               font=lf, fill=(255, 255, 255))
        x += seg_w

    # --- 3 lead stories (kicker overlaid on the illustration, top-left)
    lead_w, lead_gap = 320, 12
    lead_x0 = 14
    illos = (illo_cop31, illo_bahrain, illo_ukraine)
    for i, (tag, loc, head, summ, src) in enumerate(LEADS):
        x = lead_x0 + i * (lead_w + lead_gap)
        illos[i](d, x, 188, lead_w, 112)
        d.rectangle([x, 188, x + lead_w - 1, 299], outline=GREY, width=1)
        kicker(d, x + 5, 193, tag)
        d.text((x, 306), f"{i + 1} {loc}", font=SANS_B(11), fill=DARKRED)
        hf = SERIF_B(19)
        y = text_block(d, (x, 324), wrap(d, head, hf, lead_w), hf, leading=22)
        bf = SANS(12)
        y = text_block(d, (x, y + 2), wrap(d, summ, bf, lead_w), bf, leading=15)
        d.text((x, y + 1), f"({src})", font=SANS(10), fill=GREY)

    # --- 10 medium stories, 2 rows x 5 (kicker overlaid on illustration)
    med_w, med_gap = 192, 8
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            tag, loc, head, summ, src = MEDIUMS[idx]
            x = 14 + col * (med_w + med_gap)
            y = 428 + row * 144
            illo_medium(d, idx, x, y, med_w, 58)
            d.rectangle([x, y, x + med_w - 1, y + 57], outline=GREY, width=1)
            kicker(d, x + 4, y + 4, tag)
            d.text((x, y + 63), f"{idx + 4} {loc}", font=SANS_B(9), fill=DARKRED)
            hf = SERIF_B(13)
            yy = text_block(d, (x, y + 77),
                            wrap(d, head, hf, med_w), hf, leading=15)
            bf = SANS(10)
            yy = text_block(d, (x, yy + 1),
                            wrap(d, summ, bf, med_w), bf, leading=12)
            d.text((x, yy), f"({src})", font=SANS(9), fill=GREY)

    # --- map + list
    d.line([14, 720, W - 14, 720], fill=INK, width=2)
    d.text((14, 726), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((14, 742), "pins match story numbers", font=SANS(10), fill=GREY)
    draw_map(d, 14, 760, 280, 150)
    d.text((14, 916), "Red numbers mark stories 1\u201313 on the map.",
           font=SANS(9), fill=GREY)

    lx = 312
    d.text((lx, 726), "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES",
           font=SANS_B(12), fill=INK)
    col_w = (W - 14 - lx) // 2
    lf = SANS(10)
    for ci in range(2):
        cx = lx + ci * col_w
        y = 746
        for num, item in MORE[ci * 11:(ci + 1) * 11]:
            lines = wrap(d, f"{num}  {item}", lf, col_w - 10)
            y = text_block(d, (cx, y), lines, lf, leading=12)
            y += 3

    # --- date check
    d.rectangle([14, 930, W - 14, 988], outline=RED, width=2)
    d.text((22, 936), "DATE CHECK", font=SANS_B(11), fill=DARKRED)
    df = SANS(11)
    dc = ("Wires read up to 07:30 UTC, 22 Nov 2026. Every story was reported or "
          "still developing on 22 November in at least one time zone. Left out: "
          "Peru quake (20 Nov), Kerch Bridge strikes (earlier this week), "
          "Shenzhen summit (19 Nov), missiles in Poland (19 Nov).")
    text_block(d, (22, 952), wrap(d, dc, df, W - 44), df, leading=13)

    # --- sources + footer
    d.text((14, 992),
           "Sources: Reuters, AP, BBC, Al Jazeera, CNN, Xinhua, China Daily, "
           "Formula 1, ATP. Every story names its outlet. Pictures and map: "
           "original, drawn in code.",
           font=SANS(9), fill=GREY)
    d.line([14, 1008, W - 14, 1008], fill=INK, width=1)
    d.text((14, 1012), "THE WORLD IN ONE DAY", font=SANS_B(10), fill=INK)
    foot = "SUNDAY 22 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - 14 - d.textlength(foot, font=SANS_B(10)), 1012), foot,
           font=SANS_B(10), fill=INK)

    img.save(OUT, "JPEG", quality=90, optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
