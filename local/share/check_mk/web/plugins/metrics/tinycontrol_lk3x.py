from cmk.gui.plugins.metrics import (
    check_metrics,
)

unit_info["ug/m3"] = {
    "title": _("Micrograms per cubic meter"),
    "symbol": _("ug/m3"),
    "render": lambda v: cmk.utils.render.physical_precision(v, 3, _("ug/m3")),
    "js_render": "v => cmk.number_format.physical_precision(v, 3, 'ug/m3')",
}

check_metrics["check_mk-tinycontrol_lk3x"] = {
    "vcc": { "name": "voltage"},
    "ds1": { "name": "temp"},
    "ds2": { "name": "temp"},
    "ds3": { "name": "temp"},
    "ds4": { "name": "temp"},
    "ds5": { "name": "temp"},
    "ds6": { "name": "temp"},
    "ds7": { "name": "temp"},
    "ds8": { "name": "temp"},
    "t1": { "name": "temp"},
    "h1": { "name": "humidity"},
    "p1": { "name": "pressure", "scale": 100},
    "co2": { "name": "smoke_ppm"},
}
