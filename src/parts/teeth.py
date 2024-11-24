import cadquery as cq
from params import Params
import math
import units as u


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
    teeth_count = math.floor(path_wire_length / params.teeth_spacing)
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


def compliant_teeth(params: Params, length: float):
    teeth_count = math.floor(length / params.teeth_spacing)
    actual_spacing = length / teeth_count
    z = params.height - params.tolerance
    solid_width = u.ldu(1)
    nozzle_diameter = 0.4
    layer_height = u.ldu(0.5)
    layer_count = math.floor(params.teeth_height / layer_height)

    workplane = (
        cq.Workplane("XY")
        .pushPoints(
            [
                (0, length * ((i - 0.5) / teeth_count), z + params.teeth_height / 2)
                for i in range(1, teeth_count + 1)
            ]
        )
        .box(params.teeth_outer_width, solid_width, params.teeth_height)
    )

    side_length = math.sqrt(
        (actual_spacing - solid_width * 1.8) ** 2 + params.teeth_outer_width**2
    )
    angle = math.atan2(params.teeth_outer_width, actual_spacing - solid_width * 1.8)
    direction = cq.Vector(math.sin(angle), math.cos(angle), 0)
    direction_b = cq.Vector(math.sin(angle), -math.cos(angle), 0)

    for i in range(1, teeth_count):
        for j in range(layer_count):
            workplane.add(
                cq.Workplane(
                    cq.Plane(
                        cq.Vector(
                            0, length * i / teeth_count, z + (j + 0.5) * layer_height
                        ),
                        direction if j % 2 == 0 else direction_b,
                        cq.Vector(0, 0, 1),
                    )
                ).box(side_length, nozzle_diameter, layer_height)
            )

    return workplane.combine()
