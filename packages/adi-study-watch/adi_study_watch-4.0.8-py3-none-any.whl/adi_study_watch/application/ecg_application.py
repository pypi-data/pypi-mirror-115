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

from typing import Dict, Callable, Tuple, List

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.enums.ecg_enums import ECGCommand
from ..core.packets.command_packet import CommandPacket
from ..core.packets.stream_data_packets import ECGDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.common_packets import DecimationFactorPacket, DCBPacket, VersionPacket, LibraryConfigReadWritePacket


class ECGApplication(CommonStream):
    """
    ECG Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_ecg_application()

    """

    def __init__(self, callback_function, packet_manager, args):
        super().__init__(Application.ECG, Stream.ECG, packet_manager, callback_function, args)
        self._dcb_size = 2

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes ECG Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def get_decimation_factor(self) -> Dict:
        """
        Returns stream decimation factor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.get_decimation_factor()
            print(x["payload"]["decimation_factor"])
            # 1
        """
        packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        return self._send_packet(packet, CommonCommand.GET_STREAM_DEC_FACTOR_RES)

    def get_version(self) -> Dict:
        """
        Returns ECG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
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
        Returns ECG version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
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
        packet = VersionPacket(self._destination, ECGCommand.GET_ALGO_VENDOR_VERSION_REQ)
        return self._send_packet(packet, ECGCommand.GET_ALGO_VENDOR_VERSION_RES)

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.get_ecg_application()
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
             - 0x02

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]
        """
        address_range = [0x00, 0x02]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.READ_LCFG_REQ)
        packet.set_number_of_operations(len(fields))
        utils.check_array_address_range(fields, address_range, 1)
        packet.set_read_fields_data(fields)
        return self._send_packet(packet, CommonCommand.READ_LCFG_RES)

    def set_decimation_factor(self, decimation_factor: int) -> Dict:
        """
        Sets decimation factor for ECG stream.

        :param decimation_factor: decimation factor for stream
        :type decimation_factor: int
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Decimation Lower Limit
             - Decimation Upper Limit
           * - 0x01
             - 0x05

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.set_decimation_factor(2)
            print(x["payload"]["decimation_factor"])
            # 2
        """
        decimation_factor = utils.range_and_type_check(decimation_factor, type_of=int, num_bytes=1)
        packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        packet.set_decimation_factor([decimation_factor])
        return self._send_packet(packet, CommonCommand.SET_STREAM_DEC_FACTOR_RES)

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
             - 0x02

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.write_device_configuration_block([[0x0, 2], [0x1, 0x1]])
            print(x["payload"]["num_ops"])
            # 2
        """
        address_range = [0x00, 0x02]
        packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        num_ops = len(addresses_values)
        packet.set_size(utils.split_int_in_bytes(num_ops, length=2))
        utils.check_array_address_range(addresses_values, address_range, 2)
        packet.set_dcb_write_data(addresses_values, self._dcb_size, num_ops)
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
             - 0x02

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            application.write_device_configuration_block_from_file("ecg_dcb.lcfg")
        """
        result = self._write_device_configuration_block_from_file_helper(filename)
        if result:
            return self.write_device_configuration_block(result)

    def write_dcb_to_lcfg(self) -> Dict:
        """
        Writes Device configuration block data to library configuration.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.write_dcb_to_lcfg()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = CommandPacket(self._destination, CommonCommand.SET_LCFG_REQ)
        return self._send_packet(packet, CommonCommand.SET_LCFG_RES)

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
             - 0x03

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.write_library_configuration([[0x01, 0x2]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        address_range = [0x00, 0x03]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        packet.set_number_of_operations(len(fields_values))
        utils.check_array_address_range(fields_values, address_range, 2)
        packet.set_write_fields_data(fields_values)
        return self._send_packet(packet, CommonCommand.WRITE_LCFG_RES)

    def get_sensor_status(self) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.get_sensor_status()
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0
        """
        return super().get_sensor_status()

    def set_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream ECG data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2))
        """
        super().set_callback(callback_function, args)

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
            application = sdk.get_ecg_application()
            application.set_timeout(10)
        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Starts ECG sensor and also subscribe to the ECG stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        return super().start_and_subscribe_stream()

    def start_sensor(self) -> Dict:
        """
        Starts ECG sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            # CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Stops ECG sensor and also Unsubscribe the ECG stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().stop_and_unsubscribe_stream()

    def stop_sensor(self) -> Dict:
        """
        Stops ECG sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self) -> Dict:
        """
        Subscribe to the ECG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        return super().subscribe_stream()

    def unsubscribe_stream(self) -> Dict:
        """
        Unsubscribe the ECG stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().unsubscribe_stream()

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, packet_id, ECGDataPacket(), callback_function, args)

    def enable_csv_logging(self, filename, header=None) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.enable_csv_logging("ecg.csv")
        """
        if header is None:
            header = ["Timestamp", "Seq No.", "ECG data"]
        self._csv_logger[Stream.ECG] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_ecg_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger[Stream.ECG]:
            self._csv_logger[Stream.ECG].stop_logging()
        self._csv_logger[Stream.ECG] = None
