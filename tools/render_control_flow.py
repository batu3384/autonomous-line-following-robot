from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "control-flow.png"

WIDTH = 1680
HEIGHT = 1120

BG = (247, 243, 236)
SURFACE = (255, 255, 255)
SOFT = (243, 238, 229)
NAVY = (28, 40, 56)
SLATE = (92, 102, 116)
BORDER = (224, 216, 204)
SHADOW = (231, 222, 210)
ACCENT = (170, 150, 121)
INPUT = (235, 241, 247)
DECISION = (247, 242, 233)
OK = (228, 242, 235)
WARN = (248, 233, 229)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


FONT_TITLE = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
FONT_SUB = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
FONT_SECTION = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
FONT_CARD = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
FONT_BODY = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
FONT_TAG = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)


def card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    fill: tuple[int, int, int],
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 8, x2, y2 + 8), radius=26, fill=SHADOW)
    draw.rounded_rectangle(box, radius=26, fill=fill)
    draw.text((x1 + 22, y1 + 18), title, font=FONT_CARD, fill=NAVY)
    y = y1 + 58
    for line in lines:
        draw.text((x1 + 22, y), line, font=FONT_BODY, fill=SLATE)
        y += 30


def diamond(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: tuple[int, int],
    title: str,
    lines: list[str],
) -> tuple[int, int, int, int]:
    cx, cy = center
    w, h = size
    shadow = [
        (cx, cy - h // 2 + 8),
        (cx + w // 2, cy + 8),
        (cx, cy + h // 2 + 8),
        (cx - w // 2, cy + 8),
    ]
    poly = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy),
    ]
    draw.polygon(shadow, fill=SHADOW)
    draw.polygon(poly, fill=DECISION)
    title_box = draw.textbbox((0, 0), title, font=FONT_CARD)
    draw.text((cx - (title_box[2] - title_box[0]) / 2, cy - 42), title, font=FONT_CARD, fill=NAVY)
    y = cy - 2
    for line in lines:
        line_box = draw.textbbox((0, 0), line, font=FONT_BODY)
        draw.text((cx - (line_box[2] - line_box[0]) / 2, y), line, font=FONT_BODY, fill=SLATE)
        y += 28
    return (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    label: str | None = None,
    label_xy: tuple[int, int] | None = None,
) -> None:
    draw.line((start, end), fill=ACCENT, width=8)
    x1, y1 = start
    x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 > x1 else -1
        head = [(x2, y2), (x2 - 22 * sign, y2 - 14), (x2 - 22 * sign, y2 + 14)]
    else:
        sign = 1 if y2 > y1 else -1
        head = [(x2, y2), (x2 - 14, y2 - 22 * sign), (x2 + 14, y2 - 22 * sign)]
    draw.polygon(head, fill=ACCENT)
    if label and label_xy:
        lx, ly = label_xy
        box = draw.textbbox((0, 0), label, font=FONT_TAG)
        w = box[2] - box[0]
        h = box[3] - box[1]
        draw.rounded_rectangle((lx, ly, lx + w + 24, ly + h + 12), radius=14, fill=SURFACE)
        draw.text((lx + 12, ly + 5), label, font=FONT_TAG, fill=NAVY)


def main() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((22, 22, WIDTH - 22, HEIGHT - 22), radius=36, outline=BORDER, width=3)

    draw.text((54, 38), "Control Flow Implemented in robby.py", font=FONT_TITLE, fill=NAVY)
    draw.text((54, 96), "A different layout: inputs on the left, real decisions in the center, outcomes on the right.", font=FONT_SUB, fill=SLATE)

    # section labels
    draw.text((82, 160), "Inputs", font=FONT_SECTION, fill=NAVY)
    draw.text((630, 160), "Decisions", font=FONT_SECTION, fill=NAVY)
    draw.text((1200, 160), "Outcomes", font=FONT_SECTION, fill=NAVY)

    # left column
    card(
        draw,
        (56, 216, 462, 340),
        "Distance read",
        [
            "measure_distance()",
            "Timeout returns 999 cm",
        ],
        INPUT,
    )
    card(
        draw,
        (56, 386, 462, 540),
        "Line sensors",
        [
            "left_detect = int(not left_sensor.value)",
            "right_detect = int(not right_sensor.value)",
        ],
        INPUT,
    )
    card(
        draw,
        (56, 586, 462, 772),
        "Constants",
        [
            "speed = 0.8",
            "threshold = 10",
            "Obstacle branch uses distance < 10",
            "No steering correction logic",
        ],
        SOFT,
    )
    card(
        draw,
        (56, 818, 462, 1000),
        "Loop note",
        [
            "sleep(0.05) runs only if the loop",
            "does not hit a continue branch",
            "KeyboardInterrupt/finally stop and cleanup GPIO",
        ],
        SOFT,
    )

    # center chain
    card(
        draw,
        (584, 220, 1038, 320),
        "1. Start loop body",
        [
            "Measure distance, then read both sensors.",
        ],
        SURFACE,
    )
    d1 = diamond(
        draw,
        (810, 450),
        (420, 160),
        "2. Lost-line check",
        [
            "left_detect == 0 and right_detect == 0",
            "and distance > 10",
        ],
    )
    d2 = diamond(
        draw,
        (810, 680),
        (420, 160),
        "3. Obstacle check",
        [
            "distance < 10",
            "strictly below threshold",
        ],
    )
    d3 = diamond(
        draw,
        (810, 910),
        (420, 160),
        "4. Forward check",
        [
            "left_detect == 1 or right_detect == 1",
            "if true, move straight ahead",
        ],
    )

    # right outcomes
    card(
        draw,
        (1148, 384, 1602, 502),
        "Lost line outcome",
        [
            "robot.stop()",
            "LED_PIN1 -> LOW",
            "LED_PIN2 -> LOW",
            "continue",
        ],
        OK,
    )
    card(
        draw,
        (1148, 614, 1602, 762),
        "Obstacle outcome",
        [
            "robot.stop()",
            "LED_PIN1 -> HIGH, LED_PIN2 -> HIGH",
            "horn_sound()",
            "continue",
        ],
        WARN,
    )
    card(
        draw,
        (1148, 858, 1602, 962),
        "Forward outcome",
        [
            "robot.forward(speed)",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        INPUT,
    )
    card(
        draw,
        (1148, 1000, 1602, 1074),
        "Else outcome",
        [
            "robot.stop()",
        ],
        SURFACE,
    )

    # arrows
    arrow(draw, (810, 320), (810, d1[1]))
    arrow(draw, (810, d1[3]), (810, d2[1]), label="No", label_xy=(842, 522))
    arrow(draw, (810, d2[3]), (810, d3[1]), label="No", label_xy=(842, 752))
    arrow(draw, (810, d3[3]), (810, 1052), label="No", label_xy=(842, 984))

    arrow(draw, (d1[2], 450), (1148, 438), label="Yes", label_xy=(1012, 414))
    arrow(draw, (d2[2], 680), (1148, 688), label="Yes", label_xy=(1012, 644))
    arrow(draw, (d3[2], 910), (1148, 910), label="Yes", label_xy=(1012, 876))
    arrow(draw, (810, 1052), (1148, 1038))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, quality=95)


if __name__ == "__main__":
    main()
