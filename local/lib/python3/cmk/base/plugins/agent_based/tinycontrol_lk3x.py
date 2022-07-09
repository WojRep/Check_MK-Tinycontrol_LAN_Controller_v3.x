#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#


from typing import Any, Callable, Dict, Final, Mapping, Tuple

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)
from .agent_based_api.v1 import (
#    any_of,
#    all_of,
#    contains,
#    exist,
#    equals,
    startswith,
    check_levels,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    OIDEnd,
    SNMPTree,
    )

from typing import Dict, List

from .utils.temperature import _render_temp_with_unit


from cmk.utils import debug
from pprint import pprint

SNMP_DETECT = ".1.3.6.1.4.1.7616"
SNMP_BASE = ".1.3.6.1.4.1.7616"
OIDs = [
#	["oid","param_name","param description", do_Matric, unit],
	["2.1", "inpd1", "Digital Input 1", False, None],
	["2.2", "inpd2", "Digital Input 2", False, None],
	["2.3", "inpd3", "Digital Input 3", False, None],
	["2.4", "inpd4", "Digital Input 4", False, None],
	["3.1", "inpa1", "Analog Input 1", False, None],
	["3.2", "inpa2", "Analog Input 2", False, None],
	["3.3", "inpa3", "Analog Input 3", False, None],
	["3.4", "inpa4", "Analog Input 4", False, None],
	["3.5", "inpa5", "Analog Input 5", False, None],
	["3.6", "inpa6", "Analog Input 6", False, None],
	["3.7", "vcc", "Voltage", True, 'v'],
	["3.8", "temp", "Temperature", True, 'c'],
	["4.1", "ds1", "DS 1", False, 'c'],
	["4.2", "ds1", "DS 2", False, 'c'],
	["4.3", "ds1", "DS 3", False, 'c'],
	["4.4", "ds1", "DS 4", False, 'c'],
	["4.5", "ds1", "DS 5", False, 'c'],
	["4.6", "ds1", "DS 6", False, 'c'],
	["4.7", "ds1", "DS 7", False, 'c'],
	["4.8", "ds1", "DS 8", False, 'c'],
	["4.9", "t1", "T1", False, None],
	["4.10","h1", "H1", False, None],
	["4.11","diff1", "Diff 1", False, None],
	["4.12","diff2", "Diff 2", False, None],
	["4.13","diff3", "Diff 3", False, None],
	["4.14","p1", "P1", False, None],
	["4.15","co2", "CO2", False, None],
	["4.16","pm1", "PM 1", False, None],
	["4.17","pm2", "PM 2", False, None],
	["4.18","pm4", "PM 4", False, None],
	["4.19","pm10", "PM 10", False, None],
	["5.1", "power1", "Power 1", False, None],
	["5.2", "power2", "Power 2", False, None],
	["5.3", "power3", "Power 3", False, None],
	["5.4", "power4", "Power 4", False, None],
	["5.5", "energy1", "Energy 1", False, None],
	["5.6", "energy2", "Energy 2", False, None],
	["5.7", "energy3", "Energy 3", False, None],
	["5.8", "energy4", "Energy 4", False, None],
	["6.1", "m1", "Modbus 1", False, None],
	["6.2", "m2", "Modbus 2", False, None],
	["6.3", "m3", "Modbus 3", False, None],
	["6.4", "m4", "Modbus 4", False, None],
	["6.5", "m5", "Modbus 5", False, None],
	["6.6", "m6", "Modbus 6", False, None],
	["6.7", "m7", "Modbus 7", False, None],
	["6.8", "m8", "Modbus 8", False, None],
	["6.9", "m9", "Modbus 9", False, None],
        ["6.10", "m10", "Modbus 10", False, None],
        ["6.11", "m11", "Modbus 11", False, None],
        ["6.12", "m12", "Modbus 12", False, None],
        ["6.13", "m13", "Modbus 13", False, None],
        ["6.14", "m14", "Modbus 14", False, None],
        ["6.15", "m15", "Modbus 15", False, None],
        ["6.16", "m16", "Modbus 16", False, None],
        ["6.17", "m17", "Modbus 17", False, None],
        ["6.18", "m18", "Modbus 18", False, None],
        ["6.19", "m19", "Modbus 19", False, None],
        ["6.20", "m20", "Modbus 20", False, None],
        ["6.21", "m21", "Modbus 21", False, None],
        ["6.22", "m22", "Modbus 22", False, None],
        ["6.23", "m23", "Modbus 23", False, None],
        ["6.24", "m24", "Modbus 24", False, None],
        ["6.25", "m25", "Modbus 25", False, None],
        ["6.26", "m26", "Modbus 26", False, None],
        ["6.27", "m27", "Modbus 27", False, None],
        ["6.28", "m28", "Modbus 28", False, None],
        ["6.29", "m29", "Modbus 29", False, None],
        ["6.30", "m30", "Modbus 30", False, None],
]

OIDs_DICT = { OIDs[n][1]: { 'oid': OIDs[n][0], 'name': OIDs[n][2], 'do_metric': OIDs[n][3],} for n in range(len(OIDs)) }

TEMP_UNIT = {
    "c": u"°C",
    "f": u"°F",
    "k": u"K",
}

RENDER = {
    '%'  : render.percent,
    'Hz' : render.frequency,
    'c'  : lambda temp: _render_temp_with_unit(temp, output_unit)
}


def snmp_oids():
    return list(OIDs[n][0] for n, _ in enumerate(OIDs, start=0))


def _isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def parse_tinycontroll_lk3x(string_table):
    new_item={}
    parameters = string_table[0]
    for n in range(len(parameters)):
        param_name = OIDs[n][1]
        param_data = parameters[n]
        if _isInt(param_data):
            param_data = int(param_data)
        elif _isFloat(data):
            param_data = float(param_data)
        if param_name == 'temp' or param_name == 'vcc':
            param_data = float(param_data/100)
        new_item.update({param_name: param_data})     
    return new_item


def discover_tinycontroll_lk3x(section) -> DiscoveryResult:
    for new_item in section.keys():
        yield Service(item=new_item)


def check_tinycontroll_lk3x(item, params, section) -> CheckResult:
#    pprint("### CHECK ###")
#    pprint(item)
#    pprint(params)
#    pprint(section)

    if not section:
        yield Result(state=State.UNKNOWN, summary="No data")
        return

    if item in section:
        parameters = OIDs_DICT[item]
        parameter_name = parameters['name']
        parameter_data = section[item]
        do_metric = parameters['do_metric']

        # get parameters levels
        for value_name, value_data in parameters.items():
            # Levels
            low_warn, low_crit = params.get('levels_lower') if params.get('levels_lower') else (None, None)
            high_warn, high_crit = params.get('levels_upper') if params.get('levels_upper') else (None, None)
            # Boundaries
            boundaries_low,boundaries_high = params.get('boundaries') if params.get('boundaries') else (None, None)
            # Multipliter
            multiplier = params.get('multiplier') if (params.get('multiplier') and params.get('multiplier') != 0) else 1
            # Unit
            unit = params.get('unit') if params.get('unit') else '' 

        if do_metric:
            yield from check_levels(
			    value=(parameter_data * multiplier), 
			    label = parameter_name,
			    levels_upper = (high_warn, high_crit), 
			    levels_lower = (low_warn, low_crit), 
			    render_func = RENDER.get(unit),
			)
        else:
            summary = f'{parameter_name}: {parameter_data}'
            yield Result(state=State.OK, summary=summary)
    else:
        yield Result(state=State.UNKNOWN, summary="Sensor was not found")
    return



register.snmp_section(
    name="tinycontroll_lk3x",
    fetch=SNMPTree(base=SNMP_BASE, oids=snmp_oids()),
    detect = startswith(".1.3.6.1.2.1.1.2.0", SNMP_DETECT),
    parse_function = parse_tinycontroll_lk3x,
)

register.check_plugin(
    name="tinycontroll_lk3x",
    sections=["tinycontroll_lk3x"],
    service_name = "TinyControll %s",
    check_default_parameters={},
    discovery_function = discover_tinycontroll_lk3x,
    check_function = check_tinycontroll_lk3x,
    check_ruleset_name="tinycontroll_lk3x",
)
