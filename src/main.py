from presets import presets
from parts.rail import rail, rail_support, rail_split
import units as u
import cadquery as cq

target = "classic_pop/S10"

params = [params for name, params in presets if name == target][0]

if params.rack_print_on_print:
    body, rack = rail_split(params)
    body = body.translate((0, 0, -u.brick(1)))
    show_object(body)
    # show_object(rack)
elif params.support_clamp:
    show_object(rail(params))
    show_object(rail_support(params))
else:
    show_object(rail(params))
