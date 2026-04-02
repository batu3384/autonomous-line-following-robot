from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "control-flow.png"

WIDTH = 1680
HEIGHT = 1360

BG = (247, 243, 236)
SURFACE = (255, 255, 255)
SURFACE_SOFT = (244, 239, 230)
NAVY = (29, 42, 57)
SLATE = (90, 102, 116)
ACCENT = (169, 151, 123)
BORDER = (224, 216, 204)
GREEN = (228, 242, 235)
RED = (248, 233, 229)
BLUE = (232, 240, 246)
SHADOW = (226, 217, 205)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


FONT_TITLE = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
FONT_SUBTITLE = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
FONT_CARD_TITLE = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
FONT_BODY = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
FONT_TAG = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)


def draw_shadowed_round_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    radius: int = 28,
    shadow_offset: int = 8,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + shadow_offset, x2, y2 + shadow_offset), radius=radius, fill=SHADOW)
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_wrapped_lines(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    lines: list[str],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    gap: int = 32,
) -> None:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += gap


def card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    fill: tuple[int, int, int] = SURFACE,
) -> None:
    draw_shadowed_round_rect(draw, box, fill)
    x1, y1, _, _ = box
    draw.text((x1 + 24, y1 + 22), title, font=FONT_CARD_TITLE, fill=NAVY)
    draw_wrapped_lines(draw, x1 + 24, y1 + 66, lines, FONT_BODY, SLATE)


def diamond(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    size: tuple[int, int],
    title: str,
    lines: list[str],
) -> tuple[int, int, int, int]:
    cx, cy = center
    w, h = size
    shadow_points = [
        (cx, cy - h // 2 + 8),
        (cx + w // 2, cy + 8),
        (cx, cy + h // 2 + 8),
        (cx - w // 2, cy + 8),
    ]
    draw.polygon(shadow_points, fill=SHADOW)
    points = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy),
    ]
    draw.polygon(points, fill=SURFACE_SOFT)
    title_box = draw.textbbox((0, 0), title, font=FONT_CARD_TITLE)
    title_width = title_box[2] - title_box[0]
    draw.text((cx - title_width / 2, cy - 42), title, font=FONT_CARD_TITLE, fill=NAVY)
    draw_wrapped_lines(draw, cx - 146, cy - 2, lines, FONT_BODY, SLATE, gap=28)
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
        bbox = draw.textbbox((0, 0), label, font=FONT_TAG)
        pad_x = 12
        pad_y = 7
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
    draw.text((56, 44), "Control Flow Implemented in robby.py", font=FONT_TITLE, fill=NAVY)
    draw.text((56, 104), "Visual summary of the actual Raspberry Pi script, not an idealized flow.", font=FONT_SUBTITLE, fill=SLATE)

    # Left rail
    card(
        draw,
        (56, 164, 398, 1270),
        "Runtime truth",
        [
            "Source of truth: robby.py",
            "speed = 0.8",
            "obstacle_distance_threshold = 10",
            "Obstacle check is distance < 10",
            "No left/right correction logic",
            "time.sleep(0.05) runs only if the loop",
            "does not hit a continue branch",
            "",
            "GPIO map",
            "TRIG 23, ECHO 24",
            "LED1 16, LED2 25",
            "Buzzer 22",
            "Left sensor 17",
            "Right sensor 27",
            "Robot left=(7, 8), right=(9, 10)",
        ],
        fill=SURFACE_SOFT,
    )

    # Main flow
    card(
        draw,
        (456, 178, 900, 300),
        "1. Measure distance",
        [
            "Call measure_distance().",
            "HC-SR04 timeout returns 999 cm.",
        ],
    )
    card(
        draw,
        (456, 338, 900, 460),
        "2. Read both line sensors",
        [
            "left_detect = int(not left_sensor.value)",
            "right_detect = int(not right_sensor.value)",
        ],
    )

    d1 = diamond(
        draw,
        (678, 600),
        (360, 150),
        "3. Lost-line branch?",
        [
            "left_detect == 0 and right_detect == 0",
            "and distance > 10",
        ],
    )
    d2 = diamond(
        draw,
        (678, 820),
        (360, 150),
        "4. Obstacle branch?",
        [
            "distance < 10",
            "strictly less than the threshold",
        ],
    )
    d3 = diamond(
        draw,
        (678, 1040),
        (360, 150),
        "5. Forward branch?",
        [
            "left_detect == 1 or right_detect == 1",
            "if true, move straight ahead",
        ],
    )

    card(
        draw,
        (980, 530, 1552, 654),
        "Stop + LEDs off + continue",
        [
            "robot.stop()",
            "LED_PIN1 -> LOW",
            "LED_PIN2 -> LOW",
            "continue skips the sleep below",
        ],
        fill=GREEN,
    )
    card(
        draw,
        (980, 742, 1552, 918),
        "Stop + LEDs on + horn + continue",
        [
            "robot.stop()",
            "LED_PIN1 -> HIGH",
            "LED_PIN2 -> HIGH",
            "horn_sound()",
            "continue",
        ],
        fill=RED,
    )
    card(
        draw,
        (980, 970, 1552, 1078),
        "Drive forward",
        [
            "robot.forward(speed)",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        fill=BLUE,
    )
    card(
        draw,
        (980, 1140, 1552, 1270),
        "Else: stay stopped",
        [
            "robot.stop()",
            "LED_PIN1 -> LOW, LED_PIN2 -> LOW",
        ],
        fill=SURFACE,
    )

    card(
        draw,
        (456, 1140, 900, 1270),
        "Loop tail and cleanup",
        [
            "Only non-continue paths reach sleep(0.05).",
            "KeyboardInterrupt and finally both call stop.",
            "Then buzzer off + GPIO.cleanup().",
        ],
        fill=SURFACE_SOFT,
    )

    # Arrows
    arrow(draw, (678, 300), (678, 338))
    arrow(draw, (678, 460), (678, d1[1]))
    arrow(draw, (678, d1[3]), (678, d2[1]), label="No", label_xy=(708, 688))
    arrow(draw, (678, d2[3]), (678, d3[1]), label="No", label_xy=(708, 908))
    arrow(draw, (678, d3[3]), (678, 1140), label="No", label_xy=(708, 1110))

    arrow(draw, (d1[2], 600), (980, 592), label="Yes", label_xy=(824, 560))
    arrow(draw, (d2[2], 820), (980, 830), label="Yes", label_xy=(824, 792))
    arrow(draw, (d3[2], 1040), (980, 1024), label="Yes", label_xy=(824, 1000))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95)


if __name__ == "__main__":
    main()
