from dataclasses import dataclass, field
import math
import units as u


@dataclass
class Params:
    radius: float
    to: tuple
    shell: bool
    hollow_studs: bool
    # 3D printing optimization that allows
    # for the part to be printed flush to the
    # bed, at the expense of having to glue
    standoff_flush_cut: bool
    # Instead of 3d printing the studs,
    # a pin hole is left to insert a 4274
    # technic pit with a stud.
    standoff_uses_pins: bool
    style: str or None

    width: float = u.studs(4)
    height = u.studs(1)

    # Tolerance is also used in the injection moulded parts.
    # The tolerance applies to each individual side,
    # but is only subtracted once from the height.
    tolerance = 0.1

    start_joint = True
    end_joint = True
    joint_studs = 2

    nail_slot = True
    nail_slot_size = (u.studs(1), u.ldu(1), u.ldu(1))

    connector = True
    connector_position = u.ldu(4)
    connector_size = (u.ldu(2), u.ldu(7))

    # 3D printing optimization that makes
    # functional inner corners sharper
    corner_sharpening = True
    corner_sharpening_amount = u.ldu(1)

    shell_mid_thickness = u.stud(1)
    shell_mid_cut_thickness = u.ldu(4)
    shell_support = True

    standoff_height = u.brick(1) + u.ldu(1)
    standoff_padding = u.ldu(6)
    standoff_studs = (1, 2)

    teeth_height = u.ldu(8)
    teeth_width = u.ldu(3.5)  # 75% is correct but this leaves 0.6mm on the outside
    teeth_spacing = math.pi / 2
    teeth_inner_width = u.ldu(9) - 0.3  # 3d printing optimization
    teeth_outer_width = u.ldu(15.5) + 0.3  # 3d printing optimization
