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
from queue import Queue

from ..core import utils

logger = logging.getLogger(__name__)


class CommonApplication:
    """
    A Common Application class.
    """

    def __init__(self, destination, packet_manager):
        """
        Initialize the common application class.

        :param destination: Address of the application.
        :param packet_manager: PacketManager Object.
        """
        self._destination = destination
        self._packet_manager = packet_manager
        self._packet_queues = {}
        self._timeout = 10

    def _get_packet_id(self, response_command, destination=None):
        """
        Generates a unique packet ID.
        """
        destination = destination if destination else self._destination
        packet_id = utils.join_multi_length_packets(destination.value + response_command.value)
        return packet_id

    def _get_queue(self, packet_id):
        """
        Returns specified queue for packet ID.
        """
        queue = self._packet_queues.get(packet_id, None)
        if not queue:
            self._packet_queues[packet_id] = Queue()
        return self._packet_queues[packet_id]

    def _send_packet(self, packet, response_command=None, callback=None):
        """
        Sends the specified packet to the packet manager, subscribe the callback for the packet id,
        retrieves the packet response from queue and unsubscribe from the packet id.
        """
        callback = callback if callback else self._callback_command
        packet_id = self._get_packet_id(response_command, packet.get_destination())
        queue = self._get_queue(packet_id)
        self._packet_manager.subscribe(packet_id, callback)
        self._packet_manager.send_packet(packet)
        response_byte = self._get_queue_data(queue)
        packet.clear_packet()
        packet.decode_packet(response_byte)
        self._packet_manager.unsubscribe(packet_id, callback)
        response_dict = packet.get_dict()
        logger.debug(f"Packet decoded : {response_dict}")
        return response_dict

    def _get_queue_data(self, queue):
        response_byte = [0, 0, 0, 0, 0, 10, 0, 0, -1, -1] + [0] * 256
        try:
            response_byte = queue.get(timeout=self._timeout)
        except Exception as e:
            logger.debug(f"No data received, reason :: {e}.")
        return response_byte

    def _callback_command(self, data, packet_id):
        """
        Receives the command response packet and store it in its respective packet id queue.
        """
        self._get_queue(packet_id).put(data)

    def set_timeout(self, timeout_value: float):
        """
        Sets the time out for queue to wait for command packet response.

        :param timeout_value: queue timeout value.
        :type timeout_value: int
        """
        self._timeout = timeout_value

    @staticmethod
    def _write_device_configuration_block_from_file_helper(dcfg_file):
        try:
            with open(dcfg_file, 'r') as file:
                result = []
                for line in file:
                    if line[0] != '#' and line[0] != '\n' and line[0] != ' ' and line[0] != '\t':
                        str_val = line.split('#')
                        # str_val[0] = re.sub(r'[ ]+', " ", str_val[0], 0, re.MULTILINE)
                        dcb = str_val[0].replace('\t', '').replace('\n', '').replace("  ", " ").split(" ")
                        result.append([int(dcb[0], 16), int(dcb[1], 16)])
                return result
        except Exception as e:
            logger.error(f"Error while reading the {dcfg_file} file, reason :: {e}.", exc_info=True)
