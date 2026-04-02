from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "control-flow.png"

WIDTH = 1720
HEIGHT = 1480
BG = (247, 243, 236)
NAVY = (29, 42, 57)
SLATE = (92, 102, 116)
ACCENT = (166, 148, 121)
WHITE = (255, 255, 255)
SOFT = (243, 238, 229)
MUTED = (224, 216, 204)
GREEN = (232, 243, 235)
RED = (248, 234, 230)


def load_fonts() -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, ...]:
    try:
        return (
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20),
        )
    except Exception:
        fallback = ImageFont.load_default()
        return fallback, fallback, fallback, fallback


FONT_TITLE, FONT_LABEL, FONT_BODY, FONT_TAG = load_fonts()


def draw_multiline(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    lines: list[str],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    gap: int = 34,
) -> None:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += gap


def draw_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    fill: tuple[int, int, int] = WHITE,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=28, fill=fill)
    draw.text((x1 + 28, y1 + 24), title, font=FONT_LABEL, fill=NAVY)
    draw_multiline(draw, (x1 + 28, y1 + 74), lines, FONT_BODY, SLATE)


def draw_diamond(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: tuple[int, int],
    title: str,
    lines: list[str],
) -> tuple[int, int, int, int]:
    cx, cy = center
    w, h = size
    points = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy),
    ]
    draw.polygon(points, fill=SOFT)
    title_bbox = draw.textbbox((0, 0), title, font=FONT_LABEL)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text((cx - title_w / 2, cy - 46), title, font=FONT_LABEL, fill=NAVY)
    line_y = cy - 8
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=FONT_BODY)
        line_w = line_bbox[2] - line_bbox[0]
        draw.text((cx - line_w / 2, line_y), line, font=FONT_BODY, fill=SLATE)
        line_y += 30
    return (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)


def draw_arrow(
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
        head = [(x2, y2), (x2 - 24 * direction, y2 - 14), (x2 - 24 * direction, y2 + 14)]
    else:
        direction = 1 if y2 > y1 else -1
        head = [(x2, y2), (x2 - 14, y2 - 24 * direction), (x2 + 14, y2 - 24 * direction)]
    draw.polygon(head, fill=ACCENT)
    if label and label_pos:
        bbox = draw.textbbox((0, 0), label, font=FONT_TAG)
        pad_x = 12
        pad_y = 8
        lx, ly = label_pos
        draw.rounded_rectangle(
            (lx, ly, lx + (bbox[2] - bbox[0]) + pad_x * 2, ly + (bbox[3] - bbox[1]) + pad_y * 2),
            radius=16,
            fill=WHITE,
        )
        draw.text((lx + pad_x, ly + pad_y - 2), label, font=FONT_TAG, fill=NAVY)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((26, 26, WIDTH - 26, HEIGHT - 26), radius=40, outline=MUTED, width=3)
    draw.text((68, 56), "Control Flow Implemented in robby.py", font=FONT_TITLE, fill=NAVY)
    draw.text((68, 118), "Validated against the actual branch order in motor_control().", font=FONT_BODY, fill=SLATE)

    draw_box(
        draw,
        (90, 190, 560, 330),
        "1. Measure distance",
        [
            "measure_distance() triggers HC-SR04, waits for echo,",
            "and returns 999 cm on timeout.",
        ],
    )
    draw_box(
        draw,
        (90, 388, 560, 528),
        "2. Read both line sensors",
        [
            "left_detect = int(not left_sensor.value)",
            "right_detect = int(not right_sensor.value)",
        ],
    )

    d1 = draw_diamond(
        draw,
        (325, 635),
        (430, 190),
        "3. Lost-line branch?",
        [
            "left_detect == 0 and right_detect == 0",
            "and distance > obstacle_distance_threshold",
        ],
    )

    d2 = draw_diamond(
        draw,
        (325, 900),
        (430, 190),
        "4. Obstacle branch?",
        [
            "distance < obstacle_distance_threshold",
            "strictly below 10 cm in this script",
        ],
    )

    d3 = draw_diamond(
        draw,
        (325, 1165),
        (430, 190),
        "5. Forward branch?",
        [
            "left_detect == 1 or right_detect == 1",
            "if true, keep moving straight",
        ],
    )

    draw_box(
        draw,
        (740, 555, 1630, 710),
        "Stop + LEDs off + continue",
        [
            "robot.stop()",
            "GPIO.output(LED_PIN1, LOW)",
            "GPIO.output(LED_PIN2, LOW)",
            "continue skips time.sleep(0.05)",
        ],
        fill=GREEN,
    )

    draw_box(
        draw,
        (740, 820, 1630, 1010),
        "Stop + LEDs on + horn + continue",
        [
            "robot.stop()",
            "GPIO.output(LED_PIN1, HIGH)",
            "GPIO.output(LED_PIN2, HIGH)",
            "horn_sound(); continue",
        ],
        fill=RED,
    )

    draw_box(
        draw,
        (740, 1085, 1630, 1215),
        "Drive forward",
        [
            "robot.forward(speed)",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        fill=GREEN,
    )

    draw_box(
        draw,
        (740, 1230, 1630, 1365),
        "Else: stop in-place",
        [
            "robot.stop()",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        fill=WHITE,
    )

    draw_box(
        draw,
        (90, 1300, 620, 1430),
        "Loop tail and cleanup",
        [
            "Only non-continue paths reach time.sleep(0.05).",
            "KeyboardInterrupt and finally both stop,",
            "silence the buzzer, and cleanup GPIO.",
        ],
        fill=SOFT,
    )

    # main spine
    draw_arrow(draw, (325, 330), (325, 388))
    draw_arrow(draw, (325, 528), (325, d1[1]))

    # branch 1
    draw_arrow(draw, (d1[2], 635), (740, 632), label="Yes", label_pos=(548, 588))
    draw_arrow(draw, (325, d1[3]), (325, d2[1]), label="No", label_pos=(354, 745))

    # branch 2
    draw_arrow(draw, (d2[2], 900), (740, 915), label="Yes", label_pos=(548, 855))
    draw_arrow(draw, (325, d2[3]), (325, d3[1]), label="No", label_pos=(354, 1015))

    # branch 3
    draw_arrow(draw, (d3[2], 1165), (740, 1150), label="Yes", label_pos=(548, 1120))
    draw_arrow(draw, (d3[2], 1200), (740, 1297), label="No", label_pos=(548, 1252))

    # final note
    draw_box(
        draw,
        (740, 190, 1630, 340),
        "Validated constants",
        [
            "speed = 0.8",
            "obstacle_distance_threshold = 10",
            "The obstacle branch uses distance < 10, not <= 10.",
        ],
        fill=SOFT,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95)


if __name__ == "__main__":
    main()
