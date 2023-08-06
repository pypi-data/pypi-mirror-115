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
from typing import List, Dict, Callable, Tuple

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.adxl_packets import ADXLConfigPacket
from ..core.enums.adxl_enums import ADXLDevice, ADXLCommand
from ..core.packets.stream_data_packets import ADXLDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.common_packets import DecimationFactorPacket, DCFGPacket, DCBPacket, RegisterPacket

logger = logging.getLogger(__name__)


class ADXLApplication(CommonStream):
    """
    ADXL Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_adxl_application()

    """
    DEVICE_362 = ADXLDevice.DEVICE_362

    def __init__(self, callback_function, packet_manager, args):
        super().__init__(Application.ADXL, Stream.ADXL, packet_manager, callback_function, args)
        self._dcb_size = 25

    def _device_helper(self, device_id: ADXLDevice):
        """
        Confirms device ID is from list of Enums.
        """
        if device_id in self.get_supported_devices():
            return device_id
        else:
            logger.warning(f"{device_id} is not supported device ID, choosing {self.get_supported_devices()[0]} "
                           f"as default device ID. use get_supported_devices() to know all supported devices.")
            return self.get_supported_devices()[0]

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes Adxl Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
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
            application = sdk.get_adxl_application()
            x = application.get_decimation_factor()
            print(x["payload"]["decimation_factor"])
            # 1

        """
        packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        return self._send_packet(packet, CommonCommand.GET_STREAM_DEC_FACTOR_RES)

    def get_device_configuration(self) -> Dict:
        """
        Returns device configuration data.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_device_configuration()
            print(x["payload"]["dcfg_data"])
            # [['0x9', '0x97'], ['0x7', '0x8FFF'], ['0xB', '0x2F6'], ... ]
        """
        packet = DCFGPacket(self._destination, CommonCommand.GET_DCFG_REQ)
        return self._send_packet(packet, CommonCommand.GET_DCFG_RES)

    def get_sensor_status(self) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_sensor_status()
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0

        """
        return super().get_sensor_status()

    def get_supported_devices(self) -> List[ADXLDevice]:
        """
        List all supported device ID for adxl.

        :return: Array of device ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADXLDevice.DEVICE_362: ['0x6A', '0x1']>]
        """
        return [self.DEVICE_362]

    def load_configuration(self, device_id: ADXLDevice) -> Dict:
        """
        Loads specified device id configuration.

        :param device_id: Device ID to load, use get_supported_devices() to list all supported devices.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADXLDevice.DEVICE_362: ['0x6A', '0x1']>]
            x = application.load_configuration(application.DEVICE_362)
            print(x["payload"]["device_id"])
            # <ADXLDevice.DEVICE_362: ['0x6A', '0x1']>

        """
        device_id = self._device_helper(device_id)
        packet = ADXLConfigPacket(self._destination, ADXLCommand.LOAD_CONFIG_REQ)
        packet.set_device_id(device_id)
        return self._send_packet(packet, ADXLCommand.LOAD_CONFIG_RES)

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
            # []

        """
        packet = DCBPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.READ_CONFIG_RES)

    def read_register(self, addresses: List[int]) -> Dict:
        """
        Reads the register values of specified addresses. This function takes a list of addresses to read,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses: List of register addresses to read.
        :type addresses: List[int]
        :return: A response packet as dictionary
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x00
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]
        """
        address_range = [0x00, 0x2E]
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        packet.set_number_of_operations(len(addresses))
        utils.check_array_address_range(addresses, address_range, 2)
        packet.set_read_reg_data(addresses)
        return self._send_packet(packet, CommonCommand.REGISTER_READ_RES)

    def set_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream adxl data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2))
        """
        super().set_callback(callback_function, args)

    def set_decimation_factor(self, decimation_factor: int) -> Dict:
        """
        Sets decimation factor for adxl stream.

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
            application = sdk.get_adxl_application()
            x = application.set_decimation_factor(2)
            print(x["payload"]["decimation_factor"])
            # 2

        """
        decimation_factor = utils.range_and_type_check(decimation_factor, type_of=int, lower_and_upper_bound=[1, 5])
        packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        packet.set_decimation_factor([decimation_factor])
        return self._send_packet(packet, CommonCommand.SET_STREAM_DEC_FACTOR_RES)

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
            application = sdk.get_adxl_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Starts adxl sensor and also subscribe to the adxl stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        return super().start_and_subscribe_stream()

    def start_sensor(self) -> Dict:
        """
        Starts adxl sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            # CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Stops adxl sensor and also Unsubscribe the adxl stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().stop_and_unsubscribe_stream()

    def stop_sensor(self) -> Dict:
        """
        Stops adxl sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self) -> Dict:
        """
        Subscribe to the adxl stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        return super().subscribe_stream()

    def unsubscribe_stream(self) -> Dict:
        """
        Unsubscribe the adxl stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().unsubscribe_stream()

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
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2

        """
        address_range = [0x20, 0x2E]
        packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        packet.set_size(utils.split_int_in_bytes(len(addresses_values), length=2))
        utils.check_array_address_range(addresses_values, address_range, 2)
        packet.set_dcb_write_data(addresses_values, self._dcb_size, len(addresses_values))
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
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            application.write_device_configuration_block_from_file("adxl_dcb.dcfg")

        """
        result = self._write_device_configuration_block_from_file_helper(filename)
        if result:
            return self.write_device_configuration_block(result)

    def write_register(self, addresses_values: List[List[int]]) -> Dict:
        """
        Writes the register values of specified addresses. This function takes a list of addresses and values to write,
        and returns a response packet as dictionary containing addresses and values.

        :param addresses_values: List of register addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x20
             - 0x2E

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]

        """
        address_range = [0x20, 0x2E]
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        packet.set_number_of_operations(len(addresses_values))
        utils.check_array_address_range(addresses_values, address_range, 2)
        packet.set_write_reg_data(addresses_values)
        return self._send_packet(packet, CommonCommand.REGISTER_WRITE_RES)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, packet_id, ADXLDataPacket(), callback_function, args)

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
            application = sdk.get_adxl_application()
            x = application.enable_csv_logging("adxl.csv")
        """
        if header is None:
            header = ["Timestamp", "X", "Y", "Z"]
        self._csv_logger[Stream.ADXL] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adxl_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger[Stream.ADXL]:
            self._csv_logger[Stream.ADXL].stop_logging()
        self._csv_logger[Stream.ADXL] = None
