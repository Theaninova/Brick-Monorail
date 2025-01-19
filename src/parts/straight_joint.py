import cadquery as cq
from params import Params
import dataclasses
import units as u
import math


def straight_joint_cut(params: Params, plane: cq.Plane):
    workplane = cq.Workplane(plane).box(
        u.studs(params.joint_studs),
        params.width * 2,
        params.height - params.tolerance * 2,
        centered=(False, True, False),
    )

    return workplane


def straight_joint_sharpening_cut(params: Params, plane: cq.Plane):
    x = u.studs(params.joint_studs)
    y = params.width / 2 - u.plate(1) - params.tolerance * 2
    return (
        cq.Workplane(plane)
        .pushPoints([(x, y), (x, -y)])
        .cylinder(
            params.height - params.tolerance * 2,
            params.corner_sharpening_amount[1] / 2,
            centered=(True, True, False),
        )
    )


def joint_studs(params: Params, plane: cq.Plane, face: cq.Face):
    normal = face.normalAt()
    workplane = (
        cq.Workplane(
            cq.Plane(
                face.Center() - plane.xDir * (params.tolerance / 2),
                normal.cross(plane.zDir),
                -normal if params.standoff_uses_anti_studs else normal,
            )
        )
        .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
        .cylinder(
            u.stud_height(1)
            + (params.tolerance if params.standoff_uses_anti_studs else 0),
            u.stud(0.5) + (params.tolerance if params.standoff_uses_anti_studs else 0),
            centered=(True, True, False),
        )
    )

    if params.hollow_studs:
        workplane = workplane.faces(cq.selectors.DirectionNthSelector(normal, 1)).hole(
            u.stud(1) - u.ldu(4)
        )

    return workplane.vals()[0]


def joint_pins(params: Params, plane: cq.Plane):
    extraction_padding = u.ldu(9)
    xs = [u.studs(i + 0.5) for i in range(params.joint_studs)]
    w = params.width - u.plate(2) - params.tolerance * 2
    inner_width = w - u.studs(2) + u.pin_shim_height(2)
    # usually this would be same as shim,
    # but that would make the walls too thin
    inner_radius = u.pin(0.5) + u.ldu(1)
    workplane = (
        cq.Workplane(plane)
        .pushPoints([(x, w / -2, u.studs(0.5)) for x in xs])
        .cylinder(
            w,
            u.pin(0.5) + params.tolerance,
            direct=(0, 1, 0),
            centered=(True, True, False),
        )
        .pushPoints(
            [
                (x, w / f - h, u.studs(0.5))
                for x in xs
                for f, h in [(-2, 0), (2, u.pin_shim_height(1))]
            ]
        )
        .cylinder(
            u.pin_shim_height(1),
            u.pin_shim(0.5) + params.tolerance,
            direct=(0, 1, 0),
            centered=(True, True, False),
        )
        .pushPoints(
            [
                (
                    x,
                    inner_width / -2,
                    u.studs(0.5),
                )
                for x in xs
            ]
        )
        .cylinder(
            inner_width,
            inner_radius,
            direct=(0, 1, 0),
            centered=(True, True, False),
        )
        .pushPoints([(x, 0, -(params.standoff_height - params.height)) for x in xs])
        .box(
            inner_radius * 2,
            inner_width,
            params.standoff_height - u.studs(0.5),
            centered=(True, True, False),
        )
    )
    return workplane


def straight_joint_buildplate_studs(params: Params, plane: cq.Plane):
    height = params.height - params.tolerance * 2
    stud_slot_plane = cq.Plane(
        plane.origin - cq.Vector(0, 0, params.standoff_height - height),
        plane.xDir,
        plane.zDir,
    )

    w = u.ldu(4)
    h = 0.2

    return (
        cq.Workplane(stud_slot_plane)
        .pushPoints(
            [
                (u.studs(i + 0.5), u.studs(j - 0.5))
                for i in range(params.standoff_studs[0])
                for j in range(params.standoff_studs[1])
            ]
        )
        .cylinder(
            u.stud_height(2),
            u.stud(0.5) + params.tolerance,
            centered=(True, True, False),
        )
        .faces(">Z")
        .chamfer(u.ldu(2))
        .pushPoints([(u.studs(params.standoff_studs[0]) / 2, 0, -h)])
        .box(
            u.studs(params.standoff_studs[0]) + params.connector_size[0] * 8,
            u.studs(params.standoff_studs[1]),
            h,
            centered=(True, True, False),
        )
        .pushPoints([(-params.connector_size[0] * 2 - w / 2, 0.0)])
        .box(
            w,
            u.studs(params.standoff_studs[1]),
            params.standoff_height,
            centered=(True, True, False),
        )
    )


def straight_joint(params: Params, plane: cq.Plane):
    height = params.height - params.tolerance * 2
    inner_width = params.width - u.plate(2) - params.tolerance * 2
    half_inner_width = inner_width / 2
    workplane = (
        cq.Workplane(plane)
        .center(params.tolerance, 0)
        .box(
            u.studs(params.joint_studs) - params.tolerance,
            inner_width,
            height,
            centered=(False, True, False),
        )
    )

    if params.standoff_uses_pins:
        workplane = workplane - joint_pins(params, plane)
    else:
        workplane = workplane.faces(
            cq.selectors.SumSelector(
                cq.selectors.DirectionNthSelector(plane.yDir, 1),
                cq.selectors.DirectionNthSelector(plane.yDir, 0),
            )
        ).each(
            lambda f: joint_studs(params, plane, f),
            combine="cut" if params.standoff_uses_anti_studs else True,
        )

    if params.nail_slot:
        workplane = (
            workplane.faces(cq.selectors.DirectionNthSelector(plane.zDir, 1))
            .sketch()
            .push(
                [
                    (params.tolerance / -2, half_inner_width),
                    (params.tolerance / -2, -half_inner_width),
                ]
            )
            .rect(
                params.nail_slot_size[0],
                params.nail_slot_size[1] * 2,
            )
            .finalize()
            .cutBlind(-params.nail_slot_size[2])
        )

    workplane = workplane + (
        cq.Workplane(
            cq.Plane(
                plane.origin,
                plane.xDir,
                -plane.zDir,
            )
        )
        .center(params.tolerance, 0)
        .box(
            u.studs(params.joint_studs),
            inner_width,
            params.standoff_height - height,
            centered=(False, True, False),
        )
    )

    if params.connector:
        face: cq.Face = workplane.faces(
            cq.selectors.DirectionNthSelector(plane.xDir, 0)
        ).val()
        normal = face.normalAt()
        face_plane = cq.Plane(face.Center(), normal.cross(plane.zDir), normal)
        x_pos = (inner_width - params.connector_size[1]) / 2 - params.connector_position
        full_height = face.BoundingBox().zlen

        positive_width = params.connector_size[1] - params.tolerance
        negative_width = params.connector_size[1] + params.tolerance * 2

        positive = (
            cq.Workplane(face_plane)
            .center(-x_pos, 0)
            .box(
                positive_width,
                full_height,
                (params.connector_size[0] - params.tolerance) * 2,
            )
        )
        negative = (
            cq.Workplane(face_plane)
            .center(x_pos, 0)
            .box(
                negative_width,
                full_height,
                params.connector_size[0] * 2,
            )
        )
        workplane = workplane + positive - negative
        x_sharpen = params.corner_sharpening_amount[0] / 2
        y_sharpen = params.corner_sharpening_amount[1] / 2
        if params.corner_sharpening:
            cuts = (
                cq.Workplane(
                    cq.Plane(
                        cq.Vector(
                            face_plane.origin.x,
                            face_plane.origin.y,
                            face.BoundingBox().zmin,
                        ),
                        plane.xDir,
                        plane.zDir,
                    )
                )
                .pushPoints(
                    [
                        (
                            params.connector_size[0] + y_sharpen,
                            x_pos + negative_width / 2 - x_sharpen,
                        ),
                        (
                            params.connector_size[0] + y_sharpen,
                            x_pos - negative_width / 2 + x_sharpen,
                        ),
                        (
                            y_sharpen,
                            -x_pos + positive_width / 2 + x_sharpen,
                        ),
                        (
                            y_sharpen,
                            -x_pos - positive_width / 2 - x_sharpen,
                        ),
                    ]
                )
                .box(
                    params.corner_sharpening_amount[1],
                    params.corner_sharpening_amount[0],
                    full_height,
                    centered=(True, True, False),
                )
            )
            workplane = workplane - cuts

    h = params.standoff_height - height
    d = (params.width - params.standoff_width) / 2
    x = (params.width - d) / 2
    workplane = workplane - (
        cq.Workplane(plane)
        .pushPoints(
            [
                (-params.connector_size[1] + params.tolerance, x, -h),
                (-params.connector_size[1] + params.tolerance, -x, -h),
            ]
        )
        .box(
            u.studs(params.joint_studs) + params.connector_size[1],
            d,
            h,
            centered=(False, True, False),
        )
    )

    shell_thickness = (u.studs(1) - u.stud(1)) / 2
    stud_slot_plane = cq.Plane(
        plane.origin - cq.Vector(0, 0, params.standoff_height - height),
        plane.xDir,
        plane.zDir,
    )
    stud_slot_depth = (
        u.stud_height(2)
        if params.standoff_uses_pins
        else params.standoff_height - shell_thickness
    )

    stud_slot = (
        cq.Workplane(stud_slot_plane)
        .center(u.studs(params.standoff_studs[0] / 2), 0)
        .box(
            u.studs(params.standoff_studs[0]) - params.standoff_thickness * 2,
            u.studs(params.standoff_studs[1]),
            stud_slot_depth,
            centered=(True, True, False),
        )
        .edges("|Z")
        .chamfer(params.standoff_chamfer)
    )
    workplane = workplane - stud_slot
    for i in range(1, params.standoff_studs[0] + 1):
        x = u.studs(i / 2)
        y = (
            u.studs(params.standoff_studs[1]) / 2
            - (u.studs(1) - u.stud(1)) / 4
            - params.tolerance / 4
        )
        workplane = workplane + (
            cq.Workplane(stud_slot_plane)
            .pushPoints([(x, y), (x, -y)])
            .box(
                params.standoff_thickness,
                (u.studs(1) - u.stud(1)) / 2 + params.tolerance / 2,
                stud_slot_depth,
                centered=(True, True, False),
            )
        )

    points = [
        (u.studs(i), j - params.standoff_studs[1] / 2)
        for i in range(0, params.standoff_studs[0] + 1)
        for j in range(1, params.standoff_studs[1])
    ]
    r = (math.sqrt(2 * u.studs(1) ** 2) - u.stud(1)) / 2 + params.tolerance / 2

    workplane = workplane + (
        (
            cq.Workplane(stud_slot_plane)
            .pushPoints(points)
            .cylinder(stud_slot_depth, r, centered=(True, True, False))
            .intersect(
                cq.Workplane(stud_slot_plane)
                .center(params.tolerance, 0)
                .box(
                    u.studs(params.standoff_studs[0]) - params.tolerance,
                    params.standoff_width,
                    stud_slot_depth,
                    centered=(False, True, False),
                )
            )
        )
        - (
            cq.Workplane(stud_slot_plane)
            .pushPoints(points)
            .box(r * 2, u.ldu(4), stud_slot_depth, centered=(True, True, False))
        )
    )

    return workplane
