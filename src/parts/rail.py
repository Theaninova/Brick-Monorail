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

    return (rail_body(params, path) + rail_teeth(params, path)).combine()
