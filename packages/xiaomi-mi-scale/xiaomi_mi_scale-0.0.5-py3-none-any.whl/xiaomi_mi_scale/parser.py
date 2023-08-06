"""Parser for Xiaomi Mi advertisements.
This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py
MIT License applies.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, auto

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data.enum import StrEnum

_LOGGER = logging.getLogger(__name__)


class MiScaleSensor(StrEnum):

    WEIGHT = "weight"
    IMPEDANCE = "impedance"


class Models(Enum):

    MiScaleV1 = auto()
    MiScaleV2 = auto()


@dataclass
class ModelDescription:

    device_type: str


DEVICE_TYPES = {
    Models.MiScaleV1: ModelDescription("Mi Body Fat Scale"),
    Models.MiScaleV2: ModelDescription("Mi Body Composition Scale"),
}




ORALB_MANUFACTURER = 0x00DC


BYTES_TO_MODEL = {
    b"\x062k": Models.MiScaleV1,
    b"\x074\x0c": Models.MiScaleV2,
}



class MiScaleBluetoothDeviceData(BluetoothData):
    """Data for OralB BLE sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing OralB BLE advertisement data: %s", service_info)
        self.set_device_manufacturer("Xiaomi")
        manufacturer_data = service_info.manufacturer_data
        address = service_info.address
        
        msg_length = len(data)
        uuid16 = (data[3] << 8) | data[2]

        if msg_length == 14 and uuid16 == 0x181D:  # Mi Scale V1
            model = Models.MiScaleV1
            model_info = DEVICE_TYPES[model]
            self.set_device_type(model_info.device_type)
            name = f"{model_info.device_type} {short_address(address)}"
            self.set_device_name(name)
            self.set_title(name)

            xvalue = data[4:]
            (control_byte, weight) = unpack("<BH7x", xvalue)

            has_impedance = False
            is_stabilized = control_byte & (1 << 5)
            weight_removed = control_byte & (1 << 7)

            if control_byte & (1 << 0):
                weight = weight / 100
                weight_unit = 'lbs'
            elif control_byte & (1 << 4):
                weight = weight / 100
                weight_unit = 'jin'
            else:
                weight = weight / 200
                weight_unit = 'kg'
            self.update_sensor(str(OralBSensor.WEIGHT), None, weight, None, "Weight")

        elif msg_length == 17 and uuid16 == 0x181B:  # Mi Scale V2
            model = Models.MiScaleV2
            model_info = DEVICE_TYPES[model]
            self.set_device_type(model_info.device_type)
            name = f"{model_info.device_type} {short_address(address)}"
            self.set_device_name(name)
            self.set_title(name)

            xvalue = data[4:]
            (measunit, control_byte, impedance, weight) = unpack("<BB7xHH", xvalue)
            has_impedance = control_byte & (1 << 1)
            is_stabilized = control_byte & (1 << 5)
            weight_removed = control_byte & (1 << 7)

            if measunit & (1 << 4):
                # measurement in Chinese Catty unit
                weight = weight / 100
                weight_unit = "jin"
            elif measunit == 3:
                # measurement in lbs
                weight = weight / 100
                weight_unit = "lbs"
            elif measunit == 2:
                # measurement in kg
                weight = weight / 200
                weight_unit = "kg"
            else:
                # measurement in unknown unit
                weight = weight / 100
                weight_unit = None
            self.update_sensor(str(OralBSensor.WEIGHT), None, weight, None, "Weight")
            self.update_sensor(str(OralBSensor.IMPEDANCE), None, impedance, None, "Weight")
"""
        else:
            device_type = None

        if device_type is None:
            if self.report_unknown == "Mi Scale":
                _LOGGER.info(
                    "BLE ADV from UNKNOWN Mi Scale DEVICE: MAC: %s, ADV: %s",
                    to_mac(source_mac),
                    data.hex()
                )
            return None

        result = {
            "non-stabilized weight": weight,
            "weight unit": weight_unit,
            "weight removed": 0 if weight_removed == 0 else 1,
            "stabilized": 0 if is_stabilized == 0 else 1
        }

        if device_type == "Mi Scale V1":
            if is_stabilized and not weight_removed:
                result.update({"weight": weight})
        elif device_type == "Mi Scale V2":
            if is_stabilized and (weight_removed == 0):
                result.update({"stabilized weight": weight})
                if has_impedance:
                    result.update({"weight": weight})
                    result.update({"impedance": impedance})
        else:
            pass

        firmware = device_type
        miscale_mac = source_mac

        # Check for duplicate messages
        packet_id = xvalue.hex()
        try:
            prev_packet = self.lpacket_ids[miscale_mac]
        except KeyError:
            # start with empty first packet
            prev_packet = None
        if prev_packet == packet_id:
            # only process new messages
            if self.filter_duplicates is True:
                return None
        self.lpacket_ids[miscale_mac] = packet_id
        if prev_packet is None:
            if self.filter_duplicates is True:
                # ignore first message after a restart
                return None

        # check for MAC presence in sensor whitelist, if needed
        if self.discovery is False and miscale_mac not in self.sensor_whitelist:
            _LOGGER.debug("Discovery is disabled. MAC: %s is not whitelisted!", to_mac(miscale_mac))
            return None

        result.update({
            "type": device_type,
            "firmware": firmware,
            "mac": to_unformatted_mac(miscale_mac),
            "packet": packet_id,
            "rssi": rssi,
            "data": True,
        })
        return result
        
        if ORALB_MANUFACTURER not in manufacturer_data:
            return None

        data = manufacturer_data[ORALB_MANUFACTURER]
        self.set_device_manufacturer("Xiaomi")
        _LOGGER.debug("Parsing Xiaomi Mi Scale sensor: %s", data)
        msg_length = len(data)
        if msg_length not in (9, 11):
            return

        device_bytes = data[0:3]
        state = data[3]
        pressure = data[4]
        time = data[5] * 60 + data[6]
        mode = data[7]
        sector = data[8]
        sector_timer = None
        no_of_sectors = None
        if msg_length >= 11:
            sector_timer = data[9]
            no_of_sectors = data[10]

        model = BYTES_TO_MODEL.get(device_bytes, Models.SmartSeries7000)
        model_info = DEVICE_TYPES[model]
        modes = model_info.modes
        self.set_device_type(model_info.device_type)
        name = f"{model_info.device_type} {short_address(address)}"
        self.set_device_name(name)
        self.set_title(name)

        tb_state = STATES.get(state, f"unknown state {state}")
        tb_mode = modes.get(mode, f"unknown mode {mode}")
        tb_pressure = PRESSURE.get(pressure, f"unknown pressure {pressure}")
        tb_sector = SECTOR_MAP.get(sector, f"sector {sector}")

        self.update_sensor(str(OralBSensor.TIME), None, time, None, "Time")
        self.update_sensor(str(OralBSensor.SECTOR), None, tb_sector, None, "Sector")
        if no_of_sectors is not None:
            self.update_sensor(
                str(OralBSensor.NUMBER_OF_SECTORS),
                None,
                no_of_sectors,
                None,
                "Number of sectors",
            )
        if sector_timer is not None:
            self.update_sensor(
                str(OralBSensor.SECTOR_TIMER), None, sector_timer, None, "Sector Timer"
            )
        self.update_sensor(
            str(OralBSensor.TOOTHBRUSH_STATE), None, tb_state, None, "Toothbrush State"
        )
        self.update_sensor(
            str(OralBSensor.PRESSURE), None, tb_pressure, None, "Pressure"
        )
        self.update_sensor(str(OralBSensor.MODE), None, tb_mode, None, "Mode")
        self.update_binary_sensor(
            str(OralBBinarySensor.BRUSHING), bool(state == 3), None, "Brushing"
        )
        """