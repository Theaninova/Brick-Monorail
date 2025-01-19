import cadquery as cq
from params import Params
import units as u
import math
from parts.straight_joint import (
    straight_joint_cut,
    straight_joint_sharpening_cut,
    straight_joint,
)
from parts.shell_support import rail_shell_support


class ExcludeSelector(cq.Selector):
    def __init__(self, workplane: cq.Workplane):
        self.edges = dict.fromkeys(workplane.vals())

    def filter(self, objectList: [cq.Shape]):
        return [edge for edge in objectList if not edge in self.edges]


def rail_body(params: Params, path: cq.Wire):
    t0 = path.tangentAt(0)
    plane = cq.Plane(path.positionAt(0), -t0.cross(cq.Vector(0, 0, 1)), t0)
    workplane = (
        cq.Workplane(plane)
        .center(0, params.height / 2)
        .rect(params.width - params.tolerance * 2, params.height - params.tolerance * 2)
        .sweep(path)
    )
    if params.style == "transrapid":
        workplane = workplane.edges("<Z").chamfer(params.height / 2).fillet(u.ldu(2))

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
        try:
            workplane = workplane.faces("<Z").shell(-shell_thickness)
        except:
            pass

    standoff_cut_depth = (
        u.studs(params.joint_studs - params.standoff_studs[0]) + shell_thickness
    )
    standoff_offset = params.standoff_height - (params.height - params.tolerance * 2)
    standoff_cut_height = (
        (standoff_offset + (params.height - params.tolerance * 2) - shell_thickness)
        if params.shell
        else standoff_offset
    )
    standoff_cut_width = params.standoff_width - params.standoff_shell_thickness * 2
    if params.start_joint:
        workplane = workplane + straight_joint(params, start_joint_plane)
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

    if params.end_joint:
        workplane = workplane + straight_joint(params, end_joint_plane)
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

    if params.chamfer_bottom is not None:
        workplane = (
            workplane.faces("<Z[-2]")
            .edges(
                ExcludeSelector(
                    workplane.faces("#Z").faces("<Z").edges("#Z").edges(">Z")
                )
            )
            .chamfer(params.chamfer_bottom)
        )

    if params.start_joint and params.corner_sharpening:
        workplane = workplane - straight_joint_sharpening_cut(params, start_joint_plane)
    if params.end_joint and params.corner_sharpening:
        workplane = workplane - straight_joint_sharpening_cut(params, end_joint_plane)

    if params.shell and params.shell_support:
        workplane = workplane + rail_shell_support(params, path)

    if params.style == "transrapid":
        x = params.width / 2 - u.plate(1) - params.nail_slot_size[1]
        support_path = (
            cq.Workplane(plane)
            .pushPoints(
                [
                    (x, params.height - params.nail_slot_size[2] / 2),
                    (-x, params.height - params.nail_slot_size[2] / 2),
                ]
            )
            .rect(params.nail_slot_size[1], params.nail_slot_size[2])
            .sweep(path)
        )

        support_count = math.floor(path.Length() / u.ldu(3))
        support_count -= 1 - support_count % 4  # only odd number of supports

        for i in range(0, support_count + 1):
            if (i // 2) % 2 == 0:
                continue
            d = i / support_count
            local_plane = cq.Plane(
                path.positionAt(d)
                + cq.Vector(0, 0, params.height - params.nail_slot_size[2]),
                path.tangentAt(d),
            )
            support_path = support_path - (
                cq.Workplane(local_plane).box(
                    params.nail_slot_size[2] / 2,
                    params.width,
                    params.nail_slot_size[2],
                )
            )

        workplane = workplane - support_path

    if params.support_clamp:
        support_clamp = (
            (
                cq.Workplane(plane)
                .center(0, params.tolerance)
                .rect(
                    params.width
                    + params.support_padding * 2
                    + params.support_clamp_thickness[0] * 2,
                    params.support_clamp_height,
                    centered=(True, False),
                )
                .sweep(path)
            )
            - (
                cq.Workplane(plane)
                .center(0, params.tolerance)
                .rect(
                    params.width + params.support_clamp_margin * 2,
                    params.support_clamp_height,
                    centered=(True, False),
                )
                .sweep(path)
            )
        ) + (
            (
                cq.Workplane(plane)
                .center(0, params.height - params.standoff_height - params.tolerance)
                .rect(
                    params.width
                    + params.support_padding * 2
                    + params.support_clamp_thickness[0] * 2,
                    params.standoff_height - params.height + params.tolerance * 2,
                    centered=(True, False),
                )
                .sweep(path)
            )
            - (
                cq.Workplane(plane)
                .center(0, params.height - params.standoff_height - params.tolerance)
                .rect(
                    params.width + params.support_padding * 2 + params.tolerance * 2,
                    params.standoff_height - params.height + params.tolerance * 2,
                    centered=(True, False),
                )
                .sweep(path)
            )
        )

        if params.start_joint:
            support_clamp = support_clamp + straight_joint_clamp(
                params, start_joint_plane
            )
        if params.end_joint:
            support_clamp = support_clamp + straight_joint_clamp(
                params, end_joint_plane
            )

        workplane = workplane + support_clamp

    return workplane


def straight_joint_clamp(params: Params, plane: cq.Plane) -> cq.Workplane:
    support_offset = params.standoff_height - params.height + params.tolerance * 2
    local_plane = cq.Plane(
        plane.origin - plane.zDir * support_offset, -plane.xDir, plane.zDir
    )
    return (
        cq.Workplane(local_plane).box(
            params.support_padding * 2
            - params.tolerance
            + params.support_clamp_thickness[1],
            params.width
            + params.support_padding * 2
            + params.support_clamp_thickness[0] * 2,
            support_offset + params.support_clamp_height,
            centered=(False, True, False),
        )
        - cq.Workplane(local_plane).box(
            params.connector_size[0] - params.tolerance + params.support_clamp_margin,
            params.width + params.support_clamp_margin * 2,
            support_offset + params.support_clamp_height,
            centered=(False, True, False),
        )
        - cq.Workplane(local_plane).box(
            params.support_padding * 2 - params.support_clamp_margin,
            params.width
            - params.tolerance * 2
            + params.support_padding * 2
            + params.support_clamp_margin * 2,
            support_offset,
            centered=(False, True, False),
        )
    )
