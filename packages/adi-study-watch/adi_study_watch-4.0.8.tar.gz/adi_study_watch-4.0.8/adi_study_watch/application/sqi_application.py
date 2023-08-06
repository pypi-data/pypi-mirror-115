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

from .csv_logging import CSVLogger
from .common_stream import CommonStream
from ..core.packets.sqi_packets import SQISlotPacket
from ..core.enums.sqi_enum import SQISlot, SQICommand
from ..core.packets.common_packets import VersionPacket
from ..core.packets.stream_data_packets import SQIDataPacket
from ..core.enums.common_enums import Application, Stream, CommonCommand

logger = logging.getLogger(__name__)


class SQIApplication(CommonStream):
    """
    SQI Application class.

    .. code-block:: python3
        :emphasize-lines: 4

        from adi_study_watch import SDK

        sdk = SDK("COM4")
        application = sdk.get_sqi_application()

    """

    SLOT_F = SQISlot.SLOT_F
    SLOT_G = SQISlot.SLOT_G
    SLOT_H = SQISlot.SLOT_H
    SLOT_I = SQISlot.SLOT_I

    def __init__(self, callback_function, packet_manager, args):
        super().__init__(Application.SQI, Stream.SQI, packet_manager, callback_function, args)

    def get_supported_slots(self) -> List[SQISlot]:
        """
        List all supported slots for SQI.

        :return: Array of slot ID enums.
        :rtype: List

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.get_supported_slots()
            print(x)
            # [<SQISlot.SLOT_F: ['0x6', '0x0']>, ... , <SQISlot.SLOT_I: ['0x9', '0x0']>]

        """
        return [self.SLOT_F, self.SLOT_G, self.SLOT_H, self.SLOT_I]

    def _slot_helper(self, slot_id: SQISlot) -> SQISlot:
        """
        Confirms slot ID is from list of Enums.
        """
        if slot_id in self.get_supported_slots():
            return slot_id
        else:
            logger.warning(f"{slot_id} is not supported slot ID, choosing {self.get_supported_slots()[0]} "
                           f"as default slot ID. use get_supported_slots() to know all supported slot IDs.")
            return self.get_supported_slots()[0]

    def set_slot(self, slot_id: SQISlot) -> Dict:
        """
        Set specified Slot ID for SQI.

        :param slot_id: slot_num to set, use get_supported_slots() to list all supported slot ID.
        :type slot_id: SQISlot
        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.get_supported_slots()
            print(x)
            # [<SQISlot.SLOT_F: ['0x6', '0x0']>, ... , <SQISlot.SLOT_I: ['0x9', '0x0']>]
            x = application.set_slot(application.SLOT_F)
            print(x["payload"]["sqi_slot"])
            # SQISlot.SLOT_F

        """
        slot_id = self._slot_helper(slot_id)
        packet = SQISlotPacket(self._destination, SQICommand.SET_SLOT_REQ)
        packet.set_sqi_slot(slot_id)
        return self._send_packet(packet, SQICommand.SET_SLOT_RES)

    def get_sensor_status(self) -> Dict:
        """
        Returns packet with number of subscribers and number of sensor start request registered.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.get_sensor_status()
            print(x["payload"]["num_subscribers"], x["payload"]["num_start_registered"])
            # 0 0

        """
        return super().get_sensor_status()

    def set_callback(self, callback_function: Callable, args: Tuple = ()) -> None:
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream SQI data.
        :return: None

        .. code-block:: python3
            :emphasize-lines: 4,12

            from adi_study_watch import SDK

            # make sure optional arguments have default value to prevent them causing Exceptions.
            def callback(data, optional1=None, optional2=None):
                print(data)

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
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
            application = sdk.get_sqi_application()
            application.set_timeout(10)

        """
        super().set_timeout(timeout_value)

    def start_and_subscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Starts SQI sensor and also subscribe to the SQI stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            start_sensor, subs_stream = application.start_and_subscribe_stream()
            print(start_sensor["payload"]["status"], subs_stream["payload"]["status"])
            # CommonStatus.STREAM_STARTED CommonStatus.SUBSCRIBER_ADDED
        """
        return super().start_and_subscribe_stream()

    def start_sensor(self) -> Dict:
        """
        Starts SQI sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            start_sensor = application.start_sensor()
            print(start_sensor["payload"]["status"])
            # CommonStatus.STREAM_STARTED
        """
        return super().start_sensor()

    def stop_and_unsubscribe_stream(self) -> Tuple[Dict, Dict]:
        """
        Stops SQI sensor and also Unsubscribe the SQI stream.

        :return: A response packet as dictionary.
        :rtype: Tuple[Dict, Dict]

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            stop_sensor, unsubscribe_stream = application.stop_and_unsubscribe_stream()
            print(stop_sensor["payload"]["status"], unsubscribe_stream["payload"]["status"])
            # CommonStatus.STREAM_STOPPED CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().stop_and_unsubscribe_stream()

    def stop_sensor(self) -> Dict:
        """
        Stops SQI sensor.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            stop_sensor = application.stop_sensor()
            print(stop_sensor["payload"]["status"])
            # CommonStatus.STREAM_STOPPED
        """
        return super().stop_sensor()

    def subscribe_stream(self) -> Dict:
        """
        Subscribe to the SQI stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            subs_stream = application.subscribe_stream()
            print(subs_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_ADDED
        """
        return super().subscribe_stream()

    def unsubscribe_stream(self) -> Dict:
        """
        Unsubscribe the SQI stream.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            unsubscribe_stream = application.unsubscribe_stream()
            print(unsubscribe_stream["payload"]["status"])
            # CommonStatus.SUBSCRIBER_REMOVED
        """
        return super().unsubscribe_stream()

    def get_version(self) -> Dict:
        """
        Returns SQI version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
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
        Returns SQI version info.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
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
        packet = VersionPacket(self._destination, SQICommand.GET_ALGO_VENDOR_VERSION_REQ)
        return self._send_packet(packet, SQICommand.GET_ALGO_VENDOR_VERSION_RES)

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        self._callback_data_helper(packet, packet_id, SQIDataPacket(), callback_function, args)

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
            application = sdk.get_sqi_application()
            x = application.enable_csv_logging("sqi.csv")
        """
        if header is None:
            header = ["Timestamp", "SQI"]
        self._csv_logger[Stream.SQI] = CSVLogger(filename, header)

    def disable_csv_logging(self) -> None:
        """
        Stops logging stream data into CSV.

        :return: A response packet as dictionary.
        :rtype: Dict

        .. code-block:: python3
            :emphasize-lines: 5

            from adi_study_watch import SDK

            sdk = SDK("COM4")
            application = sdk.get_sqi_application()
            x = application.disable_csv_logging()
        """
        if self._csv_logger[Stream.SQI]:
            self._csv_logger[Stream.SQI].stop_logging()
        self._csv_logger[Stream.SQI] = None
