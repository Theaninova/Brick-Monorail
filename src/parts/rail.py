import cadquery as cq
from params import Params
import units as u
from parts.body import rail_body
from parts.teeth import rail_teeth


def rail(params: Params):
    path = cq.Wire.assembleEdges(
        (
            cq.Workplane("XY").polyline([(0, 0), params.to])
            if params.to[0] == 0
            else cq.Workplane("XY").radiusArc(params.to, params.radius)
        ).ctx.pendingEdges
    )
    dumb_path = cq.Wire.assembleEdges(
        cq.Workplane("XY")
        .spline(
            [
                (u.studs(0), u.studs(0)),
                (u.studs(10), u.studs(10)),
                (u.studs(20), u.studs(0)),
            ],
            tangents=[(0, 1), (0, -1)],
        )
        .ctx.pendingEdges
    )
    dumb_path = cq.Wire.assembleEdges(
        cq.Workplane("XY")
        .polyline(
            [
                (u.studs(0), u.studs(0)),
                (u.studs(5), u.studs(0)),
                (u.studs(5), u.studs(5)),
            ],
        )
        .ctx.pendingEdges
    )

    rail = rail_body(params, path)
    if params.teeth:
        rail = rail + rail_teeth(params, path)
    return rail


def rail_support_joint(
    workplane: cq.Workplane, plane: cq.Plane, params: Params
) -> cq.Workplane:
    standoff_offset = params.standoff_height - (params.height - params.tolerance * 2)
    workplane = workplane + cq.Workplane(
        cq.Plane(
            plane.origin - (standoff_offset) / 2 * plane.zDir,
            plane.xDir,
            plane.zDir,
        )
    ).box(
        params.connector_size[0] * 2,
        params.width - u.plate(2),
        standoff_offset,
    )

    cut = cq.Workplane(plane).box(
        (u.studs(2) + params.tolerance * 3) * 2,
        u.studs(params.standoff_studs[1])
        + params.standoff_padding
        + params.tolerance * 4,
        params.height,
    ) - cq.Workplane(plane).center(
        u.studs(params.standoff_studs[0]) + params.tolerance * 2, 0
    ).box(
        (u.studs(2) + params.tolerance * 2) * 2 - u.studs(params.standoff_studs[0]),
        u.studs(params.standoff_studs[1]) - params.tolerance * 4,
        params.height,
        centered=(False, True, True),
    )

    return workplane - cut


def rail_support(params: Params):
    path = cq.Wire.assembleEdges(
        (
            cq.Workplane("XY").polyline([(0, 0), params.to])
            if params.to[0] == 0
            else cq.Workplane("XY").radiusArc(params.to, params.radius)
        ).ctx.pendingEdges
    )

    standoff_offset = params.standoff_height - (params.height - params.tolerance * 2)

    t0 = path.tangentAt(0)
    plane = cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0)
    workplane = (
        cq.Workplane(plane)
        .center(0, -(standoff_offset) / 2 + params.tolerance)
        .rect(params.width - params.tolerance * 2, standoff_offset)
        .sweep(path)
    )

    joint_tolerance_offset = cq.Vector(0, 0, params.tolerance)
    start_joint_plane = cq.Plane(
        path.positionAt(0) + joint_tolerance_offset, path.tangentAt(0)
    )
    end_joint_plane = cq.Plane(
        path.positionAt(1) + joint_tolerance_offset, path.tangentAt(1) * -1
    )

    if params.start_joint:
        workplane = rail_support_joint(workplane, start_joint_plane, params)
    if params.end_joint:
        workplane = rail_support_joint(workplane, end_joint_plane, params)
    return workplane
