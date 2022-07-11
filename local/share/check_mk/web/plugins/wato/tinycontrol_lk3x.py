#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _

from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
    TextAscii,
    Checkbox,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)

SENSORS = [
        ["inpd1", "Digital Input 1", 'no', None],
        ["inpd2", "Digital Input 2", 'no', None],
        ["inpd3", "Digital Input 3", 'no', None],
        ["inpd4", "Digital Input 4", 'no', None],
        ["inpa1", "Analog Input 1", 'no', None],
        ["inpa2", "Analog Input 2", 'no', None],
        ["inpa3", "Analog Input 3", 'no', None],
        ["inpa4", "Analog Input 4", 'no', None],
        ["inpa5", "Analog Input 5", 'no', None],
        ["inpa6", "Analog Input 6", 'no', None],
        ["vcc", "Voltage", 'yes', 'v'],
        ["temp", "Temperature", 'yes', 'c'],
        ["ds1", "DS 1", 'no', 'c'],
        ["ds1", "DS 2", 'no', 'c'],
        ["ds1", "DS 3", 'no', 'c'],
        ["ds1", "DS 4", 'no', 'c'],
        ["ds1", "DS 5", 'no', 'c'],
        ["ds1", "DS 6", 'no', 'c'],
        ["ds1", "DS 7", 'no', 'c'],
        ["ds1", "DS 8", 'no', 'c'],
        ["t1", "T1", 'no', ''],
        ["h1", "H1", 'no', ''],
        ["diff1", "Diff 1", 'no', ''],
        ["diff2", "Diff 2", 'no', ''],
        ["diff3", "Diff 3", 'no', ''],
        ["p1", "P1", 'no', ''],
        ["co2", "CO2", 'no', ''],
        ["pm1", "PM 1", 'no', ''],
        ["pm2", "PM 2", 'no', ''],
        ["pm4", "PM 4", 'no', ''],
        ["pm10", "PM 10", 'no', ''],
        ["power1", "Power 1", 'no', ''],
        ["power2", "Power 2", 'no', ''],
        ["power3", "Power 3", 'no', ''],
        ["power4", "Power 4", 'no', ''],
        ["energy1", "Energy 1", 'no', ''],
        ["energy2", "Energy 2", 'no', ''],
        ["energy3", "Energy 3", 'no', ''],
        ["energy4", "Energy 4", 'no', ''],
        ["m1", "Modbus 1", 'no', ''],
        ["m2", "Modbus 2", 'no', ''],
        ["m3", "Modbus 3", 'no', ''],
        ["m4", "Modbus 4", 'no', ''],
        ["m5", "Modbus 5", 'no', ''],
        ["m6", "Modbus 6", 'no', ''],
        ["m7", "Modbus 7", 'no', ''],
        ["m8", "Modbus 8", 'no', ''],
        ["m9", "Modbus 9", 'no', ''],
        ["m10", "Modbus 10", 'no', ''],
        ["m11", "Modbus 11", 'no', ''],
        ["m12", "Modbus 12", 'no', ''],
        ["m13", "Modbus 13", 'no', ''],
        ["m14", "Modbus 14", 'no', ''],
        ["m15", "Modbus 15", 'no', ''],
        ["m16", "Modbus 16", 'no', ''],
        ["m17", "Modbus 17", 'no', ''],
        ["m18", "Modbus 18", 'no', ''],
        ["m19", "Modbus 19", 'no', ''],
        ["m20", "Modbus 20", 'no', ''],
        ["m21", "Modbus 21", 'no', ''],
        ["m22", "Modbus 22", 'no', ''],
        ["m23", "Modbus 23", 'no', ''],
        ["m24", "Modbus 24", 'no', ''],
        ["m25", "Modbus 25", 'no', ''],
        ["m26", "Modbus 26", 'no', ''],
        ["m27", "Modbus 27", 'no', ''],
        ["m28", "Modbus 28", 'no', ''],
        ["m29", "Modbus 29", 'no', ''],
        ["m30", "Modbus 30", 'no', ''],
]

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

def _sensor_elements():
    for sensor in SENSORS:
        sensor_id = sensor[0]
        sensor_name = sensor[1]
        sensor_do_metric = sensor[2]
        sensor_unit = UNIT.get(sensor[3])
        yield (sensor_id, Tuple(title=_(sensor_name),
                elements=[
                    TextAscii(title=_('Name'), 
                        default_value=sensor_name,
                    ),
                    Optional(
                        Tuple(title=_('Unit'), elements=[
                                TextAscii(
                                    title=_('Display unit name'), 
                                    default_value=None,
                                ),
                                Float(
                                    title=_('Multiplier'),help=_('Enter any value that is not zero.'),
                                    default_value=1, unit=None,
                                ),
                                Float(
                                    title=_('Divider'),
                                    help=_('Enter any value that is not zero.'),
                                    default_value=1, unit=None,
                                ),
                        ],),
                        sameline=True,
                        label=_('Unit definition'),
                        none_label=_("No unit definition set"),
                        none_value=(None, None, None),
                    ),

                    DropdownChoice(title=_('Create graph and metrics'),
                        default_value=sensor_do_metric,
                        choices=[
                            ('yes', _("Yes")),
                            ('no', _("No")),
                    ],),
                    Optional(
                        Tuple(
                            elements=[
                                Float(title=_('Lower warning at'), unit=sensor_unit, default_value=None),
                                Float(title=_('Lower critical at'), unit=sensor_unit, default_value=None),
                            ],
                        ),
                        sameline=True,
                        label=_('Lower levels'),
                        none_label=_("No lower lelevs set"),
                        none_value=(None, None),
                    ),
                    Optional(
                        Tuple(
                            elements=[
                                Float(title=_('Upper warning at'), unit=sensor_unit,default_value=None),
                                Float(title=_('Upper critical at'), unit=sensor_unit,default_value=None),
                            ],
                        ),
                        sameline=True,
                        label=_('Upper levels'),
                        none_label=_('No upper levels set'),
                        none_value=(None, None),                    
                   ),
            ],),
       )


def _parameter_valuespec_tinycontrol_lk3x():
    return Transform(
        Dictionary(
            title = _('Tinycontrol LanController 3.x sensors'),
            elements = _sensor_elements,
        ),
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="tinycontrol_lk3x",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_tinycontrol_lk3x,
        title=lambda: _("Tinycontrol LanController 3.x sensors"),
    )
)
