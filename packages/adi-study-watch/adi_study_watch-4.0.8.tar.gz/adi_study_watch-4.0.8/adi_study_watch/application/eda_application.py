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
from ..core.packets.command_packet import CommandPacket
from ..core.packets.stream_data_packets import EDADataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.enums.eda_enums import EDACommand, EDADFTWindow, ScaleResistor
from ..core.packets.common_packets import DecimationFactorPacket, DFTPacket
from ..core.packets.eda_packets import DynamicScalingPacket, ResistorTIACalibratePacket
from ..core.packets.common_packets import DCBPacket, VersionPacket, LibraryConfigReadWritePacket

logger = logging.getLogger(__name__)


class EDAApplication(CommonStream):
    """
    EDA Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_eda_application()

    """
    DFT_WINDOW_4 = EDADFTWindow.DFT_WINDOW_4
    DFT_WINDOW_8 = EDADFTWindow.DFT_WINDOW_8
    DFT_WINDOW_16 = EDADFTWindow.DFT_WINDOW_16
    DFT_WINDOW_32 = EDADFTWindow.DFT_WINDOW_32

    SCALE_RESISTOR_110 = ScaleResistor.SCALE_RESISTOR_110
    SCALE_RESISTOR_1K = ScaleResistor.SCALE_RESISTOR_1K
    SCALE_RESISTOR_2K = ScaleResistor.SCALE_RESISTOR_2K
    SCALE_RESISTOR_3K = ScaleResistor.SCALE_RESISTOR_3K
    SCALE_RESISTOR_4K = ScaleResistor.SCALE_RESISTOR_4K
    SCALE_RESISTOR_6K = ScaleResistor.SCALE_RESISTOR_6K
    SCALE_RESISTOR_8K = ScaleResistor.SCALE_RESISTOR_8K
    SCALE_RESISTOR_10K = ScaleResistor.SCALE_RESISTOR_10K
    SCALE_RESISTOR_12K = ScaleResistor.SCALE_RESISTOR_12K
    SCALE_RESISTOR_16K = ScaleResistor.SCALE_RESISTOR_16K
    SCALE_RESISTOR_20K = ScaleResistor.SCALE_RESISTOR_20K
    SCALE_RESISTOR_24K = ScaleResistor.SCALE_RESISTOR_24K
    SCALE_RESISTOR_30K = ScaleResistor.SCALE_RESISTOR_30K
    SCALE_RESISTOR_32K = ScaleResistor.SCALE_RESISTOR_32K
    SCALE_RESISTOR_40K = ScaleResistor.SCALE_RESISTOR_40K
    SCALE_RESISTOR_48K = ScaleResistor.SCALE_RESISTOR_48K
    SCALE_RESISTOR_64K = ScaleResistor.SCALE_RESISTOR_64K
    SCALE_RESISTOR_85K = ScaleResistor.SCALE_RESISTOR_85K
    SCALE_RESISTOR_96K = ScaleResistor.SCALE_RESISTOR_96K
    SCALE_RESISTOR_100K = ScaleResistor.SCALE_RESISTOR_100K
    SCALE_RESISTOR_120K = ScaleResistor.SCALE_RESISTOR_120K
    SCALE_RESISTOR_128K = ScaleResistor.SCALE_RESISTOR_128K
    SCALE_RESISTOR_160K = ScaleResistor.SCALE_RESISTOR_160K
    SCALE_RESISTOR_196K = ScaleResistor.SCALE_RESISTOR_196K
    SCALE_RESISTOR_256K = ScaleResistor.SCALE_RESISTOR_256K
    SCALE_RESISTOR_512K = ScaleResistor.SCALE_RESISTOR_512K

    def __init__(self, callback_function, packet_manager, args):
        super().__init__(Application.EDA, Stream.EDA, packet_manager, callback_function, args)
        self._callback_function = callback_function
        self._dcb_size = 2

    def get_supported_scales(self) -> List[ScaleResistor]:
        """
        List all supported scales for EDA.

        :return: Array of scales enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_supported_scales()
            print(x)
            # [<ScaleResistor.SCALE_RESISTOR_100K: ['0x0', '0x14']>, ...]
        """
        return [self.SCALE_RESISTOR_110, self.SCALE_RESISTOR_1K, self.SCALE_RESISTOR_2K, self.SCALE_RESISTOR_3K,
                self.SCALE_RESISTOR_4K, self.SCALE_RESISTOR_6K, self.SCALE_RESISTOR_8K, self.SCALE_RESISTOR_10K,
                self.SCALE_RESISTOR_12K, self.SCALE_RESISTOR_16K, self.SCALE_RESISTOR_20K, self.SCALE_RESISTOR_24K,
                self.SCALE_RESISTOR_30K, self.SCALE_RESISTOR_32K, self.SCALE_RESISTOR_40K, self.SCALE_RESISTOR_48K,
                self.SCALE_RESISTOR_64K, self.SCALE_RESISTOR_85K, self.SCALE_RESISTOR_96K, self.SCALE_RESISTOR_100K,
                self.SCALE_RESISTOR_120K, self.SCALE_RESISTOR_128K, self.SCALE_RESISTOR_160K, self.SCALE_RESISTOR_196K,
                self.SCALE_RESISTOR_256K, self.SCALE_RESISTOR_512K]

    def _scale_helper(self, scale: ScaleResistor) -> ScaleResistor:
        """
        Confirms scale is from list of Enums.
        """
        if scale in self.get_supported_scales():
            return scale
        else:
            logger.warning(f"{scale} is not supported scale, choosing {self.get_supported_scales()[0]} "
                           f"as default scale. use get_supported_scales() to know all supported scales.")
            return self.get_supported_scales()[0]

    def get_supported_dft_windows(self) -> List[EDADFTWindow]:
        """
        List all supported dft window for EDA.

        :return: Array of dft window enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_supported_dft_windows()
            print(x)
            # [<EDADFTWindow.DFT_WINDOW_4: ['0x0']>, ... , <EDADFTWindow.DFT_WINDOW_32: ['0x3']>]
        """
        return [self.DFT_WINDOW_4, self.DFT_WINDOW_8, self.DFT_WINDOW_16, self.DFT_WINDOW_32]

    def _dft_window_helper(self, dft_window: EDADFTWindow) -> EDADFTWindow:
        """
        Confirms dft_window is from list of Enums.
        """
        if dft_window in self.get_supported_dft_windows():
            return dft_window
        else:
            logger.warning(f"{dft_window} is not supported dft window, choosing {self.get_supported_dft_windows()[0]} "
                           f"as default dft window. use get_supported_dft_windows() to know all supported dft window.")
            return self.get_supported_dft_windows()[0]

    def calibrate_resistor_tia(self, min_scale: ScaleResistor, max_scale: ScaleResistor,
                               lp_resistor_tia: ScaleResistor) -> Dict:
        """
         Calibrate Resistor Trans Impedance Amplifier.

         :param min_scale: min scale for Resistor Trans Impedance Amplifier, use get_supported_scales()
                          | to list all supported scales.
         :param max_scale: max scale for Resistor Trans Impedance Amplifier, use get_supported_scales()
                          | to list all supported scales.
         :param lp_resistor_tia: lp_resistor_tia, use get_supported_scales() to list all supported scales.
         :type min_scale: ScaleResistor
         :type max_scale: ScaleResistor
         :type lp_resistor_tia: ScaleResistor
         :return: A response packet as dictionary.
         :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_supported_scales()
            print(x)
            # [<ScaleResistor.SCALE_RESISTOR_100K: ['0x0', '0x14']>, ... ]
            x = application.calibrate_resistor_tia(application.SCALE_RESISTOR_128K, application.SCALE_RESISTOR_256K,
                                                    application.SCALE_RESISTOR_256K)
            print(x["payload"]["status"])
            # CommonStatus.OK
         """
        min_scale = self._scale_helper(min_scale)
        max_scale = self._scale_helper(max_scale)
        lp_resistor_tia = self._scale_helper(lp_resistor_tia)
        packet = ResistorTIACalibratePacket(self._destination, EDACommand.RESISTOR_TIA_CAL_REQ)
        packet.set_min_scale(min_scale)
        packet.set_max_scale(max_scale)
        packet.set_lp_resistor_tia(lp_resistor_tia)
        packet.set_calibrated_values_count(
            [utils.join_multi_length_packets(max_scale.value) - utils.join_multi_length_packets(min_scale.value) + 1])
        return self._send_packet(packet, EDACommand.RESISTOR_TIA_CAL_RES)

    def get_decimation_factor(self) -> Dict:
        """
        Returns stream decimation factor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_decimation_factor()
            print(x["payload"]["decimation_factor"])
            # 1

        """
        packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        return self._send_packet(packet, CommonCommand.GET_STREAM_DEC_FACTOR_RES)

    def set_decimation_factor(self, decimation_factor: int) -> Dict:
        """
        Sets decimation factor for EDA stream.

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
            application = sdk.get_eda_application()
            x = application.set_decimation_factor(2)
            print(x["payload"]["decimation_factor"])
            # 2

        """
        decimation_factor = utils.range_and_type_check(decimation_factor, type_of=int, num_bytes=1)
        packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(self._stream)
        packet.set_decimation_factor([decimation_factor])
        return self._send_packet(packet, CommonCommand.SET_STREAM_DEC_FACTOR_RES)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes EDA Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def disable_dynamic_scaling(self) -> Dict:
        """
        Disables Dynamic scaling.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            application.disable_dynamic_scaling()
        """
        packet = DynamicScalingPacket(self._destination, EDACommand.DYNAMIC_SCALE_REQ)
        packet.set_enable([0x0])
        return self._send_packet(packet, EDACommand.DYNAMIC_SCALE_RES)

    def enable_dynamic_scaling(self, min_scale: ScaleResistor, max_scale: ScaleResistor,
                               lp_resistor_tia: ScaleResistor) -> Dict:
        """
         Enables Dynamic scaling.

         :param min_scale: min scale for Resistor Trans Impedance Amplifier, use get_supported_scales()
                          | to list all supported scales.
         :param max_scale: max scale for Resistor Trans Impedance Amplifier, use get_supported_scales()
                          | to list all supported scales.
         :param lp_resistor_tia: lp_resistor_tia, use get_supported_scales() to list all supported scales.
         :type min_scale: ScaleResistor
         :type max_scale: ScaleResistor
         :type lp_resistor_tia: ScaleResistor
         :return: A response packet as dictionary.
         :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_supported_scales()
            print(x)
            # [<ScaleResistor.SCALE_RESISTOR_100K: ['0x0', '0x14']>, ... ]
            x = application.enable_dynamic_scaling(application.SCALE_RESISTOR_128K, application.SCALE_RESISTOR_256K,
                                                    application.SCALE_RESISTOR_256K)
            print(x["payload"]["status"])
            # CommonStatus.OK

         """
        min_scale = self._scale_helper(min_scale)
        max_scale = self._scale_helper(max_scale)
        lp_resistor_tia = self._scale_helper(lp_resistor_tia)
        packet = DynamicScalingPacket(self._destination, EDACommand.DYNAMIC_SCALE_REQ)
        packet.set_min_scale(min_scale.value)
        packet.set_max_scale(max_scale.value)
        packet.set_lp_resistor_tia(lp_resistor_tia.value)
        packet.set_enable([0x1])
        return self._send_packet(packet, EDACommand.DYNAMIC_SCALE_RES)

    def get_version(self) -> Dict:
        """
        Returns EDA version info.

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
            # EDA_App
            print(x["payload"]["build_version"])
            # TEST EDA_VERSION STRING
        """
        packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        return self._send_packet(packet, CommonCommand.GET_VERSION_RES)

    def read_device_configuration_block(self) -> Dict:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
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
             - 0x02

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x0']]

        """
        address_range = [0x00, 0x02]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.READ_LCFG_REQ)
        fields_size = len(fields)
        packet.set_number_of_operations(fields_size)
        utils.check_array_address_range(fields, address_range, 1)
        packet.set_read_fields_data(fields)
        return self._send_packet(packet, CommonCommand.READ_LCFG_RES)

    def set_discrete_fourier_transformation(self, dft_window: EDADFTWindow) -> Dict:
        """
        Set Discrete Fourier Transformation for EDA.

        :param dft_window: DFT window for Discrete Fourier Transformation, use get_supported_dft_windows()
                          | to list all supported DFT window.
        :type dft_window: EDADFTWindow
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.get_supported_dft_windows()
            print(x)
            # [<EDADFTWindow.DFT_WINDOW_4: ['0x0']>, ... ,<EDADFTWindow.DFT_WINDOW_32: ['0x3']>]
            x = application.set_discrete_fourier_transformation(application.DFT_WINDOW_32)
            print(x["payload"]["dft_window"])
            # EDADFTWindow.DFT_WINDOW_32
        """
        dft_window = self._dft_window_helper(dft_window)
        packet = DFTPacket(self._destination, EDACommand.SET_DFT_NUM_REQ)
        packet.set_dft_num(dft_window)
        return self._send_packet(packet, EDACommand.SET_DFT_NUM_RES)

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
            application = sdk.get_eda_application()
            x = application.write_device_configuration_block([[0x0, 2], [0x1, 0x1]])
            print(x["payload"]["num_ops"])
            # 2

        """
        address_range = [0x00, 0x02]
        packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
        num_ops = len(addresses_values)
        utils.check_array_address_range(addresses_values, address_range, 2)
        packet.set_size(utils.split_int_in_bytes(num_ops, length=2))
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
            application = sdk.get_eda_application()
            application.write_device_configuration_block_from_file("adxl_dcb.dcfg")

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
            application = sdk.get_eda_application()
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
             - 0x02

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.write_library_configuration([[0x00, 0x1]])
            print(x["payload"]["data"])
            # [['0x0', '0x1']]

        """
        address_range = [0x00, 0x02]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        fields_values_size = len(fields_values)
        packet.set_number_of_operations(fields_values_size)
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
            application = sdk.get_eda_application()
            x = application.get_sensor_status()
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0

        """
        return super().get_sensor_status()

    def set_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream EDA data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
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
            application = sdk.get_eda_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Starts EDA sensor and also subscribe to the EDA stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        return super().start_and_subscribe_stream()

    def start_sensor(self) -> Dict:
        """
        Starts EDA sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            # CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Stops EDA sensor and also Unsubscribe the EDA stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().stop_and_unsubscribe_stream()

    def stop_sensor(self) -> Dict:
        """
        Stops EDA sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self) -> Dict:
        """
        Subscribe to the EDA stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        return super().subscribe_stream()

    def unsubscribe_stream(self) -> Dict:
        """
        Unsubscribe the EDA stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().unsubscribe_stream()

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, packet_id, EDADataPacket(), callback_function, args)

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
            application = sdk.get_eda_application()
            x = application.enable_csv_logging("eda.csv")
        """
        if header is None:
            header = ["Timestamp", "Seq No.", "Impedance Module", "Impedance Phase"]
        self._csv_logger[Stream.EDA] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_eda_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger[Stream.EDA]:
            self._csv_logger[Stream.EDA].stop_logging()
        self._csv_logger[Stream.EDA] = None
