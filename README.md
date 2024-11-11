# Brick Monorail

Parametric Lego-compatible monorail tracks, designed specifically for 3d printing.
Two orders of magnitude cheaper than buying used.

Since the parts are made parametric, you can have any length or curve radius you want,
but these are the original tracks you can replicate

As an overview, or why it's worth a try: They print rapidly on modern printers, and cost barely anything.

| Preset                        | Cost  | Time | Image                            |
| ----------------------------- | ----- | ---- | -------------------------------- |
| C15                           | ~10ct | tbd  | ![C15](./assets/classic/C15.svg) |
| C7                            | ~5ct  | tbd  | ![C7](./assets/classic/C7.svg)   |
| S25                           | ~12ct | tbd  | (todo)                           |
| S10                           | ~5ct  | tbd  | ![S10](./assets/classic/S10.svg) |
| S5                            | ~5ct  | tbd  | ![S5](./assets/classic/S5.svg)   |
| S4                            | ~5ct  | tbd  | (todo)                           |
| Classic Full Curve (R28 90°)  | ~25ct | tbd  | (todo)                           |
| Classic Half Curve (R28 45°)  | ~12ct | tbd  | (todo)                           |
| Classic Full Straight (L32)   | ~20ct | tbd  | (todo)                           |
| Classic Half Straight (L16)   | ~10ct | tbd  | (todo)                           |
| Classic Quarter Straight (L8) | ~5ct  | tbd  | (todo)                           |

You can also generate your own custom rails with any length, radius or angle.

Todo: ramps, switches, train assembly

## Design Options

For now, I also use non-baseplate aligned joints for curves. While this means you can't just snap the rails
on a baseplate, it enables you to use straight rails at non-90 degree angles which I think is an absolute
win over the original design since the 45 degree curves are useless outside of joining them with switches.

### Classic

**PETG/PVA support interface is mandatory to get satisfactory results**

![C15](./assets/classic/C15.svg)

Uses the classic shell design from the injection moulded parts.
PETG/PVA supports are a must if you want the part to come out clean!

There's also an option that makes the side studs solid.

### Solid

![C15](./assets/solid/C15.svg)
![Standoff](./assets/standoff.svg)

This one is optimized for 3D printing, with the rail solid and flush to the bed.
Prints entirely supportless.

Requires additional pieces per rail:

- 2x printed standoff, these are inserted into the bottom, and need to be fixated there (glue, melting).
  If you don't use any original Monorail tracks you can also simply place a 2x2 plate there (this changes the height).
- 8x 4274 (technic pin with stud)

Prints a _lot_ faster than the classic option.

## Operating on R25 instead of R28

What difference do these three studs make?
With this radius we can take advantage of the pythagorean triples `3/4/5` and `7/24/25` to stay on the stud
grid with turntables.

- Curve C15
- Curve C7
- Straight S25
- Straight S10
- Straight S5
- Straight S4

How it fits

- Two C15 and one C7 make exactly a 90 degree turn, where every part stays on the stud grid.
- An s-curve with C15 moves over 20 studs, diagonals can be done with any length divisible by 5
- An s-curve with C7 moves two studs, but diagonals require a full S25 to land cleanly again.

![](./assets/r25.svg)

## Printing

To be compatible with standard bricks, the following print settings are strongly advised

- Nozzle: **0.4**, this is equivalent to 1 LDU.
- Layer height: **0.2**, less than that is barely better and just causes more problems than it solves.
  If you want to go lower, it's advisable to use heights that satisfy `0.4 % h == 0` such as 0.1.
  - **Make sure your initial layer height is either 0.2 or 0.4!**
- Supports: **yes**, normal, don't use tree supports.
  - Multi-material is highly recommended: use PETG or PVA as a support interface layer.
    This is the only way to get these parts to print cleanly.
- **Make sure you have your flow and z offset calibrated perfectly.**
  These parts have very small tolerances, it is absolutely vital you have this right
  or you will end up with parts that have insufficient or too high clamping force.

I print on a modified Voron 2.4 with toolchanger capability through Stealthchanger.

### Filament

| Color             | RAL        | PLA Supplier           | ABS Supplier |
| ----------------- | ---------- | ---------------------- | ------------ |
| Light Bluish Gray | `RAL 7040` | dasfilament, Prusament |              |
| Light Gray        | `RAL 7005` |                        |              |

- None of these colors will be an exact match, just the texture of 3d printing it can make a huge difference, but usually fall close enough in the range.
- The original rails will be in _Light Gray_, not _Light Bluish Gray_, but since I barely own any pre- 2004 color change bricks I chose to match my other bricks instead.

_Notes for newcomers:_

- Most bricks are injection molded from ABS, however I find PLA to be much more easy and safe to handle.
- PLA starts to deform at 60°C, so don't leave it in the sun or in your car.
- PLA is brittle. While ABS deforms with force applied to it, PLA will just snap.
- ABS is harder to print, an enclosure is a must, and warping can be difficult to handle.

#### Printing Safety

In case you are new to 3D printing:

- Most filaments (including PLA) can release toxic gases when _burned_
- FDM printing can cause fine particle emission
- ABS when heated to normal printing temperatures can release styrene fumes
