import cadquery as cq
from params import Params
import math


def tooth(params: Params, plane: cq.Plane):
    return (
        cq.Workplane(plane)
        .box(params.teeth_width, params.teeth_outer_width, params.teeth_height)
        .edges("|Z")
        .chamfer(
            (params.teeth_outer_width - params.teeth_inner_width) / 2,
            params.teeth_width / 3,
        )
    )


def rail_teeth(params: Params, path: cq.Wire):
    path_wire_length = path.Length()
    teeth_count = math.floor(
        path_wire_length / params.teeth_spacing
    )
    t0 = path.tangentAt(0)
    z = params.height - params.tolerance + params.teeth_height / 2

    workplane = (
        cq.Workplane(cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0))
        .center(0, z)
        .rect(params.teeth_inner_width, params.teeth_height)
        .sweep(path)
    )

    for d in [0, 1]:
        workplane = workplane - (
            cq.Workplane(
                cq.Plane(
                    path.positionAt(d) + cq.Vector(0, 0, z),
                    path.tangentAt(d),
                ),
            ).box(params.tolerance * 2, params.teeth_outer_width, params.teeth_height)
        )

    for i in range(1, teeth_count + 1):
        d = (i - 0.5) / (teeth_count)
        workplane = workplane.add(
            tooth(
                params,
                cq.Plane(
                    path.positionAt(d) + cq.Vector(0, 0, z),
                    path.tangentAt(d),
                ),
            )
        )

    return workplane.combine()
