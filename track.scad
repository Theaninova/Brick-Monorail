include <lib/BOSL/shapes.scad>;
include <lib/BOSL/transforms.scad>;
include <lib/BOSL/constants.scad>;
include <lib/BOSL/beziers.scad>;

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


//translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("straight.stl");


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
  cuboid([$tile * w, $tile * l, $plate * h], align=V_DOWN);
  mirror_copy([1, 0, 0])
    mirror_copy([0, 1, 0])
    translate([$tile / 2, $tile / 2, 0])
    cyl(d=$fillet, h=$plate * h, align=V_DOWN, $fn=12);
  cuboid([$stud, $stud, $studHeight * 2], align=V_TOP);
}

module endCapStraight() {
  $width = $baseWidth - $plate * 2;
  union() {
    difference() {
      union() {
        cuboid([$width, $tile * 2, $tile], edges=EDGE_BOT_FR+EDGE_BOT_RT+EDGE_BOT_LF);
        difference() {
          mirror_copy([0, 1, 0])
            translate([0, $tile / 2, 0])
            cyl(l=$width + $studHeight * 2, d=$stud, orient=ORIENT_X, $fn=24);
          mirror_copy([1, 0, 0])
            translate([$tile * 2, 0, -$stud / 2])
            rotate([0, -14, 0])
            cuboid([$studHeight * 10, $tile * 4, $LDU * 2], align=V_TOP+V_LEFT);
        }

        translate([$tile, -$tile, 0]) cuboid([8 * $LDU, $LDU, $tile], align=V_RIGHT+V_FRONT);
      }
      // Fingernail slot
      mirror_copy([1, 0, 0])
        translate([$width / 2, 0, $tile / 2])
        cuboid([$LDU, $tile, $LDU])

      translate([$plate, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);
      translate([$width + $plate - $LDU, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);

      // Brick slots
      mirror_copy([1, 0, 0])
        translate([$tile / 2, -$tile / 2, $tile / 2 - $plate * 2])
        brickSlot();
      // Bridging improvements
      translate([0, 0, $tile / 2 - $plate * 2]) cuboid([$tile * 2, $tile - 4 * $LDU, $LDU], align=V_FRONT);
      translate([0, -4 * $LDU, $tile / 2 - $plate * 2]) cuboid([$tile * 2, $stud, $LDU * 2], align=V_FRONT);

      // End Slots
      translate([-$tile, -$tile, 0]) cuboid([8 * $LDU, $LDU, $tile], align=V_LEFT+V_BACK);
      place_copies([[-$tile, -$tile + $LDU], [$tile + 8 * $LDU, -$tile, 0]])
        mirror_copy([1, 0, 0], cp=[-4 * $LDU, 0, 0])
        cyl(d=$fillet, h=$tile, $fn=12);
    }

    // Rail
    translate([0, $teethTolerance / 2, $tile / 2]) cuboid([$teethRailWidth, $tile * 2 - $teethTolerance, $plate], align=V_TOP);
    translate([0, -$tile, $tile / 2]) group() {
      for (i = [0:(2 * $teeth - 1)]) {
        translate([0, i * $teethWidth, 0]) tooth();
      }
    };
  }
}

module curve90(r=12) {
  translate([r * $tile, $tile, 0]) endCapStraight();
  translate([$tile, r * $tile, 0]) rotate(-90) endCapStraight();
  //ir = ($r 
  path = [[2 * $tile, r * $tile, 0], [r * $tile / 2, r * $tile, 0], [r * $tile, r * $tile / 2, 0], [r * $tile,  2 * $tile, 0]];
  extrude_2d_shapes_along_bezier(path) {
    circle(r=10);
  }
}

//curve90();
endCapStraight();
