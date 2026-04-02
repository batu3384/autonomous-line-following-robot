from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "control-flow.png"

WIDTH = 1680
HEIGHT = 1040

BG = (11, 18, 32)
PANEL = (21, 33, 53)
PANEL_2 = (28, 43, 67)
TEXT = (238, 242, 247)
MUTED = (152, 165, 187)
BORDER = (44, 61, 90)
CYAN = (87, 197, 255)
AMBER = (255, 188, 92)
TEAL = (73, 208, 159)
CORAL = (255, 122, 97)
LAV = (150, 137, 255)
WHITE = (255, 255, 255)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


FONT_TITLE = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42)
FONT_SUB = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
FONT_SECTION = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
FONT_CARD = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
FONT_BODY = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
FONT_TAG = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: tuple[int, int, int], radius: int = 26, outline: tuple[int, int, int] | None = None) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2 if outline else 0)


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, lines: list[str], fill: tuple[int, int, int], accent: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, fill, radius=26, outline=BORDER)
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 88, y1 + 26), radius=6, fill=accent)
    draw.text((x1 + 18, y1 + 42), title, font=FONT_CARD, fill=TEXT)
    y = y1 + 78
    for line in lines:
        draw.text((x1 + 18, y), line, font=FONT_BODY, fill=MUTED)
        y += 28


def diamond(draw: ImageDraw.ImageDraw, center: tuple[int, int], size: tuple[int, int], title: str, lines: list[str], fill: tuple[int, int, int], accent: tuple[int, int, int]) -> tuple[int, int, int, int]:
    cx, cy = center
    w, h = size
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy)]
    draw.polygon(pts, fill=fill, outline=BORDER)
    draw.rounded_rectangle((cx - 70, cy - h // 2 + 16, cx + 70, cy - h // 2 + 28), radius=6, fill=accent)
    title_box = draw.textbbox((0, 0), title, font=FONT_CARD)
    title_w = title_box[2] - title_box[0]
    draw.text((cx - title_w / 2, cy - 30), title, font=FONT_CARD, fill=TEXT)
    y = cy + 4
    for line in lines:
        line_box = draw.textbbox((0, 0), line, font=FONT_BODY)
        line_w = line_box[2] - line_box[0]
        draw.text((cx - line_w / 2, y), line, font=FONT_BODY, fill=MUTED)
        y += 26
    return (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int], label: str | None = None, label_pos: tuple[int, int] | None = None) -> None:
    draw.line((start, end), fill=color, width=6)
    x1, y1 = start
    x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 1 if x2 > x1 else -1
        head = [(x2, y2), (x2 - 18 * s, y2 - 11), (x2 - 18 * s, y2 + 11)]
    else:
        s = 1 if y2 > y1 else -1
        head = [(x2, y2), (x2 - 11, y2 - 18 * s), (x2 + 11, y2 - 18 * s)]
    draw.polygon(head, fill=color)
    if label and label_pos:
        lx, ly = label_pos
        bbox = draw.textbbox((0, 0), label, font=FONT_TAG)
        rounded(draw, (lx, ly, lx + (bbox[2] - bbox[0]) + 20, ly + (bbox[3] - bbox[1]) + 10), PANEL_2, radius=14)
        draw.text((lx + 10, ly + 4), label, font=FONT_TAG, fill=WHITE)


def elbow(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    color: tuple[int, int, int],
    label: str | None = None,
    label_pos: tuple[int, int] | None = None,
) -> None:
    for start, end in zip(points, points[1:]):
        draw.line((start, end), fill=color, width=6)
    arrow(draw, points[-2], points[-1], color, label=label, label_pos=label_pos)


def main() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    rounded(draw, (16, 16, WIDTH - 16, HEIGHT - 16), BG, radius=34, outline=BORDER)
    draw.text((48, 38), "robby.py Control Surface", font=FONT_TITLE, fill=TEXT)
    draw.text((48, 92), "Dark technical layout built around the real Raspberry Pi loop.", font=FONT_SUB, fill=MUTED)

    # left rail
    rounded(draw, (46, 150, 360, 980), PANEL, radius=28, outline=BORDER)
    draw.text((74, 182), "Inputs", font=FONT_SECTION, fill=TEXT)
    card(
        draw,
        (66, 234, 340, 364),
        "Distance",
        ["measure_distance()", "timeout -> 999 cm"],
        PANEL_2,
        CYAN,
    )
    card(
        draw,
        (66, 392, 340, 548),
        "Line sensors",
        ["left_detect = int(not left_sensor.value)", "right_detect = int(not right_sensor.value)"],
        PANEL_2,
        CYAN,
    )
    card(
        draw,
        (66, 576, 340, 742),
        "Constants",
        ["speed = 0.8", "threshold = 10", "obstacle uses distance < 10"],
        PANEL_2,
        AMBER,
    )
    card(
        draw,
        (66, 770, 340, 930),
        "Loop note",
        ["sleep(0.05) only on", "the non-continue path"],
        PANEL_2,
        LAV,
    )

    # center decisions
    draw.text((520, 182), "Decisions", font=FONT_SECTION, fill=TEXT)
    rounded(draw, (430, 220, 1120, 930), PANEL, radius=28, outline=BORDER)
    card(
        draw,
        (476, 260, 790, 364),
        "1. Loop start",
        ["measure distance", "read both sensors"],
        PANEL_2,
        CYAN,
    )
    d1 = diamond(draw, (635, 500), (300, 150), "2. Lost line?", ["both sensors 0", "and distance > 10"], PANEL_2, AMBER)
    d2 = diamond(draw, (915, 500), (300, 150), "3. Obstacle?", ["distance < 10", "strict threshold"], PANEL_2, CORAL)
    d3 = diamond(draw, (775, 748), (320, 150), "4. Move forward?", ["left_detect == 1", "or right_detect == 1"], PANEL_2, TEAL)

    # right outcomes
    rounded(draw, (1180, 150, 1636, 980), PANEL, radius=28, outline=BORDER)
    draw.text((1212, 182), "Outcomes", font=FONT_SECTION, fill=TEXT)
    card(draw, (1200, 244, 1616, 372), "Lost-line outcome", ["robot.stop()", "LEDs -> LOW", "continue"], PANEL_2, AMBER)
    card(draw, (1200, 418, 1616, 574), "Obstacle outcome", ["robot.stop()", "LEDs -> HIGH", "horn_sound()", "continue"], PANEL_2, CORAL)
    card(draw, (1200, 620, 1616, 734), "Forward outcome", ["robot.forward(speed)", "LEDs -> LOW"], PANEL_2, TEAL)
    card(draw, (1200, 782, 1616, 886), "Else outcome", ["robot.stop()"], PANEL_2, LAV)

    # arrows
    arrow(draw, (790, 312), (790, 425), AMBER)
    elbow(draw, [(785, 500), (900, 420), (1080, 300), (1200, 308)], AMBER, "Yes", (958, 392))
    elbow(draw, [(635, 575), (635, 648), (915, 648), (915, 575)], AMBER, "No", (690, 606))

    arrow(draw, (1065, 500), (1200, 496), CORAL, "Yes", (1112, 452))
    elbow(draw, [(915, 575), (915, 650), (775, 650), (775, 673)], CORAL, "No", (848, 648))

    arrow(draw, (775, 823), (1200, 677), TEAL, "Yes", (1032, 706))
    elbow(draw, [(775, 823), (775, 912), (1200, 834)], LAV, "No", (1018, 848))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, quality=95)


if __name__ == "__main__":
    main()
