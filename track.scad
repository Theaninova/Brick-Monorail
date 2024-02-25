include <BOSL2/std.scad>;
include <BOSL2/beziers.scad>;

/* [Print Settings] */
// Some feature are generated with respect to the layer height
LayerHeight = 0.2; // [0.1,0.13,0.2]
// Enable built-in support for 3d printing
Support = true;
/* [Model Settings] */
Length = 8; // [4:1:56]
// Useful when working with Pythagorean Triples
UseLengthForCurveAngle = true;
Radius = 28; // [4:1:36]
// The angle the track takes
Angle = 0.0;

module __CustomizerLimit__() {}

$LDU=0.4;

$stud=12 * $LDU;
$studHeight=4 * $LDU;

$tile=20 * $LDU;
$plate=8 * $LDU;
$studBrim=$tile - $stud;
$studSupport=8 * $LDU;

$fillet=$LDU;
$edgeTolerance=$LDU / 2;

$len = 20;

$baseHeight = $tile;
$baseWidth = 4 * $tile;

$teeth = 5;
$teethTolerance = $LDU;
$teethRailWidth = 10 * $LDU;
$teethWidth = $tile / $teeth;
$teethDepth = 3 * $LDU;

module tooth() {
  $height = $teethWidth - $teethTolerance;
  $rail = $teethRailWidth / 2;
  $topY = $height / 2;
  $midY = $teethTolerance / 2;
  $endX = $rail + $teethDepth;

  translate([0, $teethWidth / 2, 0]) linear_extrude($plate) polygon(points=[
    [$rail, $topY],
    [$endX, $midY],
    [$endX, -$midY],
    [$rail, -$topY],
    [-$rail, -$topY],
    [-$endX, -$midY],
    [-$endX, $midY],
    [-$rail, $topY]
  ]);
}

module brickSlot(w=1, l=1, h=3) {
  cube([$tile * w, $tile * l, $plate * h], anchor=TOP);
  mirror_copy([1, 0, 0])
    mirror_copy([0, 1, 0])
    translate([$tile / 2, $tile / 2, 0])
    cyl(d=$fillet, h=$plate * h, anchor=TOP, $fn=12);
  cube([$stud, $stud, $studHeight * 2], anchor=BOTTOM);
}

module endCapStraight(includeRail=true) {
  $width = $baseWidth - $plate * 2;
  union() {
    difference() {
      union() {
        cube([$width, $tile * 2, $tile], anchor=CENTER);
        mirror_copy([0, 1, 0])
          translate([0, $tile / 2, 0])
          cyl(l=$width + $studHeight * 2 + $LDU / 2, d=$stud, orient=LEFT, $fn=24);

        // End Slot
        translate([$tile + $LDU, -$tile, 0]) cube([6 * $LDU, $LDU, $tile], anchor=LEFT+BACK);

        if (Support) {
          mirror_copy([1, 0, 0]) difference() {
            translate([$tile * 2 - $studHeight, 0, -$tile / 2]) cube([$LDU * 3, $tile * 2 - $LDU - 2, $LDU * 6], anchor=BOTTOM+RIGHT);
            mirror_copy([0, 1, 0])
              translate([0, $tile / 2, 0])
              cyl(l=$width + $studHeight * 2 + $LDU / 2, d=$stud + LayerHeight * 2, orient=LEFT, $fn=24);
          }
        }
      }
      // Brick slots
      mirror_copy([1, 0, 0])
        translate([$tile / 2, -$tile / 2, $tile / 2 - $plate * 2])
        brickSlot();

      // Fingernail slot
      mirror_copy([1, 0, 0])
        translate([$width / 2, 0, $tile / 2])
        cube([$LDU * 3, $tile, $LDU * 3], anchor=CENTER)

      translate([$plate, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);
      translate([$width + $plate - $LDU, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);

      // End Slots
      translate([-$tile, -$tile, 0]) cube([8 * $LDU, $LDU * 2, $tile], anchor=RIGHT+FRONT);
      translate([$tile + 7 * $LDU, -$tile, 0])
        mirror_copy([1, 0, 0], cp=[-3 * $LDU, 0, 0])
        cyl(d=$fillet, h=$tile, $fn=12);
      translate([-$tile, -$tile + $LDU * 2])
        mirror_copy([1, 0, 0], cp=[-4 * $LDU, 0, 0])
        cyl(d=$fillet, h=$tile, $fn=12);
    }

    if (Support) {
      translate([0, -$tile, -$tile / 2])
        rect_tube(size=[$tile * 2 - $LDU * 2, $tile - $LDU * 2], h=$LDU * 4 - LayerHeight, wall=$LDU * 2, anchor=FRONT+BOTTOM);
      translate([0, -$tile, -$tile / 2])
        cube([$LDU * 2, $tile - $LDU * 2, $LDU * 4 - LayerHeight], anchor=FRONT+BOTTOM);
    }

    if (includeRail) {
      // Rail
      translate([0, $teethTolerance / 2, $tile / 2]) cuboid([$teethRailWidth, $tile * 2 - $teethTolerance, $plate], anchor=BOTTOM);
      translate([0, -$tile, $tile / 2]) group() {
        for (i = [0:(2 * $teeth - 1)]) {
          translate([0, i * $teethWidth, 0]) tooth();
        }
      };
    }
  }
}

module monorailCurve(r=28, sa, ea, p1) {
  $n_teeth = round((PI * r * $tile) / (295 / abs(-sa - ea)));
  angle = [180 - ea, 180 + sa];
  points = arc($n_teeth, r=(r * $tile), angle=angle);

  translate([r * $tile, 0, 0]) union() {
    translate(points[0]) rot(180 - ea) back($tile) endCapStraight(includeRail=false);
    translate(points[len(points) - 1]) rot(sa) back($tile) endCapStraight(includeRail=false);
    difference() {
      path_sweep([
        [-$teethRailWidth / 2, $tile / 2 + $plate],
        [-$teethRailWidth / 2, $tile / 2],
        [-2 * $tile, $tile / 2],
        [-2 * $tile, -$tile / 2],
        [2 * $tile, -$tile / 2],
        [2 * $tile, $tile / 2],
        [$teethRailWidth / 2, $tile / 2],
        [$teethRailWidth / 2, $tile / 2 + $plate],
      ], points);
      translate(points[0]) rot(-ea) cube([$tile * 6, $tile * 4, $tile], anchor=CENTER);
      translate(points[len(points) - 1]) rot(sa) cube([$tile * 6, $tile * 4, $tile], anchor=CENTER);
      translate(points[0]) rot(-ea) translate([0, -$teethWidth/2, 0]) cube([$tile * 6, $tile * 4, $tile], anchor=BOTTOM+FRONT);
      translate(points[len(points) - 1]) rot(sa) translate([0, $teethWidth/2, 0]) cube([$tile * 6, $tile * 4, $tile], anchor=BOTTOM+BACK);
    }
    translate([0, 0, $tile / 2]) arc_copies($n_teeth + 1, r=(r * $tile), sa=angle[0], ea=angle[1] - (180 * ($teethWidth / (PI * r * $tile)))) tooth();
  }
}

module monorailStraight(l) {
  union() {
    translate([0, $tile, 0]) endCapStraight();
    translate([0, (l - 1) * $tile, 0]) rotate(180) endCapStraight();
    if (l > 4) {
      translate([0, $tile * 2, 0]) cube([4 * $tile, (l - 4) * $tile, $tile], anchor=FRONT);
      translate([0, $tile * 2, $tile / 2]) cube([$teethRailWidth, (l - 4) * $tile, $plate], anchor=BOTTOM+FRONT);
      translate([0, $tile * 2, $tile / 2]) group() {
        for (i = [0:($teeth * (l - 4) - 1)]) {
          translate([0, i * $teethWidth, 0]) tooth();
        }
      };
    }
  }
}

if (Angle == 0)
  monorailStraight(l=Length);
else
  monorailCurve(Radius, sa=0, ea=UseLengthForCurveAngle ? asin(Length / Radius) : Angle);

// endCapStraight();
// translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("straight.stl");
//translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("4dbrix_curve.stl");
