import cadquery as cq
from params import Params
import math
import units as u


def rail_shell_support(params: Params, path: cq.Wire):
    t0 = path.tangentAt(0)
    tolerance_offset = cq.Vector(0, 0, params.tolerance)
    plane = cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0)
    support = (
        cq.Workplane(plane)
        .center(0, params.height / 2)
        .rect(params.shell_mid_thickness, params.height - params.tolerance * 2)
        .sweep(path)
    )

    path_wire_length = path.Length()
    shell_thickness = (u.studs(1) - u.stud(1)) / 2

    target_width = params.width - shell_thickness * 4
    square_width = target_width / math.sqrt(2)

    support_count = math.floor(path_wire_length / target_width - 0.5)
    support_count -= 1 - support_count % 2  # only odd number of supports

    for i in range(1, support_count + 1):
        d = i / (support_count + 1)
        local_plane = cq.Plane(path.positionAt(d) + tolerance_offset, path.tangentAt(d))
        support_square = (
            cq.Workplane(local_plane)
            .box(
                square_width,
                square_width,
                params.height - params.tolerance * 2,
                centered=(True, True, False),
            )
            .rotateAboutCenter((0, 0, 1), 45)
        )
        support = support + (
            support_square.faces("|Z")
            .shell(-shell_thickness)
            .union(
                cq.Workplane(local_plane).box(
                    shell_thickness,
                    params.width - shell_thickness,
                    params.height - params.tolerance * 2,
                    centered=(True, True, False),
                )
                - support_square
            )
        )

    support = support - (
        cq.Workplane(plane)
        .center(0, params.height / 2)
        .rect(params.shell_mid_cut_thickness, params.height - params.tolerance * 2)
        .sweep(path)
    )

    for i in range(0, support_count + 1):
        d = (i + 0.5) / (support_count + 1)
        local_plane = cq.Plane(path.positionAt(d) + tolerance_offset, path.tangentAt(d))
        support = support + (
            cq.Workplane(local_plane).box(
                shell_thickness,
                params.shell_mid_thickness - params.shell_mid_cut_thickness,
                params.height - params.tolerance * 2,
                centered=(True, True, False),
            )
        )

    if params.start_joint:
        support = support - (
            cq.Workplane(
                cq.Plane(path.positionAt(0) + tolerance_offset, path.tangentAt(0))
            ).box(
                u.studs(params.standoff_studs[0]),
                params.width * 2,
                params.height - params.tolerance * 2,
                centered=(False, True, False),
            )
        )
    if params.end_joint:
        support = support - (
            cq.Workplane(
                cq.Plane(path.positionAt(1) + tolerance_offset, -path.tangentAt(1))
            ).box(
                u.studs(params.standoff_studs[0]),
                params.width * 2,
                params.height - params.tolerance * 2,
                centered=(False, True, False),
            )
        )

    return support
