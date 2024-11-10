import cadquery as cq
from params import Params
import units as u
from parts.straight_joint import straight_joint_cut, straight_joint
from parts.shell_support import rail_shell_support


def rail_body(params: Params, path: cq.Wire):
    half_height = params.height / 2
    t0 = path.tangentAt(0)
    plane = cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0)
    workplane = (
        cq.Workplane(plane)
        .center(0, half_height)
        .rect(params.width, params.height)
        .sweep(path)
    )

    if params.start_joint:
        workplane = workplane - straight_joint_cut(
            params, cq.Plane(path.positionAt(0), path.tangentAt(0))
        )

    if params.end_joint:
        workplane = workplane - straight_joint_cut(
            params, cq.Plane(path.positionAt(1), path.tangentAt(1) * -1)
        )

    workplane = workplane.combine()

    shell_thickness = (u.studs(1) - u.stud(1)) / 2
    if params.shell:
        workplane = workplane.faces("<Z").shell(-shell_thickness)

    standoff_cut_depth = (
        u.studs(params.joint_studs - params.standoff_studs[0]) + shell_thickness
    )
    standoff_offset = params.standoff_height - params.height
    standoff_cut_height = (
        (standoff_offset + params.height - shell_thickness)
        if params.shell
        else standoff_offset
    )
    standoff_cut_width = params.width - u.studs(params.standoff_studs[1])
    if params.start_joint:
        workplane = workplane + straight_joint(
            params,
            cq.Plane(
                path.positionAt(0),
                path.tangentAt(0),
            ),
        )
    if params.start_joint and (params.height < params.standoff_height or params.shell):
        cut = cq.Workplane(
            cq.Plane(
                path.positionAt(0)
                + path.tangentAt(0) * u.studs(params.standoff_studs[0])
                + cq.Vector(0, 0, -standoff_offset),
                path.tangentAt(0),
            )
        ).box(
            standoff_cut_depth,
            standoff_cut_width,
            standoff_cut_height,
            centered=(False, True, False),
        )
        workplane = workplane - cut

    if params.end_joint:
        workplane = workplane + straight_joint(
            params, cq.Plane(path.positionAt(1), path.tangentAt(1) * -1)
        )
    if params.end_joint and (params.height < params.standoff_height or params.shell):
        cut = cq.Workplane(
            cq.Plane(
                (
                    path.positionAt(1)
                    - path.tangentAt(1) * u.studs(params.standoff_studs[0])
                )
                + cq.Vector(0, 0, -standoff_offset),
                -path.tangentAt(1),
            )
        ).box(
            standoff_cut_depth,
            standoff_cut_width,
            standoff_cut_height,
            centered=(False, True, False),
        )
        workplane = workplane - cut

    if params.shell and params.shell_support:
        workplane = workplane + rail_shell_support(params, path)

    return workplane
