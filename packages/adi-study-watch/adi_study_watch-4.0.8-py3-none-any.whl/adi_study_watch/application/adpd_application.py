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
import time
import logging
from datetime import datetime
from typing import Dict, List, Union, Tuple, Callable

from tqdm import tqdm

from ..core import utils
from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.enums.dcb_enums import DCBCommand
from ..core.packets.stream_data_packets import ADPDDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand
from ..core.packets.adpd_packets import ExternalStreamODR, ExternalStreamData
from ..core.packets.adpd_packets import SamplingFrequencyPacket, ADPDConfigPacket
from ..core.packets.adpd_packets import ClockCalibrationPacket, ADPDPauseResumePacket
from ..core.enums.adpd_enums import ADPDDevice, ADPDCommand, ADPDSlot, Clock, ADPDLed, ADPDAppID
from ..core.packets.adpd_packets import SlotPacket, ActiveSlotPacket, ComModePacket, AgcControlPacket
from ..core.packets.common_packets import StreamPacket, VersionPacket, DecimationFactorPacket, DCFGPacket
from ..core.packets.common_packets import DCBPacket, LibraryConfigReadWritePacket, RegisterPacket, StreamStatusPacket

logger = logging.getLogger(__name__)


class ADPDApplication(CommonStream):
    """
    ADPD Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_adpd_application()

    """

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

    DEVICE_GREEN = ADPDDevice.DEVICE_GREEN
    DEVICE_RED = ADPDDevice.DEVICE_RED
    DEVICE_INFRARED = ADPDDevice.DEVICE_INFRARED
    DEVICE_BLUE = ADPDDevice.DEVICE_BLUE
    DEVICE_G_R_IR_B = ADPDDevice.DEVICE_G_R_IR_B

    SLOT_A = ADPDSlot.SLOT_A
    SLOT_B = ADPDSlot.SLOT_B
    SLOT_C = ADPDSlot.SLOT_C
    SLOT_D = ADPDSlot.SLOT_D
    SLOT_E = ADPDSlot.SLOT_E
    SLOT_F = ADPDSlot.SLOT_F
    SLOT_G = ADPDSlot.SLOT_G
    SLOT_H = ADPDSlot.SLOT_H
    SLOT_I = ADPDSlot.SLOT_I
    SLOT_J = ADPDSlot.SLOT_J
    SLOT_K = ADPDSlot.SLOT_K
    SLOT_L = ADPDSlot.SLOT_L

    NO_CLOCK = Clock.NO_CLOCK
    CLOCK_32K = Clock.CLOCK_32K
    CLOCK_1M = Clock.CLOCK_1M
    CLOCK_32M = Clock.CLOCK_32M
    CLOCK_32K_AND_1M = Clock.CLOCK_32K_AND_1M
    CLOCK_1M_AND_32M = Clock.CLOCK_1M_AND_32M

    LED_MWL = ADPDLed.LED_MWL
    LED_GREEN = ADPDLed.LED_GREEN
    LED_RED = ADPDLed.LED_RED
    LED_IR = ADPDLed.LED_IR
    LED_BLUE = ADPDLed.LED_BLUE

    APP_ECG = ADPDAppID.APP_ECG
    APP_PPG = ADPDAppID.APP_PPG
    APP_TEMPERATURE_THERMISTOR = ADPDAppID.APP_TEMPERATURE_THERMISTOR
    APP_TEMPERATURE_RESISTOR = ADPDAppID.APP_TEMPERATURE_RESISTOR
    APP_ADPD_GREEN = ADPDAppID.APP_ADPD_GREEN
    APP_ADPD_RED = ADPDAppID.APP_ADPD_RED
    APP_ADPD_INFRARED = ADPDAppID.APP_ADPD_INFRARED
    APP_ADPD_BLUE = ADPDAppID.APP_ADPD_BLUE

    def __init__(self, callback_function_default, packet_manager, args):
        super().__init__(Application.ADPD, Stream.ADPD6, packet_manager, callback_function_default, args)
        self._callback_function1 = None
        self._callback_function2 = None
        self._callback_function3 = None
        self._callback_function4 = None
        self._callback_function5 = None
        self._callback_function6 = None
        self._callback_function7 = None
        self._callback_function8 = None
        self._callback_function9 = None
        self._callback_function10 = None
        self._callback_function11 = None
        self._callback_function12 = None

        self._args_adpd1 = None
        self._args_adpd2 = None
        self._args_adpd3 = None
        self._args_adpd4 = None
        self._args_adpd5 = None
        self._args_adpd6 = None
        self._args_adpd7 = None
        self._args_adpd8 = None
        self._args_adpd9 = None
        self._args_adpd10 = None
        self._args_adpd11 = None
        self._args_adpd12 = None

        self._stream_to_callback = {self.STREAM_ADPD1: self._callback_data1, self.STREAM_ADPD2: self._callback_data2,
                                    self.STREAM_ADPD3: self._callback_data3, self.STREAM_ADPD4: self._callback_data4,
                                    self.STREAM_ADPD5: self._callback_data5, self.STREAM_ADPD6: self._callback_data6,
                                    self.STREAM_ADPD7: self._callback_data7, self.STREAM_ADPD8: self._callback_data8,
                                    self.STREAM_ADPD9: self._callback_data9, self.STREAM_ADPD10: self._callback_data10,
                                    self.STREAM_ADPD11: self._callback_data11,
                                    self.STREAM_ADPD12: self._callback_data12}
        self._last_timestamp_adpd = {}
        for stream in self._stream_to_callback:
            self._csv_logger[stream] = None
            self._last_timestamp_adpd[stream] = []

        self._dcb_size = 57

    def _adpd_stream_helper(self, stream: Stream) -> Stream:
        """
        Confirms stream is from list of Enums.
        """
        if stream in self.get_supported_streams():
            return stream
        else:
            logger.warning(f"{stream} is not supported stream, choosing {self.get_supported_streams()[5]} "
                           f"as default stream. use get_supported_streams() to know all supported streams.")
            return self.get_supported_streams()[5]

    def _app_id_helper(self, app_id: ADPDAppID) -> ADPDAppID:
        """
        Confirms app ID is from list of Enums.
        """
        if app_id in self.get_supported_app_id():
            return app_id
        else:
            logger.warning(f"{app_id} is not supported APP ID, choosing {self.get_supported_app_id()[0]} "
                           f"as default APP ID. use get_supported_app_id() to know all supported APP IDs.")
            return self.get_supported_app_id()[0]

    def _clock_helper(self, clock_id: Clock) -> Clock:
        """
        Confirms clock ID is from list of Enums.
        """
        if clock_id in self.get_supported_clocks():
            return clock_id
        else:
            logger.warning(f"{clock_id} is not supported clock ID, choosing {self.get_supported_clocks()[5]} "
                           f"as default clock ID. use get_supported_clocks() to know all supported clocks.")
            return self.get_supported_clocks()[5]

    def _device_helper(self, device_id: ADPDDevice) -> ADPDDevice:
        """
        Confirms device ID is from list of Enums.
        """
        if device_id in self.get_supported_devices():
            return device_id
        else:
            logger.warning(f"{device_id} is not supported device ID, choosing {self.get_supported_devices()[0]} "
                           f"as default device ID. use get_supported_devices() to know all supported devices.")
            return self.get_supported_devices()[0]

    def _led_helper(self, led_id: ADPDLed) -> ADPDLed:
        """
        Confirms led ID is from list of Enums.
        """
        if led_id in self.get_supported_led_ids():
            return led_id
        else:
            logger.warning(f"{led_id} is not supported led ID, choosing {self.get_supported_led_ids()[0]} "
                           f"as default led ID. use get_supported_led_ids() to know all supported led IDs.")
            return self.get_supported_led_ids()[0]

    def _slot_helper(self, slot_id: ADPDSlot) -> ADPDSlot:
        """
        Confirms slot ID is from list of Enums.
        """
        if slot_id in self.get_supported_slots():
            return slot_id
        else:
            logger.warning(f"{slot_id} is not supported slot ID, choosing {self.get_supported_slots()[0]} "
                           f"as default slot ID. use get_supported_slots() to know all supported slot IDs.")
            return self.get_supported_slots()[0]

    def calibrate_clock(self, clock_id: Clock) -> Dict:
        """
        Calibrate clock to specified clock ID.

        :param clock_id: Clock ID to calibrate, use get_supported_clocks() to list all supported clock ID.
        :type clock_id: Clock
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_clocks()
            print(x)
            # [<Clock.NO_CLOCK: ['0x0']>, ... , <Clock.CLOCK_32K_AND_1M: ['0x5']>, <Clock.CLOCK_1M_AND_32M: ['0x6']>]
            x = application.calibrate_clock(application.CLOCK_1M_AND_32M)
            print(x["payload"]["clock_id"])
            # Clock.CLOCK_1M_AND_32M

        """
        clock_id = self._clock_helper(clock_id)
        packet = ClockCalibrationPacket(self._destination, ADPDCommand.CLOCK_CALIBRATION_REQ)
        packet.set_clock_id(clock_id)
        return self._send_packet(packet, ADPDCommand.CLOCK_CALIBRATION_RES)

    def create_device_configuration(self, slot_app_ids: List[List[Union[ADPDSlot, ADPDAppID]]]) -> Dict:
        """
        Create ADPD device configuration.

        :param slot_app_ids: List of slot ID and APP ID to write, use get_supported_slots() to list all
                            | supported slot ID, and get_supported_app_id() to list all supported app ID.
        :type slot_app_ids: List[List[ADPDSlot, ADPDAppID]]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_supported_app_id()
            print(x)
            # [<ADPDAppID.APP_PPG: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>, ... , <ADPDAppID.APP_ADPD_BLUE: ['0x7']>]
            x = application.create_device_configuration([[application.SLOT_A, application.APP_ECG],
                                                        [application.SLOT_B, application.APP_ADPD_GREEN]])
            print(x["payload"]["data"])
            # [[<ADPDSlot.SLOT_A: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>], ... ]
        """
        packet = RegisterPacket(self._destination, ADPDCommand.CREATE_DCFG_REQ)
        num_ops = len(slot_app_ids)
        for i in range(num_ops):
            slot_app_ids[i][0] = self._slot_helper(slot_app_ids[i][0])
            slot_app_ids[i][1] = self._app_id_helper(slot_app_ids[i][1])
        packet.set_number_of_operations(num_ops)
        slot_app = utils.split_int_in_bytes(0, length=num_ops * 4)
        for i in range(num_ops):
            start_index = i * 4
            slot_app[start_index:start_index + 2] = utils.split_int_in_bytes(slot_app_ids[i][0].value[0], length=2)
            slot_app[start_index + 2: start_index + 4] = utils.split_int_in_bytes(slot_app_ids[i][1].value[0], length=2)
        packet.set_data(slot_app)
        return self._send_packet(packet, ADPDCommand.CREATE_DCFG_RES)

    def delete_device_configuration_block(self) -> Dict:
        """
        Deletes ADPD Device configuration block.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.delete_device_configuration_block()
        """
        packet = DCBPacket(self._destination, DCBCommand.ERASE_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        return self._send_packet(packet, DCBCommand.ERASE_CONFIG_RES)

    def disable_agc(self, led_list: List[ADPDLed]) -> Dict:
        """
        Disables AGC for LED in list.

        :param led_list: list of led to disable agc, use get_supported_led_ids() to list all supported led ID.
        :type led_list: List[ADPDLed]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.disable_agc([application.LED_GREEN, application.LED_RED])
            print(x["payload"]["agc_data"])
            # [[<ADPDLed.LED_MWL: ['0x0']>, False], [<ADPDLed.LED_GREEN: ['0x1']>, False]]
        """
        packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_REQ)
        num_ops = len(led_list)
        for i in range(num_ops):
            led_list[i] = self._led_helper(led_list[i])
        packet.set_number_of_operations([num_ops])
        agc_control_array = utils.split_int_in_bytes(0, length=num_ops * 2)
        for i in range(num_ops):
            start_index = i * 2
            agc_control_array[start_index] = 0
            agc_control_array[start_index + 1] = led_list[i].value[0]
        packet.set_fields_values(agc_control_array)
        return self._send_packet(packet, ADPDCommand.AGC_ON_OFF_RES)

    def disable_slot(self, slot_num: ADPDSlot) -> Dict:
        """
        Disable Specified ADPD Slot.

        :param slot_num: slot_num to disable, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.disable_slot(application.SLOT_A)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # ADPDSlot.SLOT_A False
        """
        slot_num = self._slot_helper(slot_num)
        packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_REQ)
        packet.set_slot_num(slot_num)
        packet.set_slot_active([0x0])
        return self._send_packet(packet, ADPDCommand.SET_SLOT_ACTIVE_RES)

    def enable_agc(self, led_list: List[ADPDLed]) -> Dict:
        """
        Enables AGC for LEDs in list.

        :param led_list: list of led to enable agc, use get_supported_led_ids() to list all supported led ID.
        :type led_list: List[ADPDLed]
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.enable_agc([application.LED_GREEN, application.LED_RED])
            print(x["payload"]["agc_data"])
            # [[<ADPDLed.LED_MWL: ['0x0']>, True], [<ADPDLed.LED_GREEN: ['0x1']>, True]]
        """
        packet = AgcControlPacket(self._destination, ADPDCommand.AGC_ON_OFF_REQ)
        num_ops = len(led_list)
        packet.set_number_of_operations([num_ops])
        for i in range(num_ops):
            led_list[i] = self._led_helper(led_list[i])
        agc_control_array = utils.split_int_in_bytes(0, length=num_ops * 2)
        for i in range(num_ops):
            start_index = i * 2
            agc_control_array[start_index] = 1
            agc_control_array[start_index + 1] = led_list[i].value[0]
        packet.set_fields_values(agc_control_array)
        return self._send_packet(packet, ADPDCommand.AGC_ON_OFF_RES)

    def enable_slot(self, slot_num: ADPDSlot) -> Dict:
        """
        Enable Specified ADPD Slot.

        :param slot_num: slot_num to enable, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.enable_slot(application.SLOT_A)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # ADPDSlot.SLOT_A  True
        """
        slot_num = self._slot_helper(slot_num)
        packet = ActiveSlotPacket(self._destination, ADPDCommand.SET_SLOT_ACTIVE_REQ)
        packet.set_slot_num(slot_num)
        packet.set_slot_active([0x1])
        return self._send_packet(packet, ADPDCommand.SET_SLOT_ACTIVE_RES)

    def get_communication_mode(self) -> Dict:
        """
        Get ADPD communication mode.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_communication_mode()
            print(x["payload"]["com_mode"])
            # 2
        """
        packet = ComModePacket(self._destination, ADPDCommand.COMMUNICATION_MODE_REQ)
        return self._send_packet(packet, ADPDCommand.COMMUNICATION_MODE_RES)

    def get_decimation_factor(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Returns stream decimation factor.

        :param stream: Stream to get decimation factor.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            x = application.get_decimation_factor(application.STREAM_ADPD6)
            print(x["payload"]["decimation_factor"])
            # 1

        """
        stream = self._adpd_stream_helper(stream)
        packet = DecimationFactorPacket(self._destination, CommonCommand.GET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, CommonCommand.GET_STREAM_DEC_FACTOR_RES)

    def get_device_configuration(self) -> List[Dict]:
        """
        Returns device configuration data.

        :return: A response packet as dictionary.
        :rtype: List[Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_device_configuration()
            print(x[0]["payload"]["data"])
            # [['0x9', '0x97'], ['0x7', '0x8FFF'], ['0xB', '0x2F6'], ... ]
        """
        packet = DCFGPacket(self._destination, CommonCommand.GET_DCFG_REQ)
        packet_id = self._get_packet_id(CommonCommand.GET_DCFG_RES)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        queue = self._get_queue(packet_id)
        result = []
        count = 1
        while True:
            data = self._get_queue_data(queue)
            packet = DCFGPacket()
            packet.decode_packet(data)
            packet_dict = packet.get_dict()
            result.append(packet_dict)
            if packet_dict["payload"]["num_tx_packets"] == count or packet_dict["payload"]["num_tx_packets"] == 0:
                break
            count += 1
        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        return result

    def get_sensor_status(self, stream=STREAM_ADPD6) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_sensor_status(application.STREAM_ADPD6)
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0
        """
        stream = self._adpd_stream_helper(stream)
        packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, CommonCommand.GET_SENSOR_STATUS_RES)

    def get_slot(self, slot_num: ADPDSlot) -> Dict:
        """
        Get Specified ADPD Slot Detail.

        :param slot_num: slot_num to get slot detail, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_slot(application.SLOT_A)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # <ADPDSlot.SLOT_A: ['0x1']> True
            print(x["payload"]["slot_format"], x["payload"]["channel_num"])
            # 3 3
        """
        slot_num = self._slot_helper(slot_num)
        packet = SlotPacket(self._destination, ADPDCommand.GET_SLOT_REQ)
        packet.set_slot_num(slot_num)
        return self._send_packet(packet, ADPDCommand.GET_SLOT_RES)

    def get_slot_status(self, slot_num) -> Dict:
        """
        Returns whether slot is enabled or not.

        :param slot_num: slot_num to get status, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.get_slot_status(application.SLOT_A)
            print(x["payload"]["slot_enabled"])
            # True
        """
        slot_num = self._slot_helper(slot_num)
        packet = ActiveSlotPacket(self._destination, ADPDCommand.GET_SLOT_ACTIVE_REQ)
        packet.set_slot_num(slot_num)
        return self._send_packet(packet, ADPDCommand.GET_SLOT_ACTIVE_RES)

    def get_supported_app_id(self) -> List[ADPDAppID]:
        """
        List all supported Apps for ADPD.

        :return: Array of APP ID enums.
        :rtype: List[ADPDAppID]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_app_id()
            print(x)
            # [<ADPDAppID.APP_PPG: ['0x1']>, <ADPDAppID.APP_ECG: ['0x0']>, ... , <ADPDAppID.APP_ADPD_BLUE: ['0x7']>]
        """
        return [self.APP_PPG, self.APP_ECG, self.APP_TEMPERATURE_THERMISTOR, self.APP_TEMPERATURE_RESISTOR,
                self.APP_ADPD_GREEN, self.APP_ADPD_RED, self.APP_ADPD_INFRARED, self.APP_ADPD_BLUE]

    def get_supported_clocks(self) -> List[Clock]:
        """
        List all supported clocks for ADPD.

        :return: Array of clock ID enums.
        :rtype: List[Clock]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_clocks()
            print(x)
            # [<Clock.NO_CLOCK: ['0x0']>, <Clock.CLOCK_32K: ['0x1']>, ... , <Clock.CLOCK_1M_AND_32M: ['0x6']>]
        """
        return [self.NO_CLOCK, self.CLOCK_32K, self.CLOCK_1M, self.CLOCK_32M, self.CLOCK_32K_AND_1M,
                self.CLOCK_1M_AND_32M]

    def get_supported_devices(self) -> List[ADPDDevice]:
        """
        List all supported devices for ADPD.

        :return: Array of device ID enums.
        :rtype: List[ADPDDevice]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_devices()
            print(x)
            # [<ADPDDevice.DEVICE_GREEN: ['0x28']>, ... , <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>]
        """
        return [self.DEVICE_GREEN, self.DEVICE_RED, self.DEVICE_INFRARED, self.DEVICE_BLUE, self.DEVICE_G_R_IR_B]

    def get_supported_led_ids(self) -> List[ADPDLed]:
        """
        List all supported led IDs for ADPD.

        :return: Array of Led ID enums.
        :rtype: List[ADPDLed]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x4']>, <ADPDLed.LED_MWL: ['0x0']>]
        """
        return [self.LED_GREEN, self.LED_RED, self.LED_IR, self.LED_BLUE, self.LED_MWL]

    def get_supported_slots(self) -> List[ADPDSlot]:
        """
        List all supported slots for ADPD.

        :return: Array of slot ID enums.
        :rtype: List[ADPDSlot]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ... , <ADPDSlot.SLOT_L: ['0xC']>]
        """
        return [self.SLOT_A, self.SLOT_B, self.SLOT_C, self.SLOT_D, self.SLOT_E, self.SLOT_F, self.SLOT_G, self.SLOT_H,
                self.SLOT_I, self.SLOT_J, self.SLOT_K, self.SLOT_L]

    def get_supported_streams(self) -> List[Stream]:
        """
        List all supported streams for ADPD.

        :return: Array of stream ID enums.
        :rtype: List[Stream]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
        """
        return [self.STREAM_ADPD1, self.STREAM_ADPD2, self.STREAM_ADPD3, self.STREAM_ADPD4, self.STREAM_ADPD5,
                self.STREAM_ADPD6, self.STREAM_ADPD7, self.STREAM_ADPD8, self.STREAM_ADPD9, self.STREAM_ADPD10,
                self.STREAM_ADPD11, self.STREAM_ADPD12]

    def get_version(self) -> Dict:
        """
        Returns ADPD version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_version()
            print(x["payload"]["major_version"])
            # 0
            print(x["payload"]["minor_version"])
            # 3
            print(x["payload"]["patch_version"])
            # 1
            print(x["payload"]["version_string"])
            # ADPD_App
            print(x["payload"]["build_version"])
            # TEST ADPD4000_VERSION STRING
        """
        packet = VersionPacket(self._destination, CommonCommand.GET_VERSION_REQ)
        return self._send_packet(packet, CommonCommand.GET_VERSION_RES)

    def load_configuration(self, device_id: ADPDDevice = DEVICE_GREEN) -> Dict:
        """
        Loads specified device id configuration.

        :param device_id: Device ID to load, use get_supported_devices() to list all supported devices.
        :type device_id: ADPDDevice
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5,8

             from adi_study_watch import SDK

             sdk = SDK("COM4")
             application = sdk.get_adpd_application()
             x = application.get_supported_devices()
             print(x)
             # [<ADPDDevice.DEVICE_GREEN: ['0x28']>, ... , <ADPDDevice.DEVICE_G_R_IR_B: ['0x2C']>]
             x = application.load_configuration(application.DEVICE_GREEN)
             print(x["payload"]["device_id"])
             # ADPDDevice.DEVICE_GREEN
         """
        device_id = self._device_helper(device_id)
        packet = ADPDConfigPacket(self._destination, ADPDCommand.LOAD_CONFIG_REQ)
        packet.set_device_id(device_id)
        return self._send_packet(packet, ADPDCommand.LOAD_CONFIG_RES)

    def pause(self) -> Dict:
        """
        Pause ADPDDevice.DEVICE_G_R_IR_B.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.pause()
            print(x["payload"]["device_id"], x["payload"]["pause"])
            # ADPDDevice.DEVICE_G_R_IR_B True
        """
        packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_REQ)
        data = utils.split_int_in_bytes(0, length=10)
        data[0] = 1
        packet.set_data(data)
        return self._send_packet(packet, ADPDCommand.SET_PAUSE_RES)

    def read_device_configuration_block(self) -> [Dict]:
        """
        Returns entire device configuration block.

        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_device_configuration_block()
            print(x["payload"]["dcb_data"])
        """
        packet = DCBPacket(self._destination, DCBCommand.READ_CONFIG_REQ)
        packet.set_dcb_data_size(0)
        packet_id = self._get_packet_id(DCBCommand.READ_CONFIG_RES)
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        count = 1
        result = []
        while True:
            data = self._get_queue_data(queue)
            packet = DCBPacket()
            packet.decode_packet(data)
            dict_packet = packet.get_dict()
            result.append(dict_packet)
            if dict_packet["payload"]["num_of_packets"] == count or dict_packet["payload"]["num_of_packets"] == 0:
                break
            count += 1
        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        return result

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
             - 0x00

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_library_configuration([0x00])
            print(x["payload"]["data"])
            # [['0x0', '0x12C']]
        """
        address_range = [0x00, 0x00]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.READ_LCFG_REQ)
        packet.set_number_of_operations(len(fields))
        utils.check_array_address_range(fields, address_range, 1)
        packet.set_read_fields_data(fields)
        return self._send_packet(packet, CommonCommand.READ_LCFG_RES)

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
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.read_register([0x15, 0x20, 0x2E])
            print(x["payload"]["data"])
            # [['0x15', '0x0'], ['0x20', '0x0'], ['0x2E', '0x0']]
        """
        address_range = [0x00, 0x0277]
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_READ_REQ)
        packet.set_number_of_operations(len(addresses))
        utils.check_array_address_range(addresses, address_range, 2)
        packet.set_read_reg_data(addresses)
        return self._send_packet(packet, CommonCommand.REGISTER_READ_RES)

    def resume(self) -> Dict:
        """
        Resumes ADPDDevice.DEVICE_G_R_IR_B.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.resume()
            print(x["payload"]["device_id"], x["payload"]["pause"])
            # ADPDDevice.DEVICE_G_R_IR_B False
        """
        packet = ADPDPauseResumePacket(self._destination, ADPDCommand.SET_PAUSE_REQ)
        data = utils.split_int_in_bytes(0, length=10)
        packet.set_data(data)
        return self._send_packet(packet, ADPDCommand.SET_PAUSE_RES)

    def set_callback(self, callback_function: Callable, args: Tuple = (), stream: Stream = STREAM_ADPD6) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for specified adpd stream.
        :param args: optional arguments that will be passed with the callback.
        :param stream: Callback for specified stream.
        :type stream: Stream
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            # these optional arguments can be used to pass file, matplotlib or other objects to manipulate data.
            optional_arg1 = "1"
            optional_arg2 = "2"
            application.set_callback(callback, args=(optional_arg1, optional_arg2), stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        if stream == self.STREAM_ADPD1:
            self._callback_function1 = callback_function
            self._args_adpd1 = args
        elif stream == self.STREAM_ADPD2:
            self._callback_function2 = callback_function
            self._args_adpd2 = args
        elif stream == self.STREAM_ADPD3:
            self._callback_function3 = callback_function
            self._args_adpd3 = args
        elif stream == self.STREAM_ADPD4:
            self._callback_function4 = callback_function
            self._args_adpd4 = args
        elif stream == self.STREAM_ADPD5:
            self._callback_function5 = callback_function
            self._args_adpd5 = args
        elif stream == self.STREAM_ADPD6:
            self._callback_function6 = callback_function
            self._args_adpd6 = args
        elif stream == self.STREAM_ADPD7:
            self._callback_function7 = callback_function
            self._args_adpd7 = args
        elif stream == self.STREAM_ADPD8:
            self._callback_function8 = callback_function
            self._args_adpd8 = args
        elif stream == self.STREAM_ADPD9:
            self._callback_function9 = callback_function
            self._args_adpd9 = args
        elif stream == self.STREAM_ADPD10:
            self._callback_function10 = callback_function
            self._args_adpd10 = args
        elif stream == self.STREAM_ADPD11:
            self._callback_function11 = callback_function
            self._args_adpd11 = args
        elif stream == self.STREAM_ADPD12:
            self._callback_function12 = callback_function
            self._args_adpd12 = args

    def set_decimation_factor(self, decimation_factor: int, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Sets decimation factor for specified ADPD stream.

        :param stream: Stream to set decimation factor.
        :type stream: Stream
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
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            x = application.set_decimation_factor(2, application.STREAM_ADPD6)
            print(x["payload"]["decimation_factor"])
            # 2
        """
        stream = self._adpd_stream_helper(stream)
        decimation_factor = utils.range_and_type_check(decimation_factor, type_of=int, lower_and_upper_bound=[1, 5])
        packet = DecimationFactorPacket(self._destination, CommonCommand.SET_STREAM_DEC_FACTOR_REQ)
        packet.set_stream_address(stream)
        packet.set_decimation_factor([decimation_factor])
        return self._send_packet(packet, CommonCommand.SET_STREAM_DEC_FACTOR_RES)

    def set_sampling_frequency(self, odr: int) -> Dict:
        """
        Set ADPD sampling frequency, ODR value in Hz.

        :param odr: ODR frequency in Hz.
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.set_sampling_frequency(100)
            print(x["payload"]["odr"])
            # 100
        """
        odr = utils.range_and_type_check(odr, type_of=int, num_bytes=2)
        packet = SamplingFrequencyPacket(self._destination, ADPDCommand.SET_SAMPLING_FREQUENCY_REQ)
        packet.set_odr(utils.split_int_in_bytes(odr, length=2))
        return self._send_packet(packet, ADPDCommand.SET_SAMPLING_FREQUENCY_RES)

    def set_slot(self, slot_num: ADPDSlot, slot_enable: bool, slot_format: int, channel_num: int) -> Dict:
        """
        Set Slot with slot format.

        :param slot_num: slot_num to set slot, use get_supported_slots() to list all supported slot ID.
        :type slot_num: ADPDSlot
        :param slot_enable: enable or disable slot.
        :type slot_enable: bool
        :param slot_format: format of the slot, possible values are 0,1,2,3,4.
        :type slot_format: int
        :param channel_num: channel for the slot, possible values are 1,3.
        :type channel_num: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_slots()
            print(x)
            # [<ADPDSlot.SLOT_A: ['0x1']>, <ADPDSlot.SLOT_B: ['0x2']>, ..., <ADPDSlot.SLOT_L: ['0xC']>]
            x = application.set_slot(application.SLOT_A, True, 3, 3)
            print(x["payload"]["slot_num"], x["payload"]["slot_enabled"])
            # ADPDSlot.SLOT_A True
            print(x["payload"]["slot_format"], x["payload"]["channel_num"])
            # 3 3

        """
        slot_num = self._slot_helper(slot_num)
        if not (channel_num == 0x1 or channel_num == 0x3):
            logger.warning(f"{'0x%X' % channel_num} is out of range, allowed values are: 1,3")
        slot_format = utils.range_and_type_check(slot_format, type_of=int, lower_and_upper_bound=[0, 4])
        packet = SlotPacket(self._destination, ADPDCommand.SET_SLOT_REQ)
        packet.set_slot_num(slot_num)
        packet.set_slot_enable([slot_enable])
        packet.set_channel_num([channel_num])
        slot_format = utils.split_int_in_bytes(slot_format, length=2)
        packet.set_slot_format(slot_format)
        return self._send_packet(packet, ADPDCommand.SET_SLOT_RES)

    def set_external_stream_sampling_frequency(self, odr: int) -> Dict:
        """
        Set ADPD external stream sampling frequency, ODR value in Hz.

        :param odr: ODR frequency in Hz.
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.set_external_stream_sampling_frequency(50)
            print(x["payload"]["odr"])
            # 100
        """
        odr = utils.range_and_type_check(odr, type_of=int, num_bytes=2, lower_and_upper_bound=[25, 100])
        packet = ExternalStreamODR(self._destination, ADPDCommand.SET_EXT_DATA_STREAM_ODR_REQ)
        packet.set_sampling_frequency(utils.split_int_in_bytes(odr, length=2))
        return self._send_packet(packet, ADPDCommand.SET_EXT_DATA_STREAM_ODR_RES)

    def set_external_stream_data(self, csv_filename: str, start_row: int, column_index: int,
                                 display_progress: bool = False) -> None:
        """
        Set csv file data for external adpd stream.

        :param csv_filename: csv file to load stream data.
        :param start_row: start row index of data.
        :param column_index: column index of data
        :param display_progress: display detail progress bar.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.set_external_stream_data("12104AD0_ADPDAppStream_SlotFChannel2.csv", 6, 2,
                                                    display_progress=True)
        """
        timestamp = []
        data = []
        try:
            with open(csv_filename, 'r') as file:
                index_count = 1
                line = file.readline()
                csv_time = line.split(',')[2].strip()
                tz_seconds = int(line.split(',')[4].strip())
                hours = int(csv_time[0:2])
                minutes = int(csv_time[3:5])
                seconds = int(csv_time[6:8])
                absolute_time_ms = ((hours * 3600) + (minutes * 60) + seconds + tz_seconds) * 1000
                for line in file:
                    line = line.strip().split(",")
                    if index_count >= start_row:
                        timestamp.append(float(line[0].strip()))
                        data.append(int(line[column_index].strip()))
                    index_count += 1
        except Exception as e:
            logger.error(f"Error while reading the {csv_filename} file, reason :: {e}.", exc_info=True)
            return None
        progress_bar = None
        max_ticks_24_hr = 2764800000

        if display_progress:
            progress_bar = tqdm(total=len(data))
        sequence_number = 1
        for timestamp_value, data_value in zip(timestamp, data):
            packet = ExternalStreamData(self._destination, ADPDCommand.EXT_ADPD_DATA_STREAM)
            packet.set_sequence_num(utils.split_int_in_bytes(sequence_number, length=4))
            # converting ms to ticks
            timestamp_value = int(((timestamp_value + absolute_time_ms) * 32.768) % max_ticks_24_hr)
            packet.set_timestamp(utils.split_int_in_bytes(timestamp_value, length=4))
            packet.set_data(utils.split_int_in_bytes(data_value, length=4))
            sequence_number += 1
            time.sleep(0.001)
            if display_progress:
                progress_bar.update(1)
            self._packet_manager.send_packet(packet)
        if display_progress:
            progress_bar.close()
        return None

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
            application = sdk.get_adpd_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Tuple[Dict, Dict]:
        """
        Starts ADPD sensor and also subscribe to the specified ADPD stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        status1 = self.start_sensor()
        status2 = self.subscribe_stream(stream)
        return status1, status2

    def start_sensor(self) -> Dict:
        """
        Starts ADPD sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Tuple[Dict, Dict]:
        """
        Stops ADPD sensor and also Unsubscribe the specified ADPD stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        status1 = self.stop_sensor()
        status2 = self.unsubscribe_stream(stream)
        return status1, status2

    def stop_sensor(self) -> Dict:
        """
        Stops ADPD sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Subscribe to the specified ADPD stream.

        :param stream: Stream to subscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        stream = self._adpd_stream_helper(stream)
        packet = StreamPacket(self._destination, CommonCommand.SUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(stream)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, stream)
        self._packet_manager.subscribe(data_packet_id, self._stream_to_callback[stream])
        date_time = datetime.now()
        ts = (32000.0 * ((date_time.hour * 3600) + (date_time.minute * 60) + date_time.second))
        self._last_timestamp_adpd[stream] = [date_time.timestamp(), ts]
        return self._send_packet(packet, CommonCommand.SUBSCRIBE_STREAM_RES)

    def unsubscribe_stream(self, stream: Stream = STREAM_ADPD6) -> Dict:
        """
        Unsubscribe the specified ADPD stream.

        :param stream: Stream to unsubscribe.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.get_supported_streams()
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.ADPD_OPTIONAL: ['0xC2', '0x1D']>]
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        stream = self._adpd_stream_helper(stream)
        packet = StreamPacket(self._destination, CommonCommand.UNSUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(stream)
        response_packet = self._send_packet(packet, CommonCommand.UNSUBSCRIBE_STREAM_RES)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, stream)
        self._packet_manager.unsubscribe(data_packet_id, self._stream_to_callback[stream])
        return response_packet

    def write_device_configuration_block(self, addresses_values: List[List[int]]) -> [Dict]:
        """
        Writes the device configuration block values of specified addresses.
        This function takes a list of addresses and values to write, and returns a response packet as
        dictionary containing addresses and values.

        :param addresses_values: List of addresses and values to write.
        :type addresses_values: List[List[int]]
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
            print(x["payload"]["size"])
            # 2
        """
        packets = math.ceil(len(addresses_values) / self._dcb_size)
        num_tx = [packets, 0x00]
        addresses_value_array = []
        for packet in range(packets):
            addresses_value_array.append(addresses_values[packet * self._dcb_size:(packet + 1) * self._dcb_size])
        result = []
        for addresses_value in addresses_value_array:
            address_range = [0x00, 0x0277]
            packet = DCBPacket(self._destination, DCBCommand.WRITE_CONFIG_REQ)
            packet.set_size(utils.split_int_in_bytes(len(addresses_value), length=2) + num_tx)
            utils.check_array_address_range(addresses_value, address_range, 2)
            packet.set_dcb_write_data(addresses_value, self._dcb_size, len(addresses_value))
            result.append(self._send_packet(packet, DCBCommand.WRITE_CONFIG_RES))
        return result

    def write_device_configuration_block_from_file(self, filename: str) -> [Dict]:
        """
        Writes the device configuration block values of specified addresses from file.

        :param filename: dcb filename
        :return: A response packet as dictionary.
        :rtype: [Dict]

        .. list-table::
           :widths: 50 50
           :header-rows: 1

           * - Address Lower Limit
             - Address Upper Limit
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            application.write_device_configuration_block_from_file("adpd4000_dcb.dcfg")
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
             - 0x00

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_library_configuration([[0x00, 0x12c]])
            print(x["payload"]["data"])
            # [['0x0', '0x12C']]
        """
        address_range = [0x00, 0x00]
        packet = LibraryConfigReadWritePacket(self._destination, CommonCommand.WRITE_LCFG_REQ)
        packet.set_number_of_operations(len(fields_values))
        utils.check_array_address_range(fields_values, address_range, 2)
        packet.set_write_fields_data(fields_values)
        return self._send_packet(packet, CommonCommand.WRITE_LCFG_RES)

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
           * - 0x0000
             - 0x0277

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
            print(x["payload"]["data"])
            # [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']]
        """
        address_range = [0x00, 0x0277]
        packet = RegisterPacket(self._destination, CommonCommand.REGISTER_WRITE_REQ)
        packet.set_number_of_operations(len(addresses_values))
        utils.check_array_address_range(addresses_values, address_range, 2)
        packet.set_write_reg_data(addresses_values)
        return self._send_packet(packet, CommonCommand.REGISTER_WRITE_RES)

    def _callback_data1(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function1, self._args_adpd1,
                            self._last_timestamp_adpd[Stream.ADPD1])

    def _callback_data2(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function2, self._args_adpd2,
                            self._last_timestamp_adpd[Stream.ADPD2])

    def _callback_data3(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function3, self._args_adpd3,
                            self._last_timestamp_adpd[Stream.ADPD3])

    def _callback_data4(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function4, self._args_adpd4,
                            self._last_timestamp_adpd[Stream.ADPD4])

    def _callback_data5(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function5, self._args_adpd5,
                            self._last_timestamp_adpd[Stream.ADPD5])

    def _callback_data6(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function6, self._args_adpd6,
                            self._last_timestamp_adpd[Stream.ADPD6])

    def _callback_data7(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function7, self._args_adpd7,
                            self._last_timestamp_adpd[Stream.ADPD7])

    def _callback_data8(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function8, self._args_adpd8,
                            self._last_timestamp_adpd[Stream.ADPD8])

    def _callback_data9(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function9, self._args_adpd9,
                            self._last_timestamp_adpd[Stream.ADPD9])

    def _callback_data10(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function10, self._args_adpd10,
                            self._last_timestamp_adpd[Stream.ADPD10])

    def _callback_data11(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function11, self._args_adpd11,
                            self._last_timestamp_adpd[Stream.ADPD11])

    def _callback_data12(self, packet, packet_id):
        self._callback_data(packet, packet_id, self._callback_function12, self._args_adpd12,
                            self._last_timestamp_adpd[Stream.ADPD12])

    def _callback_data(self, packet, packet_id, callback_function=None, args=None, last_timestamp=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, packet_id, ADPDDataPacket(), callback_function, args, last_timestamp)

    def enable_csv_logging(self, filename, header=None, stream: Stream = STREAM_ADPD6) -> None:
        """
        Start logging stream data into CSV.

        :param filename: Name of the CSV file.
        :param header: Header list of the CSV file.
        :param stream: ADPD Stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.enable_csv_logging("adpd6.csv", stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        if header is None:
            if stream == self.STREAM_ADPD1:
                header = ["Slot A", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD2:
                header = ["Slot B", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD3:
                header = ["Slot C", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD4:
                header = ["Slot D", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD5:
                header = ["Slot E", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD6:
                header = ["Slot F", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD7:
                header = ["Slot G", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD8:
                header = ["Slot H", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD9:
                header = ["Slot I", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD10:
                header = ["Slot J", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD11:
                header = ["Slot K", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
            elif stream == self.STREAM_ADPD12:
                header = ["Slot L", "CH1", "CH2", "Timestamp", "D1", "S1", "D2", "S2"]
        self._csv_logger[stream] = CSVLogger(filename, header, write_header=False)

    def disable_csv_logging(self, stream: Stream = STREAM_ADPD6) -> None:
        """
        Stops logging stream data into CSV.

        :param stream: ADPD Stream.
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_adpd_application()
            x = application.disable_csv_logging(stream=application.STREAM_ADPD6)
        """
        stream = self._adpd_stream_helper(stream)
        if self._csv_logger[stream]:
            self._csv_logger[stream].stop_logging()
        self._csv_logger[stream] = None
