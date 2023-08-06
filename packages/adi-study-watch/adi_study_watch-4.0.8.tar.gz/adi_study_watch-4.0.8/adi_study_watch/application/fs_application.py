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
import logging
from typing import List, Dict, Callable

from tqdm import tqdm

from ..core import utils
from .common_application import CommonApplication
from ..core.packets.common_packets import StreamPacket
from ..core.packets.command_packet import CommandPacket
from ..core.enums.common_enums import Application, Stream
from ..core.enums.fs_enums import FSCommand, FSStatus, FSLogging
from ..core.packets.fs_packets import LSPacket, FSStreamStatusPacket, StreamFilePacket, FileCountPacket, \
    ConfigFilePacket
from ..core.packets.fs_packets import StreamFileChunkPacket, KeyValuePairPacket, LoggingPacket, VolumeInfoPacket

logger = logging.getLogger(__name__)


class FSApplication(CommonApplication):
    """
    FS Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_fs_application()

    """

    STREAM_EDA = Stream.EDA
    STREAM_BCM = Stream.BCM
    STREAM_ECG = Stream.ECG
    STREAM_PPG = Stream.PPG
    STREAM_SQI = Stream.SQI
    STREAM_ADXL = Stream.ADXL
    STREAM_ADPD1 = Stream.ADPD1
    STREAM_ADPD2 = Stream.ADPD2
    STREAM_ADPD3 = Stream.ADPD3
    STREAM_ADPD4 = Stream.ADPD4
    STREAM_ADPD5 = Stream.ADPD5
    STREAM_ADPD6 = Stream.ADPD6
    STREAM_ADPD7 = Stream.ADPD7
    STREAM_ADPD8 = Stream.ADPD8
    STREAM_ADPD9 = Stream.ADPD9
    STREAM_ADPD10 = Stream.ADPD10
    STREAM_ADPD11 = Stream.ADPD11
    STREAM_ADPD12 = Stream.ADPD12
    STREAM_SYNC_PPG = Stream.SYNC_PPG
    STREAM_PEDOMETER = Stream.PEDOMETER
    STREAM_TEMPERATURE = Stream.TEMPERATURE

    def __init__(self, packet_manager):
        super().__init__(Application.FS, packet_manager)
        self._stream = Stream.FS
        self.stream_progress = 0
        self.total_size = 0
        self.file_stream_callback = None

    def _stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[13]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[13]

    def get_supported_streams(self) -> List[Stream]:
        """
        List all supported streams for FS.

        :return: Array of stream ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0xD']>]
        """
        return [self.STREAM_ADPD1, self.STREAM_ADPD2, self.STREAM_ADPD3, self.STREAM_ADPD4, self.STREAM_ADPD5,
                self.STREAM_ADPD6, self.STREAM_ADPD7, self.STREAM_ADPD8, self.STREAM_ADPD9, self.STREAM_ADPD10,
                self.STREAM_ADPD11, self.STREAM_ADPD12, self.STREAM_ADXL, self.STREAM_BCM, self.STREAM_ECG,
                self.STREAM_EDA, self.STREAM_PEDOMETER, self.STREAM_PPG, self.STREAM_TEMPERATURE, self.STREAM_SYNC_PPG,
                self.STREAM_SQI]

    def abort_logging(self) -> Dict:
        """
        Aborts all logging process.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.abort_logging()

        """
        packet = CommandPacket(self._destination, FSCommand.FORCE_STOP_LOG_REQ)
        return self._send_packet(packet, FSCommand.FORCE_STOP_LOG_RES)

    def delete_config_file(self) -> Dict:
        """
        Deletes config file.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.delete_config_file()

        """
        packet = CommandPacket(self._destination, FSCommand.DELETE_CONFIG_FILE_REQ)
        return self._send_packet(packet, FSCommand.DELETE_CONFIG_FILE_RES)

    def disable_config_log(self) -> Dict:
        """
        Disables config log.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.disable_config_log()

        """
        packet = CommandPacket(self._destination, FSCommand.DCFG_STOP_LOG_REQ)
        return self._send_packet(packet, FSCommand.DCFG_STOP_LOG_RES)

    def _write_config_file(self, commands) -> [Dict]:
        packet_size = 70
        packets = math.ceil(len(commands) / packet_size)
        packet_array = []
        for packet in range(packets):
            packet_array.append(commands[packet * packet_size:(packet + 1) * packet_size])
        result = []
        for i, byte in enumerate(packet_array):
            packet = ConfigFilePacket(self._destination, FSCommand.LOG_USER_CONFIG_DATA_REQ)
            packet.set_bytes(byte)
            if i + 1 == packets:
                packet.set_status(FSStatus.END_OF_FILE.value)
            else:
                packet.set_status(FSStatus.OK.value)
            result.append(self._send_packet(packet, FSCommand.LOG_USER_CONFIG_DATA_RES))
        return result

    def write_config_file(self, filename: str) -> [Dict]:
        """
        Writes user config file into FS.

        :param filename: file to write.
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.write_config_file("config.lcfg")
        """
        with open(filename, 'rb') as file:
            data = file.readlines()
            result = []
            for value in data:
                result += value
            return self._write_config_file(result)

    def stop_logging(self) -> Dict:
        """
        Stops current logging process.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.stop_logging()

        """
        packet = LoggingPacket(self._destination, FSCommand.STOP_LOGGING_REQ)
        packet.set_logging_type(FSLogging.STOP_LOGGING)
        return self._send_packet(packet, FSCommand.STOP_LOGGING_RES)

    def enable_config_log(self) -> Dict:
        """
        Enables config log.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.enable_config_log()

        """
        packet = CommandPacket(self._destination, FSCommand.DCFG_START_LOG_REQ)
        return self._send_packet(packet, FSCommand.DCFG_START_LOG_RES)

    def start_logging(self) -> Dict:
        """
        Starts current logging process.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.start_logging()

        """
        packet = LoggingPacket(self._destination, FSCommand.START_LOGGING_REQ)
        return self._send_packet(packet, FSCommand.START_LOGGING_RES)

    def get_file_count(self) -> Dict:
        """
        Returns a packet containing number of file present on the device.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_file_count()
            print(x["payload"]["file_count"])
            # 3
        """
        packet = FileCountPacket(self._destination, FSCommand.GET_NUMBER_OF_FILE_REQ)
        return self._send_packet(packet, FSCommand.GET_NUMBER_OF_FILE_RES)

    def format(self) -> Dict:
        """
        Format the entire file system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.format()

        """
        packet = CommandPacket(self._destination, FSCommand.FORMAT_REQ)
        return self._send_packet(packet, FSCommand.FORMAT_RES)

    def get_stream_status(self, stream: Stream) -> Dict:
        """
        Returns specified stream status information.

        :param stream: stream to obtain status information, use get_supported_streams() to list all supported streams.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0x0D']>]
            x = application.get_stream_status(application.STREAM_ADXL)
            print(x["payload"]["stream_address"], x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # Stream.ADXL 0 0
        """
        stream = self._stream_helper(stream)
        packet = FSStreamStatusPacket(self._destination, FSCommand.GET_STREAM_SUB_STATUS_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, FSCommand.GET_STREAM_SUB_STATUS_RES)

    def inject_key_value_pair(self, value_id: int) -> Dict:
        """
        Inject Key Value Pair into the log.

        :param value_id: Key Value pair to inject in log.
        :type value_id: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.inject_key_value_pair(1234)
            print(x["payload"]["status"])
            # FSStatus.OK
        """
        value_id = utils.range_and_type_check(value_id, type_of=int, num_bytes=16)
        value_id = utils.split_int_in_bytes(value_id, length=16)
        packet = KeyValuePairPacket(self._destination, FSCommand.SET_KEY_VALUE_PAIR_REQ)
        packet.set_value_id(value_id)
        return self._send_packet(packet, FSCommand.SET_KEY_VALUE_PAIR_RES)

    def ls(self) -> List[Dict]:
        """
        List all the files present on the device.

        :return: list of response packet as dictionary.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            files = application.ls()
            for file in files:
                print(file["payload"]["filename"], file["payload"]["filetype"], file["payload"]["file_size"])

            # 1216471B.LOG FileType.DATA_FILE 5242880
            # 121647E1.LOG FileType.DATA_FILE 477636
            # 121647ED.LOG FileType.DATA_FILE 140206

        """
        packet = LSPacket(self._destination, FSCommand.LS_REQ)
        packet_id = self._get_packet_id(FSCommand.LS_RES)
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        result = []
        while True:
            data = self._get_queue_data(queue)
            packet = LSPacket()
            packet.decode_packet(data)
            packet_dict = packet.get_dict()
            if not packet_dict["payload"]["status"] == FSStatus.OK:
                break
            result.append(packet_dict)
        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        return result

    def mount(self) -> Dict:
        """
        Mounts the File system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            application.mount()
        """
        packet = CommandPacket(self._destination, FSCommand.MOUNT_REQ)
        return self._send_packet(packet, FSCommand.MOUNT_RES)

    def get_status(self) -> Dict:
        """
        Returns current logging status.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_status()
            print(x["payload"]["status"])
            # FSStatus.LOGGING_IN_PROGRESS
        """
        packet = CommandPacket(self._destination, FSCommand.GET_STATUS_REQ)
        return self._send_packet(packet, FSCommand.GET_STATUS_RES)

    def stream_file(self, filename: str, file_stream_callback: Callable) -> None:
        """
        Stream specified file from the device.

        :param filename: filename to download, use ls() to obtain list of all files.
        :type filename: str
        :param file_stream_callback: callback for streaming file
        :type file_stream_callback: Callable

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            def file_callback(data, total_size, stream_progress):
                print(data)
                # [{'header': {'source': <Stream.FS: ['0xC6', '0x1']>, .. , 'crc16': 18166}}]


            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            # alternately yo can use download_file if you don't want to stream file content
            application.stream_file("1216471B.LOG", file_callback)

            # wait for stream to finish
            while True:
                pass

        """
        if self._packet_manager.source == Application.APP_BLE:
            logger.error(f"Can't stream file over BLE.")
            return
        files = self.ls()
        file_size = None
        for file in files:
            if file["payload"]["filename"] == filename.strip():
                file_size = file["payload"]["file_size"]

        if file_size is None:
            logger.error(f"{filename} is not present on the device, use ls() to list all the files.")
            return
        self.file_stream_callback = file_stream_callback
        filename = utils.range_and_type_check(filename, type_of=str)
        file_name_byte = [ord(char) for char in filename]
        packet = StreamFilePacket(self._destination, FSCommand.DOWNLOAD_LOG_REQ)
        packet.set_filename(file_name_byte)
        data_packet_id = self._get_packet_id(FSCommand.DOWNLOAD_LOG_RES, self._stream)
        self.stream_progress = 0
        self.total_size = file_size
        self._packet_manager.subscribe(data_packet_id, self._file_callback)
        self._packet_manager.send_packet(packet)

    def _file_callback(self, response_data, packet_id):
        response_packet = StreamFilePacket()
        response_packet.decode_packet(response_data)
        packet_dict = response_packet.get_dict()
        self.stream_progress += packet_dict["payload"]["stream_length"]
        if self.file_stream_callback:
            self.file_stream_callback(packet_dict, self.total_size, self.stream_progress)
        else:
            logger.error(f"No callback to stream file.")
        if not packet_dict["payload"]["status"] == FSStatus.OK:
            self._packet_manager.unsubscribe(8061382, self._file_callback)

    def download_file(self, filename: str, download_to_file: bool = False, display_progress: bool = False) \
            -> List[Dict]:
        """
        Download specified file from the device.

        :param filename: filename to download, use ls() to obtain list of all files.
        :type filename: str
        :param download_to_file: save the payload.data_stream to the file
        :type download_to_file: bool
        :param display_progress: display progress of download.
        :type display_progress: bool
        :return: list of response packet as dictionary.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.download_file("1216471B.LOG")
            print(x)
            # [{'header': {'source': <Stream.FS: ['0xC6', '0x1']>, .. , 'crc16': 18166}}]
        """
        if self._packet_manager.source == Application.APP_BLE:
            logger.error(f"Can't Download file over BLE.")
            return []
        files = self.ls()
        file_size = None
        for file in files:
            if file["payload"]["filename"] == filename.strip():
                file_size = file["payload"]["file_size"]

        if file_size is None:
            logger.error(f"{filename} is not present on the device, use ls() to list all the files.")
            return []
        filename = utils.range_and_type_check(filename, type_of=str)
        file_name_byte = [ord(char) for char in filename]
        packet = StreamFilePacket(self._destination, FSCommand.DOWNLOAD_LOG_REQ)
        packet.set_filename(file_name_byte)
        data_packet_id = self._get_packet_id(FSCommand.DOWNLOAD_LOG_RES, self._stream)
        self._packet_manager.subscribe(data_packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        queue = self._get_queue(data_packet_id)
        data = []
        progress_bar = None
        file_writer = None
        if download_to_file:
            try:
                file_writer = open(filename, 'wb')
            except Exception as e:
                logger.error(f"Can't open file {filename} with write binary permission, reason :: {e}.")
        if display_progress:
            progress_bar = tqdm(total=file_size)
        while True:
            response_data = self._get_queue_data(queue)
            packet = StreamFilePacket()
            packet.decode_packet(response_data)
            packet_dict = packet.get_dict()
            if display_progress:
                progress = packet_dict["payload"]["stream_length"]
                progress_bar.update(progress)
            if download_to_file:
                stream_length = packet_dict["payload"]["stream_length"]
                if not stream_length == len(packet_dict["payload"]["byte_stream"]):
                    file_writer.write(bytearray(packet_dict["payload"]["byte_stream"][:stream_length]))
                else:
                    file_writer.write(bytearray(packet_dict["payload"]["byte_stream"]))
            else:
                data.append(packet_dict)
            if not packet_dict["payload"]["status"] == FSStatus.OK:
                break
        if display_progress:
            progress_bar.close()
        if download_to_file:
            file_writer.close()
        self._packet_manager.unsubscribe(data_packet_id, self._callback_command)
        return data

    def download_file_chunk(self, filename: str, rollover: int, chunk_number: int) -> Dict:
        """
        Download specified chunk of file from the device.

        :param filename: filename to download, use ls() to obtain list of all files.
        :type filename: str
        :param rollover: rollover value for file.
        :type rollover: int
        :param chunk_number: chunk number for file.
        :type chunk_number: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.download_file_chunk(0, 50, "1216471B.LOG")
            print(x)
            # {'header': {'source': <Stream.FS: ['0xC6', '0x1']>, .. , 'crc16': 18166}}
        """
        rollover = utils.range_and_type_check(rollover, type_of=int, num_bytes=1)
        chunk_number = utils.range_and_type_check(chunk_number, type_of=int, num_bytes=2)
        filename = utils.range_and_type_check(filename, type_of=str)
        chunk_number = utils.split_int_in_bytes(chunk_number, length=2)
        file_name_byte = []
        for char in filename:
            file_name_byte.append(ord(char))
        packet = StreamFileChunkPacket(self._destination, FSCommand.CHUNK_RETRANSMIT_REQ)
        packet.set_chunk_detail([rollover], chunk_number, file_name_byte)
        return self._send_packet(packet, FSCommand.CHUNK_RETRANSMIT_RES)

    def subscribe_stream(self, stream: Stream) -> Dict:
        """
        Subscribe to the specified stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0xD']>]
            x = application.subscribe_stream(application.STREAM_ADXL)
            print(x["payload"]["status"], x["payload"]["stream_address"])
            # CommonStatus.SUBSCRIBER_ADDED Stream.ADXL
        """
        stream = self._stream_helper(stream)
        packet = StreamPacket(self._destination, FSCommand.START_STREAM_LOGGING_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, FSCommand.START_STREAM_LOGGING_RES)

    def unsubscribe_stream(self, stream: Stream) -> Dict:
        """
        UnSubscribe to the specified stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0xD']>]
            x = application.unsubscribe_stream(application.STREAM_ADXL)
            print(x["payload"]["status"], x["payload"]["stream_address"])
            # CommonStatus.SUBSCRIBER_COUNT_DECREMENT Stream.ADXL
        """
        stream = self._stream_helper(stream)
        packet = StreamPacket(self._destination, FSCommand.STOP_STREAM_LOGGING_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, FSCommand.STOP_STREAM_LOGGING_RES)

    def volume_info(self) -> Dict:
        """
        Returns file system volume information.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_fs_application()
            x = application.volume_info()
            print(f'{x["payload"]["total_memory"]}, {x["payload"]["used_memory"]}, {x["payload"]["available_memory"]}%')
            # 536870656, 6197248, 98%
        """
        packet = VolumeInfoPacket(self._destination, FSCommand.VOL_INFO_REQ)
        return self._send_packet(packet, FSCommand.VOL_INFO_RES)

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
            application = sdk.get_fs_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)
