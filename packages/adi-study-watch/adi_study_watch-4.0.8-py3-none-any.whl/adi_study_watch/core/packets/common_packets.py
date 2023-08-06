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
from ..enums.bcm_enums import BCMDFTWindow
from ..enums.eda_enums import EDADFTWindow
from ..enums.common_enums import Stream, Application
from ..enums.adpd_enums import ADPDCommand, ADPDSlot, ADPDAppID


class DCBPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.AD7156: ['0xC8', '0x0B']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x5C',
                'checksum': '0x0'
            },
            'payload': {
                'command': <DCBCommand.READ_CONFIG_RES: ['0x98']>,
                'status': <DCBStatus.OK: ['0x97']>,
                'size': 2,
                'dcb_data': [
                    [ '0x1F', '0xFF' ],
                    [ '0x0', '0x7' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = {"size": 2, "join": True}
        self._config["payload"]["dcb_data"] = {"size": 8}
        self._packet["payload"]["size"] = [0x00, 0x00]
        self._packet["payload"]["dcb_data"] = [0x00] * 8

    def set_size(self, size):
        self._packet["payload"]["size"] = size

    def set_dcb_data_size(self, size):
        self._packet["payload"]["dcb_data"] = [0x00, 0x00, 0x00, 0x00] * size

    def set_dcb_write_data(self, dcb_data, dcb_size, num_ops):
        dcb_data_array = []
        if self._packet["header"]["destination"] == Application.PPG.value:
            dcb_data_array = utils.split_int_in_bytes(0, length=dcb_size * 4)
            for i in range(num_ops):
                start_index = i * 4
                dcb_data_array[start_index: start_index + 4] = utils.split_int_in_bytes(dcb_data[i], length=4)
        elif self._packet["header"]["destination"] in [Application.ADXL.value, Application.AD7156.value,
                                                       Application.PM.value]:
            dcb_data_array = utils.split_int_in_bytes(0, length=dcb_size * 4)
            for i in range(num_ops):
                start_index = i * 4
                dcb_data_array[start_index] = dcb_data[i][1]
                dcb_data_array[start_index + 1] = dcb_data[i][0]
        elif self._packet["header"]["destination"] == Application.ADPD.value:
            dcb_data_array = utils.split_int_in_bytes(0, length=(dcb_size * 4))
            for i in range(num_ops):
                start_index = i * 4
                dcb_data_array[start_index: start_index + 2] = utils.split_int_in_bytes(dcb_data[i][1], length=2)
                dcb_data_array[start_index + 2: start_index + 4] = utils.split_int_in_bytes(dcb_data[i][0], length=2)
        elif self._packet["header"]["destination"] == Application.LT_APP.value:
            dcb_data_array = dcb_data
        elif self._packet["header"]["destination"] in [Application.ECG.value, Application.EDA.value,
                                                       Application.BCM.value]:
            dcb_data_array = utils.split_int_in_bytes(0, length=dcb_size * 4)
            for i in range(num_ops):
                start_index = i * 4
                dcb_data_array[start_index: start_index + 2] = utils.split_int_in_bytes(dcb_data[i][1], length=2)
                dcb_data_array[start_index + 2] = dcb_data[i][0]
        self._packet["payload"]["dcb_data"] = dcb_data_array

    def decode_packet(self, data):
        super().decode_packet(data)
        dcb_data = data[12:]
        size = self._packet["payload"]["size"]
        result = []
        if self._packet["header"]["source"] == Application.PPG:
            for i in range(size):
                start_index = i * 4
                dcb_value = utils.join_multi_length_packets(dcb_data[start_index: start_index + 4], convert_to_hex=True)
                result.append([i, dcb_value])
        elif self._packet["header"]["source"] in [Application.ADXL, Application.AD7156, Application.PM]:
            for i in range(size):
                i = i * 4
                dcb_value = utils.join_multi_length_packets(dcb_data[i: i + 1], convert_to_hex=True)
                dcb_address = utils.join_multi_length_packets(dcb_data[i + 1: i + 2], convert_to_hex=True)
                result.append([dcb_address, dcb_value])
        elif self._packet["header"]["source"] == Application.ADPD:
            self._packet["payload"]["num_of_packets"] = utils.join_multi_length_packets(data[12:14])
            dcb_data = data[14:]
            for i in range(size):
                i = i * 4
                dcb_value = utils.join_multi_length_packets(dcb_data[i: i + 2], convert_to_hex=True)
                dcb_address = utils.join_multi_length_packets(dcb_data[i + 2: i + 4], convert_to_hex=True)
                result.append([dcb_address, dcb_value])
        elif self._packet["header"]["source"] == Application.LT_APP:
            self._packet["payload"]["num_of_packets"] = utils.join_multi_length_packets(data[12:14])
            result = data[14:]
        elif self._packet["header"]["source"] in [Application.ECG, Application.EDA, Application.BCM]:
            for i in range(size):
                i = i * 4
                dcb_value = utils.join_multi_length_packets(dcb_data[i: i + 2], convert_to_hex=True)
                dcb_address = utils.join_multi_length_packets(dcb_data[i + 2: i + 3], convert_to_hex=True)
                result.append([dcb_address, dcb_value])

        self._packet["payload"]["dcb_data"] = result


class DCFGPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xF0',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.GET_DCFG_RES: ['0x26']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 57,
                'num_tx_packets': 1,
                'data': [
                    [ '0x9', '0x9C' ],
                    [ '0x7', '0x8FFF' ],
                    [ '0xB', '0x322' ],
                            ...
                    [ '0x1B5', '0x0' ],
                    [ '0x1B6', '0x0' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = {"size": 1, "join": True}
        self._config["payload"]["num_tx_packets"] = {"size": 1, "join": True}
        self._config["payload"]["dcfg_data"] = {"size": -1}

    def decode_packet(self, data):
        super().decode_packet(data)
        address_value_data = self._packet["payload"]["dcfg_data"]
        num_ops = self._packet["payload"]["size"]
        data = []
        if self._packet["header"]["source"] in [Application.TEMPERATURE, Application.ADPD]:
            for i in range(num_ops):
                start_index = i * 4
                value_data = address_value_data[start_index:start_index + 2]
                value = utils.join_multi_length_packets(value_data, convert_to_hex=True)
                address_data = address_value_data[start_index + 2:start_index + 4]
                address = utils.join_multi_length_packets(address_data, convert_to_hex=True)
                data.append([address, value])
        else:
            for i in range(num_ops):
                start_index = i * 2
                value_data = address_value_data[start_index:start_index + 1]
                value = utils.join_multi_length_packets(value_data, convert_to_hex=True)
                address_data = address_value_data[start_index + 1:start_index + 2]
                address = utils.join_multi_length_packets(address_data, convert_to_hex=True)
                data.append([address, value])
        self._packet["payload"]["data"] = data
        del self._packet["payload"]["dcfg_data"]


class DecimationFactorPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xD',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.GET_STREAM_DEC_FACTOR_RES: ['0x2A']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'stream_address': <Stream.ADPD6: ['0xC2', '0x16']>,
                'decimation_factor': 1
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_address"] = {"size": 2}
        self._config["payload"]["decimation_factor"] = {"size": 1, "join": True}
        self._packet["payload"]["stream_address"] = [0x00, 0x00]
        self._packet["payload"]["decimation_factor"] = [0x00]

    def set_decimation_factor(self, decimation_factor):
        self._packet["payload"]["decimation_factor"] = decimation_factor

    def set_stream_address(self, stream):
        self._packet["payload"]["stream_address"] = list(reversed(stream.value))

    def decode_packet(self, data):
        super().decode_packet(data)
        stream_address = self._packet["payload"]["stream_address"]
        self._packet["payload"]["stream_address"] = Stream(list(reversed(stream_address)))


class LibraryConfigDataPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PPG: ['0xC3', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xDF',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.GET_LCFG_RES: ['0x13']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'size': 53,
                'lcfg_data': [
                    [ 0, '0x0' ],
                    [ 1, '0x0' ],
                        ...
                    [ 52, '0x0' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["size"] = {"size": 1, "join": True}
        self._config["payload"]["lcfg_data"] = {"size": -1}
        self._packet["payload"]["size"] = [0x00]
        self._packet["payload"]["lcfg_data"] = [0x00] * (4 * 53)

    def decode_packet(self, data):
        super().decode_packet(data)
        size = self._packet["payload"]["size"]
        lcfg_data = self._packet["payload"]["lcfg_data"]
        data = []
        for i in range(size):
            start_index = i * 4
            value = utils.join_multi_length_packets(lcfg_data[start_index:start_index + 4], convert_to_hex=True)
            data.append([i, value])
        self._packet["payload"]["lcfg_data"] = data


class SetLibraryConfigPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.PPG: ['0xC3', '0x00']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xA',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.SET_LCFG_RES: ['0x15']>,
                'status': <CommonStatus.OK: ['0x00']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)

    def set_lcfg_id(self, lcfg_id):
        self._packet["payload"]["lcfg_id"] = lcfg_id


class LibraryConfigReadWritePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xE',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.READ_LCFG_RES: ['0x17']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'num_ops': 1,
                'data': [
                    [ '0x0', '0x12C' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["num_ops"] = {"size": 1, "join": True}
        self._packet["payload"]["num_ops"] = [0x01]
        self._packet["payload"]["data"] = [0x00, 0x00, 0x00, 0x00, 0x00]

    def set_number_of_operations(self, num_ops):
        self._packet["payload"]["num_ops"] = [num_ops]

    def set_write_fields_data(self, data):
        num_ops = len(data)
        if self._packet["header"]["destination"] in [Application.ECG.value, Application.ADPD.value,
                                                     Application.LT_APP.value]:
            fields_array = utils.split_int_in_bytes(0, length=num_ops * 3)
            for i in range(num_ops):
                start_index = i * 3
                fields_array[start_index] = data[i][0]
                fields_array[start_index + 1: start_index + 3] = utils.split_int_in_bytes(data[i][1], length=2)
            self._packet["payload"]["data"] = fields_array
        else:
            fields_array = utils.split_int_in_bytes(0, length=num_ops * 5)
            for i in range(num_ops):
                start_index = i * 5
                fields_array[start_index] = data[i][0]
                fields_array[start_index + 1: start_index + 5] = utils.split_int_in_bytes(data[i][1], length=4)
            self._packet["payload"]["data"] = fields_array

    def set_read_fields_data(self, data):
        num_ops = len(data)
        if self._packet["header"]["destination"] in [Application.ECG.value, Application.ADPD.value,
                                                     Application.LT_APP.value]:
            fields_array = utils.split_int_in_bytes(0, length=num_ops * 3)
            for i in range(num_ops):
                start_index = i * 3
                fields_array[start_index] = data[i]
            self._packet["payload"]["data"] = fields_array
        else:
            fields_array = utils.split_int_in_bytes(0, length=num_ops * 5)
            for i in range(num_ops):
                start_index = i * 5
                fields_array[start_index] = data[i]
            self._packet["payload"]["data"] = fields_array

    def decode_packet(self, data):
        super().decode_packet(data)
        num_ops = self._packet["payload"]["num_ops"]
        address_value_data = data[11:]
        data = []
        if self._packet["header"]["source"] in [Application.ECG, Application.ADPD, Application.LT_APP]:
            for i in range(num_ops):
                start_index = i * 3
                address_data = address_value_data[start_index:start_index + 1]
                address = utils.join_multi_length_packets(address_data, convert_to_hex=True)
                value_data = address_value_data[start_index + 1:start_index + 3]
                value = utils.join_multi_length_packets(value_data, convert_to_hex=True)
                data.append([address, value])
        else:
            for i in range(num_ops):
                start_index = i * 5
                address_data = address_value_data[start_index:start_index + 1]
                address = utils.join_multi_length_packets(address_data, convert_to_hex=True)
                value_data = address_value_data[start_index + 1:start_index + 5]
                value = utils.join_multi_length_packets(value_data, convert_to_hex=True)
                data.append([address, value])
        self._packet["payload"]["data"] = data


class RegisterPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x17',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.REGISTER_READ_RES: ['0x22']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'num_ops': 3,
                'data': [
                    [ '0x15', '0x6000' ],
                    [ '0x22', '0x83' ],
                    [ '0x2E', '0x0' ]
                ]
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["num_ops"] = {"size": 1, "join": True}
        self._config["payload"]["data"] = {"size": 2}
        self._packet["payload"]["num_ops"] = [0x01]
        self._packet["payload"]["data"] = [0x00, 0x00, 0x00, 0x00]

    def set_number_of_operations(self, num_ops):
        self._packet["payload"]["num_ops"] = [num_ops]

    def set_data(self, data):
        self._packet["payload"]["data"] = data

    def set_write_reg_data(self, data):
        num_ops = len(data)
        reg_array = utils.split_int_in_bytes(0, length=num_ops * 4)
        for i in range(num_ops):
            start_index = i * 4
            reg_array[start_index:start_index + 2] = utils.split_int_in_bytes(data[i][0], length=2)
            reg_array[start_index + 2:start_index + 4] = utils.split_int_in_bytes(data[i][1], length=2)
        self._packet["payload"]["data"] = reg_array

    def set_read_reg_data(self, data):
        num_ops = len(data)
        reg_array = utils.split_int_in_bytes(0, length=num_ops * 4)
        for i in range(num_ops):
            start_index = i * 4
            reg_array[start_index:start_index + 2] = utils.split_int_in_bytes(data[i], length=2)
        self._packet["payload"]["data"] = reg_array

    def decode_packet(self, data):
        super().decode_packet(data)
        num_ops = self._packet["payload"]["num_ops"]
        address_value_data = data[11:]
        data = []
        for i in range(num_ops):
            start_index = i * 4
            if self._packet["payload"]["command"] == ADPDCommand.CREATE_DCFG_RES:
                address_data = address_value_data[start_index:start_index + 2]
                address = ADPDSlot([utils.join_multi_length_packets(address_data)])
                value_data = address_value_data[start_index + 2:start_index + 4]
                value = ADPDAppID([utils.join_multi_length_packets(value_data)])
            else:
                address_data = address_value_data[start_index:start_index + 2]
                address = utils.join_multi_length_packets(address_data, convert_to_hex=True)
                value_data = address_value_data[start_index + 2:start_index + 4]
                value = utils.join_multi_length_packets(value_data, convert_to_hex=True)
            data.append([address, value])
        self._packet["payload"]["data"] = data


class StreamPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADXL: ['0xC1', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.SUBSCRIBE_STREAM_RES: ['0x0D']>,
                'status': <CommonStatus.SUBSCRIBER_ADDED: ['0x09']>,
                'stream_address': <Stream.ADXL: ['0xC2', '0x02']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_address"] = {"size": 2}
        self._packet["payload"]["stream_address"] = [0x00, 0x00]

    def set_stream_address(self, stream_address):
        self._packet["payload"]["stream_address"] = list(reversed(stream_address.value))

    def decode_packet(self, data):
        super().decode_packet(data)
        # if not self._packet["payload"]["stream_address"] == [0, 0]:
        stream_address = self._packet["payload"]["stream_address"]
        self._packet["payload"]["stream_address"] = Stream(list(reversed(stream_address)))


class StreamStatusPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADXL: ['0xC1', '0x02']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xE',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.GET_SENSOR_STATUS_RES: ['0x11']>,
                'status': <CommonStatus.STREAM_STOPPED: ['0x03']>,
                'stream_address': <Stream.ADXL: ['0xC2', '0x02']>,
                'num_subscribers': 0,
                'num_start_registered': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_address"] = {"size": 2}
        self._config["payload"]["num_subscribers"] = {"size": 1, "join": True}
        self._config["payload"]["num_start_registered"] = {"size": 1, "join": True}
        self._packet["payload"]["stream_address"] = [0x00, 0x00]
        self._packet["payload"]["num_subscribers"] = [0x00]
        self._packet["payload"]["num_start_registered"] = [0x00]

    def set_stream_address(self, stream_address):
        self._packet["payload"]["stream_address"] = list(reversed(stream_address.value))

    def decode_packet(self, data):
        super().decode_packet(data)
        if not self._packet["payload"]["stream_address"] == [0, 0]:
            stream_address = list(reversed(self._packet["payload"]["stream_address"]))
            self._packet["payload"]["stream_address"] = Stream(stream_address)


class VersionPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.ADPD: ['0xC1', '0x10']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x42',
                'checksum': '0x0'
            },
            'payload': {
                'command': <CommonCommand.GET_VERSION_RES: ['0x01']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'major_version': 0,
                'minor_version': 3,
                'patch_version': 1,
                'version_string': 'ADPD_App',
                'build_version': 'TEST ADPD4000_VERSION STRING'
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["major_version"] = {"size": 2, "join": True}
        self._config["payload"]["minor_version"] = {"size": 2, "join": True}
        self._config["payload"]["patch_version"] = {"size": 2, "join": True}
        self._config["payload"]["version_string"] = {"size": 10}
        self._config["payload"]["build_version"] = {"size": 40}

    def decode_packet(self, data):
        super().decode_packet(data)
        version_string = ""
        build_version = ""
        for s in self._packet["payload"]["version_string"]:
            if not int(s):
                break
            version_string += chr(s)
        for s in self._packet["payload"]["build_version"]:
            if not int(s):
                break
            build_version += chr(s)
        self._packet["payload"]["version_string"] = str(version_string).encode('utf8').decode("utf-8")
        self._packet["payload"]["build_version"] = build_version


class DFTPacket(CommandPacket):
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
                'command': <BCMCommand.SET_DFT_NUM_RES: ['0x47']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'dft_window': <BCMDFTWindow.DFT_WINDOW_16: ['0x00', '0x02']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["dft_window"] = {"size": 2}
        self._packet["payload"]["dft_window"] = [0x00]

    def set_dft_num(self, dft_window):
        self._packet["payload"]["dft_window"] = dft_window.value

    def decode_packet(self, data):
        super().decode_packet(data)
        if self._packet["header"]["source"] == Application.EDA:
            self._packet["payload"]["dft_window"] = EDADFTWindow(self._packet["payload"]["dft_window"])
        else:
            self._packet["payload"]["dft_window"] = BCMDFTWindow(self._packet["payload"]["dft_window"])
