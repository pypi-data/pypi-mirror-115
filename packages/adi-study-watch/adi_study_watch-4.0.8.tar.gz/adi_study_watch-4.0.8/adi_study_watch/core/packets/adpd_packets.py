# ******************************************************************************
# Copyright (c) 2019 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

from .command_packet import CommandPacket
from .. import utils
from ..enums.adpd_enums import ADPDDevice, ADPDSlot, Clock, ADPDLed


class ActiveSlotPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_SLOT_ACTIVE_RES: ['0x6B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'slot_num': <ADPDSlot.SLOT_A: ['0x01']>,
                'slot_enabled': False
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["slot_num"] = {"size": 1}
        self._config["payload"]["slot_enabled"] = {"size": 1, "join": True}
        self._packet["payload"]["slot_num"] = [0x00]
        self._packet["payload"]["slot_enabled"] = [0x00]

    def set_slot_num(self, slot_num):
        self._packet["payload"]["slot_num"] = slot_num.value

    def set_slot_active(self, slot_active):
        self._packet["payload"]["slot_enabled"] = slot_active

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["slot_num"] = ADPDSlot(self._packet["payload"]["slot_num"])
        self._packet["payload"]["slot_enabled"] = bool(self._packet["payload"]["slot_enabled"])


class AgcControlPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xF',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_ON_OFF_RES: ['0x77']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'num_ops': 2,
                'agc_data': [
                    [ <ADPDLed.LED_MWL: ['0x00']>, True ],
                    [ <ADPDLed.LED_GREEN: ['0x01']>, True ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["num_ops"] = {"size": 1, "join": True}
        self._packet["payload"]["num_ops"] = [0x01]
        self._packet["payload"]["agc_data"] = [0x00, 0x00]

    def set_number_of_operations(self, num_ops):
        self._packet["payload"]["num_ops"] = num_ops

    def set_fields_values(self, fields_values):
        self._packet["payload"]["agc_data"] = fields_values

    def decode_packet(self, data):
        super().decode_packet(data)
        address_value_data = data[11:]
        data = []
        for i in range((len(address_value_data) // 2)):
            start_index = i * 2
            value_data = address_value_data[start_index:start_index + 1]
            value = bool(utils.join_multi_length_packets(value_data))
            address_data = address_value_data[start_index + 1:start_index + 2]
            address = ADPDLed(address_data)
            data.append([address, value])
        self._packet["payload"]["agc_data"] = data


class AgcInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x61',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_INFO_RES: ['0x7B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'led_index': <ADPDLed.LED_GREEN: ['0x01']>,
                'ch1': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                'ch2': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                'dc0_led_current': 0,
                'tia_ch1': 0,
                'tia_ch2': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["led_index"] = {"size": 1}
        self._config["payload"]["ch1"] = {"size": 40}
        self._config["payload"]["ch2"] = {"size": 40}
        self._config["payload"]["dc0_led_current"] = {"size": 2}
        self._config["payload"]["tia_ch1"] = {"size": 2}
        self._config["payload"]["tia_ch2"] = {"size": 2}

    def set_led_index(self, led_index):
        self._packet["payload"]["led_index"] = led_index.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["led_index"] = ADPDLed(self._packet["payload"]["led_index"])
        ch1 = self._packet["payload"]["ch1"]
        data = []
        for i in range(10):
            start_index = i * 4
            value = utils.join_multi_length_packets(ch1[start_index:start_index + 4])
            data.append(value)
        self._packet["payload"]["ch1"] = data
        ch2 = self._packet["payload"]["ch2"]
        data = []
        for i in range(10):
            start_index = i * 4
            value = utils.join_multi_length_packets(ch2[start_index:start_index + 4])
            data.append(value)
        self._packet["payload"]["ch2"] = data
        dc0_led_current = utils.join_multi_length_packets(self._packet["payload"]["dc0_led_current"])
        self._packet["payload"]["dc0_led_current"] = dc0_led_current
        self._packet["payload"]["tia_ch1"] = utils.join_multi_length_packets(self._packet["payload"]["tia_ch1"])
        self._packet["payload"]["tia_ch2"] = utils.join_multi_length_packets(self._packet["payload"]["tia_ch2"])


class AgcStatusPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.AGC_STATUS_RES: ['0x7D']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'agc_type': <ADPDLed.LED_GREEN: ['0x01']>,
                'agc_status': True
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["agc_type"] = {"size": 1}
        self._config["payload"]["agc_status"] = {"size": 1, "join": True}

    def set_agc_type(self, agc_type):
        self._packet["payload"]["agc_type"] = agc_type.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["agc_type"] = ADPDLed(self._packet["payload"]["agc_type"])
        if self._packet["payload"]["agc_status"] in [0, 1]:
            self._packet["payload"]["agc_status"] = bool(self._packet["payload"]["agc_status"])
        else:
            self._packet["payload"]["agc_status"] = None


class ComModePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.COMMUNICATION_MODE_RES: ['0x69']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'com_mode': 2
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["com_mode"] = {"size": 1, "join": True}
        self._packet["payload"]["com_mode"] = [0x00]

    def set_com_mode(self, com_mode):
        self._packet["payload"]["com_mode"] = com_mode


class SamplingFrequencyPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_SAMPLING_FREQUENCY_RES: ['0x73']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'odr': 100
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["odr"] = {"size": 2, "join": True}
        self._packet["payload"]["odr"] = [0x00, 0x00]

    def set_odr(self, odr):
        self._packet["payload"]["odr"] = odr


class SlotPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xF',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.GET_SLOT_RES: ['0x49']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'slot_num': <ADPDSlot.SLOT_F: ['0x06']>,
                'slot_enabled': True,
                'slot_format': 3,
                'channel_num': 3
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["slot_num"] = {"size": 1}
        self._config["payload"]["slot_enabled"] = {"size": 1, "join": True}
        self._config["payload"]["slot_format"] = {"size": 2, "join": True}
        self._config["payload"]["channel_num"] = {"size": 1, "join": True}
        self._packet["payload"]["slot_num"] = [0x00]
        self._packet["payload"]["slot_enabled"] = [0x00]
        self._packet["payload"]["slot_format"] = [0x00, 0x00]
        self._packet["payload"]["channel_num"] = [0x00]

    def set_slot_num(self, slot_num):
        self._packet["payload"]["slot_num"] = slot_num.value

    def set_slot_enable(self, slot_enable):
        self._packet["payload"]["slot_enabled"] = slot_enable

    def set_slot_format(self, slot_format):
        self._packet["payload"]["slot_format"] = slot_format

    def set_channel_num(self, channel_num):
        self._packet["payload"]["channel_num"] = channel_num

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["slot_num"] = ADPDSlot(self._packet["payload"]["slot_num"])
        self._packet["payload"]["slot_enabled"] = bool(self._packet["payload"]["slot_enabled"])


class TestCommandPacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = {"size": 2}
        self._config["payload"]["return_data"] = {"size": 12}
        self._packet["payload"]["device_id"] = [0x00, 0x00]
        self._packet["payload"]["return_data"] = [0x00] * 12

    def set_data(self, data):
        self._packet["payload"]["return_data"] = data

    def decode_packet(self, data):
        super().decode_packet(data)
        print(utils.convert_int_array_to_hex(self._packet["payload"]["device_id"]))


class ADPDConfigPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x15',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.LOAD_CONFIG_RES: ['0x43']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'device_id': <ADPDDevice.DEVICE_GREEN: ['0x28']>,
                'return_data': [ 255, 255, 31, 0, 112, 7, 0, 99, 0, 0 ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = {"size": 1}
        self._config["payload"]["return_data"] = {"size": 10}
        self._packet["payload"]["device_id"] = [0x00]

    def set_device_id(self, device_id):
        self._packet["payload"]["device_id"] = device_id.value

    def decode_packet(self, data):
        super().decode_packet(data)
        if not self._packet["payload"]["device_id"] == [0]:
            self._packet["payload"]["device_id"] = ADPDDevice(self._packet["payload"]["device_id"])


class ADPDPauseResumePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x15',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_PAUSE_RES: ['0x67']>,
                'status': <CommonStatus.ERROR: ['0x01']>,
                'device_id': <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>,
                'pause': True
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["device_id"] = {"size": 1}
        self._config["payload"]["pause"] = {"size": 10, "join": True}
        self._packet["payload"]["device_id"] = ADPDDevice.DEVICE_G_R_IR_B.value
        self._packet["payload"]["pause"] = [0x00] * 10

    def set_device_id(self, device_id):
        self._packet["payload"]["device_id"] = device_id.value

    def set_data(self, data):
        self._packet["payload"]["pause"] = data

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["device_id"] = ADPDDevice(self._packet["payload"]["device_id"])
        self._packet["payload"]["pause"] = bool(self._packet["payload"]["pause"])


class ClockCalibrationPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.CLOCK_CALIBRATION_RES: ['0x45']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'clock_id': <Clock.CLOCK_1M_AND_32M: ['0x06']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["clock_id"] = {"size": 1}
        self._packet["payload"]["clock_id"] = [0x00]

    def set_clock_id(self, clock_id):
        self._packet["payload"]["clock_id"] = clock_id.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["clock_id"] = Clock(self._packet["payload"]["clock_id"])


class ExternalStreamData(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header':{
                'source': <Application.ADPD: ['0xC1','0x10']>,
                'destination': <Application.APP_USB: ['0xC7','0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
           'payload':{
                'command': <ADPDCommand.EXT_ADPD_DATA_STREAM: ['0x80']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_num': [ 2, 0, 0, 0 ],
                'data': [ 37, 26, 6, 0 ],
                'timestamp': [ 148, 201, 188, 2 ]
           }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["sequence_num"] = {"size": 4}
        self._config["payload"]["data"] = {"size": 4}
        self._config["payload"]["timestamp"] = {"size": 4}
        self._packet["payload"]["sequence_num"] = [0x00] * 4
        self._packet["payload"]["data"] = [0x00] * 4
        self._packet["payload"]["timestamp"] = [0x00] * 4

    def set_sequence_num(self, sequence_num):
        self._packet["payload"]["sequence_num"] = sequence_num

    def set_data(self, data):
        self._packet["payload"]["data"] = data

    def set_timestamp(self, timestamp):
        self._packet["payload"]["timestamp"] = timestamp


class ExternalStreamODR(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <ADPDCommand.SET_EXT_DATA_STREAM_ODR_RES: ['0x7F']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'odr': 50
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["odr"] = {"size": 2, "join": True}
        self._packet["payload"]["odr"] = [0x00] * 2

    def set_sampling_frequency(self, sampling_frequency):
        self._packet["payload"]["odr"] = sampling_frequency
