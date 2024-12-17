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
    chamfer_bottom: float or None
    style: str or None

    width: float = u.studs(4)
    height = u.studs(1)

    support_padding = u.ldu(4)
    support_clamp = True
    support_clamp_thickness = u.ldu(4)
    support_clamp_height = 0.2
    support_clamp_margin = 0.2

    support_expansion_joint_width = 0.8
    support_expansion_joint_thickness = 1.0
    support_z_offset = 0.1

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
    corner_sharpening_amount = (u.ldu(0.5), u.ldu(1))

    shell_mid_thickness = u.stud(1)
    shell_mid_cut_thickness = u.ldu(4)
    shell_support = True

    standoff_height = u.brick(1) + u.ldu(1)
    standoff_padding = u.ldu(6)
    standoff_studs = (1, 2)

    teeth = True
    teeth_height = u.ldu(8)
    teeth_width = u.ldu(3.5)  # 75% is correct but this leaves 0.6mm on the outside
    teeth_spacing = math.pi / 2
    teeth_inner_width = u.ldu(9) - 0.3  # 3d printing optimization
    teeth_outer_width = u.ldu(15.5) + 0.3  # 3d printing optimization


@dataclass
class StanchionParams:
    base_size: tuple[float, float, float]
    base_chamfer: float
    height: float
    beam_count: int
    tip_size = (2, 2, u.ldu(4))
    stanchion_angle = (math.radians(86.5), math.radians(87.5))
    stanchion_fillet = u.ldu(3)
    stanchion_tip_size = (u.ldu(32), u.ldu(20))
    stanchion_inner_thickness = u.ldu(9)
    stanchion_strength = u.ldu(4)
    angles = [
        0,
        math.atan(4 / 3),
        math.atan(3 / 4),
        math.atan(24 / 7),
        math.atan(7 / 24),
    ]
    tip_support = True
