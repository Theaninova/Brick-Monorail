include <BOSL2/std.scad>;
include <BOSL2/beziers.scad>;

Type="straight"; // [straight, curve]
// Only applies to straight tracks
Length=8; // [4:1:56]
// Only applies to curves
Radius=28; // [4:1:36]
// The angle at which the curve starts
StartAngle=0; // [0:15:360]
// The angle at which the curve ends
EndAngle=45; // [0:15:360]

module __CustomizerLimit__() {}

$LDU=0.4;

$stud=12 * $LDU;
$studHeight=4 * $LDU;

$tile=20 * $LDU;
$plate=8 * $LDU;
$studBrim=$tile - $stud;
$studSupport=8 * $LDU;

$fillet=$LDU / 2;
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

module endCapStraight() {
  $width = $baseWidth - $plate * 2;
  union() {
    difference() {
      union() {
        cube([$width, $tile * 2, $tile], anchor=CENTER);
        difference() {
          mirror_copy([0, 1, 0])
            translate([0, $tile / 2, 0])
            cyl(l=$width + $studHeight * 2 + $LDU / 2, d=$stud + $LDU, orient=LEFT, $fn=24);
          mirror_copy([1, 0, 0])
            translate([$tile * 2, 0, -$stud / 2 - 0.2])
            rotate([0, -7, 0])
            cube([$studHeight * 10, $tile * 4, $LDU], anchor=BOTTOM+RIGHT);
        }

        translate([$tile, -$tile, 0]) cube([8 * $LDU, $LDU, $tile], anchor=LEFT+BACK);
      }
      // Brick slots
      mirror_copy([1, 0, 0])
        translate([$tile / 2, -$tile / 2, $tile / 2 - $plate * 2])
        brickSlot();
      // Bridging improvements
      translate([0, 0, $tile / 2 - $plate * 2]) cube([$tile * 2, $tile - 4 * $LDU, $LDU], anchor=BACK);
      translate([0, -4 * $LDU, $tile / 2 - $plate * 2]) cube([$tile * 2, $stud, $LDU * 2], anchor=BACK);

      // Fingernail slot
      mirror_copy([1, 0, 0])
        translate([$width / 2, 0, $tile / 2])
        cube([$LDU * 3, $tile, $LDU * 3], anchor=CENTER)

      translate([$plate, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);
      translate([$width + $plate - $LDU, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);

      // End Slots
      translate([-$tile, -$tile, 0]) cube([8 * $LDU, $LDU, $tile], anchor=RIGHT+FRONT);
      move_copies([[-$tile, -$tile + $LDU], [$tile + 8 * $LDU, -$tile, 0]])
        mirror_copy([1, 0, 0], cp=[-4 * $LDU, 0, 0])
        cyl(d=$fillet, h=$tile, $fn=12);
    }

    // Rail
    translate([0, $teethTolerance / 2, $tile / 2]) cuboid([$teethRailWidth, $tile * 2 - $teethTolerance, $plate], anchor=BOTTOM);
    translate([0, -$tile, $tile / 2]) group() {
      for (i = [0:(2 * $teeth - 1)]) {
        translate([0, i * $teethWidth, 0]) tooth();
      }
    };
  }
}

module monorailCurve(p0, p1, p2, resolution=512) {
  union() {
    /*translate([r * $tile, $tile, 0]) endCapStraight();
    translate([$tile, r * $tile, 0]) rotate(-90) endCapStraight();

    $radius = (r - 2) * $tile;*/

    bez = [p0, p1, p2];
    debug_bezier(bez, N=len(bez)-1);
    $n_teeth = round(bezier_length(bez) / $tile * $teeth);
    echo($n_teeth);
    $points = bezier_curve(bez, $n_teeth);

    translate($points[0]) rot(from=[0, 1, 0], to=bezier_tangent(bez, 0)) fwd($tile) endCapStraight();
    translate($points[len($points) - 1]) rot(from=[0, -1, 0], to=bezier_tangent(bez, 1)) fwd($tile) endCapStraight();
    path_sweep([
      [-$teethRailWidth / 2, $tile / 2 + $plate],
      [-$teethRailWidth / 2, $tile / 2],
      [-2 * $tile, $tile / 2],
      [-2 * $tile, -$tile / 2],
      [2 * $tile, -$tile / 2],
      [2 * $tile, $tile / 2],
      [$teethRailWidth / 2, $tile / 2],
      [$teethRailWidth / 2, $tile / 2 + $plate],
    ], $points, tangent=bezier_tangent(bez, [0:1/$n_teeth:1]));
    translate([0, 0, $tile / 2]) path_copies($points, n=$n_teeth) rotate([-90, 90, 0]) tooth();

    //extrude_2d_shapes_along_bezier(path) square([4 * $tile, $tile]);

    /*translate([2 * $tile, 2 * $tile]) intersection() {
      arced_slot(r=$radius, h=$tile, sd=4 * $tile, sa=sa, ea=ea, $fn=resolution);
    }
    translate([2 * $tile, 2 * $tile, $tile / 2])
      arced_slot($radius, h=$plate, sd=$teethRailWidth, align=V_TOP, sa=sa, ea=ea, $fn=resolution);
    translate([2 * $tile, 2 * $tile, $tile / 2])
      arc_of(n = round(((PI * $radius) / (180 / (ea - sa))) / $tile * $teeth), r=(r - 2) * $tile, rot=true, sa=sa, ea=ea, $fn=resolution)
      tooth();*/
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

if (Type == "straight")
  monorailStraight(l=Length);
else if (Type == "curve")
  monorailCurve(p0=[0, 0, 0], p1=[5, 40, 0], p2=[80, 80, 0]);

// endCapStraight();
// translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("straight.stl");
