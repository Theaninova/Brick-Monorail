import cadquery as cq
import math
from params import Params
import units as u
from parts.body import rail_body
from parts.teeth import rail_teeth
from parts.straight_joint import straight_joint_buildplate_studs


def rail_arc(params: Params) -> cq.Wire:
    return cq.Wire.assembleEdges(
        (
            cq.Workplane("XY").polyline([(0, 0), params.to])
            if params.to[0] == 0
            else cq.Workplane("XY").radiusArc(params.to, params.radius)
        ).ctx.pendingEdges
    )


def rail_spline(params: Params) -> cq.Wire:
    return cq.Wire.assembleEdges(
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


def rail_split(params: Params) -> tuple[cq.Workplane, cq.Workplane]:
    path = rail_arc(params)
    body = rail_body(params, path)
    body = body.rotate((0, 0, 0), (0, 1, 0), 180)

    rack = rail_teeth(params, path)

    joint_tolerance_offset = cq.Vector(0, 0, params.tolerance)
    if params.start_joint:
        start_joint_plane = cq.Plane(
            path.positionAt(0) + joint_tolerance_offset, path.tangentAt(0)
        )
        rack = rack + straight_joint_buildplate_studs(params, start_joint_plane)
    if params.end_joint:
        end_joint_plane = cq.Plane(
            path.positionAt(1) + joint_tolerance_offset, path.tangentAt(1) * -1
        )
        rack = rack + straight_joint_buildplate_studs(params, end_joint_plane)

    return body, rack


def rail(params: Params):
    path = rail_arc(params)
    rail = rail_body(params, path)
    if params.teeth:
        rail = rail + rail_teeth(params, path)

    return rail


def rail_support_joint(
    workplane: cq.Workplane, plane: cq.Plane, params: Params
) -> cq.Workplane:
    standoff_offset = params.standoff_height - (params.height - params.tolerance * 2)
    connector_offset = params.connector_size[0]
    workplane = workplane + cq.Workplane(
        cq.Plane(
            plane.origin
            - ((standoff_offset) / 2 + params.support_z_offset / 2) * plane.zDir,
            plane.xDir,
            plane.zDir,
        )
    ).box(
        params.connector_size[0] * 2 + connector_offset + params.support_padding * 2,
        params.width + params.support_padding * 2 - params.tolerance * 2,
        standoff_offset - params.support_z_offset,
    )

    x_size = u.studs(2) + params.tolerance * 3
    cut = cq.Workplane(plane).center(x_size / 2 - connector_offset / 2, 0).box(
        x_size + connector_offset,
        params.standoff_width + params.tolerance * 2,
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
        .center(
            0, -(standoff_offset) / 2 + params.tolerance - params.support_z_offset / 2
        )
        .rect(
            params.width + params.support_padding * 2 - params.tolerance * 2,
            standoff_offset - params.support_z_offset,
        )
        .sweep(path)
    )

    path_length = path.Length()
    expansion_cut_count = math.floor(path_length / u.studs(2))
    for i in range(1, expansion_cut_count - 1):
        d = (i + 1) / (expansion_cut_count + 1)
        workplane = workplane - (
            cq.Workplane(
                cq.Plane(
                    path.positionAt(d)
                    + cq.Vector(
                        0,
                        0,
                        -(standoff_offset) / 2
                        - params.support_expansion_joint_thickness
                        - params.support_z_offset / 2,
                    ),
                    path.tangentAt(d),
                ),
            ).box(
                params.support_expansion_joint_width,
                params.width * 2,
                standoff_offset,
            )
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
