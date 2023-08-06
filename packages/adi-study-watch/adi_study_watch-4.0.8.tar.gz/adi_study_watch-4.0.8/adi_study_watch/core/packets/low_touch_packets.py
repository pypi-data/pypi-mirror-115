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


class ReadCH2CapPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.LT_APP: ['0xC8', '0x0A']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <LTCommand.READ_CH2_CAP_RES: ['0x47']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'cap_value': 1179
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["cap_value"] = {"size": 2, "join": True}


class CommandLogPacket(CommandPacket):
    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["start_cmd_len"] = {"size": 2, "join": True}
        self._config["payload"]["start_cmd_count"] = {"size": 2, "join": True}
        self._config["payload"]["stop_cmd_len"] = {"size": 2, "join": True}
        self._config["payload"]["stop_cmd_count"] = {"size": 2, "join": True}
        self._config["payload"]["crc16"] = {"size": 2, "join": True}
        self._config["payload"]["commands"] = {"size": -1}

        self._packet["payload"]["start_cmd_len"] = [0x0, 0x0]
        self._packet["payload"]["start_cmd_count"] = [0x0, 0x0]
        self._packet["payload"]["stop_cmd_len"] = [0x0, 0x0]
        self._packet["payload"]["stop_cmd_count"] = [0x0, 0x0]
        self._packet["payload"]["crc16"] = [0x0, 0x0]
        self._packet["payload"]["commands"] = []

    def add_start_command(self, command):
        start_cmd_len = utils.join_multi_length_packets(self._packet["payload"]["start_cmd_len"])
        start_cmd_count = utils.join_multi_length_packets(self._packet["payload"]["start_cmd_count"])
        self._packet["payload"]["start_cmd_count"] = utils.split_int_in_bytes(start_cmd_count + 1, length=2)
        self._packet["payload"]["start_cmd_len"] = utils.split_int_in_bytes(start_cmd_len + len(command), length=2)
        self._packet["payload"]["commands"] += command

    def add_stop_command(self, command):
        stop_cmd_len = utils.join_multi_length_packets(self._packet["payload"]["stop_cmd_len"])
        stop_cmd_count = utils.join_multi_length_packets(self._packet["payload"]["stop_cmd_count"])
        self._packet["payload"]["stop_cmd_count"] = utils.split_int_in_bytes(stop_cmd_count + 1, length=2)
        self._packet["payload"]["stop_cmd_len"] = utils.split_int_in_bytes(stop_cmd_len + len(command), length=2)
        self._packet["payload"]["commands"] += command
