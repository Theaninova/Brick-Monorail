# Brick Monorail

Parametric Lego-compatible monorail tracks, designed specifically for 3d printing.
Two orders of magnitude cheaper than buying used.

Since the parts are made parametric, you can have any length or curve radius you want,
but these are the original tracks you can replicate

As an overview, or why it's worth a try: They print rapidly on modern printers, and cost barely anything.

| Preset                        | Cost  | Time | Image                                                                            |
| ----------------------------- | ----- | ---- | -------------------------------------------------------------------------------- |
| C15                           | ~10ct | 45m  | ![C15](./assets/generated/C15.png)                                               |
| C7                            | ~5ct  | 15m  | ![C7](./assets/generated/C7.png)                                                 |
| S25                           | ~12ct | 1h   | ![S25](./assets/generated/S25.png)                                               |
| S10                           | ~5ct  | 15m  | ![S10](./assets/generated/S10.png)                                               |
| S5                            | ~5ct  | 15m  | ![S5](./assets/generated/S5.png)                                                 |
| S4                            | ~5ct  | 15m  | ![S4](./assets/generated/S4.png)                                                 |
| Classic Full Curve (R28 90°)  | ~25ct | 2h   | ![Classic Full Curve](./assets/generated/Classic%20Full%20Curve.png)             |
| Classic Half Curve (R28 45°)  | ~12ct | 1h   | ![Classic Half Curve](./assets/generated/Classic%20Half%20Curve.png)             |
| Classic Full Straight (L32)   | ~20ct | 1.5h | ![Classic Full Straight](./assets/generated/Classic%20Full%20Straight.png)       |
| Classic Half Straight (L16)   | ~10ct | 45m  | ![Classic Half Straight](./assets/generated/Classic%20Half%20Straight.png)       |
| Classic Quarter Straight (L8) | ~5ct  | 15m  | ![Classic Quarter Straight](./assets/generated/Classic%20Quarter%20Straight.png) |

You can also generate your own custom rails with any length, radius or angle.

Todo: ramps, switches, train assembly

## Design differences

Injection molding has vastly different requirements to 3d printing.
Due to this the original rails print absolutely horribly due to the copious amounts of supports needed.
Surfaces printed on supports just never look good.

Because of that, I decided to instead of having a support part on the bottom, I'd carve out space for
a 1x2 plate, which you can fit there for the same effect.

The monorail tracks are also solid now, which is not something you can do in injection molding but leaves
a really nice surface finish at the bottom of the rail for us.

For now, I also use non-baseplate aligned joints for curves. While this means you can't just snap the rails
on a baseplate, it enables you to use straight rails at non-90 degree angles which I think is an absolute
win over the original design since the 45 degree curves are useless outside of joining them with switches.

_These are 3d printing optimized, compatible rails, not replicas. Replicas print horribly due to support._

### Optional Differences

#### Operating on r25 instead of r28

What difference do these three studs make?
With this radius we can take advantage of the pythagorean triples `3/4/5` and `7/24/25` to stay on the stud
grid with turntables.

- Curve C15
- Curve C7
- Straight S21
- Straight S7
- Straight S6
- Incline I4

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
- Set your "Initial Layer Horizontal Expansion" to a value that works for you, for example -0.2mm to compensate for elephant's foot.
  Alternatively, you can trim the extra plastic off by hand.

My prints were done on a modified SecKit SK-Go2 running Klipper, with 10k acceleration and 150mm/s print speed for a good
balance of speed and quality. A short rail will take about an hour to print.

### Filament

| Color             | RAL        | PLA Supplier | ABS Supplier |
| ----------------- | ---------- | ------------ | ------------ |
| Light Bluish Gray | `RAL 7040` | dasfilament  |              |
| Light Gray        | `RAL 7005` |              |              |

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
