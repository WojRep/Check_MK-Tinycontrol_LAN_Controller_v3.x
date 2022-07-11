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

import sqlite3


SNMP_DETECT = ".1.3.6.1.4.1.7616"
SNMP_BASE = ".1.3.6.1.4.1.7616"
OIDs = [
#	["oid","param_name","param description", do_Matric, factory unit, factory_divider],
	["2.1", "inpd1", "Digital Input 1", 'no', '',1],
	["2.2", "inpd2", "Digital Input 2", 'no', '',1],
	["2.3", "inpd3", "Digital Input 3", 'no', '',1],
	["2.4", "inpd4", "Digital Input 4", 'no', '',1],
	["3.1", "inpa1", "Analog Input 1", 'no', 'v',100],
	["3.2", "inpa2", "Analog Input 2", 'no', 'v',100],
	["3.3", "inpa3", "Analog Input 3", 'no', 'v',100],
	["3.4", "inpa4", "Analog Input 4", 'no', 'v',100],
	["3.5", "inpa5", "Analog Input 5", 'no', 'v',100],
	["3.6", "inpa6", "Analog Input 6", 'no', 'v',100],
	["3.7", "vcc", "Voltage", 'yes', 'v',100],
	["3.8", "temp", "Temperature", 'yes', 'c',100],
	["4.1", "ds1", "DS 1", 'no', 'c',10],
	["4.2", "ds2", "DS 2", 'no', 'c',10],
	["4.3", "ds3", "DS 3", 'no', 'c',10],
	["4.4", "ds4", "DS 4", 'no', 'c',10],
	["4.5", "ds5", "DS 5", 'no', 'c',10],
	["4.6", "ds6", "DS 6", 'no', 'c',10],
	["4.7", "ds7", "DS 7", 'no', 'c',10],
	["4.8", "ds8", "DS 8", 'no', 'c',10],
	["4.9", "t1", "T1", 'no', 'c',10],
	["4.10","h1", "H1", 'no', '%',10],
	["4.11","diff1", "Diff 1", 'no', '',1],
	["4.12","diff2", "Diff 2", 'no', '',1],
	["4.13","diff3", "Diff 3", 'no', '',1],
	["4.14","p1", "P1", 'no', 'pa',1],
	["4.15","co2", "CO2", 'no', 'ppm',1],
	["4.16","pm1", "PM 1", 'no', 'ug/m3',1],
	["4.17","pm2", "PM 2", 'no', 'ug/m3',1],
	["4.18","pm4", "PM 4", 'no', 'ug/m3',1],
	["4.19","pm10", "PM 10", 'no', 'ug/m3',1],
	["5.1", "power1", "Power 1", 'no', 'w',1],
	["5.2", "power2", "Power 2", 'no', 'w',1],
	["5.3", "power3", "Power 3", 'no', 'w',1],
	["5.4", "power4", "Power 4", 'no', 'w',1],
	["5.5", "energy1", "Energy 1", 'no', 'wh',1],
	["5.6", "energy2", "Energy 2", 'no', 'wh',1],
	["5.7", "energy3", "Energy 3", 'no', 'wh',1],
	["5.8", "energy4", "Energy 4", 'no', 'wh',1],
	["6.1", "m1", "Modbus 1", 'no', '',1],
	["6.2", "m2", "Modbus 2", 'no', '',1],
	["6.3", "m3", "Modbus 3", 'no', '',1],
	["6.4", "m4", "Modbus 4", 'no', '',1],
	["6.5", "m5", "Modbus 5", 'no', '',1],
	["6.6", "m6", "Modbus 6", 'no', '',1],
	["6.7", "m7", "Modbus 7", 'no', '',1],
	["6.8", "m8", "Modbus 8", 'no', '',1],
	["6.9", "m9", "Modbus 9", 'no', '',1],
        ["6.10", "m10", "Modbus 10", 'no', '',1],
        ["6.11", "m11", "Modbus 11", 'no', '',1],
        ["6.12", "m12", "Modbus 12", 'no', '',1],
        ["6.13", "m13", "Modbus 13", 'no', '',1],
        ["6.14", "m14", "Modbus 14", 'no', '',1],
        ["6.15", "m15", "Modbus 15", 'no', '',1],
        ["6.16", "m16", "Modbus 16", 'no', '',1],
        ["6.17", "m17", "Modbus 17", 'no', '',1],
        ["6.18", "m18", "Modbus 18", 'no', '',1],
        ["6.19", "m19", "Modbus 19", 'no', '',1],
        ["6.20", "m20", "Modbus 20", 'no', '',1],
        ["6.21", "m21", "Modbus 21", 'no', '',1],
        ["6.22", "m22", "Modbus 22", 'no', '',1],
        ["6.23", "m23", "Modbus 23", 'no', '',1],
        ["6.24", "m24", "Modbus 24", 'no', '',1],
        ["6.25", "m25", "Modbus 25", 'no', '',1],
        ["6.26", "m26", "Modbus 26", 'no', '',1],
        ["6.27", "m27", "Modbus 27", 'no', '',1],
        ["6.28", "m28", "Modbus 28", 'no', '',1],
        ["6.29", "m29", "Modbus 29", 'no', '',1],
        ["6.30", "m30", "Modbus 30", 'no', '',1],

]

OIDs_DICT = { OIDs[n][1]: { 'oid': OIDs[n][0], 'name': OIDs[n][2], 'do_metric': OIDs[n][3], 'unit': OIDs[n][4], 'factory_divider': OIDs[n][5]} for n in range(len(OIDs)) }

UNIT = {
    "c": u"°C",
    "f": u"°F",
    "k": u"K",
    'v': u"V",
    'a': u"A",
    'w': u"W",
    'wh': u"Wh",
    'hz': u"Hz",
    'pa': u"Pa",
    '%': u"%",
    'ug/m3': u"µg/㎥",
}



def _render_template(value: float):
    template = "%%%s" % ("d" if isinstance(value, int) else ".1f")
    return template % value    


def _render_func(value: float, unit: str) -> str:
    return _render_template(value) + UNIT.get(unit) if UNIT.get(unit) else ''


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


def parse_tinycontrol_lk3x(string_table):
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


def discover_tinycontrol_lk3x(section) -> DiscoveryResult:
    for new_item in section.keys():
        yield Service(item=new_item)


def check_tinycontrol_lk3x(item, params, section) -> CheckResult:

    if not section:
        yield Result(state=State.UNKNOWN, summary="No data")
        return

    if item in section:
        parameters = OIDs_DICT[item]
        # Default parameters form sensor definition
        sensor_default_params = ( parameters['name'], (parameters['unit'], 1, 1), parameters['do_metric'], (None, None), (None, None))
        # get parameters form Check_MK rules
        sensor_params = params.get(item) if params.get(item) else sensor_default_params
#        pprint(sensor_params)

        parameter_name, parameter_unit, do_metric, lower_levels, upper_levels = sensor_params
#        pprint(parameter_unit)
#        pprint(parameters['unit'])
        unit = parameter_unit[0]  if parameter_unit[0] is not None  else parameters['unit']
#        pprint(unit)
        multiplier = parameter_unit[1]  if parameter_unit[1] != 0 and parameter_unit[1] is not None else 1
        divider = parameter_unit[2]  if parameter_unit[2] != 0 and parameter_unit[2] is not None else 1
        factory_divider = parameters['factory_divider'] if parameters.get('factory_divider') != 0 and parameters.get('factory_divider') is not None  else 1
        parameter_data = section[item]
#        pprint(f"{item}: {parameter_data}")
        parameter_data = (parameter_data/factory_divider * multiplier) / divider
#        pprint(f"{item}: {parameter_data} {unit}")
        if do_metric == 'yes':
            yield from check_levels(
			    value=(parameter_data), 
			    metric_name = item,
			    label = parameter_name,
			    levels_upper = upper_levels, 
			    levels_lower = lower_levels, 
			    render_func = lambda parameter_data: _render_func(parameter_data, unit),
			)
        else:
            unit = UNIT.get(unit) if UNIT.get(unit) else unit
            summary = f'{parameter_name}: {parameter_data}{unit}'
            yield Result(state=State.OK, summary=summary)
    else:
        yield Result(state=State.UNKNOWN, summary="Sensor was not found")
    return



register.snmp_section(
    name="tinycontrol_lk3x",
    fetch=SNMPTree(base=SNMP_BASE, oids=snmp_oids()),
    detect = startswith(".1.3.6.1.2.1.1.2.0", SNMP_DETECT),
    parse_function = parse_tinycontrol_lk3x,
)

register.check_plugin(
    name="tinycontrol_lk3x",
    sections=["tinycontrol_lk3x"],
    service_name = "TinyControl %s",
    check_default_parameters={},
    discovery_function = discover_tinycontrol_lk3x,
    check_function = check_tinycontrol_lk3x,
    check_ruleset_name="tinycontrol_lk3x",
)
