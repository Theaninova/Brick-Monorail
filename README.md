# Brick Monorail

Parametric Lego-compatible monorail tracks, designed specifically for 3d printing.

Since the parts are made parametric, you can have any length or curve radius you want,
but these are the original tracks you can replicate

| Lego Name         | Parameters               |
| ----------------- | ------------------------ |
| Straight Long     | `monorailStraight(l=32)` |
| Straight Short    | `monorailStraight(l=8)`  |
| Curve Long        | `monorailCurve90(r=28)`  |
| Curve Short Left  | ❌                       |
| Curve Short Right | ❌                       |
| Ramp Upper Part   | ❌                       |
| Ramp Lower Part   | ❌                       |
| Monoswitch        | ❌                       |
| Point Right       | ❌                       |
| Point Left        | ❌                       |

## Design differences

Injection molding has vastly different requirements to 3d printing.
Due to this the original rails print absolutely horribly due to the copious amounts of supports needed.
Surfaces printed on supports just never look good.

Because of that, I decided to instead of having a support part on the bottom, I'd carve out space for
a 1x2 plate, which you can fit there for the same effect.

The monorail tracks are also solid now, which is not something you can do in injection molding but leaves
a really nice surface finish at the bottom of the rail for us.

_These are 3d printing optimized, compatible rails, not replicas. Replicas print horribly due to support._

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
