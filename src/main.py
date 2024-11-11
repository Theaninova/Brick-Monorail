from presets import presets
from parts.rail import rail
from parts.straight_joint import straight_joint_standoff_insert
import cadquery as cq

target = "solid/C7"

params = [params for name, params in presets if name == target][0]

# standoff_joint = straight_joint_standoff_insert(params, cq.Plane(cq.Vector(0, 0, 0)))
# show_object(standoff_joint)
show_object(rail(params))
