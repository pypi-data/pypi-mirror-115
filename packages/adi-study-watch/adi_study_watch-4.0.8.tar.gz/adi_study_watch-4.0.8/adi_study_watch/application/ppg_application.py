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

import logging
from datetime import datetime
from typing import Dict, List, Callable, Tuple

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.enums.ppg_enums import PPGLcfgId, PPGCommand
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.stream_data_packets import PPGDataPacket, SYNCPPGDataPacket
from ..core.packets.common_packets import LibraryConfigDataPacket, LibraryConfigReadWritePacket
from ..core.packets.common_packets import DCBPacket, SetLibraryConfigPacket, StreamPacket, VersionPacket

logger = logging.getLogger(__name__)


class PPGApplication(CommonStream):
    """
    PPG Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_ppg_application()

    """

    LCFG_ID_ADPD107 = PPGLcfgId.LCFG_ID_ADPD107
    LCFG_ID_ADPD185 = PPGLcfgId.LCFG_ID_ADPD185
    LCFG_ID_ADPD108 = PPGLcfgId.LCFG_ID_ADPD108
    LCFG_ID_ADPD188 = PPGLcfgId.LCFG_ID_ADPD188
    LCFG_ID_ADPD4000 = PPGLcfgId.LCFG_ID_ADPD4000

    PPG = Stream.PPG
    SYNC_PPG = Stream.SYNC_PPG

    def __init__(self, callback_ppg, callback_syncppg, packet_manager, args_ppg, args_syncppg):
        super().__init__(Application.PPG, Stream.PPG, packet_manager, callback_ppg, args_ppg)
        self._callback_ppg_function = callback_ppg
        self._callback_syncppg_function = callback_syncppg
        self._ppg_stream = Stream.PPG
        self._syncppg_stream = Stream.SYNC_PPG
        self._args_ppg = args_ppg
        self._args_syncppg = args_syncppg
        self._csv_logger[Stream.PPG] = None
        self._csv_logger[Stream.SYNC_PPG] = None
        self._last_timestamp_syncppg = []
        self._last_timestamp_ppg = []
        self._dcb_size = 53

    def _callback_ppg(self, packet, packet_id):
        """
        PPG Callback.
        """
        self._callback_data_helper(packet, packet_id, PPGDataPacket(), self._callback_ppg_function, self._args_ppg,
                                   self._last_timestamp_ppg)

    def _callback_syncppg(self, packet, packet_id):
        """
        SYNC PPG Callback
        """
        self._callback_data_helper(packet, packet_id, SYNCPPGDataPacket(), self._callback_syncppg_function,
                                   self._args_syncppg, self._last_timestamp_syncppg)

    def _lcfg_id_helper(self, lcfg_id: PPGLcfgId) -> PPGLcfgId:
        """
        Confirms lcfg_id is from list of Enums.
        """
        if lcfg_id in self.get_supported_lcfg_ids():
            return lcfg_id
        else:
            logger.warning(
                f"{lcfg_id} is not supported Lcfg ID, choosing {self.get_supported_lcfg_ids()[0]} "
                f"as default Lcfg ID. use get_supported_lcfg_ids() to know all supported Lcfg IDs.")
            return self.get_supported_lcfg_ids()[0]

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes PPG Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def get_library_configuration(self) -> Dict:
        """
        Returns entire library configuration PPG.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_library_configuration()
            print(x["payload"]["lcfg_data"])
            # [192, 0, 0, 0, 32, 0, 0, 0, 1, 0, ... , 0,0,0]

        """
        packet = LibraryConfigDataPacket(self._destination, CommonCommand.GET_LCFG_REQ)
        return self._send_packet(packet, CommonCommand.GET_LCFG_RES)

    def get_sensor_status(self) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_sensor_status()
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0

        """
        return super().get_sensor_status()

    def get_supported_lcfg_ids(self) -> List[PPGLcfgId]:
        """
        List all supported lcfg ID for PPG.

        :return: Array of lcfg ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_supported_lcfg_ids()
            print(x)
            # [<PPGLcfgId.LCFG_ID_ADPD107: ['0x6B']>, ... , <PPGLcfgId.LCFG_ID_ADPD4000: ['0x28']>]
        """
        return [self.LCFG_ID_ADPD107, self.LCFG_ID_ADPD185, self.LCFG_ID_ADPD108, self.LCFG_ID_ADPD188,
                self.LCFG_ID_ADPD4000]

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
            # []

        """
        packet = DCBPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.READ_CONFIG_RES)

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
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]

        """
        address_range = [0x00, 0x34]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.READ_LCFG_REQ)
        packet.set_number_of_operations(len(fields))
        utils.check_array_address_range(fields, address_range, 1)
        packet.set_read_fields_data(fields)
        return self._send_packet(packet, CommonCommand.READ_LCFG_RES)

    def set_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream PPG data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2))

        """
        super().set_callback(callback_function, args)

    def set_library_configuration(self, lcfg_id: PPGLcfgId) -> Dict:
        """
        Set PPG to specified library configuration.

        :param lcfg_id: PPG lcfg_id to set, use get_supported_lcfg_ids() to list all supported lcfg IDs
        :type lcfg_id: PPGLcfgId
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.set_library_configuration(application.LCFG_ID_ADPD4000)
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        lcfg_id = self._lcfg_id_helper(lcfg_id)
        packet = SetLibraryConfigPacket(self._destination, CommonCommand.SET_LCFG_REQ)
        packet.set_lcfg_id(lcfg_id.value)
        return self._send_packet(packet, CommonCommand.SET_LCFG_RES)

    def set_ppg_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream PPG data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_ppg_callback(callback, args=(optional_arg1, optional_arg2))

        """
        self._callback_ppg_function = callback_function
        self._args = args

    def set_syncppg_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream SYNC PPG data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_syncppg_callback(callback, args=(optional_arg1, optional_arg2))

        """
        self._callback_syncppg_function = callback_function
        self._args = args

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
            application = sdk.get_ppg_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Starts PPG sensor and also subscribe to the PPG stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        return super().start_and_subscribe_stream()

    def start_sensor(self) -> Dict:
        """
        Starts PPG sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            # CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Stops PPG sensor and also Unsubscribe the PPG stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().stop_and_unsubscribe_stream()

    def stop_sensor(self) -> Dict:
        """
        Stops PPG sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self) -> Dict:
        """
        Subscribe to the PPG and SYNC PPG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        packet = StreamPacket(self._destination, CommonCommand.SUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(self._ppg_stream)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._ppg_stream)
        self._packet_manager.subscribe(data_packet_id, self._callback_ppg)
        sync_data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._syncppg_stream)
        self._packet_manager.subscribe(sync_data_packet_id, self._callback_syncppg)
        date_time = datetime.now()
        ts = (32000.0 * ((date_time.hour * 3600) + (date_time.minute * 60) + date_time.second))
        self._last_timestamp_syncppg = [date_time.timestamp(), ts, date_time.timestamp(), ts]
        self._last_timestamp_ppg = [date_time.timestamp(), ts]
        return self._send_packet(packet, CommonCommand.SUBSCRIBE_STREAM_RES)

    def unsubscribe_stream(self) -> Dict:
        """
        Unsubscribe the PPG and SYNC PPG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        packet = StreamPacket(self._destination, CommonCommand.UNSUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(self._ppg_stream)
        response_packet = self._send_packet(packet, CommonCommand.UNSUBSCRIBE_STREAM_RES)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._ppg_stream)
        self._packet_manager.unsubscribe(data_packet_id, self._callback_ppg)
        sync_data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._syncppg_stream)
        self._packet_manager.unsubscribe(sync_data_packet_id, self._callback_syncppg)
        return response_packet

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the device configuration block values of specified addresses.
        This function takes a list of addresses and values to write, and returns a response packet as
        dictionary containing addresses and values.

        :param addresses_values: List of addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x00
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["num_ops"])
            # 2

        """
        address_range = [0x00, 0x34]
        dcb_array = [0] * self._dcb_size
        for address_value in addresses_values:
            address = address_value[0]
            value = address_value[1]
            utils.address_range_check(address, address_range)
            utils.range_and_type_check(value, type_of=int, num_bytes=4)
            dcb_array[address] = value
        packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        num_ops = len(dcb_array)
        packet.set_size(utils.split_int_in_bytes(num_ops, length=2))
        packet.set_dcb_write_data(dcb_array, self._dcb_size, num_ops)
        return self._send_packet(packet, DCBCommand.WRITE_CONFIG_RES)

    def write_device_configuration_block_from_file(self, filename: str) -> Dict:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x00
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            application.write_device_configuration_block_from_file("ppg_dcb.lcfg")

        """
        result = self._write_device_configuration_block_from_file_helper(filename)
        if result:
            return self.write_device_configuration_block(result)

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
             - 0x34

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.write_library_configuration([[0x00, 0x1]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        address_range = [0x00, 0x34]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        utils.check_array_address_range(fields_values, address_range, 2)
        packet.set_number_of_operations(len(fields_values))
        packet.set_write_fields_data(fields_values)
        return self._send_packet(packet, CommonCommand.WRITE_LCFG_RES)

    def get_supported_streams(self) -> List[Stream]:
        """
        List all supported streams for PPG.

        :return: Array of stream ID enums.
        :rtype: List[Stream]
        """
        return [self.PPG, self.SYNC_PPG]

    def _ppg_stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[0]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[0]

    def get_version(self) -> Dict:
        """
        Returns PPG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 3
            print(x["payload"]["minor_version"])
            # 4
            print(x["payload"]["patch_version"])
            # 3
            print(x["payload"]["version_string"])
            # ECG_App
            print(x["payload"]["build_version"])
            # TEST ECG_VERSION STRING
        """
        packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        return self._send_packet(packet, CommonCommand.GET_VERSION_RES)

    def get_algo_version(self) -> Dict:
        """
        Returns PPG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.get_algo_version()
            print(x["payload"]["major_version"])
            # 3
            print(x["payload"]["minor_version"])
            # 4
            print(x["payload"]["patch_version"])
            # 3
            print(x["payload"]["version_string"])
            # ECG_App
            print(x["payload"]["build_version"])
            # TEST ECG_VERSION STRING
        """
        packet = VersionPacket(self._destination, PPGCommand.GET_ALGO_VENDOR_VERSION_REQ)
        return self._send_packet(packet, PPGCommand.GET_ALGO_VENDOR_VERSION_RES)

    def enable_csv_logging(self, filename, header=None, stream: Stream = PPG) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :param stream: PPG or SYNC_PPG stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.enable_csv_logging("ppg.csv", stream = application.PPG)
        """
        stream = self._ppg_stream_helper(stream)
        if header is None:
            if stream == self.PPG:
                header = ["Timestamp", "HR", "Confidence", "HR Type"]
            elif stream == self.SYNC_PPG:
                header = ["PPG Timestamp", "PPG", "ADXL Timestamp", "X", "Y", "Z"]
        self._csv_logger[stream] = CSVLogger(filename, header)

    def disable_csv_logging(self, stream: Stream = PPG) -> None:
        """
        Stops logging stream data into CSV.

        :param stream: PPG or SYNC_PPG stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ppg_application()
            x = application.disable_csv_logging(stream = application.PPG)
        """
        stream = self._ppg_stream_helper(stream)
        if self._csv_logger[stream]:
            self._csv_logger[stream].stop_logging()
        self._csv_logger[stream] = None
