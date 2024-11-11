from params import Params
import units as u

presets = [
    (
        "classic/C7",
        Params(
            shell=True,
            hollow_studs=True,
            standoff_flush_cut=False,
            standoff_uses_pins=False,
            radius=u.studs(25),
            to=(u.studs(1), u.studs(7)),
        ),
    ),
    (
        "classic/C15",
        Params(
            shell=True,
            hollow_studs=True,
            standoff_flush_cut=False,
            standoff_uses_pins=False,
            radius=u.studs(25),
            to=(u.studs(5), u.studs(15)),
        ),
    ),
    # (
    #    "classic/S4",
    #    Params(
    #        shell=True,
    #        hollow_studs=True,
    #        standoff_flush_cut=False,
    #        standoff_uses_pins=False,
    #        radius=u.studs(25),
    #        to=(u.studs(0), u.studs(4)),
    #    ),
    # ),
    (
        "classic/S5",
        Params(
            shell=True,
            hollow_studs=True,
            standoff_flush_cut=False,
            standoff_uses_pins=False,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(5)),
        ),
    ),
    (
        "classic/S10",
        Params(
            shell=True,
            hollow_studs=True,
            standoff_flush_cut=False,
            standoff_uses_pins=False,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(10)),
        ),
    ),
    (
        "standoff",
        Params(
            shell=True,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(5)),
        ),
    ),
    (
        "solid/C7",
        Params(
            shell=False,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(1), u.studs(7)),
        ),
    ),
    (
        "solid/C15",
        Params(
            shell=False,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(5), u.studs(15)),
        ),
    ),
    (
        "solid/S4",
        Params(
            shell=False,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(4)),
        ),
    ),
    (
        "solid/S5",
        Params(
            shell=False,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(5)),
        ),
    ),
    (
        "solid/S10",
        Params(
            shell=False,
            hollow_studs=False,
            standoff_flush_cut=True,
            standoff_uses_pins=True,
            radius=u.studs(25),
            to=(u.studs(0), u.studs(10)),
        ),
    ),
]
