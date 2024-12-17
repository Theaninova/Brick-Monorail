from params import StanchionParams
import units as u

presets = [
    (
        "2x2x1",
        StanchionParams(
            base_size=(2, 2, u.plate(1)),
            base_chamfer=u.studs(0.2),
            height=u.brick(1),
            beam_count=0,
        ),
    ),
    (
        "2x2x2",
        StanchionParams(
            base_size=(2, 2, u.plate(1)),
            base_chamfer=u.studs(0.2),
            height=u.brick(2),
            beam_count=0,
        ),
    ),
    (
        "2x2x3",
        StanchionParams(
            base_size=(2, 2, u.plate(1)),
            base_chamfer=u.studs(0.2),
            height=u.brick(3),
            beam_count=0,
        ),
    ),
    (
        "2x2x4",
        StanchionParams(
            base_size=(2, 2, u.plate(1)),
            base_chamfer=u.studs(0.2),
            height=u.brick(4),
            beam_count=1,
        ),
    ),
    (
        "4x4x2",
        StanchionParams(
            base_size=(4, 4, u.plate(1)),
            base_chamfer=0,
            height=u.brick(2),
            beam_count=0,
        ),
    ),
    (
        "4x4x3",
        StanchionParams(
            base_size=(4, 4, u.plate(1)),
            base_chamfer=0,
            height=u.brick(3),
            beam_count=0,
        ),
    ),
    (
        "4x4x4",
        StanchionParams(
            base_size=(4, 4, u.plate(1)),
            base_chamfer=0,
            height=u.brick(4),
            beam_count=1,
        ),
    ),
    (
        "4x4x5",
        StanchionParams(
            base_size=(4, 4, u.plate(1)),
            base_chamfer=0,
            height=u.brick(5),
            beam_count=1,
        ),
    ),
    (
        "6x6x10",
        StanchionParams(
            base_size=(6, 6, u.plate(1)),
            base_chamfer=0,
            height=u.brick(10),
            beam_count=3,
        ),
    ),
]
