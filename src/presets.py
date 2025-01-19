from params import Params
import math
import units as u
import copy

classic_base = Params()
classic_base.corner_sharpening = False

classic_pop = Params()
classic_pop.standoff_uses_anti_studs = True
classic_pop.rack_print_on_print = True

solid_base = Params()
solid_base.shell = False
solid_base.standoff_uses_pins = True

solid_support_base = Params()
solid_support_base.shell = False
solid_support_base.standoff_uses_pins = True
solid_support_base.support_clamp = True
solid_support_base.chamfer_bottom = 0.4

bases = {
    "classic": classic_base,
    "classic_pop": classic_pop,
    "solid": solid_base,
    "solid_support": solid_support_base,
}

tracks = {
    "C7": {"radius": u.studs(25), "to": (u.studs(1), u.studs(7))},
    "C15": {"radius": u.studs(25), "to": (u.studs(5), u.studs(15))},
    "S4": {"radius": u.studs(25), "to": (u.studs(0), u.studs(4))},
    "S5": {"radius": u.studs(25), "to": (u.studs(0), u.studs(5))},
    "S10": {"radius": u.studs(25), "to": (u.studs(0), u.studs(10))},
    "S15": {"radius": u.studs(25), "to": (u.studs(0), u.studs(15))},
    "S25": {"radius": u.studs(25), "to": (u.studs(0), u.studs(25))},
    "R28/S32": {"radius": u.studs(28), "to": (u.studs(0), u.studs(32))},
    "R28/S16": {"radius": u.studs(28), "to": (u.studs(0), u.studs(16))},
    "R28/S8": {"radius": u.studs(28), "to": (u.studs(0), u.studs(8))},
    "R28/C45": {
        "radius": u.studs(28),
        "to": (
            u.studs(math.sin(math.radians(45)) * 28),
            u.studs((1 - math.cos(math.radians(45))) * 28),
        ),
    },
    "R28/C90": {"radius": u.studs(28), "to": (u.studs(28), u.studs(28))},
}


presets: list[tuple[str, Params]] = []

for name, base in bases.items():
    for track, track_params in tracks.items():
        params = copy.deepcopy(base)
        for k, v in track_params.items():
            setattr(params, k, v)
        presets.append((f"{name}/{track}", params))
