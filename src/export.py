import cadquery as cq
from parts.rail import rail
import presets
import os

for name, params in presets.presets:
    part = rail(params)
    c = part.val().BoundingBox().center
    part = part.translate(c * -1)
    dir = os.path.dirname(f"{name}.x")
    os.makedirs(f"STEPs/{dir}", exist_ok=True)
    os.makedirs(f"STLs/{dir}", exist_ok=True)
    os.makedirs(f"assets/{dir}", exist_ok=True)
    cq.exporters.export(part, f"STEPs/{name}.step")
    cq.exporters.export(part, f"STLs/{name}.stl")

    part = part.rotate((0, 0, 0), (1, 0, 0), -90)
    cq.exporters.export(
        part,
        f"assets/{name}.svg",
        opt={
            "width": 480,
            "height": 480,
            "marginLeft": 48,
            "marginRight": 0,
            "marginTop": 112,
            "marginBottom": 0,
            "showAxes": False,
            "showHidden": True,
            "projectionDir": (
                1,
                1,
                1,
            ),
            "strokeColor": (200, 20, 20),
            "hiddenColor": (100, 40, 40),
            "perspective": params.radius,
        },
    )
