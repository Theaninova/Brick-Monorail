# Brick Monorail

Parametric Lego-compatible monorail tracks, designed specifically for 3d printing.

Since the parts are made parametric, you can have any length or curve radius you want,
but these are the original tracks you can replicate

| Common Name         | Supported | Material Cost | Print Time |
| ------------------- | --------- | ------------- | ---------- |
| Straight Long/Full  | ✓         |               |            |
| Straight Short/Half | ✓         |               |            |
| Straight Quarter    | ✓         |               |            |
| Straight 4-studs    | ✓         | ~10ct         | 15m        |
| Curve Long          | ✓         |               |            |
| Curve Short Left    | ⚠️        |               |            |
| Curve Short Right   | ⚠️        |               |            |
| Ramp Upper Part     | ❌        |               |            |
| Ramp Lower Part     | ❌        |               |            |
| Monoswitch          | ❌        |               |            |
| Point Right         | ❌        |               |            |
| Point Left          | ❌        |               |            |

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

Two C15 and one C7 make exactly a 90 degree turn, where every part stays on the stud grid.

An s-curve with C7 moves two studs, and can be extended by 1 stud
with S7 or 3 studs with S21.

An s-curve with C15 moves over 20 studs, and can be extended by 8 studs
with S6 or 28 studs with S21 straights.

## Printing

To be compatible with standard bricks, the following print settings are strongly advised

- Nozzle: 0.4, this is equivalent to 1 LDU.
- Layer height: Ideally 0.1, though 0.2 will also do. Refrain from using 0.15, since that does not cleanly divides the LDU.
  - Make sure your initial layer height is either 0.2 or 0.4!
- Enable Bridge Settings in Cura
- Supports: **none**. These parts are designed to be printed without any supports, though some of the bridging is not exactly
  what you would call easy for the printer, so be on the lookout.
- Make sure you set your "Initial Layer Horizontal Expansion" to a value that works for you, for example -0.2mm to
  compensate for elephant's foot. Better overcompensate here, if you don't do this you might not be able to fit
  bricks in the slot!

My prints were done on a modified SecKit SK-Go2 running Klipper, with 10k acceleration and 150mm/s print speed for a good
balance of speed and quality. A short rail will take about an hour to print.

### Filament

| Color             | RAL Color  | Pantone | PLA                                                                                                         | ABS |
| ----------------- | ---------- | ------- | ----------------------------------------------------------------------------------------------------------- | --- | --- |
| Light Bluish Gray | `RAL 7040` |         | [dasfilament 20,56€/kg](https://www.dasfilament.de/filament-spulen/pla-1-75-mm/8/pla-filament-1-75-mm-grau) |     |
| Light Gray        | `RAL 7005` |         |                                                                                                             |     |     |

- None of these colors will be an exact match, just the texture of 3d printing it can make a huge difference, but usually fall close enough in the range.
- The original rails will be in _Light Gray_, not _Light Bluish Gray_, but since I barely own any pre- 2004 color change bricks I chose to match my other bricks instead.
- Most bricks are injection molded from ABS, however I find PLA to be much more easy and safe to handle.
  - PLA starts to deform at 60&deg;C, so don't leave it in the sun or in your car.
  - PLA is brittle. While ABS deforms with force applied to it, PLA will just snap.
  - ABS is harder to print, an enclosure is a must, and warping can be difficult to handle.

#### Printing Safety

In case you are new to 3D printing:

- Most filaments (including PLA) release toxic gases when _burned_
- FDM printing can cause fine particle emission
- ABS when heated to normal printing temperatures can release styrene fumes
