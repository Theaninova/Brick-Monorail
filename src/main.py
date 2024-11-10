from presets import presets
from parts.rail import rail

name = "classic/C7"

params = [params for name, params in presets if name == name][0]

show_object(rail(params))
