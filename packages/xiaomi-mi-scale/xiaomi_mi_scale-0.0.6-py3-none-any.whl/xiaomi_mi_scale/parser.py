"""Parser for Xiaomi Mi Scale advertisements.
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
    """Data for Xiaomi Mi Scale sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Xiaomi Mi Scale advertisement data: %s", service_info)
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
            self.update_sensor(str(MiScaleBSensor.WEIGHT), None, weight, None, "Weight")

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
            self.update_sensor(str(MiScaleBSensor.WEIGHT), None, weight, None, "Weight")
            self.update_sensor(str(MiScaleBSensor.IMPEDANCE), None, impedance, None, "Weight")