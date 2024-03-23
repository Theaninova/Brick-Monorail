include <BOSL2/std.scad>;

/* [Print Settings] */
Tolerance = 0.4;
// Mid-print stud inserts allowing the studs to be printed facing up seperately
StudInserts = true;
// Mid-print slot inserts eliminating the need for supports
AntiStudInserts = true;
// Part to generate
Type = "rail"; // [rail,switch,studs,antistuds]

/* [Model Settings] */
Length = 20; // [4:1:56]
Radius = 25; // [4:1:36]
// The angle the track takes
Angle = 15;
// Useful when working with Pythagorean Triples
AngleIsLength = true;
SwitchSupportCount = 3;
SwitchFrontLength = 4;

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

module antiStudInsert(carve=true, depth=$studHeight * 2, supportHeight=$LDU * 4, supportWidth=$LDU * 4) {
  difference() {
    union() {
      cube([$tile * 2, $tile, depth + supportHeight], anchor=FRONT+BOTTOM);
      translate([0, $tile + supportWidth + (carve ? 0 : Tolerance), 0])
        cube([
          $tile * 2 + supportWidth + (carve ? 0 : Tolerance * 2),
          supportWidth + $tile * 0.6 + (carve ? 0 : Tolerance * 2),
          depth + supportHeight
        ], anchor=BACK+BOTTOM);
    }

    if (carve) {
      mirror_copy([1, 0, 0])
      translate([$tile / 2, $tile / 2, 0]) group() {
        cube([$stud, $stud, depth], anchor=BOTTOM+CENTER);
        mirror_copy([0, 1, 0])
          mirror_copy([1, 0, 0])
          translate([$LDU * 2, $LDU * 2, 0])
          cube([$stud / 2, $stud / 2, depth], anchor=BOTTOM+FRONT+LEFT);
      }
    }
  }
}

module studInsert(carve=true, supportThickness = $LDU * 4) {
  mirror_copy([0, 1, 0])
    translate([0, $tile / 2, 0])
    cyl(l=$studHeight + $LDU / 2, d=$stud + $LDU / 2, $fn=48, anchor=TOP, orient=LEFT);
  cube([supportThickness, $tile + $stud, $stud], anchor=RIGHT);
  translate([-supportThickness, 0, $stud / 2])
    cube([
      supportThickness + (carve ? 0 : Tolerance * 2),
      $tile + $stud + $LDU + (carve ? 0 : Tolerance * 2),
      $stud + $LDU * 1.5 + (carve ? 0 : Tolerance * 2)
    ], anchor=RIGHT+TOP);
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
        if (!StudInserts) {
          mirror_copy([1, 0, 0]) translate([$width / 2, 0, 0]) studInsert();
        }

        // End Slot
        translate([$tile + $LDU, -$tile, 0]) cube([6 * $LDU, $LDU, $tile], anchor=LEFT+BACK);
      }

      if (StudInserts) {
        mirror_copy([1, 0, 0]) translate([$width / 2, 0, 0]) studInsert(carve=false);
      }
      
      mirror_copy([1, 0, 0]) translate([$tile, 0, $tile / 2 - $plate * 2]) cyl(d=$fillet, h=$tile, $fn=12, anchor=TOP);
      translate([0, -$tile, $tile / 2 - $plate * 2]) cube([$tile * 2, $tile, $plate], anchor=FRONT+TOP);
      translate([0, -$tile, $tile / 2 - $plate * 2]) antiStudInsert(carve=false);

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

    if (!AntiStudInserts) {
      translate([0, -$tile, $tile / 2 - $plate * 2]) antiStudInsert();
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

module monorailCurve(startCaps=true, endCaps=true, guiderail=true, widthAddRight=0, widthAddLeft=0) {
  sa = 0;
  ea = AngleIsLength ? asin(Angle / Radius) : Angle;
  $n_teeth = round((PI * Radius * $tile) / (295 / abs(-sa - ea)));
  angle = [180 - ea, 180 + sa];
  points = arc($n_teeth, r=(Radius * $tile), angle=angle);

  translate([Radius * $tile, 0, 0]) union() {
    if (endCaps) {
      translate(points[0]) rot(180 - ea) back($tile) endCapStraight(includeRail=false);
    }
    if (startCaps) {
      translate(points[len(points) - 1]) rot(sa) back($tile) endCapStraight(includeRail=false);
    }
    difference() {
      path_sweep(guiderail ? [
        [-$teethRailWidth / 2, $tile / 2 + $plate],
        [-$teethRailWidth / 2, $tile / 2],
        [-(2 + widthAddLeft) * $tile, $tile / 2],
        [-(2 + widthAddLeft) * $tile, -$tile / 2],
        [(2 + widthAddRight) * $tile, -$tile / 2],
        [(2 + widthAddRight) * $tile, $tile / 2],
        [$teethRailWidth / 2, $tile / 2],
        [$teethRailWidth / 2, $tile / 2 + $plate],
      ] : [
        [-(2 + widthAddLeft) * $tile, $tile / 2],
        [-(2 + widthAddLeft) * $tile, -$tile / 2],
        [(2 + widthAddRight) * $tile, -$tile / 2],
        [(2 + widthAddRight) * $tile, $tile / 2],
      ], points);
      if (endCaps) {
        translate(points[0]) rot(-ea) cube([$tile * 8, $tile * 4, $tile], anchor=CENTER);
        translate(points[0]) rot(-ea) translate([0, -$teethWidth/2, 0]) cube([$tile * 6, $tile * 4, $tile], anchor=BOTTOM+FRONT);
      }
      if (startCaps) {
        translate(points[len(points) - 1]) rot(sa) cube([$tile * 8, $tile * 4, $tile], anchor=CENTER);
        translate(points[len(points) - 1]) rot(sa) translate([0, $teethWidth / 2, 0]) cube([$tile * 6, $tile * 4, $tile], anchor=BOTTOM+BACK);
      }
    }
    if (guiderail) {
      translate([0, 0, $tile / 2])
        arc_copies($n_teeth + 1, r=(Radius * $tile), sa=angle[0], ea=angle[1] - (180 * ($teethWidth / (PI * Radius * $tile))))
        tooth();
    }
  }
}

module monorailStraight() {
  union() {
    translate([0, $tile, 0]) endCapStraight();
    translate([0, (Length - 1) * $tile, 0]) rotate(180) endCapStraight();
    if (Length > 4) {
      translate([0, $tile * 2, 0]) cube([4 * $tile, (Length - 4) * $tile, $tile], anchor=FRONT);
      translate([0, $tile * 2, $tile / 2]) cube([$teethRailWidth, (Length - 4) * $tile, $plate], anchor=BOTTOM+FRONT);
      translate([0, $tile * 2, $tile / 2]) group() {
        for (i = [0:($teeth * (Length - 4) - 1)]) {
          translate([0, i * $teethWidth, 0]) tooth();
        }
      };
    }
  }
}

module guiderailChainLink() {
  difference() {
    tooth();
    translate([0, $teethWidth / 2, 0]) cyl(d=$LDU * 4, h=$plate, anchor=BOTTOM, $fn=32);
  }
  translate([0, $teethWidth / 2 * 3, 0]) cyl(d=$LDU * 3, h=$plate, anchor=BOTTOM, $fn=32);
  translate([0, $teethWidth / 2, 0]) cube([$teethRailWidth, $teethWidth, $plate], anchor=BOTTOM+FRONT);
}

module switchLeverSlot(travelDistance) {
  leverHeight = $plate;
  slotAngle = asin(leverHeight / (travelDistance * $tile));
  translate([0, $tile / 2, $tile / 2 + $plate])
    cube([$teethRailWidth / 2, travelDistance * $tile, $plate], anchor=TOP+FRONT);
}

module monorailSwitch() {
  travelDistance = 2 + ($teethRailWidth / $tile);
  strength = 4 * $LDU;
  tolerance = $LDU;

  midLength = ceil(cos(asin(1 - 3 / Radius)) * Radius);

  difference() {
    union() {
      translate([0, $tile, 0]) endCapStraight();
      translate([0, $tile * (Length - 1), 0]) rotate([0, 0, 180]) endCapStraight();
      translate([0, $tile * SwitchFrontLength, 0]) cube([$tile * 3, $tile * midLength, $tile], anchor=FRONT+RIGHT);
      translate([0, $tile * SwitchFrontLength, 0]) cube([$tile * 4, $tile * midLength, $tile], anchor=FRONT+CENTER);
      difference() {
        translate([0, $tile * SwitchFrontLength, 0]) monorailCurve(startCaps=false, widthAddRight=1);
        translate([0, $tile * Length, 0]) cube([$tile * 4 + $plate * 2, $tile * 2, $tile], anchor=BACK);
      }

      // straight teeth
      translate([-$tile * travelDistance, $tile * SwitchFrontLength, $tile / 2]) group() {
        cube([$teethRailWidth, $tile * midLength, $plate], anchor=BOTTOM+FRONT);
        for (i = [0:($teeth * midLength - 1)]) {
          translate([0, i * $teethWidth, 0]) tooth();
        }
      }

      translate([0, $tile * (midLength + SwitchFrontLength), $tile / 2]) group() {
        segmentLength = Length - midLength - SwitchFrontLength - 2;
        cube([$teethRailWidth, $tile * segmentLength, $plate], anchor=BOTTOM+FRONT);
        cube([$tile * 4, $tile * segmentLength, $tile], anchor=TOP+FRONT);
        for (i = [0:($teeth * segmentLength - 1)]) {
          translate([0, i * $teethWidth, 0]) tooth();
        }
      }
    }
    translate([0, $tile * SwitchFrontLength, $tile / 2]) cube([$tile * 20, $teethTolerance, $plate], anchor=BOTTOM);
    translate([0, $tile * (SwitchFrontLength + midLength), $tile / 2]) cube([$tile * 20, $teethTolerance, $plate], anchor=BOTTOM);
    difference() {
      translate([0, $tile * SwitchFrontLength, $tile / 2]) cube([$tile * 20, midLength * $tile, Tolerance], anchor=BOTTOM+FRONT);

      for (i = [0:SwitchSupportCount - 1]) {
        y = SwitchFrontLength + 1 + ((midLength - 2) / (SwitchSupportCount - 1) * i);
        wl = 2 * $tile + travelDistance + $teethRailWidth;
        wr = (1 - cos(asin((y - SwitchFrontLength) / Radius))) * Radius * $tile + travelDistance + 2 * $tile + $teethRailWidth;
        translate([-wl, $tile * y, 0]) cube([wl + wr, strength, $tile * 2], anchor=LEFT);
      }
    }
    
    // Mechanism
    curveAngleMax = asin((midLength + 0.5 + travelDistance) / Radius);
    curveAngleMin = asin(midLength / Radius);
    curveAngle = curveAngleMin + (curveAngleMax - curveAngleMin) / 2;
    curveX = (1 - cos(curveAngleMin)) * Radius * $tile;
    translate([0, $tile * (SwitchFrontLength + midLength), 0]) switchLeverSlot(travelDistance);
    translate([curveX - $LDU, $tile * (SwitchFrontLength + midLength), 0]) rotate([0, 0, -curveAngle]) switchLeverSlot(travelDistance);

    for (i = [0:SwitchSupportCount - 1]) {
      y = SwitchFrontLength + 1 + ((midLength - 2) / (SwitchSupportCount - 1) * i);
      wl = 2 * $tile + travelDistance + $teethRailWidth;
      wr = (1 - cos(asin((y - SwitchFrontLength) / Radius))) * Radius * $tile + travelDistance + 2 * $tile + $teethRailWidth;
      translate([-wl, $tile * y, 0]) group() {
        cube([wl + wr, strength + Tolerance * 2, $tile], anchor=LEFT);
        rotate([45, 0, 0]) cube([wl + wr, strength * 2 + Tolerance * 2, strength * 2 + Tolerance * 2], anchor=LEFT);
      };
    }

    //translate([0, $tile * (SwitchFrontLength + midLength / 2), -$tile / 2])
    //  cyl(d=$tile * (4 + travelDistance / 2) + $LDU * 2, h=$tile / 2, chamfer=$LDU * 4, $fn=64, anchor=BOTTOM);
  }

  if (SwitchFrontLength > 2) {
    translate([0, $tile * 2, 0]) cube([$tile * 4, $tile * 2, $tile], anchor=FRONT);
    translate([0, $tile * 2, $tile / 2])
      cube([$teethRailWidth, (SwitchFrontLength - 2) * $tile - $teethWidth / 2, $plate], anchor=BOTTOM+FRONT);
    translate([0, $tile * 2, $tile / 2]) group() {
      for (i = [0:($teeth * (SwitchFrontLength - 2) - 1)]) {
        translate([0, i * $teethWidth, 0]) tooth();
      }
    };
  }

  union() {
    for (i = [0:SwitchSupportCount - 1]) {
      y = SwitchFrontLength + 1 + ((midLength - 2) / (SwitchSupportCount - 1) * i);
      wl = 2 * $tile + travelDistance + $teethRailWidth;
      wr = (1 - cos(asin((y - SwitchFrontLength) / Radius))) * Radius * $tile + travelDistance;
      translate([-wl + $LDU, $tile * y, 0]) group() {
        cube([wl + wr, strength, $tile], anchor=LEFT);
        rotate([45, 0, 0]) cube([wl + wr, strength * 2, strength * 2], anchor=LEFT);
      };
    }
  }
}

union() {
if (Type == "rail") {
  if (Angle == 0)
    monorailStraight();
  else
    monorailCurve();
} else if (Type == "studs") {
  rotate([0, -90, 0]) studInsert();
} else if (Type == "antistuds") {
  rotate([180, 0, 180]) antiStudInsert();
} else if (Type == "switch") {
  //guiderailChainLink();
  intersection() {
    monorailSwitch();
    translate([0, 55, 0]) cube([100, 60, 100], FRONT);
  }
}
}


// endCapStraight();
// translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("straight.stl");
//translate([28.75, -232, -5.75]) rotate([0, 0, 90]) import("4dbrix_curve.stl");
