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
from ..enums.common_enums import Stream
from .command_packet import CommandPacket
from ..enums.fs_enums import FileType, FSCommand, FSLogging, FSSubState


class BadBlockPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xE',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.GET_BAD_BLOCKS_RES: ['0x7F']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'bad_blocks': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["bad_blocks"] = {"size": 4, "join": True}
        self._packet["payload"]["bad_blocks"] = [0x00] * 4


class DebugInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x2A',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.GET_DEBUG_INFO_RES: ['0x89']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'head_pointer': 374,
                'tail_pointer': 4,
                'usb_avg_tx_time': 0,
                'usb_avg_port_write_time': 0,
                'page_read_time': 0,
                'page_write_time': 1
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["head_pointer"] = {"size": 4, "join": True}
        self._config["payload"]["tail_pointer"] = {"size": 4, "join": True}
        self._config["payload"]["usb_avg_tx_time"] = {"size": 4, "join": True}
        self._config["payload"]["usb_avg_port_write_time"] = {"size": 4, "join": True}
        self._config["payload"]["page_read_time"] = {"size": 4, "join": True}
        self._config["payload"]["init_circular_buffer_flag"] = {"size": 2, "join": True}
        self._config["payload"]["mem_full_flag"] = {"size": 2, "join": True}
        self._config["payload"]["data_offset"] = {"size": 2, "join": True}
        self._config["payload"]["config_file_occupied"] = {"size": 2, "join": True}
        self._config["payload"]["page_write_time"] = {"size": 4, "join": True}


class FileCountPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xC',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.GET_NUMBER_OF_FILE_RES: ['0x71']>,
                'status': <CommonStatus.OK: ['0x00']>,
                'file_count': 2
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["file_count"] = {"size": 2, "join": True}


class KeyValuePairPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xA',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.SET_KEY_VALUE_PAIR_RES: ['0x65']>,
                'status': <FSStatus.OK: ['0x41']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)

    def set_value_id(self, value_id):
        self._packet["payload"]["value_id"] = value_id


class LSPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x37',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.LS_RES: ['0x49']>,
                'status': <FSStatus.OK: ['0x41']>,
                'filename': '03043B06.LOG',
                'filetype': <FileType.DATA_FILE: ['0x01']>,
                'file_size': 160309
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["filename"] = {"size": 40}
        self._config["payload"]["filetype"] = {"size": 1}
        self._config["payload"]["file_size"] = {"size": 4, "join": True}
        self._packet["payload"]["dir_path"] = [0x01, 0x01]

    def set_dir_path(self, dir_path):
        self._packet["payload"]["dir_path"] = dir_path

    def decode_packet(self, data):
        super().decode_packet(data)
        del self._packet["payload"]["dir_path"]
        full_filename = ""
        for s in self._packet["payload"]["filename"]:
            if not int(s):
                break
            full_filename += chr(s)
        self._packet["payload"]["filename"] = full_filename
        self._packet["payload"]["filetype"] = FileType(self._packet["payload"]["filetype"])


class StreamDebugInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x26',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.STREAM_DEBUG_INFO_RES: ['0x57']>,
                'status': <FSStatus.OK: ['0x41']>,
                'stream_address': <Stream.ADXL: ['0xC2', '0x02']>,
                'packets_received': 0,
                'packets_missed': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_address"] = {"size": 2}
        self._config["payload"]["packets_received"] = {"size": 4, "join": True}
        self._config["payload"]["packets_missed"] = {"size": 4, "join": True}
        self._config["payload"]["last_page_read"] = {"size": 4, "join": True}
        self._config["payload"]["last_page_read_offset"] = {"size": 4, "join": True}
        self._config["payload"]["last_page_read_status"] = {"size": 1, "join": True}
        self._config["payload"]["num_bytes_transferred"] = {"size": 4, "join": True}
        self._config["payload"]["bytes_read"] = {"size": 4, "join": True}
        self._config["payload"]["usb_cdc_write_failed"] = {"size": 1, "join": True}
        self._packet["payload"]["stream_address"] = [0x00, 0x00]
        self._packet["payload"]["packets_received"] = [0x00] * 4
        self._packet["payload"]["packets_missed"] = [0x00] * 4

    def set_stream_address(self, stream_address):
        self._packet["payload"]["stream_address"] = list(reversed(stream_address.value))

    def decode_packet(self, data):
        super().decode_packet(data)
        stream_address = list(reversed(self._packet["payload"]["stream_address"]))
        self._packet["payload"]["stream_address"] = Stream(stream_address)


class StreamFileChunkPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x20E',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.CHUNK_RETRANSMIT_RES: ['0x85']>,
                'status': <FSStatus.OK: ['0x41']>,
                'stream_length': 9,
                'byte_stream': [ 0, 195, 0, ... , 0, 0, 0, 0, 0, 0, 0 ],
                'crc16': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_length"] = {"size": 2, "join": True}
        self._config["payload"]["byte_stream"] = {"size": 512}
        self._config["payload"]["crc16"] = {"size": 2, "join": True}

    def set_chunk_detail(self, rollover, chunk_number, filename):
        self._packet["payload"]["roll_over"] = rollover
        self._packet["payload"]["chunk_number"] = chunk_number
        self._packet["payload"]["filename"] = filename


class StreamFilePacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x20E',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.DOWNLOAD_LOG_RES: ['0x7B']>,
                'status': <FSStatus.OK: ['0x41']>,
                'stream_length': 9,
                'byte_stream': [ 0, 195, 0, ... , 0, 0, 0, 0, 0, 0, 0 ],
                'crc16': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_length"] = {"size": 2, "join": True}
        self._config["payload"]["byte_stream"] = {"size": 512}
        self._config["payload"]["crc16"] = {"size": 2, "join": True}

    def set_filename(self, filename):
        self._packet["payload"]["file_name"] = filename


class FSStreamStatusPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xD',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.GET_STREAM_SUB_STATUS_RES: ['0x53']>,
                'status': <FSStatus.OK: ['0x41']>,
                'stream_address': <Stream.ADXL: ['0xC2', '0x02']>,
                'sub_state': 0
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["stream_address"] = {"size": 2}
        self._config["payload"]["sub_state"] = {"size": 1}
        self._packet["payload"]["stream_address"] = [0x00, 0x00]

    def set_stream_address(self, stream_address):
        self._packet["payload"]["stream_address"] = list(reversed(stream_address.value))

    def decode_packet(self, data):
        super().decode_packet(data)
        self._packet["payload"]["stream_address"] = Stream(list(reversed(self._packet["payload"]["stream_address"])))
        self._packet["payload"]["sub_state"] = FSSubState(list(reversed(self._packet["payload"]["sub_state"])))


class VolumeInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x14',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.VOL_INFO_RES: ['0x4F']>,
                'status': <FSStatus.OK: ['0x41']>,
                'total_memory': 536870656,
                'used_memory': 487424,
                'available_memory': 99
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["total_memory"] = {"size": 4, "join": True}
        self._config["payload"]["used_memory"] = {"size": 4, "join": True}
        self._config["payload"]["available_memory"] = {"size": 2, "join": True}


class ConfigFilePacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["length"] = {"size": 2, "join": True}
        self._config["payload"]["bytes"] = {"size": 70}

    def set_bytes(self, byte):
        self._packet["payload"]["length"] = utils.split_int_in_bytes(len(byte), length=2)
        self._packet["payload"]["bytes"] = byte

    def set_status(self, status):
        self._packet["payload"]["status"] = status


class PatternWritePacket(CommandPacket):

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)

    def set_pattern_data(self, file_size, scale_type, scale_factor, num_files_to_write):
        self._packet["payload"]["file_size"] = file_size
        self._packet["payload"]["scale_type"] = scale_type
        self._packet["payload"]["scale_factor"] = scale_factor
        self._packet["payload"]["num_files_to_write"] = num_files_to_write


class LoggingPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0xA',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.START_LOGGING_RES: ['0x77']>,
                'status': <FSStatus.OK: ['0x41']>
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)

    def set_logging_type(self, logging_type):
        self._packet["payload"]["logging_type"] = logging_type.value

    def decode_packet(self, data):
        super().decode_packet(data)
        if self._packet["payload"]["command"] == FSCommand.STOP_LOGGING_RES:
            self._packet["payload"]["stop_type"] = FSLogging(data[10:])


class FileInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x26',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.GET_FILE_INFO_RES: ['0x8D']>,
                'status': <FSStatus.OK: ['0x41']>,
                'filename': '03123EBD.LOG',
                'start_page': 375,
                'end_page': 375,
                'file_size': 426
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["filename"] = {"size": 16}
        self._config["payload"]["start_page"] = {"size": 4, "join": True}
        self._config["payload"]["end_page"] = {"size": 4, "join": True}
        self._config["payload"]["file_size"] = {"size": 4, "join": True}

    def set_file_index(self, file_index):
        self._packet["payload"]["file_index"] = [file_index]

    def decode_packet(self, data):
        super().decode_packet(data)
        full_filename = ""
        for s in self._packet["payload"]["filename"]:
            if not int(s):
                break
            full_filename += chr(s)
        self._packet["payload"]["filename"] = full_filename


class PageInfoPacket(CommandPacket):
    """
    Packet Structure:

    .. code-block::

        {
            'header': {
                'source': <Application.FS: ['0xC5', '0x01']>,
                'destination': <Application.APP_USB: ['0xC7', '0x05']>,
                'length': '0x7A',
                'checksum': '0x0'
            },
            'payload': {
                'command': <FSCommand.PAGE_READ_TEST_RES: ['0x8F']>,
                'status': <FSStatus.OK: ['0x41']>,
                'page_num': 300,
                'ecc_zone_status': 0,
                'next_page': 301,
                'occupied': 1,
                'data_region_status': 0,
                'sample_data': [ 4, 0, 74, 71, 104, 6, 75, 126, 4, 0 ],
                'num_bytes': 10
            }
        }
    """

    def __init__(self, destination=None, command=None):
        super().__init__(destination, command)
        self._config["payload"]["page_num"] = {"size": 4, "join": True}
        self._config["payload"]["ecc_zone_status"] = {"size": 1, "join": True}
        self._config["payload"]["next_page"] = {"size": 4, "join": True}
        self._config["payload"]["occupied"] = {"size": 1, "join": True}
        self._config["payload"]["data_region_status"] = {"size": 1, "join": True}
        self._config["payload"]["sample_data"] = {"size": 100}
        self._config["payload"]["num_bytes"] = {"size": 1, "join": True}
        self._packet["payload"]["page_num"] = [0x00] * 4
        self._packet["payload"]["num_bytes"] = [0x00]

    def set_page_num(self, page_num):
        self._packet["payload"]["page_num"] = page_num

    def set_num_bytes(self, num_bytes):
        self._packet["payload"]["num_bytes"] = [num_bytes]

    def decode_packet(self, data):
        super().decode_packet(data)
        sample_data = self._packet["payload"]["sample_data"][:self._packet["payload"]["num_bytes"]]
        self._packet["payload"]["sample_data"] = sample_data
