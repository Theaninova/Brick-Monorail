from parts.rail import rail
import cadquery as cq
import units as u
import math
import dataclasses
from params import Params


def switch(params: Params):
    straight_length = u.studs(20)
    move_dist = u.studs(3)
    cut_tolerance = params.teeth_spacing / 2

    straight_params = dataclasses.replace(params, to=(u.studs(0), straight_length))
    # straight_params.teeth = False
    curve_params = dataclasses.replace(params, to=(u.studs(5), u.studs(15)))
    # curve_params.teeth = False
    cut_start = u.studs(2)
    cut_end = math.sqrt(params.radius**2 - (params.radius - move_dist) ** 2)
    cut_length = cut_end - cut_start

    straight_rail = rail(straight_params)
    curved_rail = rail(curve_params)

    # plate slot
    curved_rail = curved_rail - (
        cq.Workplane("XY")
        .pushPoints(
            [
                (
                    params.width / 2 - u.plate(1) - params.tolerance * 2,
                    straight_length - u.studs(params.joint_studs),
                    0,
                )
            ]
        )
        .box(
            u.stud_height(1) + u.plate(1),
            u.studs(params.joint_studs),
            params.height,
            centered=(False, False, False),
        )
    )

    # cut out teeth
    tolerance_cut = (
        cq.Workplane("XY")
        .pushPoints(
            [
                (0, cut_start, params.height - params.tolerance),
                (0, cut_end, params.height - params.tolerance),
            ]
        )
        .box(
            params.width * 3,
            cut_tolerance,
            params.height,
            centered=(True, True, False),
        )
    )
    curved_rail = curved_rail - tolerance_cut
    straight_rail = straight_rail - tolerance_cut

    straight_teeth_cut = (
        cq.Workplane("XY")
        .pushPoints(
            [
                (
                    0,
                    cut_start,
                    params.height - params.tolerance,
                )
            ]
        )
        .box(
            params.width * 3,
            cut_length,
            params.height,
            centered=(True, False, False),
        )
    )
    straight_teeth = straight_rail.intersect(straight_teeth_cut)
    straight_rail = straight_rail - straight_teeth_cut

    curved_teeth_cut = (
        cq.Workplane("XY")
        .pushPoints(
            [
                (
                    0,
                    0,
                    params.height - params.tolerance,
                )
            ]
        )
        .box(
            params.width * 3,
            cut_length + cut_start,
            params.height,
            centered=(True, False, False),
        )
    )
    curved_teeth = curved_rail.intersect(curved_teeth_cut)
    curved_rail = curved_rail - curved_teeth_cut

    rails = straight_rail + curved_rail

    return rails
