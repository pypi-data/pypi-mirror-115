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

from .. import utils
from .command_packet import CommandPacket
from ..enums.pm_enums import MCUType, ElectrodeSwitch, LDO, ChipID, BatteryStatus, PowerMode


class AppsHealthPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x16',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.GET_APPS_HEALTH_RES: ['0x91']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'ad5940_isr_count': 202,
                'adpd_isr_count': 3350,
                'adxl_isr_count': 1187
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["ad5940_isr_count"] = {"size": 4, "join": True}
        self._config["payload"]["adpd_isr_count"] = {"size": 4, "join": True}
        self._config["payload"]["adxl_isr_count"] = {"size": 4, "join": True}


class BatteryInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x12',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.GET_BAT_INFO_RES: ['0x45']>,
                'status': <PMStatus.OK: ['0x41']>,
                'timestamp': 668880834,
                'battery_status': <BatteryStatus.COMPLETE: ['0x03']>,
                'battery_level': 100,
                'battery_mv': 4334
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["battery_status"] = {"size": 1}
        self._config["payload"]["battery_level"] = {"size": 1, "join": True}
        self._config["payload"]["battery_mv"] = {"size": 2, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["battery_status"] = BatteryStatus(self._packet["payload"]["battery_status"])


class BatteryThresholdPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xA',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.SET_BAT_THR_RES: ['0x47']>,
                'status': <PMStatus.OK: ['0x41']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._packet["payload"]["bat_low_level"] = [0x00]
        self._packet["payload"]["bat_critical_level"] = [0x00]

    def set_critical_level(self, critical_level):
        self._packet["payload"]["bat_critical_level"] = critical_level

    def set_low_level(self, low_level):
        self._packet["payload"]["bat_low_level"] = low_level


class ChipIDPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xD',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.CHIP_ID_RES: ['0x7D']>,
                'status': <PMStatus.OK: ['0x41']>,
                'chip_name': <ChipID.ADPD4K: ['0x02']>,
                'chip_id': 192
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["chip_name"] = {"size": 1}
        self._config["payload"]["chip_id"] = {"size": 2, "join": True}
        self._packet["payload"]["chip_name"] = [0x00]
        self._packet["payload"]["chip_id"] = [0x00, 0x00]

    def set_chip_name(self, chip_name):
        self._packet["payload"]["chip_name"] = chip_name.value

    def decode_packet(self, data):
        super().decode_packet(data)
        if not self._packet["payload"]["chip_name"] == [0x0]:
            self._packet["payload"]["chip_name"] = ChipID(self._packet["payload"]["chip_name"])


class SwitchControlPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.SW_CONTROL_RES: ['0x79']>,
                'status': <PMStatus.OK: ['0x41']>,
                'switch_name': <ElectrodeSwitch.ADPD4000: ['0x02']>,
                'enabled': False
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["switch_name"] = {"size": 1}
        self._config["payload"]["enabled"] = {"size": 1, "join": True}
        self._packet["payload"]["switch_name"] = [0x00]
        self._packet["payload"]["enabled"] = [0x00]

    def set_enable(self, enable):
        self._packet["payload"]["enabled"] = enable

    def set_name(self, name):
        self._packet["payload"]["switch_name"] = name.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["enabled"] = bool(self._packet["payload"]["enabled"])
        self._packet["payload"]["switch_name"] = ElectrodeSwitch(self._packet["payload"]["switch_name"])


class LDOControlPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.LDO_CONTROL_RES: ['0x7B']>,
                'status': <PMStatus.OK: ['0x41']>,
                'ldo_name': <LDO.OPTICAL: ['0x02']>,
                'enabled': False
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["ldo_name"] = {"size": 1}
        self._config["payload"]["enabled"] = {"size": 1, "join": True}
        self._packet["payload"]["ldo_name"] = [0x00]
        self._packet["payload"]["enabled"] = [0x00]

    def set_enable(self, enable):
        self._packet["payload"]["enabled"] = enable

    def set_name(self, name):
        self._packet["payload"]["ldo_name"] = name.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["enabled"] = bool(self._packet["payload"]["enabled"])
        if not self._packet["payload"]["ldo_name"] == [0x0]:
            self._packet["payload"]["ldo_name"] = LDO(self._packet["payload"]["ldo_name"])


class ControlPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.CAP_SENSE_TEST_RES: ['0x7F']>,
                'status': <PMStatus.OK: ['0x41']>,
                'enabled': False
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["enabled"] = {"size": 1, "join": True}
        self._packet["payload"]["enabled"] = [0x00]

    def set_enable(self, enable):
        self._packet["payload"]["enabled"] = enable

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["enabled"] = bool(self._packet["payload"]["enabled"])


class DateTimePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x15',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.GET_DATE_TIME_RES: ['0x53']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'year': 2021,
                'month': 3,
                'day': 12,
                'hour': 16,
                'minute': 33,
                'second': 12,
                'tz_sec': 19800
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["year"] = {"size": 2, "join": True}
        self._config["payload"]["month"] = {"size": 1, "join": True}
        self._config["payload"]["day"] = {"size": 1, "join": True}
        self._config["payload"]["hour"] = {"size": 1, "join": True}
        self._config["payload"]["minute"] = {"size": 1, "join": True}
        self._config["payload"]["second"] = {"size": 1, "join": True}
        self._config["payload"]["tz_sec"] = {"size": 4, "join": True, "signed": True}
        self._packet["payload"]["year"] = [0x00, 0x00]
        self._packet["payload"]["month"] = [0x00]
        self._packet["payload"]["day"] = [0x00]
        self._packet["payload"]["hour"] = [0x00]
        self._packet["payload"]["minute"] = [0x00]
        self._packet["payload"]["second"] = [0x00]
        self._packet["payload"]["tz_sec"] = [0x00, 0x00, 0x00, 0x00]

    def decode_packet(self, data):
        super().decode_packet(data)
        length = int(self._packet["header"]["length"], 16)
        if length == 10:
            del self._packet["payload"]["year"]
            del self._packet["payload"]["month"]
            del self._packet["payload"]["day"]
            del self._packet["payload"]["hour"]
            del self._packet["payload"]["minute"]
            del self._packet["payload"]["second"]
            del self._packet["payload"]["tz_sec"]

    def set_day(self, day):
        self._packet["payload"]["day"] = day

    def set_hour(self, hour):
        self._packet["payload"]["hour"] = hour

    def set_minute(self, minute):
        self._packet["payload"]["minute"] = minute

    def set_month(self, month):
        self._packet["payload"]["month"] = month

    def set_second(self, second):
        self._packet["payload"]["second"] = second

    def set_tz_sec(self, tz_sec):
        self._packet["payload"]["tz_sec"] = tz_sec

    def set_year(self, year):
        self._packet["payload"]["year"] = year


class DCBStatusPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x1A',
                'checksum': '0x0'
            },
            'payload': {
                'command': <DCBCommand.QUERY_STATUS_RES: ['0x9E']>,
                'status': <PMStatus.OK: ['0x41']>,
                'general_block': 0,
                'ad5940_block': 0,
                'adpd_block': 0,
                'adxl_block': 0,
                'ppg_block': 0,
                'ecg_block': 0,
                'eda_block': 0,
                'ad7156_block': 1,
                'pedometer_block': 0,
                'temperature_block': 0,
                'low_touch_block': 0,
                'ui_config_block': 0,
                'user0_block': 0,
                'user1_block': 0,
                'user2_block': 0,
                'user3_block': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["general_block"] = {"size": 1, "join": True}
        self._config["payload"]["ad5940_block"] = {"size": 1, "join": True}
        self._config["payload"]["adpd_block"] = {"size": 1, "join": True}
        self._config["payload"]["adxl_block"] = {"size": 1, "join": True}
        self._config["payload"]["ppg_block"] = {"size": 1, "join": True}
        self._config["payload"]["ecg_block"] = {"size": 1, "join": True}
        self._config["payload"]["eda_block"] = {"size": 1, "join": True}
        self._config["payload"]["ad7156_block"] = {"size": 1, "join": True}
        self._config["payload"]["pedometer_block"] = {"size": 1, "join": True}
        self._config["payload"]["temperature_block"] = {"size": 1, "join": True}
        self._config["payload"]["low_touch_block"] = {"size": 1, "join": True}
        self._config["payload"]["ui_config_block"] = {"size": 1, "join": True}
        self._config["payload"]["user0_block"] = {"size": 1, "join": True}
        self._config["payload"]["user1_block"] = {"size": 1, "join": True}
        self._config["payload"]["user2_block"] = {"size": 1, "join": True}
        self._config["payload"]["user3_block"] = {"size": 1, "join": True}
        self._config["payload"]["bcm_block"] = {"size": 1, "join": True}


class MCUVersionPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.GET_MCU_VERSION_RES: ['0x59']>,
                'status': <PMStatus.OK: ['0x41']>,
                'mcu': <MCUType.MCU_M4: ['0x02']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["mcu"] = {"size": 1}
        self._packet["payload"]["mcu"] = [0x00]

    def set_mcu(self, mcu):
        self._packet["payload"]["mcu"] = mcu

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["mcu"] = MCUType(self._packet["payload"]["mcu"])


class PingPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x49',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.PING_RES: ['0x1B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_num': 1,
                'data': [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ... , 0, 0, 0, 0 ],
                'elapsed_time': 0.016231060028076172
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["sequence_num"] = {"size": 4, "join": True}
        self._config["payload"]["data"] = {"size": -1}
        self._packet["payload"]["sequence_num"] = [0x00]

    def set_num_pings(self, num_pings):
        self._packet["payload"]["sequence_num"] = num_pings

    def set_packet_size(self, packet_size):
        self._packet["header"]["length"] = packet_size
        size = utils.join_multi_length_packets(packet_size, reverse=True)
        self._packet["payload"]["data"] = [0x00] * (size - 11)


class PowerStatePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.SET_POWER_STATE_RES: ['0x49']>,
                'status': <PMStatus.OK: ['0x41']>,
                'power_state': <PowerMode.ACTIVE: ['0x00']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["power_state"] = {"size": 1}
        self._packet["payload"]["power_state"] = [0x00]

    def set_state(self, state):
        self._packet["payload"]["power_state"] = state.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["power_state"] = PowerMode(self._packet["payload"]["power_state"])


class SystemInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PM: ['0xC5', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x24',
                'checksum': '0x0'
            },
            'payload': {
                'command': <PMCommand.SYS_INFO_RES: ['0x4B']>,
                'status': <PMStatus.OK: ['0x41']>,
                'version': 0,
                'mac_address': 'C5-05-CA-F1-67-D5',
                'device_id': 0,
                'model_number': 0,
                'hw_id': 0,
                'bom_id': 0,
                'batch_id': 0,
                'date': 0,
                'board_type': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["version"] = {"size": 2, "join": True}
        self._config["payload"]["mac_address"] = {"size": 6}
        self._config["payload"]["device_id"] = {"size": 4, "join": True}
        self._config["payload"]["model_number"] = {"size": 4, "join": True}
        self._config["payload"]["hw_id"] = {"size": 2, "join": True}
        self._config["payload"]["bom_id"] = {"size": 2, "join": True}
        self._config["payload"]["batch_id"] = {"size": 1, "join": True}
        self._config["payload"]["date"] = {"size": 4, "join": True}
        self._config["payload"]["board_type"] = {"size": 1, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["mac_address"] = ''.join(
            '{:02X}-'.format(x) for x in self._packet["payload"]["mac_address"])[:-1]
