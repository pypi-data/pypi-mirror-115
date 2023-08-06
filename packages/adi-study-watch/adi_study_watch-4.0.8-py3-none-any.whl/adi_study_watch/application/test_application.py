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
from typing import List, Dict, Callable, Optional

from tqdm import tqdm

from ..core import utils
from .fs_application import FSApplication
from ..core.enums.ppg_enums import PPGCommand
from ..core.enums.bcm_enums import BCMCommand
from ..core.enums.adxl_enums import ADXLCommand
from .common_application import CommonApplication
from ..core.enums.fs_enums import FSCommand, FSStatus
from ..core.packets.ppg_packets import PPGStatesPacket
from ..core.packets.command_packet import CommandPacket
from ..core.packets.display_packets import DisplayPacket
from ..core.enums.adpd_enums import ADPDCommand, ADPDLed
from ..core.packets.adxl_packets import ADXLConfigPacket
from ..core.enums.display_enums import DisplayColor, DisplayCommand
from ..core.packets.adpd_packets import AgcInfoPacket, TestCommandPacket
from ..core.packets.bcm_packets import FdsStatusPacket, DCBTimingInfoPacket
from ..core.enums.pm_enums import PMCommand, PowerMode, LDO, ElectrodeSwitch
from ..core.enums.common_enums import Application, CommonCommand, Stream, CommonStatus
from ..core.packets.pm_packets import LDOControlPacket, SwitchControlPacket, PingPacket
from ..core.packets.fs_packets import PatternWritePacket, DebugInfoPacket, BadBlockPacket
from ..core.packets.fs_packets import StreamDebugInfoPacket, FileInfoPacket, PageInfoPacket
from ..core.packets.stream_data_packets import KeyStreamDataPacket, CapSenseStreamDataPacket
from ..core.packets.pm_packets import AppsHealthPacket, ControlPacket, PowerStatePacket, BatteryThresholdPacket

logger = logging.getLogger(__name__)


class TestApplication(CommonApplication):
    WHITE = DisplayColor.WHITE
    BLACK = DisplayColor.BLACK
    RED = DisplayColor.RED
    GREEN = DisplayColor.GREEN
    BLUE = DisplayColor.BLUE

    POWER_MODE_ACTIVE = PowerMode.ACTIVE
    POWER_MODE_HIBERNATE = PowerMode.HIBERNATE
    POWER_MODE_SHUTDOWN = PowerMode.SHUTDOWN

    LDO_FS = LDO.FS
    LDO_OPTICAL = LDO.OPTICAL
    LDO_EPHYZ = LDO.EPHYZ

    SWITCH_AD8233 = ElectrodeSwitch.AD8233
    SWITCH_AD5940 = ElectrodeSwitch.AD5940
    SWITCH_ADPD4000 = ElectrodeSwitch.ADPD4000

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
    STREAM_ADXL = Stream.ADXL
    STREAM_BCM = Stream.BCM
    STREAM_ECG = Stream.ECG
    STREAM_EDA = Stream.EDA
    STREAM_PEDOMETER = Stream.PEDOMETER
    STREAM_PPG = Stream.PPG
    STREAM_TEMPERATURE = Stream.TEMPERATURE
    STREAM_SYNC_PPG = Stream.SYNC_PPG
    STREAM_SQI = Stream.SQI

    LED_MWL = ADPDLed.LED_MWL
    LED_GREEN = ADPDLed.LED_GREEN
    LED_RED = ADPDLed.LED_RED
    LED_IR = ADPDLed.LED_IR
    LED_BLUE = ADPDLed.LED_BLUE

    def __init__(self, key_press_callback_function, cap_sense_callback_function, packet_manager):
        super().__init__(Application.FS, packet_manager)
        self._key_press_callback = key_press_callback_function
        self._cap_sense_callback = cap_sense_callback_function

    # PM
    def flash_reset(self) -> Dict:
        """
        Resets device flash.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.flash_reset()
            print(x["payload"]["status"])
            # PMStatus.OK

        """
        packet = CommandPacket(Application.PM, PMCommand.FLASH_RESET_REQ)
        return self._send_packet(packet, PMCommand.FLASH_RESET_RES)

    def get_supported_power_states(self) -> List[PowerMode]:
        """
        List all supported power states for PM.

        :return: Array of power states enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_power_states()
            print(x)
            # [<PowerState.ACTIVE_MODE: ['0x0']>, ... , <PowerState.SHUTDOWN_MODE: ['0x3']>]
        """
        return [self.POWER_MODE_ACTIVE, self.POWER_MODE_HIBERNATE, self.POWER_MODE_SHUTDOWN]

    def _power_mode_helper(self, power_mode: PowerMode) -> PowerMode:
        """
        Confirms power mode is from list of Enums.
        """
        if power_mode in self.get_supported_power_states():
            return power_mode
        else:
            logger.warning(
                f"{power_mode} is not supported power mode, choosing {self.get_supported_power_states()[0]} "
                f"as default power mode. use get_supported_power_states() to know all supported power modes.")
            return self.get_supported_power_states()[0]

    def set_power_mode(self, power_state: PowerMode) -> Dict:
        """
        Set specified power state to PM.

        :param power_state: power state to set, use get_supported_power_states() to list all supported power states.
        :type power_state: PowerMode
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_power_states()
            print(x)
            # [<PowerState.ACTIVE_MODE: ['0x0']>, ... , <PowerState.SHUTDOWN_MODE: ['0x3']>]
            x = application.set_power_mode(application.ACTIVE_MODE)
            print(x["payload"]["power_state"])
            # PowerState.ACTIVE_MODE

        """
        power_state = self._power_mode_helper(power_state)
        packet = PowerStatePacket(Application.PM, PMCommand.SET_POWER_STATE_REQ)
        packet.set_state(power_state)
        return self._send_packet(packet, PMCommand.SET_POWER_STATE_RES)

    def set_battery_threshold(self, low_level: int, critical_level: int) -> Dict:
        """
        Set low and critical level threshold for device battery.

        :param low_level: low level threshold for device battery.
        :type low_level: int
        :param critical_level: critical level threshold for device battery.
        :type critical_level: int
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.set_battery_threshold(20, 5)
            print(x["payload"]["status"])
            # PMStatus.OK

        """
        low_level = utils.range_and_type_check(low_level, type_of=int, lower_and_upper_bound=[0, 100])
        critical_level = utils.range_and_type_check(critical_level, type_of=int, lower_and_upper_bound=[0, 100])
        packet = BatteryThresholdPacket(Application.PM, PMCommand.SET_BAT_THR_REQ)
        packet.set_low_level([low_level])
        packet.set_critical_level([critical_level])
        return self._send_packet(packet, PMCommand.SET_BAT_THR_RES)

    def get_supported_ldo(self) -> List[LDO]:
        """
        List all supported ldo for PM.

        :return: Array of ldo enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
        """
        return [self.LDO_FS, self.LDO_OPTICAL, self.LDO_EPHYZ]

    def _ldo_helper(self, ldo_id: LDO) -> LDO:
        """
        Confirms ldo id is from list of Enums.
        """
        if ldo_id in self.get_supported_ldo():
            return ldo_id
        else:
            logger.warning(f"{ldo_id} is not supported ldo id, choosing {self.get_supported_ldo()[0]} "
                           f"as default ldo id. use get_supported_ldo() to know all supported ldo IDs")
            return self.get_supported_ldo()[0]

    def disable_ldo(self, ldo_id: LDO) -> Dict:
        """
        Disables specified ldo ID.

        :param ldo_id: ldo ID to disable, use get_supported_ldo() to list all supported ldo IDs.
        :type ldo_id: LDO
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
            x = application.disable_ldo(application.LDO_OPTICAL)
            print(x["payload"]["ldo_name"], x["payload"]["enabled"])
            # LDO.OPTICAL False

        """
        ldo_id = self._ldo_helper(ldo_id)
        packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_REQ)
        packet.set_name(ldo_id)
        packet.set_enable([0x0])
        return self._send_packet(packet, PMCommand.LDO_CONTROL_RES)

    def enable_ldo(self, ldo_id: LDO) -> Dict:
        """
        Enables specified ldo ID.

        :param ldo_id: ldo ID to enable, use get_supported_ldo() to list all supported ldo IDs.
        :type ldo_id: LDO
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_ldo()
            print(x)
            # [<LDO.LDO_FS: ['0x1']>, <LDO.OPTICAL_LDO: ['0x2']>, <LDO.LDO_EPHYZ: ['0x3']>]
            x = application.enable_ldo(application.LDO_OPTICAL)
            print(x["payload"]["ldo_name"], x["payload"]["enabled"])
            # LDO.OPTICAL True

        """
        ldo_id = self._ldo_helper(ldo_id)
        packet = LDOControlPacket(Application.PM, PMCommand.LDO_CONTROL_REQ)
        packet.set_name(ldo_id)
        packet.set_enable([0x1])
        return self._send_packet(packet, PMCommand.LDO_CONTROL_RES)

    def _switch_helper(self, switch_id: ElectrodeSwitch) -> ElectrodeSwitch:
        """
        Confirms switch id is from list of Enums.
        """
        if switch_id in self.get_supported_switches():
            return switch_id
        else:
            logger.warning(f"{switch_id} is not supported switch id, choosing {self.get_supported_switches()[0]} "
                           f"as default switch id. use get_supported_switches() to know all supported switch IDs")
            return self.get_supported_switches()[0]

    def get_supported_switches(self) -> List[ElectrodeSwitch]:
        """
        List all supported switches for PM.

        :return: Array of switches enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.SWITCH_AD8233: ['0x0']>, ... , <ElectrodeSwitch.SWITCH_ADPD4000: ['0x2']>]
        """
        return [self.SWITCH_AD8233, self.SWITCH_AD5940, self.SWITCH_ADPD4000]

    def enable_electrode_switch(self, switch_name: ElectrodeSwitch) -> Dict:
        """
        Enables specified electrode switch.

        :param switch_name: electrode switch to enable, use get_supported_switches() to list all supported switches.
        :type switch_name: ElectrodeSwitch
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.AD8233_SWITCH: ['0x0']>, ... , <ElectrodeSwitch.ADPD4000_SWITCH: ['0x2']>]
            x = application.enable_electrode_switch(application.SWITCH_AD5940)
            print(x["payload"]["switch_name"], x["payload"]["enabled"])
            # ElectrodeSwitch.AD5940 True

        """
        switch_name = self._switch_helper(switch_name)
        packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_REQ)
        packet.set_name(switch_name)
        packet.set_enable([0x1])
        return self._send_packet(packet, PMCommand.SW_CONTROL_RES)

    def disable_electrode_switch(self, switch_name: ElectrodeSwitch) -> Dict:
        """
        Disables specified electrode switch.

        :param switch_name: electrode switch to disable, use get_supported_switches() to list all supported switches.
        :type switch_name: ElectrodeSwitch
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_switches()
            print(x)
            # [<ElectrodeSwitch.AD8233_SWITCH: ['0x0']>, ... , <ElectrodeSwitch.ADPD4000_SWITCH: ['0x2']>]
            x = application.disable_electrode_switch(application.SWITCH_AD5940)
            print(x["payload"]["switch_name"], x["payload"]["enabled"])
            # ElectrodeSwitch.AD5940 False

        """
        switch_name = self._switch_helper(switch_name)
        packet = SwitchControlPacket(Application.PM, PMCommand.SW_CONTROL_REQ)
        packet.set_name(switch_name)
        packet.set_enable([0x0])
        return self._send_packet(packet, PMCommand.SW_CONTROL_RES)

    def get_apps_health_status(self) -> Dict:
        """
        Returns ISR count of ad5940, adpd, adxl.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_apps_health_status()
            print(x["payload"]["ad5940_isr_count"], x["payload"]["adpd_isr_count"], x["payload"]["adxl_isr_count"])
            # 0 0 0
        """
        packet = AppsHealthPacket(Application.PM, PMCommand.GET_APPS_HEALTH_REQ)
        return self._send_packet(packet, PMCommand.GET_APPS_HEALTH_RES)

    def disable_cap_sense_test(self) -> Dict:
        """
        Disable cap sense test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.disable_cap_sense_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_REQ)
        packet.set_enable([0x0])
        response_packet = self._send_packet(packet, PMCommand.CAP_SENSE_TEST_RES)
        data_packet_id = self._get_packet_id(PMCommand.CAP_SENSE_STREAM_DATA, packet.get_destination())
        self._packet_manager.unsubscribe(data_packet_id, self._cap_sense_callback_data)
        return response_packet

    def enable_cap_sense_test(self) -> Dict:
        """
        Enables cap sense test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_cap_sense_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = ControlPacket(Application.PM, PMCommand.CAP_SENSE_TEST_REQ)
        packet.set_enable([0x1])
        data_packet_id = self._get_packet_id(PMCommand.CAP_SENSE_STREAM_DATA, packet.get_destination())
        self._packet_manager.subscribe(data_packet_id, self._cap_sense_callback_data)
        return self._send_packet(packet, PMCommand.CAP_SENSE_TEST_RES)

    def set_cap_sense_callback(self, callback_function: Callable) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for stream key test data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 7

            from adi_study_watch import SDK

            def callback(data):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.set_cap_sense_callback(callback)
        """
        self._cap_sense_callback = callback_function

    def _cap_sense_callback_data(self, packet, packet_id) -> None:
        """
        Callback for data packets.
        """
        if self._cap_sense_callback:
            try:
                response_packet = CapSenseStreamDataPacket()
                response_packet.decode_packet(packet)
                self._cap_sense_callback(response_packet.get_dict())
            except Exception as e:
                logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)
        else:
            logger.warning("No callback function provided")

    def ping(self, num_pings: int, packet_size: int) -> List[Dict]:
        """
        Pings the device to send response of specified packet size and specified times (num_pings).

        :param num_pings: number of times packets to be sent from device.
        :type num_pings: int
        :param packet_size: size of the ping packet from device, must be between 15 and 244.
        :type packet_size: int
        :return: list of response packet as dictionary.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.ping(3, 16)
            for packet in x:
                print(packet["payload"]["sequence_num"])
            # 1
            # 2
            # 3

        """
        packet_size = utils.range_and_type_check(packet_size, type_of=int, lower_and_upper_bound=[15, 244])
        num_pings = utils.range_and_type_check(num_pings, type_of=int, num_bytes=4)
        packet = PingPacket(Application.PM, CommonCommand.PING_REQ)
        num_pings_arr = utils.split_int_in_bytes(num_pings, length=4)
        packet.set_num_pings(num_pings_arr)
        packet_size = utils.split_int_in_bytes(packet_size, length=2, reverse=True)
        packet.set_packet_size(packet_size)
        packet_id = self._get_packet_id(CommonCommand.PING_RES, packet.get_destination())
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, self._callback_command)
        self._packet_manager.send_packet(packet)
        result = []
        for _ in range(num_pings):
            start_time = time.time()
            data = self._get_queue_data(queue)
            packet = PingPacket()
            packet.decode_packet(data)
            packet_dict = packet.get_dict()
            elapsed_time = time.time() - start_time
            packet_dict["payload"]["elapsed_time"] = elapsed_time
            result.append(packet_dict)

        self._packet_manager.unsubscribe(packet_id, self._callback_command)
        return result

    # BCM
    def get_fds_status(self) -> Dict:
        """
        FDS status.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.get_fds_status()
        """
        packet = FdsStatusPacket(Application.BCM, BCMCommand.FDS_STATUS_REQ)
        return self._send_packet(packet, BCMCommand.FDS_STATUS_RES)

    def read_device_configuration_block_info(self) -> Dict:
        """
        Read Device config block info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.read_device_configuration_block_info()
        """
        packet = DCBTimingInfoPacket(Application.BCM, BCMCommand.DCB_TIMING_INFO_REQ)
        return self._send_packet(packet, BCMCommand.DCB_TIMING_INFO_RES)

    # FS
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
            application = sdk.get_test_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... ]
        """
        return [self.STREAM_ADPD1, self.STREAM_ADPD2, self.STREAM_ADPD3, self.STREAM_ADPD4, self.STREAM_ADPD5,
                self.STREAM_ADPD6, self.STREAM_ADPD7, self.STREAM_ADPD8, self.STREAM_ADPD9, self.STREAM_ADPD10,
                self.STREAM_ADPD11, self.STREAM_ADPD12, self.STREAM_ADXL, self.STREAM_SQI, self.STREAM_ECG,
                self.STREAM_EDA, self.STREAM_PEDOMETER, self.STREAM_PPG, self.STREAM_BCM, self.STREAM_TEMPERATURE,
                self.STREAM_SYNC_PPG]

    def pattern_write(self, file_size: int, scale_type: int, scale_factor: int, base: int,
                      num_files_to_write: int, display_progress=False) -> List[Dict]:
        """
        Pattern Write.
        16384 0 2 1 2 (linear scale)
        16384 1 2 2 2 (log scale)
        16384 2 2 2 2 (exp scale)

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.pattern_write(16384, 0, 2, 1, 2)
        """
        result = []
        progress_bar = None
        file_count = 0
        if display_progress:
            progress_bar = tqdm(total=num_files_to_write)
        while file_count < num_files_to_write:
            packet = PatternWritePacket(Application.FS, FSCommand.PATTERN_WRITE_REQ)
            file_size_arr = utils.split_int_in_bytes(file_size, length=4)
            scale_factor_arr = utils.split_int_in_bytes(scale_factor, length=2)
            num_files_to_write_arr = utils.split_int_in_bytes(num_files_to_write, length=2)
            packet.set_pattern_data(file_size_arr, [scale_type], scale_factor_arr, num_files_to_write_arr)
            response_packet = self._send_packet(packet, FSCommand.PATTERN_WRITE_RES)
            result.append(response_packet)
            if response_packet["payload"]["status"] == CommonStatus.OK:
                if scale_type == 0:
                    file_size *= scale_factor
                elif scale_type == 1 and not scale_factor == 1:
                    file_size *= int(math.log(base, scale_factor))
                elif scale_type == 2:
                    file_size *= int(math.exp(scale_factor))
            else:
                if response_packet["payload"]["status"] == FSStatus.ERR_MEMORY_FULL:
                    logger.error("Memory full breaking loop as new files cannot be written!")
                    break
                elif response_packet["payload"]["status"] == FSStatus.ERR_MAX_FILE_COUNT:
                    logger.error("Max file count crossed!")
                    break
            file_count += 1
            if display_progress:
                progress_bar.update(1)
        if display_progress:
            progress_bar.close()
        return result

    def fs_log_test(self) -> Dict:
        """
        Log test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.fs_log_test()
        """
        packet = CommandPacket(Application.FS, FSCommand.TEST_LOG_REQ)
        return self._send_packet(packet, FSCommand.TEST_LOG_RES)

    def get_debug_info(self) -> Dict:
        """
        Returns debug info of FS.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_debug_info()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = DebugInfoPacket(Application.FS, FSCommand.GET_DEBUG_INFO_REQ)
        return self._send_packet(packet, FSCommand.GET_DEBUG_INFO_RES)

    def get_bad_blocks(self) -> Dict:
        """
        Returns a packet containing number of bad blocks in the file system.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_bad_blocks()
            print(x["payload"]["bad_blocks"])
            # 0
        """
        packet = BadBlockPacket(Application.FS, FSCommand.GET_BAD_BLOCKS_REQ)
        return self._send_packet(packet, FSCommand.GET_BAD_BLOCKS_RES)

    def get_stream_debug_info(self, stream: Stream) -> Dict:
        """
        Returns specified stream debug info of FS.

        :param stream: stream to obtain debug info, use get_supported_streams() to list all supported streams.
        :type stream: Stream
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_streams()
            print(x)
            # [<Stream.ADPD1: ['0xC2', '0x11']>, ... , <Stream.SQI: ['0xC8', '0x0D']>]
            x = application.get_stream_debug_info(application.STREAM_ADXL)
            print(x["payload"]["stream_address"], x["payload"]["packets_received"], x["payload"]["packets_missed"])
            # Stream.ADXL 0 0
        """
        stream = self._stream_helper(stream)
        packet = StreamDebugInfoPacket(Application.FS, FSCommand.STREAM_DEBUG_INFO_REQ)
        packet.set_stream_address(stream)
        return self._send_packet(packet, FSCommand.STREAM_DEBUG_INFO_RES)

    def get_file_info(self, file_index: int) -> Dict:
        """
        File info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_file_info(4)

        """
        packet = FileInfoPacket(Application.FS, FSCommand.GET_FILE_INFO_REQ)
        packet.set_file_index(file_index)
        return self._send_packet(packet, FSCommand.GET_FILE_INFO_RES)

    def file_read_test(self, filename: str) -> Optional[dict]:
        """
        File read test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.file_read_test("03124671.LOG")

        """
        fs_app = FSApplication(self._packet_manager)
        files = fs_app.ls()
        file_index = 0
        file_found = False
        for file in files:
            if not file_found:
                file_index += 1
            if file["payload"]["filename"] == filename:
                file_found = True
        if not file_found:
            logger.error(f"{filename} is not present on the device, use ls() to list all the files.")
            return None
        response_packet = self.get_file_info(file_index)
        return response_packet

    def page_read_test(self, page_num: int, num_bytes: int) -> Dict:
        """
        Page read test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.page_read_test(300, 20)

        """
        utils.range_and_type_check(page_num, type_of=int, num_bytes=4)
        utils.range_and_type_check(num_bytes, type_of=int, num_bytes=1)
        packet = PageInfoPacket(Application.FS, FSCommand.PAGE_READ_TEST_REQ)
        packet.set_page_num(utils.split_int_in_bytes(page_num, length=4))
        packet.set_num_bytes(num_bytes)
        return self._send_packet(packet, FSCommand.PAGE_READ_TEST_RES)

    # Display
    def get_supported_display_colors(self) -> List[DisplayColor]:
        """
        List all supported Display colors for Display Application.

        :return: Array of Display color enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_display_colors()
            print(x)
            # [<DisplayColor.WHITE: ['0x0']>, <DisplayColor.BLACK: ['0x1']>, ... , <DisplayColor.BLUE: ['0x4']>]
        """
        return [self.WHITE, self.BLACK, self.RED, self.GREEN, self.BLUE]

    def _color_helper(self, color: DisplayColor) -> DisplayColor:
        """
        Confirms color is from list of Enums.
        """
        if color in self.get_supported_display_colors():
            return color
        else:
            logger.warning(
                f"{color} is not supported display color, choosing {self.get_supported_display_colors()[0]} "
                f"as default display color. use get_supported_display_colors() to know all supported colors.")
            return self.get_supported_display_colors()[0]

    def disable_back_light(self) -> Dict:
        """
        Disables the back light of the watch.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.disable_back_light()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = DisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_REQ)
        packet.set_data([0x0])
        return self._send_packet(packet, DisplayCommand.BACKLIGHT_CONTROL_RES)

    def disable_key_press_test(self) -> Dict:
        """"
        Disables and unsubscribe to key press test data.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_key_press_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = DisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_REQ)
        packet.set_data([0x0])
        response_packet = self._send_packet(packet, DisplayCommand.KEY_TEST_RES)
        data_packet_id = self._get_packet_id(DisplayCommand.KEY_STREAM_DATA, packet.get_destination())
        self._packet_manager.unsubscribe(data_packet_id, self._key_press_callback_data)
        return response_packet

    def enable_key_press_test(self) -> Dict:
        """"
        Enables and subscribe to key press test data.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_key_press_test()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = DisplayPacket(Application.DISPLAY, DisplayCommand.KEY_TEST_REQ)
        packet.set_data([0x1])
        data_packet_id = self._get_packet_id(DisplayCommand.KEY_STREAM_DATA, packet.get_destination())
        self._packet_manager.subscribe(data_packet_id, self._key_press_callback_data)
        return self._send_packet(packet, DisplayCommand.KEY_TEST_RES)

    def enable_back_light(self) -> Dict:
        """"
        Enables the back light of the watch.

        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.enable_back_light()
            print(x["payload"]["status"])
            # CommonStatus.OK
        """
        packet = DisplayPacket(Application.DISPLAY, DisplayCommand.BACKLIGHT_CONTROL_REQ)
        packet.set_data([0x1])
        return self._send_packet(packet, DisplayCommand.BACKLIGHT_CONTROL_RES)

    def set_display_color(self, color: DisplayColor) -> Dict:
        """
        Set the specified color to watch screen, to check for pixel damage.

        :param color: color to set on watch screen, use get_supported_display_colors() to list all supported colors.
        :type color: DisplayColor
        :return: A response packet as dictionary
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_display_colors()
            print(x)
            # [<DisplayColor.WHITE: ['0x0']>, <DisplayColor.BLACK: ['0x1']>, ... , <DisplayColor.BLUE: ['0x4']>]
            x = application.set_display_color(application.BLUE)
            print(x["payload"]["color"])
            # DisplayColor.BLUE
        """
        color = self._color_helper(color)
        packet = DisplayPacket(Application.DISPLAY, DisplayCommand.SET_DISPLAY_REQ)
        packet.set_data(color.value)
        return self._send_packet(packet, DisplayCommand.SET_DISPLAY_RES)

    def _key_press_callback_data(self, packet, packet_id) -> None:
        """
        Callback for key test
        """
        if self._key_press_callback:
            try:
                response_packet = KeyStreamDataPacket()
                response_packet.decode_packet(packet)
                self._key_press_callback(response_packet.get_dict())
            except Exception as e:
                logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)
        else:
            logger.warning("No callback function provided.")

    def set_key_press_callback(self, callback_function: Callable) -> None:
        """
        Sets the callback for the stream data.

        :param callback_function: callback function for stream key test data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 7

            from adi_study_watch import SDK

            def callback(data):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            application.set_callback(callback)

        """
        self._key_press_callback = callback_function

    # ADPD
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

    def get_supported_led_ids(self) -> List[ADPDLed]:
        """
        List all supported led IDs for ADPD.

        :return: Array of Led ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_MWL: ['0x0']>, <ADPDLed.LED_GREEN: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x4']>]
        """
        return [self.LED_MWL, self.LED_GREEN, self.LED_RED, self.LED_IR, self.LED_BLUE]

    def get_agc_info(self, led_index: ADPDLed) -> Dict:
        """
        Returns AGC info of specified led index.

        :param led_index: led_index to obtain info, use get_supported_led_ids() to list all supported led ID.
        :type led_index: ADPDLed
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_supported_led_ids()
            print(x)
            # [<ADPDLed.LED_GREEN: ['0x0']>, <ADPDLed.LED_RED: ['0x1']>, ... , <ADPDLed.LED_BLUE: ['0x3']>]
            x = application.get_agc_info(application.LED_GREEN)
            print(x["payload"]["led_index"])
            # ADPDLed.LED_GREEN
            print(x["payload"]["ch1"])
            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            print(x["payload"]["ch2"])
            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            print(x["payload"]["dc0_led_current"])
            # 0
            print(x["payload"]["tia_ch1"])
            # 0
            print(x["payload"]["tia_ch2"])
            # 0
        """
        led_index = self._led_helper(led_index)
        packet = AgcInfoPacket(Application.ADPD, ADPDCommand.AGC_INFO_REQ)
        packet.set_led_index(led_index)
        return self._send_packet(packet, ADPDCommand.AGC_INFO_RES)

    def test_command1(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command1()

        """
        packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST1_REQ)
        data = utils.split_int_in_bytes(data, length=12)
        packet.set_data(data)
        return self._send_packet(packet, ADPDCommand.COMMAND_DO_TEST1_RES)

    def test_command2(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command2()

        """
        packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST2_REQ)
        data = utils.split_int_in_bytes(data, length=12)
        packet.set_data(data)
        return self._send_packet(packet, ADPDCommand.COMMAND_DO_TEST2_RES)

    def test_command3(self, data: int) -> Dict:
        """
        ADPD test command.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.test_command3()

        """
        packet = TestCommandPacket(Application.ADPD, ADPDCommand.COMMAND_DO_TEST3_REQ)
        data = utils.split_int_in_bytes(data, length=12)
        packet.set_data(data)
        return self._send_packet(packet, ADPDCommand.COMMAND_DO_TEST3_RES)

    # PPG
    def get_ppg_states(self) -> Dict:
        """
        Get PPG states.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.get_states()
            print(x["payload"]["states"])
            # [0,0,0, ... ,0,0]

        """
        packet = PPGStatesPacket(Application.PPG, PPGCommand.GET_LAST_STATES_REQ)
        return self._send_packet(packet, PPGCommand.GET_LAST_STATES_RES)

    # ADXL
    def adxl_self_test(self) -> Dict:
        """
        ADXL self test.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_test_application()
            x = application.adxl_self_test()

        """
        packet = ADXLConfigPacket(Application.ADXL, ADXLCommand.SELF_TEST_REQ)
        return self._send_packet(packet, ADXLCommand.SELF_TEST_RES)
