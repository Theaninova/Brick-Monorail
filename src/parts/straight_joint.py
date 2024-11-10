import cadquery as cq
from params import Params
import units as u


def straight_joint_cut(params: Params, plane: cq.Plane):
    return cq.Workplane(plane).box(
        u.studs(params.joint_studs),
        params.width * 2,
        params.height,
        centered=(False, True, False),
    )


def joint_studs(params: Params, plane: cq.Plane, face: cq.Face):
    normal = face.normalAt()
    workplane = (
        cq.Workplane(cq.Plane(face.Center(), normal.cross(plane.zDir), normal))
        .rarray(u.studs(1), u.studs(1), params.joint_studs, 1)
        .cylinder(u.stud_height(1), u.stud(0.5), centered=(True, True, False))
    )

    if params.hollow_studs:
        workplane = workplane.faces(cq.selectors.DirectionNthSelector(normal, 1)).hole(
            u.stud(1) - u.ldu(4)
        )

    return workplane.vals()[0]


def straight_joint(params: Params, plane: cq.Plane):
    half_width = (params.width - u.plate(2)) / 2
    workplane = (
        cq.Workplane(plane)
        .box(
            u.studs(params.joint_studs),
            params.width - u.plate(2),
            params.height,
            centered=(False, True, False),
        )
        .faces(
            cq.selectors.SumSelector(
                cq.selectors.DirectionNthSelector(plane.yDir, 1),
                cq.selectors.DirectionNthSelector(plane.yDir, 0),
            )
        )
        .each(
            lambda f: joint_studs(params, plane, f),
            useLocalCoordinates=True,
        )
    )

    if params.nail_slot:
        workplane = (
            workplane.faces(cq.selectors.DirectionNthSelector(plane.zDir, 1))
            .sketch()
            .push(
                [
                    (0, half_width),
                    (0, -half_width),
                ]
            )
            .rect(
                params.nail_slot_size[0],
                params.nail_slot_size[1] * 2,
            )
            .finalize()
            .cutBlind(-params.nail_slot_size[2])
        )

    if params.height < params.standoff_height:
        workplane = (
            workplane.faces("<Z")
            .rect(
                u.studs(params.joint_studs),
                params.width - u.plate(2),
            )
            .extrude(params.height - params.standoff_height)
        )
    else:
        workplane = (
            workplane.faces("<Z")
            .rect(
                -u.studs(params.standoff_studs[0]),
                u.studs(params.standoff_studs[1]),
                centered=(False, True),
            )
            .cutBlind(params.standoff_height - params.height)
        )

    if params.connector:
        face: cq.Face = workplane.faces(
            cq.selectors.DirectionNthSelector(plane.xDir, 0)
        ).val()
        normal = face.normalAt()
        face_plane = cq.Plane(face.Center(), normal.cross(plane.zDir), normal)
        x_pos = (
            params.width - u.plate(2) - params.connector_width
        ) / 2 - params.connector_position
        positive = (
            cq.Workplane(face_plane)
            .center(-x_pos, 0)
            .box(
                params.connector_width,
                face.BoundingBox().zlen,
                params.connector_depth * 2,
            )
        )
        negative = (
            cq.Workplane(face_plane)
            .center(x_pos, 0)
            .box(
                params.connector_width,
                face.BoundingBox().zlen,
                params.connector_depth * 2,
            )
        )
        workplane = workplane + positive - negative

    if params.height < params.standoff_height:
        h = params.standoff_height - params.height
        d = (
            params.width - u.studs(params.standoff_studs[1]) - params.standoff_padding
        ) / 2
        x = (params.width - d) / 2
        workplane = workplane - (
            cq.Workplane(plane)
            .pushPoints(
                [(-params.connector_depth, x, -h), (-params.connector_depth, -x, -h)]
            )
            .box(
                u.studs(params.joint_studs) + params.connector_depth,
                d,
                h,
                centered=(False, True, False),
            )
        )

    shell_thickness = (u.studs(1) - u.stud(1)) / 2
    stud_slot_plane = cq.Plane(
        plane.origin + cq.Vector(0, 0, params.height - shell_thickness),
        plane.xDir,
        -plane.zDir,
    )
    stud_slot = (
        cq.Workplane(stud_slot_plane)
        .center(u.studs(params.standoff_studs[0] / 2), 0)
        .box(
            u.studs(params.standoff_studs[0]) - params.standoff_padding,
            u.studs(params.standoff_studs[1]),
            params.height,
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
                params.height,
                centered=(True, True, False),
            )
        )

    return workplane
