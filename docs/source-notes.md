# Source Notes

This repository is built around the real Raspberry Pi script exported from the original robot project: [`robby.py`](../robby.py).

What is preserved from the Raspberry Pi file:

- GPIO numbering and pin map
- ultrasonic distance measurement logic
- `gpiozero.Robot`, `Buzzer`, and `LineSensor` usage
- obstacle threshold of `10 cm`
- fixed forward speed of `0.8`
- the exact high-level behavior implemented in the script

What this repository adds around that file:

- product photography for GitHub presentation
- a documented wiring table
- the original course report
- a lightweight validation workflow that checks Python syntax on every push

Important accuracy note:

- The current script does not implement left/right differential steering.
- If either line sensor sees the line, the robot drives forward.
- If both sensors lose the line, it stops.
- If an obstacle is closer than the threshold, it stops and triggers the buzzer and LEDs.

