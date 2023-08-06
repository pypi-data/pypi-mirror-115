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
from ..enums.eda_enums import ScaleResistor


class DynamicScalingPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.EDA: ['0xC3', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x11',
                'checksum': '0x0'
            },
            'payload': {
                'command': <EDACommand.DYNAMIC_SCALE_RES: ['0x43']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'enabled': True,
                'min_scale': <ScaleResistor.SCALE_RESISTOR_100K: ['0x14', '0x00']>,
                'max_scale': <ScaleResistor.SCALE_RESISTOR_128K: ['0x16', '0x00']>,
                'lp_resistor_tia': <ScaleResistor.SCALE_RESISTOR_100K: ['0x14', '0x00']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["enabled"] = {"size": 1, "join": True}
        self._config["payload"]["min_scale"] = {"size": 2}
        self._config["payload"]["max_scale"] = {"size": 2}
        self._config["payload"]["lp_resistor_tia"] = {"size": 2}
        self._packet["payload"]["enabled"] = [0x00]
        self._packet["payload"]["min_scale"] = [0x00, 0x00]
        self._packet["payload"]["max_scale"] = [0x00, 0x00]
        self._packet["payload"]["lp_resistor_tia"] = [0x00, 0x00]

    def set_enable(self, enable):
        self._packet["payload"]["enabled"] = enable

    def set_max_scale(self, max_scale):
        self._packet["payload"]["max_scale"] = max_scale

    def set_min_scale(self, min_scale):
        self._packet["payload"]["min_scale"] = min_scale

    def set_lp_resistor_tia(self, lp_resistor_tia):
        self._packet["payload"]["lp_resistor_tia"] = lp_resistor_tia

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["enabled"] = bool(self._packet["payload"]["enabled"])
        self._packet["payload"]["max_scale"] = ScaleResistor(self._packet["payload"]["max_scale"])
        self._packet["payload"]["lp_resistor_tia"] = ScaleResistor(self._packet["payload"]["lp_resistor_tia"])
        self._packet["payload"]["min_scale"] = ScaleResistor(self._packet["payload"]["min_scale"])


class ResistorTIACalibratePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.EDA: ['0xC3', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2A',
                'checksum': '0x0'
            },
            'payload': {
                'command': <EDACommand.RESISTOR_TIA_CAL_RES: ['0x4B']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'min_scale': <ScaleResistor.SCALE_RESISTOR_100K: ['0x14', '0x00']>,
                'max_scale': <ScaleResistor.SCALE_RESISTOR_128K: ['0x16', '0x00']>,
                'lp_resistor_tia': <ScaleResistor.SCALE_RESISTOR_100K: ['0x14', '0x00']>,
                'calibrated_values_count': 3,
                'calibrated_values': [
                    [ 106299, 100000 ],
                    [ 127514, 120000 ],
                    [ 136008, 128000 ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["min_scale"] = {"size": 2}
        self._config["payload"]["max_scale"] = {"size": 2}
        self._config["payload"]["lp_resistor_tia"] = {"size": 2}
        self._config["payload"]["calibrated_values_count"] = {"size": 2, "join": True}
        self._config["payload"]["calibrated_values"] = {"size": -1}
        self._packet["payload"]["min_scale"] = [0x00, 0x00]
        self._packet["payload"]["max_scale"] = [0x00, 0x00]
        self._packet["payload"]["lp_resistor_tia"] = [0x00, 0x00]
        self._packet["payload"]["calibrated_values_count"] = [0x00, 0x00]
        self._packet["payload"]["calibrated_values"] = [0x00] * 25

    def set_max_scale(self, max_scale):
        self._packet["payload"]["max_scale"] = max_scale.value

    def set_min_scale(self, min_scale):
        self._packet["payload"]["min_scale"] = min_scale.value

    def set_lp_resistor_tia(self, lp_resistor_tia):
        self._packet["payload"]["lp_resistor_tia"] = lp_resistor_tia.value

    def set_calibrated_values_count(self, calibrated_values_count):
        self._packet["payload"]["calibrated_values_count"] = calibrated_values_count

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["max_scale"] = ScaleResistor(self._packet["payload"]["max_scale"])
        self._packet["payload"]["min_scale"] = ScaleResistor(self._packet["payload"]["min_scale"])
        self._packet["payload"]["lp_resistor_tia"] = ScaleResistor(self._packet["payload"]["lp_resistor_tia"])
        values_count = self._packet["payload"]["calibrated_values_count"]
        calibrated_values = data[18:]
        data = []
        for i in range(values_count):
            start_index = i * 8
            address_data = calibrated_values[start_index:start_index + 4]
            address = utils.join_multi_length_packets(address_data)
            value_data = calibrated_values[start_index + 4:start_index + 8]
            value = utils.join_multi_length_packets(value_data)
            data.append([address, value])
        self._packet["payload"]["calibrated_values"] = data
