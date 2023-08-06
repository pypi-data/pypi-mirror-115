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
from ..enums.bcm_enums import HSResistorTIA


class DCBTimingInfoPacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["clear_entries_time"] = {"size": 2, "join": True}
        self._config["payload"]["check_entries_time"] = {"size": 2, "join": True}
        self._config["payload"]["delete_record_time"] = {"size": 2, "join": True}
        self._config["payload"]["read_entry_time"] = {"size": 2, "join": True}
        self._config["payload"]["update_entry_time"] = {"size": 2, "join": True}


class FdsStatusPacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dirty_records"] = {"size": 2, "join": True}
        self._config["payload"]["open_records"] = {"size": 2, "join": True}
        self._config["payload"]["valid_records"] = {"size": 2, "join": True}
        self._config["payload"]["pages_available"] = {"size": 2, "join": True}
        self._config["payload"]["num_blocks"] = {"size": 2, "join": True}
        self._config["payload"]["blocks_free"] = {"size": 2, "join": True}


class HSRTIAPacket(CommandPacket):
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
                'hs_resistor_tia': <HSResistorTIA.RESISTOR_1K: ['0x00', '0x01']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["hs_resistor_tia"] = {"size": 2}
        self._packet["payload"]["hs_resistor_tia"] = [0x00, 0x00]

    def set_hs_resistor_tia(self, hs_resistor_tia_id):
        self._packet["payload"]["hs_resistor_tia"] = hs_resistor_tia_id.value

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["hs_resistor_tia"] = HSResistorTIA(self._packet["payload"]["hs_resistor_tia"])
