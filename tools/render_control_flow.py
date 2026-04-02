from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "control-flow.png"

WIDTH = 1680
HEIGHT = 1280

BG = (247, 243, 236)
SURFACE = (255, 255, 255)
SURFACE_SOFT = (244, 239, 230)
NAVY = (29, 42, 57)
SLATE = (91, 102, 116)
ACCENT = (166, 148, 121)
BORDER = (223, 215, 203)
GREEN = (228, 242, 235)
RED = (248, 233, 229)
BLUE = (232, 240, 246)
SHADOW = (228, 219, 207)


def font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


FONT_TITLE = font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
FONT_SUBTITLE = font("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
FONT_CARD_TITLE = font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
FONT_BODY = font("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
FONT_TAG = font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)


def shadow_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int] = SURFACE,
    radius: int = 28,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 8, x2, y2 + 8), radius=radius, fill=SHADOW)
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def write_lines(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    lines: list[str],
    font_obj: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    gap: int = 30,
) -> None:
    x, y = start
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += gap


def card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    fill: tuple[int, int, int] = SURFACE,
) -> None:
    shadow_card(draw, box, fill=fill)
    x1, y1, _, _ = box
    draw.text((x1 + 24, y1 + 20), title, font=FONT_CARD_TITLE, fill=NAVY)
    write_lines(draw, (x1 + 24, y1 + 64), lines, FONT_BODY, SLATE)


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
    draw.polygon(shadow, fill=SHADOW)
    poly = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy),
    ]
    draw.polygon(poly, fill=SURFACE_SOFT)
    title_box = draw.textbbox((0, 0), title, font=FONT_CARD_TITLE)
    title_width = title_box[2] - title_box[0]
    draw.text((cx - title_width / 2, cy - 42), title, font=FONT_CARD_TITLE, fill=NAVY)
    write_lines(draw, (cx - 140, cy - 4), lines, FONT_BODY, SLATE, gap=28)
    return (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    label: str | None = None,
    label_pos: tuple[int, int] | None = None,
) -> None:
    draw.line((start, end), fill=ACCENT, width=8)
    x1, y1 = start
    x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        head = [(x2, y2), (x2 - 22 * direction, y2 - 14), (x2 - 22 * direction, y2 + 14)]
    else:
        direction = 1 if y2 > y1 else -1
        head = [(x2, y2), (x2 - 14, y2 - 22 * direction), (x2 + 14, y2 - 22 * direction)]
    draw.polygon(head, fill=ACCENT)

    if label and label_pos:
        lx, ly = label_pos
        bbox = draw.textbbox((0, 0), label, font=FONT_TAG)
        pad_x = 12
        pad_y = 6
        draw.rounded_rectangle(
            (lx, ly, lx + (bbox[2] - bbox[0]) + 2 * pad_x, ly + (bbox[3] - bbox[1]) + 2 * pad_y),
            radius=14,
            fill=SURFACE,
        )
        draw.text((lx + pad_x, ly + pad_y - 1), label, font=FONT_TAG, fill=NAVY)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((24, 24, WIDTH - 24, HEIGHT - 24), radius=38, outline=BORDER, width=3)

    draw.text((56, 42), "Control Flow Implemented in robby.py", font=FONT_TITLE, fill=NAVY)
    draw.text((56, 102), "Redesigned around the real loop so the diagram reads cleanly at a glance.", font=FONT_SUBTITLE, fill=SLATE)

    # Top info row
    card(
        draw,
        (56, 164, 528, 294),
        "Source of truth",
        [
            "This visual is based on the Raspberry Pi file",
            "exported as robby.py.",
        ],
        fill=SURFACE_SOFT,
    )
    card(
        draw,
        (604, 164, 1060, 294),
        "Validated constants",
        [
            "speed = 0.8",
            "obstacle_distance_threshold = 10",
            "Obstacle branch uses distance < 10",
        ],
        fill=SURFACE_SOFT,
    )
    card(
        draw,
        (1136, 164, 1610, 294),
        "Important behavior",
        [
            "No left/right steering correction exists.",
            "sleep(0.05) runs only on the non-continue path.",
        ],
        fill=SURFACE_SOFT,
    )

    # Center spine
    card(
        draw,
        (320, 354, 790, 466),
        "1. Measure distance",
        [
            "Call measure_distance().",
            "Return 999 cm on timeout.",
        ],
    )
    card(
        draw,
        (320, 522, 790, 634),
        "2. Read both line sensors",
        [
            "left_detect = int(not left_sensor.value)",
            "right_detect = int(not right_sensor.value)",
        ],
    )
    d1 = diamond(
        draw,
        (555, 756),
        (390, 158),
        "3. Lost-line branch?",
        [
            "left_detect == 0 and right_detect == 0",
            "and distance > 10",
        ],
    )
    d2 = diamond(
        draw,
        (555, 944),
        (390, 158),
        "4. Obstacle branch?",
        [
            "distance < 10",
            "strictly less than the threshold",
        ],
    )
    d3 = diamond(
        draw,
        (555, 1130),
        (390, 158),
        "5. Forward branch?",
        [
            "left_detect == 1 or right_detect == 1",
            "if true, move straight ahead",
        ],
    )

    # Right-side outcomes
    card(
        draw,
        (972, 688, 1554, 804),
        "Stop + LEDs off + continue",
        [
            "robot.stop()",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
            "continue skips the final sleep",
        ],
        fill=GREEN,
    )
    card(
        draw,
        (972, 882, 1554, 1028),
        "Stop + LEDs on + horn + continue",
        [
            "robot.stop()",
            "LED_PIN1 -> HIGH, LED_PIN2 -> HIGH",
            "horn_sound()",
            "continue",
        ],
        fill=RED,
    )
    card(
        draw,
        (972, 1072, 1554, 1178),
        "Drive forward",
        [
            "robot.forward(speed)",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        fill=BLUE,
    )
    card(
        draw,
        (972, 1200, 1554, 1260),
        "Else: stay stopped",
        [
            "robot.stop()",
        ],
        fill=SURFACE,
    )

    # Footer note
    card(
        draw,
        (320, 1200, 790, 1260),
        "Loop tail and cleanup",
        [
            "Only the non-continue path reaches sleep(0.05).",
        ],
        fill=SURFACE_SOFT,
    )

    # Vertical spine arrows
    arrow(draw, (555, 466), (555, 522))
    arrow(draw, (555, 634), (555, d1[1]))
    arrow(draw, (555, d1[3]), (555, d2[1]), label="No", label_pos=(586, 828))
    arrow(draw, (555, d2[3]), (555, d3[1]), label="No", label_pos=(586, 1014))
    arrow(draw, (555, d3[3]), (555, 1200), label="No", label_pos=(586, 1186))

    # Branch arrows
    arrow(draw, (d1[2], 756), (972, 746), label="Yes", label_pos=(802, 718))
    arrow(draw, (d2[2], 944), (972, 954), label="Yes", label_pos=(802, 916))
    arrow(draw, (d3[2], 1130), (972, 1124), label="Yes", label_pos=(802, 1096))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95)


if __name__ == "__main__":
    main()
