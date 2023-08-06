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

import time
import logging
from datetime import datetime
from typing import Dict, List

from ..core import utils
from ..core.enums.dcb_enums import DCBCommand
from .common_application import CommonApplication
from ..core.enums.pm_enums import PMCommand, ChipID
from ..core.packets.command_packet import CommandPacket
from ..core.enums.common_enums import Application, CommonCommand
from ..core.packets.common_packets import VersionPacket, RegisterPacket, DCBPacket
from ..core.packets.pm_packets import BatteryInfoPacket, DCBStatusPacket, ChipIDPacket
from ..core.packets.pm_packets import MCUVersionPacket, SystemInfoPacket, DateTimePacket

logger = logging.getLogger(__name__)


class PMApplication(CommonApplication):
    """
    PM Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_pm_application()

    """

    CHIP_ADPD4K = ChipID.ADPD4K
    CHIP_AD5940 = ChipID.AD5940
    CHIP_AD7156 = ChipID.AD7156
    CHIP_ADXL362 = ChipID.ADXL362
    CHIP_ADP5360 = ChipID.ADP5360
    CHIP_NAND_FLASH = ChipID.NAND_FLASH

    def __init__(self, packet_manager):
        super().__init__(Application.PM, packet_manager)
        self._dcb_size = 57

    def _chip_helper(self, chip_id: ChipID) -> ChipID:
        """
        Confirms chip id is from list of Enums.
        """
        if chip_id in self.get_supported_chips():
            return chip_id
        else:
            logger.warning(f"{chip_id} is not supported chip id, choosing {self.get_supported_chips()[0]} "
                           f"as default chip id. use get_supported_chips() to know all supported chip IDs")
            return self.get_supported_chips()[0]

    def device_configuration_block_status(self) -> Dict:
        """
        Display dcb status of all applications.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.device_configuration_block_status()
            print(x["payload"]["adxl_block"], x["payload"]["adpd4000_block"], x["payload"]["ppg_block"])
            # 0 0 0

        """
        packet = DCBStatusPacket(self._destination, DCBCommand.QUERY_STATUS_REQ)
        return self._send_packet(packet, DCBCommand.QUERY_STATUS_RES)

    def disable_touch_sensor(self) -> Dict:
        """
        Disables touch sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.disable_touch_sensor()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        packet = CommandPacket(self._destination, PMCommand.DEACTIVATE_TOUCH_SENSOR_REQ)
        return self._send_packet(packet, PMCommand.DEACTIVATE_TOUCH_SENSOR_RES)

    def enable_touch_sensor(self) -> Dict:
        """
        Enables touch sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.enable_touch_sensor()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        packet = CommandPacket(self._destination, PMCommand.ACTIVATE_TOUCH_SENSOR_REQ)
        return self._send_packet(packet, PMCommand.ACTIVATE_TOUCH_SENSOR_RES)

    def enter_boot_loader_mode(self) -> Dict:
        """
        Sets the device to boot loader mode.

        :return: A empty dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.enter_boot_loader_mode()

        """
        packet = CommandPacket(self._destination, PMCommand.ENTER_BOOTLOADER_REQ)
        self._packet_manager.send_packet(packet)
        return {}

    def get_battery_info(self) -> Dict:
        """
        Returns device current battery information.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_battery_info()
            print(x["payload"]["battery_status"], x["payload"]["battery_level"])
            # BatteryStatus.COMPLETE 100

        """
        packet = BatteryInfoPacket(self._destination, PMCommand.GET_BAT_INFO_REQ)
        return self._send_packet(packet, PMCommand.GET_BAT_INFO_RES)

    def get_chip_id(self, chip_name: ChipID) -> Dict:
        """
        Returns chip id for specified chip name.

        :param chip_name: get chip id of the chip_name, use get_supported_chips() to list all support chip names.
        :type chip_name: ChipID
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_supported_chips()
            print(x)
            # [<ChipID.CHIP_ADXL362: ['0x1']>, ... , <ChipID.CHIP_AD7156: ['0x6']>]
            x = application.get_chip_id(application.CHIP_ADPD4K)
            print(x["payload"]["chip_name"], x["payload"]["chip_id"])
            # ChipID.ADPD4K 192

        """
        chip_name = self._chip_helper(chip_name)
        packet = ChipIDPacket(self._destination, PMCommand.CHIP_ID_REQ)
        packet.set_chip_name(chip_name)
        return self._send_packet(packet, PMCommand.CHIP_ID_RES)

    def get_datetime(self) -> Dict:
        """
        Returns device current datetime.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_datetime()
            print(f"{x['payload']['year']}-{x['payload']['month']}-{x['payload']['day']}")
            # 2020-12-16
            print(f"{x['payload']['hour']}:{x['payload']['minute']}:{x['payload']['second']}")
            # 15:17:57
        """
        packet = DateTimePacket(self._destination, PMCommand.GET_DATE_TIME_REQ)
        return self._send_packet(packet, PMCommand.GET_DATE_TIME_RES)

    def get_low_touch_status(self) -> Dict:
        """
        Returns low touch status.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_low_touch_status()
            print(x["payload"]["status"])
            # PMStatus.LOW_TOUCH_LOGGING_NOT_STARTED
        """
        packet = CommandPacket(self._destination, PMCommand.GET_LOW_TOUCH_LOGGING_STATUS_REQ)
        return self._send_packet(packet, PMCommand.GET_LOW_TOUCH_LOGGING_STATUS_RES)

    def get_mcu_version(self) -> Dict:
        """
        Returns Device MCU version.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_mcu_version()
            print(x["payload"]["mcu"])
            # MCUType.MCU_M4
        """
        packet = MCUVersionPacket(self._destination, PMCommand.GET_MCU_VERSION_REQ)
        return self._send_packet(packet, PMCommand.GET_MCU_VERSION_RES)

    def get_supported_chips(self) -> List[ChipID]:
        """
        List all supported chips for PM.

        :return: Array of chips enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_supported_chips()
            print(x)
            # [<ChipID.CHIP_ADXL362: ['0x1']>, ... , <ChipID.CHIP_AD7156: ['0x6']>]
        """
        return [self.CHIP_ADXL362, self.CHIP_ADPD4K, self.CHIP_ADP5360, self.CHIP_AD5940, self.CHIP_NAND_FLASH,
                self.CHIP_AD7156]

    def get_system_info(self) -> Dict:
        """
        Returns Device system info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_system_info()
            print(x["payload"]["version"])
            # 0
            print(x["payload"]["mac_address"])
            # C5-05-CA-F1-67-D5
            print(x["payload"]["device_id"])
            # 0

        """
        packet = SystemInfoPacket(self._destination, PMCommand.SYS_INFO_REQ)
        return self._send_packet(packet, PMCommand.SYS_INFO_RES)

    def get_version(self) -> Dict:
        """
        Returns Device version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 1
            print(x["payload"]["minor_version"])
            # 0
            print(x["payload"]["patch_version"])
            # 1
            print(x["payload"]["version_string"])
            # -Perseus
            print(x["payload"]["build_version"])
            # |298b4ce1_Rl|2020-12-14 12:34:31 -0500
        """
        packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        return self._send_packet(packet, CommonCommand.GET_VERSION_RES)

    def read_register(self, addresses: List[int]) -> Dict:
        """
        Reads the register values of specified addresses. This function takes a list of addresses to read,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses: List of register addresses to read.
        :type addresses: List[int]
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x00
             - 0x36

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]

        """
        address_range = [0x00, 0x36]
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        packet.set_number_of_operations(len(addresses))
        utils.check_array_address_range(addresses, address_range, 2)
        packet.set_read_reg_data(addresses)
        return self._send_packet(packet, CommonCommand.REGISTER_READ_RES)

    def set_datetime(self, date_time: datetime) -> Dict:
        """
        Set specified datetime to device.

        :param date_time: datetime for device.
        :type date_time: datetime
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK
            import datetime

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            now = datetime.datetime.now()
            x = application.set_datetime(now)
            print(x["payload"]["status"])
            # CommonStatus.OK

        """
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        packet = DateTimePacket(self._destination, PMCommand.SET_DATE_TIME_REQ)
        year = utils.split_int_in_bytes(date_time.year, length=2)
        packet.set_year(year)
        packet.set_month([date_time.month])
        packet.set_day([date_time.day])
        packet.set_hour([date_time.hour])
        packet.set_minute([date_time.minute])
        packet.set_second([date_time.second])
        tz_sec = utils.split_int_in_bytes(utc_offset, length=4)
        packet.set_tz_sec(tz_sec)
        return self._send_packet(packet, PMCommand.SET_DATE_TIME_RES)

    def set_timeout(self, timeout_value: float) -> None:
        """
        Sets the time out for queue to wait for command packet response.

        :param timeout_value: queue timeout value (in sec).
        :type timeout_value: int
        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def system_hardware_reset(self) -> Dict:
        """
        Reset device hardware.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.system_hardware_reset()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        packet = CommandPacket(self._destination, PMCommand.SYSTEM_HW_RESET_REQ)
        return self._send_packet(packet, PMCommand.SYSTEM_HW_RESET_RES)

    def system_reset(self) -> Dict:
        """
        Reset device system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.system_reset()
            print(x["payload"]["status"])
            # PMStatus.OK
        """
        packet = CommandPacket(self._destination, PMCommand.SYSTEM_RESET_REQ)
        return self._send_packet(packet, PMCommand.SYSTEM_RESET_RES)

    def write_register(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the register values of specified addresses. This function takes a list of addresses and values to write,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses_values: List of register addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 75
           :header-rows: 1

           * - Address ranges
           * - [0x2-0x7], [0xA-0xE], [0x11-0x22], [0x27-0x2E], [0x30-0x33], [0x36]


        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]

        """
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        num_ops = len(addresses_values)
        packet.set_number_of_operations(num_ops)
        for i in range(num_ops):
            if not (0x2 <= addresses_values[i][0] <= 0x7 or 0xA <= addresses_values[i][0] <= 0xE or
                    0x11 <= addresses_values[i][0] <= 0x22 or 0x27 <= addresses_values[i][0] <= 0x2E or
                    0x30 <= addresses_values[i][0] <= 0x33 or addresses_values[i][0] == 0x36):
                logger.warning(f"{'0x%X' % addresses_values[i][0]} is out of range, allowed ranges are: [0x2-0x7], "
                               f"[0xA-0xE], [0x11-0x22], [0x27-0x2E], [0x30-0x33], [0x36]")
            addresses_values[i][0] = utils.range_and_type_check(addresses_values[i][0], type_of=int, num_bytes=2)
            addresses_values[i][1] = utils.range_and_type_check(addresses_values[i][1], type_of=int, num_bytes=2)
        packet.set_write_reg_data(addresses_values)
        return self._send_packet(packet, CommonCommand.REGISTER_WRITE_RES)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes AD7156 Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
            # []

        """
        packet = DCBPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.READ_CONFIG_RES)

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the device configuration block values of specified addresses.
        This function takes a list of addresses and values to write, and returns a response packet as
        dictionary containing addresses and values.

        :param addresses_values: List of addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            x = application.write_device_configuration_block([[0x2, 2], [0x1, 0x1]])
            print(x["payload"]["size"])
            # 2

        """
        packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        packet.set_size(utils.split_int_in_bytes(len(addresses_values), length=2))
        packet.set_dcb_write_data(addresses_values, self._dcb_size, len(addresses_values))
        return self._send_packet(packet, DCBCommand.WRITE_CONFIG_RES)

    def write_device_configuration_block_from_file(self, filename: str) -> Dict:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_pm_application()
            application.write_device_configuration_block_from_file("pm_dcb.dcfg")

        """
        result = self._write_device_configuration_block_from_file_helper(filename)
        if result:
            return self.write_device_configuration_block(result)
