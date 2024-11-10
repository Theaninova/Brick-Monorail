from dataclasses import dataclass
import math
import units as u


@dataclass
class Params:
    radius: float
    to: tuple
    shell: bool
    hollow_studs: bool

    width: float = u.studs(4)
    height = u.studs(1)

    start_joint = True
    end_joint = True
    joint_studs = 2

    nail_slot = True
    nail_slot_size = (u.studs(1), u.ldu(1), u.ldu(1))

    connector = True
    connector_position = u.ldu(4)
    connector_width = u.ldu(8)
    connector_depth = u.ldu(1)

    shell_mid_thickness = u.stud(1)
    shell_mid_cut_thickness = u.ldu(4)
    shell_support = True

    standoff_height = u.brick(1)
    standoff_padding = u.ldu(6)
    standoff_studs = (1, 2)

    teeth_height = u.ldu(8)
    teeth_width = math.pi / 2 * 0.75
    teeth_spacing = math.pi / 2 * 0.25
    teeth_inner_width = u.ldu(9)
    teeth_outer_width = u.ldu(15.5)
