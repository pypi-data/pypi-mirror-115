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

from .common_application import CommonApplication
from ..core.enums.common_enums import CommonCommand
from ..core.packets.common_packets import StreamPacket, StreamStatusPacket

logger = logging.getLogger(__name__)


class CommonStream(CommonApplication):
    """
    A Common Stream class for streaming data from sensors.
    """

    def __init__(self, destination, stream, packet_manager, callback_function, args):
        """
        Initialize the common stream packet variable.

        :param destination: Address of the application.
        :param stream: Address of stream.
        :param packet_manager: PacketManager Object.
        :param callback_function: callback function for stream.
        """
        super().__init__(destination, packet_manager)
        self._args = args
        self._stream = stream
        self._last_timestamp = []
        self._csv_logger = {self._stream: None}
        self._callback_function = callback_function

    def set_callback(self, callback_function, args=()):
        """
        Sets the callback for the stream data.

        :param args: optional arguments that will be passed with the callback.
        :param callback_function: callback function for stream data.
        """
        self._callback_function = callback_function
        self._args = args

    def _callback_data(self, packet, packet_id, callback_function=None, args=None):
        """
        Process and returns the data back to user's callback function.
        """
        pass

    def _callback_data_helper(self, packet, packet_id, response_packet, callback_function=None, args=None,
                              last_timestamp=None):
        """
        Process and returns the data back to user's callback function.
        """
        callback_function = callback_function if callback_function else self._callback_function
        args = args if args else self._args
        response_packet.decode_packet(packet)
        last_timestamp = self._last_timestamp if last_timestamp is None else last_timestamp
        response_packet.update_timestamp(last_timestamp)
        result = response_packet.get_dict()
        if self._csv_logger[result["header"]["source"]]:
            self._csv_logger[result["header"]["source"]].add_row(result, last_timestamp[0])
        if callback_function:
            try:
                callback_function(result, *args)
            except Exception as e:
                logger.error(f"Can't send packet back to user callback function, reason :: {e}", exc_info=True)
        else:
            if self._csv_logger[result["header"]["source"]]:
                pass
            else:
                logger.warning(f"No callback function provided for {result['header']['source']}")

    def get_sensor_status(self):
        """
        Returns packet with sensor status.
        """
        packet = StreamStatusPacket(self._destination, CommonCommand.GET_SENSOR_STATUS_REQ)
        packet.set_stream_address(self._destination)
        return self._send_packet(packet, CommonCommand.GET_SENSOR_STATUS_RES)

    def start_and_subscribe_stream(self):
        """
        Start sensor and subscribe to stream
        """
        status2 = self.subscribe_stream()
        status1 = self.start_sensor()
        return status1, status2

    def start_sensor(self):
        """
        Starts the specified sensor.
        """
        packet = StreamPacket(self._destination, CommonCommand.START_SENSOR_REQ)
        return self._send_packet(packet, CommonCommand.START_SENSOR_RES)

    def stop_and_unsubscribe_stream(self):
        """
        Stop sensor and unsubscribe to stream
        """
        status1 = self.stop_sensor()
        status2 = self.unsubscribe_stream()
        return status1, status2

    def stop_sensor(self):
        """
        Stops the specified sensor
        """
        packet = StreamPacket(self._destination, CommonCommand.STOP_SENSOR_REQ)
        return self._send_packet(packet, CommonCommand.STOP_SENSOR_RES)

    def subscribe_stream(self):
        """
        Subscribe to specified stream.
        """
        packet = StreamPacket(self._destination, CommonCommand.SUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(self._stream)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._stream)
        self._packet_manager.subscribe(data_packet_id, self._callback_data)
        date_time = datetime.now()
        ts = (32000.0 * ((date_time.hour * 3600) + (date_time.minute * 60) + date_time.second))
        self._last_timestamp = [date_time.timestamp(), ts]
        return self._send_packet(packet, CommonCommand.SUBSCRIBE_STREAM_RES)

    def unsubscribe_stream(self):
        """
        Unsubscribe from specified stream.
        """
        packet = StreamPacket(self._destination, CommonCommand.UNSUBSCRIBE_STREAM_REQ)
        packet.set_stream_address(self._stream)
        response_packet = self._send_packet(packet, CommonCommand.UNSUBSCRIBE_STREAM_RES)
        data_packet_id = self._get_packet_id(CommonCommand.STREAM_DATA, self._stream)
        self._packet_manager.unsubscribe(data_packet_id, self._callback_data)
        return response_packet
