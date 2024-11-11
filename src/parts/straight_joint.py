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
    y = params.width / 2 - u.plate(1)
    return (
        cq.Workplane(plane)
        .pushPoints([(x, y), (x, -y)])
        .cylinder(
            params.height - params.tolerance * 2,
            params.corner_sharpening_amount / 2,
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
                normal,
            )
        )
        .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
        .cylinder(u.stud_height(1), u.stud(0.5), centered=(True, True, False))
    )

    if params.hollow_studs:
        workplane = workplane.faces(cq.selectors.DirectionNthSelector(normal, 1)).hole(
            u.stud(1) - u.ldu(4)
        )

    return workplane.vals()[0]


def joint_pins(params: Params, plane: cq.Plane, face: cq.Face):
    normal = -face.normalAt()
    local_plane = cq.Plane(
        face.Center() - plane.xDir * (params.tolerance / 2),
        normal.cross(plane.zDir),
        normal,
    )
    extraction_padding = u.ldu(9)
    workplane = (
        cq.Workplane(local_plane)
        .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
        .cylinder(u.pin_shim_height(1) + u.ldu(1), u.pin_shim(1) / 2)
        .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
        .cylinder(u.studs(1), u.pin(1) / 2, centered=(True, True, False))
        .add(
            cq.Workplane(
                cq.Plane(
                    local_plane.origin
                    + local_plane.zDir * (u.studs(1) + extraction_padding / 2)
                    - cq.Vector(0, 0, u.brick(0.5)),
                    local_plane.xDir,
                    local_plane.zDir,
                )
            )
            .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
            .box(u.pin_clip(1), u.brick(1), u.ldu(3) + extraction_padding)
        )
        .add(
            cq.Workplane(
                cq.Plane(
                    local_plane.origin
                    + local_plane.zDir * (u.studs(1) + extraction_padding / 2),
                    local_plane.xDir,
                    local_plane.zDir,
                )
            )
            .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
            .cylinder(u.ldu(3) + extraction_padding, u.pin_clip(1) / 2)
        )
        .combine()
    )

    return workplane.vals()[0]


def straight_joint_standoff_insert(params: Params, plane: cq.Plane):
    standoff_height = params.standoff_height - params.height
    joint = straight_joint(dataclasses.replace(params, standoff_flush_cut=False), plane)
    x = u.studs(params.standoff_studs[0]) / 2
    y = (
        u.studs(params.standoff_studs[1]) - (u.studs(1) - u.stud(1))
    ) / 2 + params.standoff_padding / 2
    guides = (
        cq.Workplane(
            cq.Plane(
                plane.origin - (plane.zDir * standoff_height), plane.xDir, plane.zDir
            )
        )
        .pushPoints([(x, y), (x, -y)])
        .box(
            u.studs(params.standoff_studs[0]) - params.standoff_padding,
            params.standoff_padding / 2,
            u.stud_height(2),
            centered=(True, True, False),
        )
    ) - joint

    return (
        joint.intersect(
            cq.Workplane(
                cq.Plane(
                    plane.origin - (plane.zDir * standoff_height / 2),
                    plane.xDir,
                    plane.zDir,
                )
            ).box(
                u.studs(params.standoff_studs[0]) * 2,
                params.width,
                standoff_height,
            )
        )
        + guides
    )


def straight_joint(params: Params, plane: cq.Plane):
    height = params.height - params.tolerance * 2
    half_width = (params.width - u.plate(2)) / 2
    workplane = (
        cq.Workplane(plane)
        .center(params.tolerance, 0)
        .box(
            u.studs(params.joint_studs) - params.tolerance,
            params.width - u.plate(2),
            height,
            centered=(False, True, False),
        )
    )

    if params.standoff_uses_pins:
        workplane = workplane.faces(
            cq.selectors.SumSelector(
                cq.selectors.DirectionNthSelector(plane.yDir, 1),
                cq.selectors.DirectionNthSelector(plane.yDir, 0),
            )
        ).each(
            lambda f: joint_pins(params, plane, f),
            combine="s",
        )
    else:
        workplane = workplane.faces(
            cq.selectors.SumSelector(
                cq.selectors.DirectionNthSelector(plane.yDir, 1),
                cq.selectors.DirectionNthSelector(plane.yDir, 0),
            )
        ).each(
            lambda f: joint_studs(params, plane, f),
        )

    if params.nail_slot:
        workplane = (
            workplane.faces(cq.selectors.DirectionNthSelector(plane.zDir, 1))
            .sketch()
            .push(
                [
                    (params.tolerance / -2, half_width),
                    (params.tolerance / -2, -half_width),
                ]
            )
            .rect(
                params.nail_slot_size[0],
                params.nail_slot_size[1] * 2,
            )
            .finalize()
            .cutBlind(-params.nail_slot_size[2])
        )

    workplane = (
        workplane.faces("<Z")
        .rect(
            u.studs(params.joint_studs) - params.tolerance,
            params.width - u.plate(2),
        )
        .extrude(height - params.standoff_height)
    )

    if params.connector:
        face: cq.Face = workplane.faces(
            cq.selectors.DirectionNthSelector(plane.xDir, 0)
        ).val()
        normal = face.normalAt()
        face_plane = cq.Plane(face.Center(), normal.cross(plane.zDir), normal)
        x_pos = (
            params.width - u.plate(2) - params.connector_size[1]
        ) / 2 - params.connector_position
        full_height = face.BoundingBox().zlen

        positive = (
            cq.Workplane(face_plane)
            .center(-x_pos, 0)
            .box(
                params.connector_size[1] - params.tolerance,
                full_height,
                (params.connector_size[0] - params.tolerance) * 2,
            )
        )
        negative = (
            cq.Workplane(face_plane)
            .center(x_pos, 0)
            .box(
                params.connector_size[1],
                full_height,
                params.connector_size[0] * 2,
            )
        )
        workplane = workplane + positive - negative
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
                            params.connector_size[0],
                            x_pos + params.connector_size[1] / 2,
                        ),
                        (
                            params.connector_size[0],
                            x_pos - params.connector_size[1] / 2,
                        ),
                        (
                            0,
                            -x_pos + (params.connector_size[1]) / 2,
                        ),
                        (
                            0,
                            -x_pos - (params.connector_size[1]) / 2,
                        ),
                    ]
                )
                .cylinder(
                    full_height,
                    params.corner_sharpening_amount / 2,
                    centered=(True, True, False),
                )
            )
            workplane = workplane - cuts

    h = params.standoff_height - height
    d = (params.width - u.studs(params.standoff_studs[1]) - params.standoff_padding) / 2
    x = (params.width - d) / 2
    workplane = workplane - (
        cq.Workplane(plane)
        .pushPoints(
            [
                (-params.connector_size[1], x, -h),
                (-params.connector_size[1], -x, -h),
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
            u.studs(params.standoff_studs[0]) - params.standoff_padding,
            u.studs(params.standoff_studs[1]),
            stud_slot_depth,
            centered=(True, True, False),
        )
    )
    workplane = workplane - stud_slot
    for i in range(1, params.standoff_studs[0] + 1):
        x = u.studs(i / 2)
        y = u.studs(params.standoff_studs[1]) / 2 - (u.studs(1) - u.stud(1)) / 4
        workplane = workplane + (
            cq.Workplane(stud_slot_plane)
            .pushPoints([(x, y), (x, -y)])
            .box(
                params.standoff_padding / 2,
                (u.studs(1) - u.stud(1)) / 2,
                stud_slot_depth,
                centered=(True, True, False),
            )
        )

    points = [
        (u.studs(i), j - params.standoff_studs[1] / 2)
        for i in range(0, params.standoff_studs[0] + 1)
        for j in range(1, params.standoff_studs[1])
    ]
    r = (math.sqrt(2 * u.studs(1) ** 2) - u.stud(1)) / 2

    workplane = workplane + (
        cq.Workplane(stud_slot_plane)
        .pushPoints(points)
        .cylinder(stud_slot_depth, r, centered=(True, True, False))
        .intersect(
            cq.Workplane(stud_slot_plane)
            .center(params.tolerance, 0)
            .box(
                u.studs(params.standoff_studs[0]) - params.tolerance,
                u.studs(params.standoff_studs[1]),
                stud_slot_depth,
                centered=(False, True, False),
            )
        )
    )

    if params.standoff_flush_cut:
        workplane = workplane.intersect(
            cq.Workplane(
                cq.Plane(
                    plane.origin + (plane.zDir * height / 2),
                    plane.xDir,
                    plane.zDir,
                )
            ).box(
                u.studs(params.joint_studs) * 2,
                params.width,
                height,
            )
        )

    return workplane
