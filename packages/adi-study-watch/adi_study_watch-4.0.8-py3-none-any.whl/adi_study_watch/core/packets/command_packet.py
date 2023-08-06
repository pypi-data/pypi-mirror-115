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
from ..enums.common_enums import Application, Command, Status


class CommandPacket:
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.BCM: ['0xC3', '0x07']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <BCMCommand.SET_HS_TRANS_IMPEDANCE_AMPLIFIER_CAL_RES: ['0x49']>,
                'status': <CommonStatus.OK: ['0x00']>,
            }
        }
    """

    def __init__(self, destination=None, command=None):
        self._config = dict(header={}, payload={})
        self._config["header"]["source"] = {"size": 2}
        self._config["header"]["destination"] = {"size": 2}
        self._config["header"]["length"] = {"size": 2, "join": True, "reverse": True, "hex": True}
        self._config["header"]["checksum"] = {"size": 2, "join": True, "reverse": True, "hex": True}
        self._config["payload"]["command"] = {"size": 1}
        self._config["payload"]["status"] = {"size": 1}

        self._packet = dict(header={}, payload={})
        self._packet["header"]["source"] = [0x00, 0x00]
        self._packet["header"]["destination"] = destination.value if destination else [0x00, 0x00]
        self._packet["header"]["length"] = [0x00, 0x0c]
        self._packet["header"]["checksum"] = [0x00, 0x00]
        self._packet["payload"]["command"] = command.value if command else [0x00]
        self._packet["payload"]["status"] = [0x00]

        self._request_command = command
        self._destination = destination

    def __str__(self):
        return str(self.get_dict())

    def get_destination(self):
        return self._destination

    def clear_packet(self):
        self._packet = dict(header={}, payload={})

    @staticmethod
    def decode(data, config, start_index):
        data_slice = data[start_index:start_index + config["size"] if not config["size"] == -1 else None]
        # data_slice = data[config["size"][0]:config["size"][1]]
        join = config.get("join", False)
        sign = config.get("signed", False)
        reverse = config.get("reverse", False)
        to_hex = config.get("hex", False)
        if join:
            return utils.join_multi_length_packets(data_slice, sign=sign, reverse=reverse, convert_to_hex=to_hex)
        else:
            return data_slice

    def decode_packet(self, data):
        command = data[8:9]
        source = data[0:2]
        command = Command(command, source)
        start_index = 0
        for key in self._config["header"]:
            self._packet["header"][key] = self.decode(data, self._config["header"][key], start_index)
            if key == "source":
                self._packet["header"][key] = command.get_source()
            elif key == "destination":
                self._packet["header"][key] = Application(self._packet["header"][key])
            start_index += self._config["header"][key]["size"]
        # self._packet["header"]["time"] = datetime.now()

        for key in self._config["payload"]:
            self._packet["payload"][key] = self.decode(data, self._config["payload"][key], start_index)
            if key == "command":
                self._packet["payload"][key] = command.get_enum()
            elif key == "status":
                self._packet["payload"][key] = Status(self._packet["payload"][key], source,
                                                      command.get_enum().value).get_enum()
            start_index += self._config["payload"][key]["size"]

    def get_id(self, from_device=False):
        subscribe_id = []
        if from_device:
            subscribe_id += self._packet["header"]["source"].value
            subscribe_id += self._packet["payload"]["command"].value

        return utils.join_multi_length_packets(subscribe_id)

    def get_dict(self):
        return self._packet

    def get_request_command(self):
        return self._request_command

    def set_source(self, source):
        self._packet["header"]["source"] = source.value

    def to_list(self):
        packet_list = []
        for key in self._packet["header"]:
            packet_list += self._packet["header"][key]
        for key in self._packet["payload"]:
            packet_list += self._packet["payload"][key]
        return packet_list

    def update_packet_length(self):
        length = 0
        for key in self._packet["header"]:
            length += len(self._packet["header"][key])
        for key in self._packet["payload"]:
            length += len(self._packet["payload"][key])

        length = utils.split_int_in_bytes(length, length=2)
        self._packet["header"]["length"] = list(reversed(length))
