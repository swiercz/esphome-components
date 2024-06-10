import logging
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_KEY,
    UNIT_DECIBEL_MILLIWATT,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    STATE_CLASS_MEASUREMENT,
    UNIT_CUBIC_METER,
    DEVICE_CLASS_WATER,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_KILOWATT_HOURS,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    STATE_CLASS_TOTAL,
    UNIT_KILOWATT,
    UNIT_EMPTY,
    DEVICE_CLASS_EMPTY,
    UNIT_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_GAS,
    UNIT_VOLT,
    DEVICE_CLASS_VOLTAGE,
    ENTITY_CATEGORY_DIAGNOSTIC,
    UNIT_SECOND,
    DEVICE_CLASS_TIMESTAMP,
)

_LOGGER = logging.getLogger(__name__)

AUTO_LOAD = ["wmbus"]

CONF_METER_ID = "meter_id"
CONF_LISTENER_ID = "listener_id"
CONF_ADD_PREFIX = "add_prefix"
CONF_MODE = "mode"

UNIT_LITER = "l"
UNIT_LITER_PER_HOUR = "l/h"
UNIT_GIGA_JOULE = "GJ"
UNIT_DAY = "d"

from .. import (
    WMBusComponent,
    CONF_WMBUS_ID,
    wmbus_ns
)

CODEOWNERS = ["@SzczepanLeon"]

WMBusListener = wmbus_ns.class_('WMBusListener')
FrameMode = wmbus_ns.enum("FrameMode")

FRAME_MODE = {
    "T1": FrameMode.MODE_T1,
    "C1": FrameMode.MODE_C1,
    "T1C1": FrameMode.MODE_T1C1,
}
validate_mode = cv.enum(FRAME_MODE, upper=True)

def my_key(value):
    value = cv.string_strict(value)
    parts = [value[i : i + 2] for i in range(0, len(value), 2)]
    if (len(parts) != 16) and (len(parts) != 0):
        raise cv.Invalid("Key must consist of 16 hexadecimal numbers")
    parts_int = []
    if any(len(part) != 2 for part in parts):
        raise cv.Invalid("Key must be format XX")
    for part in parts:
        try:
            parts_int.append(int(part, 16))
        except ValueError:
            # pylint: disable=raise-missing-from
            raise Invalid("Key must be hex values from 00 to FF")
    return "".join(f"{part:02X}" for part in parts_int)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_LISTENER_ID): cv.declare_id(WMBusListener),
        cv.GenerateID(CONF_WMBUS_ID): cv.use_id(WMBusComponent),
        cv.Optional(CONF_METER_ID, default=0): cv.hex_int,
        cv.Optional(CONF_TYPE, default="unknown"): cv.string_strict,
        cv.Optional(CONF_KEY, default=""): my_key,
        cv.Optional(CONF_ADD_PREFIX, default=True): cv.boolean,
        cv.Optional(CONF_MODE, default="T1"): cv.templatable(validate_mode),
        cv.Optional("rssi"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
            device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
            state_class=STATE_CLASS_MEASUREMENT,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional("lqi"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_EMPTY,
            device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
            state_class=STATE_CLASS_MEASUREMENT,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional("total_water_m3"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_CUBIC_METER,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:water",
        ),
        cv.Optional("target_water_m3"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_CUBIC_METER,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:water",
        ),
        cv.Optional("last_month_total_water_m3"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_CUBIC_METER,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:water",
        ),
        cv.Optional("current_month_total_water_l"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_LITER,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:water",
        ),
        cv.Optional("total_energy_consumption_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("total_energy_consumption_tarrif_1_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("total_energy_consumption_tarrif_2_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("total_energy_consumption_tarrif_3_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("current_power_consumption_kw"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("total_energy_production_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:transmission-tower-import",
        ),
        cv.Optional("current_power_production_kw"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:transmission-tower-import",
        ),
        cv.Optional("current_hca"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_EMPTY,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:heat-wave",
        ),
        cv.Optional("previous_hca"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_EMPTY,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:heat-wave",
        ),
        cv.Optional("current_m_hca"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_EMPTY,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:heat-wave",
        ),
        cv.Optional("previous_m_hca"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_EMPTY,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:heat-wave",
        ),
        cv.Optional("temp_room_c"): sensor.sensor_schema(
            accuracy_decimals=2,
            unit_of_measurement=UNIT_CELSIUS,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:thermometer",
        ),
        cv.Optional("temp_radiator_c"): sensor.sensor_schema(
            accuracy_decimals=2,
            unit_of_measurement=UNIT_CELSIUS,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:thermometer",
        ),
        cv.Optional("temp_room_avg_c"): sensor.sensor_schema(
            accuracy_decimals=2,
            unit_of_measurement=UNIT_CELSIUS,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:thermometer",
        ),
        cv.Optional("total_heating_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:radiator",
        ),
        cv.Optional("total_heating_gj"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_GIGA_JOULE,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:radiator",
        ),
        cv.Optional("current_heating_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:radiator",
        ),
        cv.Optional("previous_heating_kwh"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:radiator",
        ),
        cv.Optional("total_gas_m3"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_CUBIC_METER,
            device_class=DEVICE_CLASS_GAS,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:meter-gas",
        ),
        cv.Optional("flow_temperature_c"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_CELSIUS,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:coolant-temperature",
        ),
        cv.Optional("return_temperature_c"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_CELSIUS,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:coolant-temperature",
        ),
        cv.Optional("voltage_at_phase_1_v"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:sine-wave",
        ),
        cv.Optional("voltage_at_phase_2_v"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:sine-wave",
        ),
        cv.Optional("voltage_at_phase_3_v"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:sine-wave",
        ),
        cv.Optional("transmit_period_s"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_SECOND,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("remaining_battery_life_y"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("status"): sensor.sensor_schema(
            accuracy_decimals=0,
            icon="mdi:alarm-light-outline",
        ),
        cv.Optional("current_alarms"): sensor.sensor_schema(
            accuracy_decimals=0,
            icon="mdi:alarm-light-outline",
        ),
        cv.Optional("previous_alarms"): sensor.sensor_schema(
            accuracy_decimals=0,
            icon="mdi:alarm-light-outline",
        ),
        cv.Optional("total_energy_consumption_gj"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_GIGA_JOULE,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:heating-coil",
        ),
        cv.Optional("power_kw"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_KILOWATT,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:transmission-tower-export",
        ),
        cv.Optional("total_forward_energy_m3c"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_GIGA_JOULE,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:heating-coil",
        ),
        cv.Optional("total_return_energy_m3c"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_GIGA_JOULE,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:heating-coil",
        ),
        cv.Optional("total_volume_m3"): sensor.sensor_schema(
            accuracy_decimals=3,
            unit_of_measurement=UNIT_CUBIC_METER,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:water",
        ),
        cv.Optional("volume_flow_lh"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_LITER_PER_HOUR,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:water",
        ),
        cv.Optional("max_flow_lh"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_LITER_PER_HOUR,
            device_class=DEVICE_CLASS_WATER,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:water",
        ),
        cv.Optional("operating_time_d"): sensor.sensor_schema(
            accuracy_decimals=0,
            unit_of_measurement=UNIT_DAY,
            device_class=DEVICE_CLASS_EMPTY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:clock",
        ),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_LISTENER_ID], config[CONF_METER_ID], config[CONF_TYPE].lower(), config[CONF_KEY], config[CONF_MODE])
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == sensor.Sensor:
            if config[CONF_ADD_PREFIX]:
                conf['name'] = str(config[CONF_METER_ID]) + " " + conf['name']
            sens = await sensor.new_sensor(conf)
            cg.add(var.add_sensor(key, sens))
    wmbus = await cg.get_variable(config[CONF_WMBUS_ID])
    cg.add(wmbus.register_wmbus_listener(var))
