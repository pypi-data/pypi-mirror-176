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



class MiScaleBluetoothDeviceData(BluetoothData):
    """Data for Xiaomi Mi Scale sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Xiaomi Mi Scale advertisement data: %s", service_info)
        print("Parsing Xiaomi Mi Scale advertisement data: %s", service_info)
        self.set_device_manufacturer("Xiaomi")
        manufacturer_data = service_info.manufacturer_data
        address = service_info.address
        service_data = service_info.service_data


        if list(advertising_data.service_data.keys())[0] == "0000181b-0000-1000-8000-00805f9b34fb":
            ### Xiaomi V2 Scale ###
            data = binascii.b2a_hex(advertising_data.service_data['0000181b-0000-1000-8000-00805f9b34fb']).decode('ascii')
            #logging.debug(f"miscale v2 with advertising_data: {advertising_data}")
            data2 = bytes.fromhex(data)
            ctrlByte1 = data2[1]
            isStabilized = ctrlByte1 & (1<<5)
            hasImpedance = ctrlByte1 & (1<<1)
            measunit = data[0:2]
            measured = int((data[24:26] + data[22:24]), 16) * 0.01
            unit = ''
            if measunit == "03": unit = 'lbs'
            if measunit == "02": unit = 'kg' ; measured = measured / 2
            miimpedance = str(int((data[20:22] + data[18:20]), 16))
            if unit and isStabilized:
                if OLD_MEASURE != round(measured, 2) + int(miimpedance):
                    OLD_MEASURE = round(measured, 2) + int(miimpedance)
                    self.update_sensor(str(OralBSensor.TIME), None, time, None, "Time")
                    #MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), hasImpedance, miimpedance)
                    self.update_sensor(str(MiScaleSensor.WEIGHT), None, measured, None, "Weight")
                    self.update_sensor(str(MiScaleSensor.IMPEDANCE), None, miimpedance, None, "Impedance")
        elif list(advertising_data.service_data.keys())[0] == "0000181d-0000-1000-8000-00805f9b34fb":
            ### Xiaomi V1 Scale ###
            data = binascii.b2a_hex(advertising_data.service_data['0000181d-0000-1000-8000-00805f9b34fb']).decode('ascii')
            logging.debug(f"miscale v1 found with advertising_data: {advertising_data}")
            measunit = data[0:2]
            measured = int((data[4:6] + data[2:4]), 16) * 0.01
            unit = ''
            if measunit.startswith(('03', 'a3')): unit = 'lbs'
            if measunit.startswith(('12', 'b2')): unit = 'jin'
            if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
            if unit:
                if OLD_MEASURE != round(measured, 2):
                    OLD_MEASURE = round(measured, 2)
                    #MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), "", "")
                    self.update_sensor(str(MiScaleSensor.WEIGHT), None, measured, None, "Weight")