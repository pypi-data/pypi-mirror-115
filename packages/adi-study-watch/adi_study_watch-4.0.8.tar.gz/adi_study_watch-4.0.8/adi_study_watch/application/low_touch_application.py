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
import math
from typing import Dict, List

from ..core import utils
from ..core.enums.fs_enums import FSCommand
from ..core.enums.dcb_enums import DCBCommand
from .common_application import CommonApplication
from ..core.packets.command_packet import CommandPacket
from ..core.enums.low_touch_enum import LTCommand, CommandType
from ..core.enums.common_enums import Application, CommonCommand
from ..core.packets.low_touch_packets import ReadCH2CapPacket, CommandLogPacket
from ..core.packets.common_packets import LibraryConfigReadWritePacket, DCBPacket


class LowTouchApplication(CommonApplication):
    """
    FS Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_low_touch_application()
    """

    START_COMMAND = CommandType.START
    STOP_COMMAND = CommandType.STOP

    def __init__(self, packet_manager):
        super().__init__(Application.LT_APP, packet_manager)
        self._dcb_size = 57
        self._log_command = None

    def read_ch2_cap(self) -> Dict:
        """
        Read the AD7156 CH2 Capacitance in uF.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_ch2_cap()
            print(x["payload"]["cap_value"])
            # 0
        """
        packet = ReadCH2CapPacket(self._destination, LTCommand.READ_CH2_CAP_REQ)
        return self._send_packet(packet, LTCommand.READ_CH2_CAP_RES)

    def write_library_configuration(self, fields_values: List[List[int]]) -> Dict:
        """
        Writes library configuration from List of fields and values.

        :param fields_values: List of fields and values to write.
        :type fields_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x04

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.write_library_configuration([[0x00, 0x1]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        address_range = [0x00, 0x04]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        packet.set_number_of_operations(len(fields_values))
        utils.check_array_address_range(fields_values, address_range, 2)
        packet.set_write_fields_data(fields_values)
        return self._send_packet(packet, CommonCommand.WRITE_LCFG_RES)

    def read_library_configuration(self, fields: List[int]) -> Dict:
        """
        Reads library configuration from specified field values.

        :param fields: List of field values to read.
        :type fields: List[int]
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Fields Lower Limit
             - Fields Upper Limit
           * - 0x00
             - 0x04

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]
        """
        address_range = [0x00, 0x04]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.READ_LCFG_REQ)
        packet.set_number_of_operations(len(fields))
        utils.check_array_address_range(fields, address_range, 1)
        packet.set_read_fields_data(fields)
        return self._send_packet(packet, CommonCommand.READ_LCFG_RES)

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
            application = sdk.get_low_touch_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def read_device_configuration_block(self, readable_format=False) -> [Dict]:
        """
        Returns entire device configuration block.

        :param readable_format: Converts binary result into readable commands.
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
        """
        packet = DCBPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        packet_id = self._get_packet_id(DCBCommand.READ_CONFIG_RES)
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        count = 1
        result = []
        while True:
            data = self._get_queue_data(queue)
            packet = DCBPacket()
            packet.decode_packet(data)
            dict_packet = packet.get_dict()
            result.append(dict_packet)
            if dict_packet["payload"]["num_of_packets"] == count or dict_packet["payload"]["num_of_packets"] == 0:
                break
            count += 1
        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        if readable_format:
            raw_data = []
            total_size = 0
            for packet in result:
                total_size += packet["payload"]["size"]
                raw_data += packet["payload"]["dcb_data"][:packet["payload"]["size"] * 4]

            dcb_readable_format = []
            data_read = 0
            start_cmd_count = 0
            stop_cmd_count = 0
            if len(raw_data) > 0:
                raw_data[0:2], raw_data[2:4] = raw_data[2:4], raw_data[0:2]
                log_packet = CommandLogPacket()
                log_packet.decode_packet(raw_data)
                log_packet = log_packet.get_dict()
                raw_data = log_packet["payload"]["commands"]
                start_cmd_count = log_packet["payload"]["start_cmd_count"]
                stop_cmd_count = log_packet["payload"]["stop_cmd_count"]

                while data_read < len(raw_data):
                    pkt = raw_data[data_read:data_read + 8]
                    if not len(pkt) == 8:
                        break
                    length = (int(pkt[4]) << 8) + int(pkt[5])
                    pkt = raw_data[data_read:data_read + length]
                    pkt[0:2], pkt[2:4] = pkt[2:4], pkt[0:2]
                    packet = CommandPacket()
                    packet.decode_packet(pkt)
                    packet = packet.get_dict()
                    dcb_readable_format.append({"application": packet["header"]["source"],
                                                "command": packet["payload"]["command"]})
                    data_read += length
            result = result[0]
            result["payload"]["size"] = total_size
            result["payload"]["dcb_data"] = dcb_readable_format
            result["payload"]["start_command_count"] = start_cmd_count
            result["payload"]["stop_command_count"] = stop_cmd_count
        return result

    def _write_device_configuration_block(self, commands) -> [Dict]:
        dcb_size = (self._dcb_size * 4)
        packets = math.ceil(len(commands) / dcb_size)
        if packets > 18:
            raise Exception("Can't write more than 18 packets. Size limit 4104 bytes.")
        commands_array = []
        num_tx = utils.split_int_in_bytes(packets, length=2)
        for packet in range(packets):
            commands_array.append(commands[packet * dcb_size:(packet + 1) * dcb_size])
        result = []
        for commands in commands_array:
            packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
            packet.set_size(utils.split_int_in_bytes((len(commands) // 4), length=2) + num_tx)
            packet.set_dcb_write_data(commands, self._dcb_size, len(commands))
            result.append(self._send_packet(packet, DCBCommand.WRITE_CONFIG_RES))
        return result

    def write_device_configuration_block_from_file(self, filename: str) -> [Dict]:
        """
        Writes the device configuration block values from specified binary file.

        :param filename: binary filename
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.write_device_configuration_block_from_file("lt_dcb.dcb")
        """
        with open(filename, 'rb') as file:
            data = file.readlines()
            result = []
            for value in data:
                result += value
            return self._write_device_configuration_block(result)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes ADPD Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def enable_command_logging(self, command_type: CommandType):
        """
        Starts recording SDK commands to a file.

        :param command_type: Start or Stop command recording.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.enable_command_logging(application.START)
        """
        if command_type == CommandType.START:
            self._log_command = CommandLogPacket(Application.FS, command=FSCommand.LOG_USER_CONFIG_DATA_REQ)
            self._packet_manager.subscribe_command_logger(self._log_command)
        self._packet_manager.enable_command_logging(command_type)

    def disable_command_logging(self, command_type: CommandType, filename="commands.LOG"):
        """
        Stops recording SDK commands to a file.

        :param command_type: Start or Stop command recording.
        :param filename: Name of the file to store commands.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_low_touch_application()
            application.disable_command_logging(application.START)
        """
        self._packet_manager.disable_command_logging(command_type)
        if command_type == CommandType.STOP:
            self._packet_manager.unsubscribe_command_logger()
            self._generate_log_file(filename)

    def _generate_log_file(self, filename):
        self._log_command.set_source(self._packet_manager.source)
        with open(filename, 'wb') as file:
            commands = bytearray(self._log_command.to_list())
            remaining = len(commands) % 4
            if remaining:
                commands += b'\0' * (4 - remaining)
            file.write(commands)
