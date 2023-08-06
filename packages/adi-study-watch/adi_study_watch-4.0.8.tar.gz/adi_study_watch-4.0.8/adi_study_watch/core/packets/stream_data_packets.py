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

import struct
from .. import utils
from .command_packet import CommandPacket


class ADPDDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADPD6: ['0xC2', '0x16']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 4,
                'channel_num': 2,
                'timestamp': 1751731879,
                'sample_num': 2,
                'signal_data': [ 351762, 351755 ],
                'dark_data': [ 0, 0 ],
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["data_type"] = {"size": 2, "join": True}
        self._config["payload"]["channel_num"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["sample_num"] = {"size": 1, "join": True}
        self._config["payload"]["data"] = {"size": 25}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["dark_data"] = []
        self._packet["payload"]["signal_data"] = []
        if self._packet["payload"]["data_type"] & 0x100 == 0:
            signal_size = (self._packet["payload"]["data_type"] & 0xF)
            dark_size = (self._packet["payload"]["data_type"] & 0xF0) >> 4
            data_size = signal_size + dark_size
            sample_num = self._packet["payload"]["sample_num"]
            for i in range(0, sample_num * data_size, data_size):
                data = self._packet["payload"]["data"][i: i + dark_size]
                dark_data = utils.join_multi_length_packets(data)
                data = self._packet["payload"]["data"][i + dark_size: i + dark_size + signal_size]
                signal_data = utils.join_multi_length_packets(data)
                self._packet["payload"]["dark_data"].append(dark_data)
                self._packet["payload"]["signal_data"].append(signal_data)
        else:
            signal_size = (self._packet["payload"]["data_type"] & 0xFF)
            for i in range(0, signal_size, 2):
                self._packet["payload"]["dark_data"].append(0)
                data = self._packet["payload"]["data"][i: i + 1]
                signal_data = utils.join_multi_length_packets(data)
                self._packet["payload"]["signal_data"].append(signal_data)
        del self._packet["payload"]["data"]

    def update_timestamp(self, last_timestamp):
        reference_time, last_ts = last_timestamp
        timestamp = self._packet["payload"]["timestamp"]
        reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
        self._packet["payload"]["timestamp"] = reference_time * 1000
        last_timestamp[0] = reference_time
        last_timestamp[1] = timestamp


class ADXLDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ADXL: ['0xC2', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x37',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 395,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1767361372,
                        'x': -85,
                        'y': 90,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362027,
                        'x': -80,
                        'y': 88,
                        'z': 55
                    },
                    {
                        'timestamp': 1767362682,
                        'x': 40,
                        'y': 274,
                        'z': 79
                    },
                    {
                        'timestamp': 1767363337,
                        'x': 70,
                        'y': 273,
                        'z': 54
                    },
                    {
                        'timestamp': 1767363931,
                        'x': 57,
                        'y': 257,
                        'z': 48
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["data_type"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["x1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["y1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["z1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp2"] = {"size": 2, "join": True}
        self._config["payload"]["x2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["y2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["z2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp3"] = {"size": 2, "join": True}
        self._config["payload"]["x3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["y3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["z3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp4"] = {"size": 2, "join": True}
        self._config["payload"]["x4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["y4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["z4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp5"] = {"size": 2, "join": True}
        self._config["payload"]["x5"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["y5"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["z5"] = {"size": 2, "join": True, "signed": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 6):
            timestamp += self._packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "x": self._packet["payload"][f"x{i}"],
                    "y": self._packet["payload"][f"y{i}"],
                    "z": self._packet["payload"][f"z{i}"]}
            [self._packet["payload"].pop(key) for key in [f"timestamp{i}", f"x{i}", f"y{i}", f"z{i}"]]
            self._packet["payload"]["stream_data"].append(data)

    def update_timestamp(self, last_timestamp):
        for i in range(len(self._packet["payload"]["stream_data"])):
            reference_time, last_ts = last_timestamp
            timestamp = self._packet["payload"]["stream_data"][i]["timestamp"]
            reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
            self._packet["payload"]["stream_data"][i]["timestamp"] = reference_time * 1000
            last_timestamp[0] = reference_time
            last_timestamp[1] = timestamp


class ECGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.ECG: ['0xC4', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x3D',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 1,
                'ecg_info': 0,
                'hr': 0,
                'stream_data': [
                    {
                        'timestamp': 1771095376,
                        'ecg_data': 12351
                    },
                    {
                        'timestamp': 1771095703,
                        'ecg_data': 12353
                    },
                    {
                        'timestamp': 1771096030,
                        'ecg_data': 52470
                    },
                    {
                        'timestamp': 1771096357,
                        'ecg_data': 41129
                    },
                    {
                        'timestamp': 1771096676,
                        'ecg_data': 63838
                    },
                    {
                        'timestamp': 1771096995,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097314,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097633,
                        'ecg_data': 63848
                    },
                    {
                        'timestamp': 1771097954,
                        'ecg_data': 63833
                    },
                    {
                        'timestamp': 1771098273,
                        'ecg_data': 63846
                    },
                    {
                        'timestamp': 1771098592,
                        'ecg_data': 63846
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["data_type"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["ecg_info"] = {"size": 1, "join": True}
        self._config["payload"]["hr"] = {"size": 1, "join": True}
        self._config["payload"]["ecg_data1"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp2"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data2"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp3"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data3"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp4"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data4"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp5"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data5"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp6"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data6"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp7"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data7"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp8"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data8"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp9"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data9"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp10"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data10"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp11"] = {"size": 2, "join": True}
        self._config["payload"]["ecg_data11"] = {"size": 2, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_data"] = []
        timestamp = 0
        for i in range(1, 12):
            timestamp += self._packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "ecg_data": self._packet["payload"][f"ecg_data{i}"]}
            [self._packet["payload"].pop(key) for key in [f"timestamp{i}", f"ecg_data{i}"]]
            self._packet["payload"]["stream_data"].append(data)

    def update_timestamp(self, last_timestamp):
        for i in range(len(self._packet["payload"]["stream_data"])):
            reference_time, last_ts = last_timestamp
            timestamp = self._packet["payload"]["stream_data"][i]["timestamp"]
            reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
            self._packet["payload"]["stream_data"][i]["timestamp"] = reference_time * 1000
            last_timestamp[0] = reference_time
            last_timestamp[1] = timestamp


class EDADataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.EDA: ['0xC4', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x3D',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1774366622,
                        'real_data': 0,
                        'imaginary_data': 0
                    },
                    {
                        'timestamp': 1774374407,
                        'real_data': 0,
                        'imaginary_data': 16708
                    },
                    {
                        'timestamp': 1774382157,
                        'real_data': 16728,
                        'imaginary_data': 3257
                    },
                    {
                        'timestamp': 1774389924,
                        'real_data': 3277,
                        'imaginary_data': -20751
                    },
                    {
                        'timestamp': 1774397691,
                        'real_data': -20731,
                        'imaginary_data': -15161
                    },
                    {
                        'timestamp': 1774405458,
                        'real_data': -15141,
                        'imaginary_data': -30319
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["data_type"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["real_data1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp2"] = {"size": 4, "join": True}
        self._config["payload"]["real_data2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp3"] = {"size": 4, "join": True}
        self._config["payload"]["real_data3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp4"] = {"size": 4, "join": True}
        self._config["payload"]["real_data4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp5"] = {"size": 4, "join": True}
        self._config["payload"]["real_data5"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data5"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["timestamp6"] = {"size": 4, "join": True}
        self._config["payload"]["real_data6"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["imaginary_data6"] = {"size": 2, "join": True, "signed": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_data"] = []
        for i in range(1, 7):
            timestamp = self._packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "real_data": self._packet["payload"][f"real_data{i}"],
                    "imaginary_data": self._packet["payload"][f"imaginary_data{i}"]}
            [self._packet["payload"].pop(key) for key in [f"timestamp{i}", f"real_data{i}", f"imaginary_data{i}"]]
            self._packet["payload"]["stream_data"].append(data)

    def update_timestamp(self, last_timestamp):
        for i in range(len(self._packet["payload"]["stream_data"])):
            reference_time, last_ts = last_timestamp
            timestamp = self._packet["payload"]["stream_data"][i]["timestamp"]
            reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
            self._packet["payload"]["stream_data"][i]["timestamp"] = reference_time * 1000
            last_timestamp[0] = reference_time
            last_timestamp[1] = timestamp


class PedometerDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.PEDOMETER: ['0xC4', '0x04']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x17',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 1,
                'steps': 0,
                'algo_status': 8193,
                'timestamp': 1776836792,
                'reserved': 0
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["steps"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["algo_status"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["reserved"] = {"size": 1, "join": True}

    def update_timestamp(self, last_timestamp):
        reference_time, last_ts = last_timestamp
        timestamp = self._packet["payload"]["timestamp"]
        reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
        self._packet["payload"]["timestamp"] = reference_time * 1000
        last_timestamp[0] = reference_time
        last_timestamp[1] = timestamp


class TemperatureDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.TEMPERATURE: ['0xC4', '0x06']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x14',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 2,
                'timestamp': 1779692742,
                'skin_temperature': 30.1, # celsius
                'impedance': 79000 # ohm
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["skin_temperature"] = {"size": 2, "join": True}
        self._config["payload"]["impedance"] = {"size": 2, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["skin_temperature"] = self._packet["payload"]["skin_temperature"] / 10.0
        self._packet["payload"]["impedance"] = self._packet["payload"]["impedance"] * 100

    def update_timestamp(self, last_timestamp):
        reference_time, last_ts = last_timestamp
        timestamp = self._packet["payload"]["timestamp"]
        reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
        self._packet["payload"]["timestamp"] = reference_time * 1000
        last_timestamp[0] = reference_time
        last_timestamp[1] = timestamp


class PPGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.PPG: ['0xC4', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2E',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.NEW_STREAM_STATUS: ['0x43']>,
                'sequence_number': 9,
                'timestamp': 1782357951,
                'adpd_lib_state': 7,
                'hr': 0,
                'confidence': 0,
                'hr_type': 0,
                'rr_interval': 0,
                'debug_info': [ 0, 320, 50, 0, 5, 0, 320, 50, 978 ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["adpd_lib_state"] = {"size": 2, "join": True}
        self._config["payload"]["hr"] = {"size": 2, "join": True}
        self._config["payload"]["confidence"] = {"size": 2, "join": True}
        self._config["payload"]["hr_type"] = {"size": 2, "join": True}
        self._config["payload"]["rr_interval"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info1"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info2"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info3"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info4"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info5"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info6"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info7"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info8"] = {"size": 2, "join": True}
        self._config["payload"]["debug_info9"] = {"size": 2, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["debug_info"] = [self._packet["payload"][f"debug_info"]]
        for i in range(1, 10):
            self._packet["payload"]["debug_info"].append(self._packet["payload"][f"debug_info{i}"])
            del self._packet["payload"][f"debug_info{i}"]

    def update_timestamp(self, last_timestamp):
        reference_time, last_ts = last_timestamp
        timestamp = self._packet["payload"]["timestamp"]
        reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
        self._packet["payload"]["timestamp"] = reference_time * 1000
        last_timestamp[0] = reference_time
        last_timestamp[1] = timestamp


class SYNCPPGDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SYNC_PPG: ['0xC4', '0x05']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x48',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 119,
                'stream_data': [
                    {
                        'ppg_timestamp': 1782379042,
                        'ppg_data': 186278,
                        'adxl_timestamp': 1782378429,
                        'adxl_x': 48,
                        'adxl_y': 268,
                        'adxl_z': 62
                    },
                    {
                        'ppg_timestamp': 1782379682,
                        'ppg_data': 186278,
                        'adxl_timestamp': 1782379070,
                        'adxl_x': 55,
                        'adxl_y': 264,
                        'adxl_z': 60
                    },
                    {
                        'ppg_timestamp': 1782380323,
                        'ppg_data': 186289,
                        'adxl_timestamp': 1782379709,
                        'adxl_x': 68,
                        'adxl_y': 268,
                        'adxl_z': 57
                    },
                    {
                        'ppg_timestamp': 1782380962,
                        'ppg_data': 186305,
                        'adxl_timestamp': 1782380349,
                        'adxl_x': 60,
                        'adxl_y': 263,
                        'adxl_z': 62
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["ppg_timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["adxl_timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["ppg_timestamp2"] = {"size": 2, "join": True}
        self._config["payload"]["ppg_timestamp3"] = {"size": 2, "join": True}
        self._config["payload"]["ppg_timestamp4"] = {"size": 2, "join": True}
        self._config["payload"]["adxl_timestamp2"] = {"size": 2, "join": True}
        self._config["payload"]["adxl_timestamp3"] = {"size": 2, "join": True}
        self._config["payload"]["adxl_timestamp4"] = {"size": 2, "join": True}
        self._config["payload"]["ppg_data1"] = {"size": 4, "join": True}
        self._config["payload"]["ppg_data2"] = {"size": 4, "join": True}
        self._config["payload"]["ppg_data3"] = {"size": 4, "join": True}
        self._config["payload"]["ppg_data4"] = {"size": 4, "join": True}
        self._config["payload"]["adxl_x1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_x2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_x3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_x4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_y1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_y2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_y3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_y4"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_z1"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_z2"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_z3"] = {"size": 2, "join": True, "signed": True}
        self._config["payload"]["adxl_z4"] = {"size": 2, "join": True, "signed": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_data"] = []
        ppg_timestamp = 0
        adxl_timestamp = 0
        for i in range(1, 5):
            ppg_timestamp += self._packet["payload"][f"ppg_timestamp{i}"]
            adxl_timestamp += self._packet["payload"][f"adxl_timestamp{i}"]
            data = {"ppg_timestamp": ppg_timestamp,
                    "ppg_data": self._packet["payload"][f"ppg_data{i}"],
                    "adxl_timestamp": adxl_timestamp,
                    "adxl_x": self._packet["payload"][f"adxl_x{i}"],
                    "adxl_y": self._packet["payload"][f"adxl_y{i}"],
                    "adxl_z": self._packet["payload"][f"adxl_z{i}"]}
            [self._packet["payload"].pop(key) for key in
             [f"ppg_timestamp{i}", f"ppg_data{i}", f"adxl_timestamp{i}", f"adxl_x{i}", f"adxl_y{i}", f"adxl_z{i}"]]
            self._packet["payload"]["stream_data"].append(data)

    def update_timestamp(self, last_timestamp):
        for i in range(len(self._packet["payload"]["stream_data"])):
            ppg_reference_time, ppg_last_ts, adxl_reference_time, adxl_last_ts = last_timestamp
            ppg_timestamp = self._packet["payload"]["stream_data"][i]["ppg_timestamp"]
            adxl_timestamp = self._packet["payload"]["stream_data"][i]["adxl_timestamp"]
            ppg_reference_time = utils.get_updated_timestamp(ppg_reference_time, ppg_last_ts, ppg_timestamp)
            adxl_reference_time = utils.get_updated_timestamp(adxl_reference_time, adxl_last_ts, adxl_timestamp)
            self._packet["payload"]["stream_data"][i]["ppg_timestamp"] = ppg_reference_time * 1000
            self._packet["payload"]["stream_data"][i]["adxl_timestamp"] = adxl_reference_time * 1000
            last_timestamp[0] = ppg_reference_time
            last_timestamp[1] = ppg_timestamp
            last_timestamp[2] = adxl_reference_time
            last_timestamp[3] = adxl_timestamp


class SQIDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.SQI: ['0xC8', '0x0D']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x19',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 0,
                'sqi': 2.537532566293521e-07,
                'sqi_slot': 42405,
                'algo_status': 0,
                'timestamp': 1786433199,
                'reserved': 0
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["sqi"] = {"size": 4}
        self._config["payload"]["sqi_slot"] = {"size": 2, "join": True}
        self._config["payload"]["algo_status"] = {"size": 2, "join": True}
        self._config["payload"]["timestamp"] = {"size": 4, "join": True}
        self._config["payload"]["reserved"] = {"size": 1, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["sqi"] = struct.unpack("f", bytes(self._packet["payload"]["sqi"]))[0]

    def update_timestamp(self, last_timestamp):
        reference_time, last_ts = last_timestamp
        timestamp = self._packet["payload"]["timestamp"]
        reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
        self._packet["payload"]["timestamp"] = reference_time * 1000
        last_timestamp[0] = reference_time
        last_timestamp[1] = timestamp


class BCMDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Stream.BCM: ['0xC4', '0x07']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x41',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.STREAM_DATA: ['0x28']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'sequence_number': 1,
                'data_type': 0,
                'stream_data': [
                    {
                        'timestamp': 1788107093,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 82
                    },
                    {
                        'timestamp': 1788114863,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 5
                    },
                    {
                        'timestamp': 1788122630,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 8
                    },
                    {
                        'timestamp': 1788130399,
                        'real': 0,
                        'imaginary': 0,
                        'frequency_index': 54
                    }
                ]
            }
        }
    """

    def __init__(self):
        super().__init__()
        self._config["payload"]["sequence_number"] = {"size": 2, "join": True}
        self._config["payload"]["data_type"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp1"] = {"size": 4, "join": True}
        self._config["payload"]["real1"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["imaginary1"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["frequency_index1"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp2"] = {"size": 4, "join": True}
        self._config["payload"]["real2"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["imaginary2"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["frequency_index2"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp3"] = {"size": 4, "join": True}
        self._config["payload"]["real3"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["imaginary3"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["frequency_index3"] = {"size": 1, "join": True}
        self._config["payload"]["timestamp4"] = {"size": 4, "join": True}
        self._config["payload"]["real4"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["imaginary4"] = {"size": 4, "join": True, "signed": True}
        self._config["payload"]["frequency_index4"] = {"size": 1, "join": True}

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_data"] = []
        for i in range(1, 5):
            timestamp = self._packet["payload"][f"timestamp{i}"]
            data = {"timestamp": timestamp,
                    "real": self._packet["payload"][f"real{i}"],
                    "imaginary": self._packet["payload"][f"imaginary{i}"],
                    "frequency_index": self._packet["payload"][f"frequency_index{i}"]}
            [self._packet["payload"].pop(key) for key in
             [f"timestamp{i}", f"real{i}", f"imaginary{i}", f"frequency_index{i}"]]
            self._packet["payload"]["stream_data"].append(data)

    def update_timestamp(self, last_timestamp):
        for i in range(len(self._packet["payload"]["stream_data"])):
            reference_time, last_ts = last_timestamp
            timestamp = self._packet["payload"]["stream_data"][i]["timestamp"]
            reference_time = utils.get_updated_timestamp(reference_time, last_ts, timestamp)
            self._packet["payload"]["stream_data"][i]["timestamp"] = reference_time * 1000
            last_timestamp[0] = reference_time
            last_timestamp[1] = timestamp


class KeyStreamDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.DISPLAY: ['0xC5', '0x03']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xB',
                'checksum': '0x0'
            },
            'payload': {
                'command': <DisplayCommand.KEY_STREAM_DATA: ['0x48']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'key_code': 18
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["key_code"] = {"size": 1, "join": True}

    def update_timestamp(self, last_timestamp):
        pass


class CapSenseStreamDataPacket(CommandPacket):
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
                'command': <PMCommand.CAP_SENSE_STREAM_DATA: ['0x82']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'position': 1,
                'value': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["position"] = {"size": 1, "join": True}
        self._config["payload"]["value"] = {"size": 1, "join": True}

    def update_timestamp(self, last_timestamp):
        pass
