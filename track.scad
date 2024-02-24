include <lib/BOSL/shapes.scad>;
include <lib/BOSL/transforms.scad>;
include <lib/BOSL/constants.scad>;

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
  difference () {
    cuboid([$stud+2*$LDU, $stud+2*$LDU, $studHeight], align=V_TOP);
    mirror_copy([1, -1, 0])
      mirror_copy([1, 0, 0])
      translate([$stud / 2, 0, 0])
      cyl(d=2*$LDU, h=$studHeight, align=V_TOP+V_RIGHT, $fn=12);
  }
  mirror_copy([1, 0, 0])
    mirror_copy([0, 1, 0])
    translate([$stud/2+$LDU, $stud/2+$LDU, 0])
    cyl(d=$fillet, h=$studHeight, align=V_TOP, $fn=12);
}

module endCap() {
  $width = $baseWidth - $plate * 2;
  union() {
    difference() {
      union() {
        cuboid([$width, $tile * 2, $tile], edges=EDGE_BOT_FR+EDGE_BOT_RT+EDGE_BOT_LF);
        mirror_copy([0, 1, 0])
          translate([0, $tile / 2, 0])
          cyl(l=$width + $studHeight * 2, d=$stud, orient=ORIENT_X, $fn=24);

        translate([$tile, -$tile, 0]) cuboid([8 * $LDU, $LDU, $tile], align=V_RIGHT+V_FRONT);
      }
      mirror_copy([1, 0, 0])
        mirror_copy([0, 1, 0])
        translate([$width / 2, $tile / 2, 0])
        torus(d2=$edgeTolerance, d=$stud, orient=ORIENT_X, $fn=24);

      translate([$plate, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);
      translate([$width + $plate - $LDU, $tile / 2, $tile - $LDU]) cube([$LDU, $tile, $LDU]);
  
      mirror_copy([1, 0, 0])
        translate([$tile / 2, -$tile / 2, $tile / 2 - $plate])
        brickSlot();


      translate([-$tile, -$tile, 0]) cuboid([8 * $LDU, $LDU, $tile], align=V_LEFT+V_BACK);
      place_copies([[-$tile, -$tile + $LDU], [$tile + 8 * $LDU, -$tile, 0]])
        mirror_copy([1, 0, 0], cp=[-4 * $LDU, 0, 0])
        cyl(d=$fillet, h=$tile, $fn=12);
    }

    translate([0, $teethTolerance / 2, $tile / 2]) cuboid([$teethRailWidth, $tile * 2 - $teethTolerance, $plate], align=V_TOP);
    translate([0, -$tile, $tile / 2]) group() {
      for (i = [0:(2 * $teeth - 1)]) {
        translate([0, i * $teethWidth, 0]) tooth();
      }
    };
  }
}


endCap();
