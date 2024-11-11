import cadquery as cq
from params import Params
import units as u
from parts.straight_joint import (
    straight_joint_cut,
    straight_joint_sharpening_cut,
    straight_joint,
)
from parts.shell_support import rail_shell_support


def rail_body(params: Params, path: cq.Wire):
    t0 = path.tangentAt(0)
    plane = cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0)
    workplane = (
        cq.Workplane(plane)
        .center(0, params.height / 2)
        .rect(params.width - params.tolerance * 2, params.height - params.tolerance * 2)
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
        workplane = workplane - straight_joint_cut(params, start_joint_plane)

    if params.end_joint:
        workplane = workplane - straight_joint_cut(params, end_joint_plane)

    workplane = workplane.combine()

    shell_thickness = (u.studs(1) - u.stud(1)) / 2
    if params.shell:
        workplane = workplane.faces("<Z").shell(-shell_thickness)

    standoff_cut_depth = (
        u.studs(params.joint_studs - params.standoff_studs[0]) + shell_thickness
    )
    standoff_offset = params.standoff_height - (params.height - params.tolerance * 2)
    standoff_cut_height = (
        (standoff_offset + (params.height - params.tolerance * 2) - shell_thickness)
        if params.shell
        else standoff_offset
    )
    standoff_cut_width = params.width - u.studs(params.standoff_studs[1])
    if params.start_joint:
        workplane = workplane + straight_joint(params, start_joint_plane)
    if params.start_joint and params.shell:
        cut = cq.Workplane(
            cq.Plane(
                start_joint_plane.origin
                + start_joint_plane.xDir * u.studs(params.standoff_studs[0])
                + cq.Vector(0, 0, -standoff_offset),
                start_joint_plane.xDir,
            )
        ).box(
            standoff_cut_depth,
            standoff_cut_width,
            standoff_cut_height,
            centered=(False, True, False),
        )
        workplane = workplane - cut
    if params.start_joint and params.corner_sharpening:
        workplane = workplane - straight_joint_sharpening_cut(params, start_joint_plane)

    if params.end_joint:
        workplane = workplane + straight_joint(params, end_joint_plane)
    if params.end_joint and params.shell:
        cut = cq.Workplane(
            cq.Plane(
                end_joint_plane.origin
                + end_joint_plane.xDir * u.studs(params.standoff_studs[0])
                + cq.Vector(0, 0, -standoff_offset),
                end_joint_plane.xDir,
            )
        ).box(
            standoff_cut_depth,
            standoff_cut_width,
            standoff_cut_height,
            centered=(False, True, False),
        )
        workplane = workplane - cut
    if params.end_joint and params.corner_sharpening:
        workplane = workplane - straight_joint_sharpening_cut(params, end_joint_plane)

    if params.shell and params.shell_support:
        workplane = workplane + rail_shell_support(params, path)

    return workplane