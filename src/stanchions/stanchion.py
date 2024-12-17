import cadquery as cq
import units as u
import math
from params import StanchionParams


def stanchion(params: StanchionParams) -> cq.Workplane:

    tip_points = [
        (
            u.studs(x - params.tip_size[0] / 2 + 0.5),
            u.studs(y - params.tip_size[1] / 2 + 0.5),
        )
        for x in range(params.tip_size[0])
        for y in range(params.tip_size[1])
    ]
    workplane = cq.Workplane("XY").box(
        u.studs(params.base_size[0]),
        u.studs(params.base_size[1]),
        params.base_size[2],
        centered=(True, True, False),
    )
    if params.base_chamfer != 0:
        workplane = workplane.edges("|Z").chamfer(params.base_chamfer)

    workplane = (
        workplane
        + (
            cq.Workplane("XY", origin=(0, 0, params.height - params.tip_size[2])).box(
                u.studs(params.tip_size[0]),
                u.studs(params.tip_size[1]),
                params.tip_size[2],
                centered=(True, True, False),
            )
        )
        + (
            cq.Workplane("XY", origin=(0, 0, params.height))
            .pushPoints(tip_points)
            .cylinder(
                u.stud_height(2), u.stud(1) / 2 + 0.05, centered=(True, True, False)
            )
            .pushPoints(tip_points)
            .cylinder(
                u.stud_height(2),
                u.stud(1) / 2 - u.ldu(2),
                centered=(True, True, False),
                combine="cut",
            )
        )
    )

    cut = cq.Workplane("XY")
    for angle in params.angles:
        x_dir = cq.Vector(math.cos(angle), math.sin(angle), 0)
        y_dir = cq.Vector(math.sin(angle), math.cos(angle), 0)
        cut = cut + (
            cq.Workplane(cq.Plane(cq.Vector(0, 0, 0), x_dir, cq.Vector(0, 0, 1)))
            .pushPoints(
                [
                    (
                        u.studs(x - (params.base_size[0] + 4) / 2 + 0.5),
                        u.studs(y - (params.base_size[1] + 4) / 2 + 0.5),
                    )
                    for x in range((params.base_size[0] + 4))
                    for y in range((params.base_size[1] + 4))
                ]
            )
            .cylinder(
                u.stud_height(1) + u.ldu(1),
                u.stud(0.5) + 0.05,
                centered=(True, True, False),
            )
        )

    pz0 = params.base_size[2]
    pz1 = params.height - params.tip_size[2]
    ph = pz1 - pz0
    px1 = params.stanchion_tip_size[0] / 2
    py1 = params.stanchion_tip_size[1] / 2
    pdx = math.cos(params.stanchion_angle[0]) * ph
    pdy = math.cos(params.stanchion_angle[1]) * ph
    px0 = px1 + pdx
    py0 = params.stanchion_tip_size[1] / 2 + pdy
    polygon = [
        (px1, pz1),
        (-px1, pz1),
        (-px0, pz0),
        (px0, pz0),
    ]

    support_base = cq.Workplane("XY").box(
        max(px0 * 2, u.studs(params.tip_size[0])),
        max(py0 * 2, u.studs(params.tip_size[1])),
        u.stud_height(2) + u.ldu(3),
        centered=(True, True, False),
    )
    if params.base_chamfer != 0:
        support_base = support_base.edges("|Z").chamfer(params.base_chamfer)

    workplane = (
        workplane
        + (
            cq.Workplane("XZ")
            .workplane(offset=params.stanchion_strength / -2)
            .sketch()
            .polygon(polygon)
            .wires()
            .offset(-params.stanchion_inner_thickness, mode="s")
            .push(
                [
                    (
                        0,
                        pz0 + (i + 1) / (params.beam_count + 1) * ph,
                    )
                    for i in range(params.beam_count)
                ]
            )
            .rect(px0 * 2, params.stanchion_inner_thickness - params.stanchion_strength)
            .reset()
            .polygon(polygon, mode="i")
            .reset()
            .clean()
            .vertices()
            .fillet(params.stanchion_fillet)
            .finalize()
            .extrude(params.stanchion_strength)
        )
        + (
            cq.Workplane("XY")
            .workplane(offset=pz0)
            .rect(px0 * 2, py0 * 2)
            .workplane(offset=ph)
            .rect(px1 * 2, py1 * 2)
            .loft(combine=True)
            .faces("<Z")
            .rect((px0 - params.stanchion_strength) * 2, py0 * 2)
            .workplane(offset=-ph)
            .rect((px1 - params.stanchion_strength) * 2, py0 * 2)
            .loft(combine="cut")
        )
        + support_base
    )

    if params.tip_support:
        dz = u.brick(1)
        workplane = workplane + (
            (
                cq.Workplane("XY")
                .workplane(offset=pz1 - dz)
                .rect(
                    *[
                        params.stanchion_tip_size[i]
                        + math.cos(params.stanchion_angle[i]) * dz * 2
                        for i in range(2)
                    ]
                )
                .workplane(offset=dz)
                .rect(*[u.studs(params.tip_size[i]) for i in range(2)])
                .loft(combine=True)
            )
            - (
                cq.Workplane("XY")
                .workplane(offset=pz0)
                .rect(
                    (px0 - params.stanchion_strength) * 2, u.studs(params.tip_size[1])
                )
                .workplane(offset=ph)
                .rect(
                    (px1 - params.stanchion_strength) * 2, u.studs(params.tip_size[1])
                )
                .loft(combine=True)
            )
            - (
                cq.Workplane("XY")
                .workplane(offset=pz0)
                .rect(u.studs(params.tip_size[0]), (py0) * 2)
                .workplane(offset=ph)
                .rect(u.studs(params.tip_size[0]), (py1) * 2)
                .loft(combine=True)
            )
        )

    rings = (
        (
            (
                cq.Workplane("XY").cylinder(
                    params.base_size[2],
                    math.sqrt(u.studs(4) ** 2 + u.studs(4) ** 2) - u.stud(0.5),
                    centered=(True, True, False),
                )
                - cq.Workplane("XY").cylinder(
                    params.base_size[2],
                    math.sqrt(u.studs(2.5) ** 2 + u.studs(1.5) ** 2) + u.stud(0.5),
                    centered=(True, True, False),
                )
            ).intersect(
                cq.Workplane("XY")
                .box(
                    u.studs(10),
                    u.studs(1.5),
                    params.base_size[2],
                    centered=(True, True, False),
                )
                .rotateAboutCenter(cq.Vector(0, 0, 1), 45)
                .mirror(cq.Vector(1, 0, 0), union=True)
            )
            + (
                cq.Workplane("XY").cylinder(
                    params.base_size[2],
                    math.sqrt(u.studs(2.5) ** 2 + u.studs(1) ** 2) - u.stud(0.5),
                    centered=(True, True, False),
                )
                - cq.Workplane("XY").cylinder(
                    params.base_size[2],
                    math.sqrt(u.studs(1.5) ** 2 + u.studs(0.5) ** 2) + u.stud(0.5),
                    centered=(True, True, False),
                )
            ).intersect(
                cq.Workplane("XY")
                .box(
                    u.studs(8),
                    u.stud(0.5),
                    params.base_size[2],
                    centered=(True, True, False),
                )
                .rotateAboutCenter(
                    cq.Vector(0, 0, 1), math.degrees(params.angles[2] / 2)
                )
                .mirror(cq.Vector(1, 1, 0), union=True)
                .mirror(cq.Vector(1, 0, 0), union=True)
            )
            + (
                cq.Workplane("XY").cylinder(
                    u.stud_height(2) + 0.1,
                    math.sqrt(u.studs(1.5) ** 2 + u.studs(0.5) ** 2) - u.stud(0.5),
                    centered=(True, True, False),
                )
                - cq.Workplane("XY").cylinder(
                    u.stud_height(2) + 0.1,
                    math.sqrt(u.studs(0.5) ** 2 + u.studs(0.5) ** 2) + u.stud(0.5),
                    centered=(True, True, False),
                )
            )
            + (
                cq.Workplane("XY").cylinder(
                    u.stud_height(2) + 0.1,
                    u.studs(1) - u.stud(1),
                    centered=(True, True, False),
                )
                - cq.Workplane("XY").cylinder(
                    u.stud_height(2) + 0.1,
                    u.studs(1) - u.stud(1) - u.ldu(4),
                    centered=(True, True, False),
                )
            )
        )
        - cut
    ).intersect(workplane)

    workplane = (
        workplane
        - cq.Workplane("XY").cylinder(
            u.stud_height(2) + 0.1,
            math.sqrt(u.studs(1.5) ** 2 + u.studs(0.5) ** 2) - u.stud(0.5),
            centered=(True, True, False),
        )
        - cq.Workplane("XY").box(
            u.studs(params.base_size[0]),
            u.studs(params.base_size[1]),
            u.stud_height(1) + 0.1,
            centered=(True, True, False),
        )
        + rings
    ).clean()

    return workplane
