from presets import presets
from parts.rail import rail, rail_support
from parts.straight_joint import straight_joint_standoff_insert
from parts.switch import switch
from parts.teeth import compliant_teeth
import units as u
import cadquery as cq

target = "solid_support/C7"

params = [params for name, params in presets if name == target][0]

# standoff_joint = straight_joint_standoff_insert(params, cq.Plane(cq.Vector(0, 0, 0)))
# show_object(standoff_joint)
show_object(switch(params))
# teeth = compliant_teeth(params, u.studs(10))
# cq.exporters.export(teeth, f"STEPs/compliant_teeth.step")
# show_object(teeth)


# show_object(rail_support(params))
