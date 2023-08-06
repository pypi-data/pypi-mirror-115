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
import csv
import os
import sys
import logging
import threading
from typing import List
from datetime import datetime

import serial
import serial.tools.list_ports

from .core.packet_manager import PacketManager
from .core.enums.common_enums import CommonCommand
from .application.pm_application import PMApplication
from .application.fs_application import FSApplication
from .application.sqi_application import SQIApplication
from .application.ecg_application import ECGApplication
from .application.eda_application import EDAApplication
from .application.bcm_application import BCMApplication
from .application.ppg_application import PPGApplication
from .application.test_application import TestApplication
from .application.adxl_application import ADXLApplication
from .application.adpd_application import ADPDApplication
from .application.ad7156_application import AD7156Application
from .application.low_touch_application import LowTouchApplication
from .application.pedometer_application import PedometerApplication
from .application.temperature_application import TemperatureApplication

logger = logging.getLogger(__name__)


class SDK:
    """
    SDK class
    """

    def __init__(self, serial_port_address: str, is_ble: bool = False, baud_rate: int = 921600,
                 logging_filename: str = None, debug: bool = False, **kwargs):
        """
        Creates a SDK object

        :param serial_port_address: serial port of the device connected
        :param baud_rate: baud rate
        :param **kwargs: other keys and values  for creating serial object
        """
        self._serial_object = None
        self._packet_manager = None
        self.connect(serial_port_address, is_ble, baud_rate, logging_filename, debug, **kwargs)

    def connect(self, serial_port_address: str, is_ble: bool = False, baud_rate: int = 921600,
                logging_filename: str = None, debug: bool = False, **kwargs):
        """
        Connect method allows you to reconnect to SDK; you must call disconnect before using connect.
        """

        log_format = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        if logging_filename:
            logging.basicConfig(filename=logging_filename, filemode='a', format=log_format, datefmt=date_format,
                                level=logging.DEBUG)
        else:
            if debug:
                logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)
            else:
                logging.basicConfig(format=log_format, datefmt=date_format)
        logger.debug("----- Study Watch SDK Started -----")
        self._serial_object = serial.Serial(serial_port_address, baud_rate, **kwargs)
        self._packet_manager = PacketManager(self._serial_object)
        if is_ble:
            self._packet_manager.set_ble_source()
        else:
            self._packet_manager.set_usb_source()

        self._packet_manager.start_receive_and_process_threads()
        self.get_pm_application().set_datetime(datetime.now())

    def get_adpd_application(self, callback_function_default=None, args=()):
        """
        Creates an adpd application object

        :param callback_function_default: callback function for all adpd slot stream.
        :type callback_function_default: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: an Adpd Application
        :rtype: ADPDApplication
        """
        return ADPDApplication(callback_function_default, self._packet_manager, args)

    def get_adxl_application(self, callback_function=None, args=()):
        """
        Creates an adxl application object

        :param callback_function: callback function for adxl stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: an Adxl Application
        :rtype: ADXLApplication
        """
        return ADXLApplication(callback_function, self._packet_manager, args)

    def get_ecg_application(self, callback_function=None, args=()):
        """
        Creates an ecg application object

        :param callback_function: callback function for ecg stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: an ecg Application
        :rtype: ECGApplication
        """
        return ECGApplication(callback_function, self._packet_manager, args)

    def get_eda_application(self, callback_function=None, args=()):
        """
        Creates an eda application object

        :param callback_function: callback function for eda stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: an eda Application
        :rtype: EDAApplication
        """
        return EDAApplication(callback_function, self._packet_manager, args)

    def get_fs_application(self):
        """
        Creates an fs application object

        :returns: an fs Application
        :rtype: FSApplication
        """
        return FSApplication(self._packet_manager)

    def get_pedometer_application(self, callback_function=None, args=()):
        """
        Creates an pedometer application object

        :param callback_function: callback function for pedometer stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: an pedometer Application
        :rtype: PedometerApplication
        """
        return PedometerApplication(callback_function, self._packet_manager, args)

    def get_pm_application(self):
        """
        Creates an pm application object

        :returns: an pm Application
        :rtype: PMApplication
        """
        return PMApplication(self._packet_manager)

    def get_ppg_application(self, callback_ppg=None, callback_syncppg=None, args_ppg=(), args_syncppg=()):
        """
        Creates an ppg application object

        :param callback_ppg: callback function for ppg stream.
        :type callback_ppg: Callable
        :param callback_syncppg: callback function for sync ppg stream.
        :type callback_syncppg: Callable
        :param args_ppg: optional arguments that will be passed back with ppg callback.
        :param args_syncppg: optional arguments that will be passed back with sync ppg callback.
        :returns: an Ppg Application
        :rtype: PPGApplication
        """
        return PPGApplication(callback_ppg, callback_syncppg, self._packet_manager, args_ppg, args_syncppg)

    def get_temperature_application(self, callback_function=None, args=()):
        """
        Creates a temperature application object

        :param callback_function: callback function for temperature stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: a Temperature Application
        :rtype: TemperatureApplication
        """
        return TemperatureApplication(callback_function, self._packet_manager, args)

    def get_sqi_application(self, callback_function=None, args=()):
        """
        Creates a sqi application object

        :param callback_function: callback function for sqi stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: a SQI Application
        :rtype: SQIApplication
        """
        return SQIApplication(callback_function, self._packet_manager, args)

    def get_bcm_application(self, callback_function=None, args=()):
        """
        Creates a bcm application object

        :param callback_function: callback function for bcm stream
        :type callback_function: Callable
        :param args: optional arguments that will be passed back with the callback.
        :returns: a BCM Application
        :rtype: BCMApplication
        """
        return BCMApplication(callback_function, self._packet_manager, args)

    def get_ad7156_application(self):
        """
        Creates a ad7156 application object

        :returns: a AD7156 Application
        :rtype: AD7156Application
        """
        return AD7156Application(self._packet_manager)

    def get_low_touch_application(self):
        """
        Creates a low touch application object

        :returns: a LowTouch Application
        :rtype: LowTouchApplication
        """
        return LowTouchApplication(self._packet_manager)

    def get_test_application(self, key_test_callback=None, cap_sense_callback=None):
        """
        Creates a test application object, used for internal firmware testing.

        :returns: a Test Application
        :rtype: TestApplication
        """
        return TestApplication(key_test_callback, cap_sense_callback, self._packet_manager)

    def unsubscribe_all_streams(self):
        """
        Unsubscribe from all application streams
        """
        result = [self.get_adxl_application().unsubscribe_stream(), self.get_sqi_application().unsubscribe_stream(),
                  self.get_ppg_application().unsubscribe_stream(), self.get_bcm_application().unsubscribe_stream(),
                  self.get_ecg_application().unsubscribe_stream(), self.get_eda_application().unsubscribe_stream(),
                  self.get_temperature_application().unsubscribe_stream(),
                  self.get_pedometer_application().unsubscribe_stream()]
        adpd_app = self.get_adpd_application()
        fs_app = self.get_fs_application()
        for stream in adpd_app.get_supported_streams():
            result.append(adpd_app.unsubscribe_stream(stream))
        for stream in fs_app.get_supported_streams():
            result.append(fs_app.unsubscribe_stream(stream))
        return result

    @staticmethod
    def get_available_ports() -> List:
        """
        returns the list of tuple (port, description, hardware_id) of available ports.
        """
        ports = serial.tools.list_ports.comports()
        result = []
        for port, desc, hardware_id in sorted(ports):
            result.append((port, desc, hardware_id))
        return result

    @staticmethod
    def join_csv(*args, output_filename="combined.csv"):
        """
        Joins multiple data stream csv file into single csv file.
        """
        rows = {}
        space = {}
        max_lines = 0
        header = None
        # reading each file
        for file in args:
            try:
                csv_file = open(file, 'r')
                reader = csv.reader(csv_file, quoting=csv.QUOTE_NONE, delimiter=',')
                csv_rows = []
                max_space = 0
                # reading each row
                for row in reader:
                    if len(row) > 0:
                        csv_rows.append(row)
                    # max length of row in a file, used in the case where files have unequal sizes
                    max_space = max(max_space, len(row))
                space[file] = max_space
                rows[file] = csv_rows
                # obtaining header
                if header is None:
                    header = rows[file][:2]
                rows[file] = rows[file][2:]
                # max lines in all files
                max_lines = max(max_lines, len(rows[file]))
                csv_file.close()
            except Exception as e:
                logger.debug(e)

        # creating required rows in combined csv
        final_rows = [[]] * max_lines
        for file in rows:
            for i in range(max_lines):
                # adding spaces because no data, check for final_rows[i] += [" "] * space[file]
                if i + 1 > len(rows[file]):
                    final_rows[i] = final_rows[i] + [" "] * space[file]
                else:
                    # appending data to the row
                    final_rows[i] = final_rows[i] + rows[file][i]

        # writing data to final csv
        final_rows = header + final_rows
        file = open(output_filename, 'w', newline="")
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\'')
        for row in final_rows:
            writer.writerow(row)
        file.close()

    @staticmethod
    def _sub_helper(app, stream, packet_manager):
        packet_id = app._get_packet_id(CommonCommand.STREAM_DATA, app._stream if stream is None else stream)
        if type(app) == ADPDApplication:
            packet_manager.subscribe(packet_id, app._stream_to_callback[stream])
        else:
            packet_manager.subscribe(packet_id, app._callback_data)

    @staticmethod
    def convert_log_to_csv(filename):
        """
        Converts M2M2 log file into csv.
        """
        folder_name = filename.split(".")[0]
        try:
            os.mkdir(folder_name)
        except Exception as e:
            logger.debug(e)
        # creating all applications
        packet_manager = PacketManager(None, filename=filename)
        packet_manager.set_usb_source()
        adpd_app = ADPDApplication(None, packet_manager, None)
        adxl_app = ADXLApplication(None, packet_manager, None)
        ecg_app = ECGApplication(None, packet_manager, None)
        eda_app = EDAApplication(None, packet_manager, None)
        ped_app = PedometerApplication(None, packet_manager, None)
        ppg_app = PPGApplication(None, None, packet_manager, None, None)
        temp_app = TemperatureApplication(None, packet_manager, None)
        sqi_app = SQIApplication(None, packet_manager, None)
        bcm_app = BCMApplication(None, packet_manager, None)
        pm_app = PMApplication(packet_manager)

        # enabling csv logging
        adxl_app.enable_csv_logging(f"{folder_name}/adxl.csv")
        for i, stream in enumerate(adpd_app.get_supported_streams()):
            adpd_app.enable_csv_logging(f"{folder_name}/adpd{i + 1}.csv", stream=stream)
        ecg_app.enable_csv_logging(f"{folder_name}/ecg.csv")
        eda_app.enable_csv_logging(f"{folder_name}/eda.csv")
        ped_app.enable_csv_logging(f"{folder_name}/ped.csv")
        ppg_app.enable_csv_logging(f"{folder_name}/ppg.csv", stream=ppg_app.PPG)
        ppg_app.enable_csv_logging(f"{folder_name}/sync_ppg.csv", stream=ppg_app.SYNC_PPG)
        temp_app.enable_csv_logging(f"{folder_name}/temp.csv")
        sqi_app.enable_csv_logging(f"{folder_name}/sqi.csv")
        bcm_app.enable_csv_logging(f"{folder_name}/bcm.csv")

        # subscribing
        apps = [adxl_app, ecg_app, eda_app, ped_app, ppg_app, temp_app, sqi_app, bcm_app]
        for app in apps:
            SDK._sub_helper(app, None, packet_manager)
        for stream in adpd_app.get_supported_streams():
            SDK._sub_helper(adpd_app, stream, packet_manager)

        info_result = {}

        # callback for sum initial packets
        def info_packets(function, key):
            if key == "ecg_lcfg":
                response_packet = function([0x0])
            else:
                response_packet = function()
            info_result[key] = response_packet
            if key == "datetime":
                dt = datetime(response_packet['payload']['year'], response_packet['payload']['month'],
                              response_packet['payload']['day'], response_packet['payload']['hour'],
                              response_packet['payload']['minute'], response_packet['payload']['second'])
                ticks = (32000.0 * ((response_packet['payload']['hour'] * 3600) +
                                    (response_packet['payload']['minute'] * 60) + response_packet['payload']['second']))
                ref_timestamp = datetime.timestamp(dt)
                last_timestamp = [ref_timestamp, ticks]
                for _stream in adpd_app.get_supported_streams():
                    adpd_app._last_timestamp_adpd[_stream] = last_timestamp
                adxl_app._last_timestamp = last_timestamp
                ecg_app._last_timestamp = last_timestamp
                eda_app._last_timestamp = last_timestamp
                ped_app._last_timestamp = last_timestamp
                ppg_app._last_timestamp_ppg = last_timestamp
                ppg_app._last_timestamp_syncppg = last_timestamp
                temp_app._last_timestamp = last_timestamp
                sqi_app._last_timestamp = last_timestamp
                bcm_app._last_timestamp = last_timestamp

        # threads for initial packets
        threading.Thread(target=info_packets, args=(pm_app.get_datetime, "datetime")).start()
        threading.Thread(target=info_packets, args=(pm_app.get_system_info, "system_info")).start()
        threading.Thread(target=info_packets, args=(pm_app.get_version, "version")).start()
        threading.Thread(target=info_packets, args=(ppg_app.get_algo_version, "ppg_algo_version")).start()
        threading.Thread(target=info_packets, args=(ped_app.get_algo_version, "ped_algo_version")).start()
        threading.Thread(target=info_packets, args=(ecg_app.get_algo_version, "ecg_algo_version")).start()
        threading.Thread(target=info_packets, args=(sqi_app.get_algo_version, "sqi_algo_version")).start()
        threading.Thread(target=info_packets, args=(adpd_app.get_device_configuration, "adpd_dcfg")).start()
        threading.Thread(target=info_packets, args=(adxl_app.get_device_configuration, "adxl_dcfg")).start()
        threading.Thread(target=info_packets, args=(ppg_app.get_library_configuration, "ppg_lcfg")).start()
        threading.Thread(target=info_packets, args=(ecg_app.read_library_configuration, "ecg_lcfg")).start()

        packet_manager.start_receive_and_process_threads()

        # waiting for packet manager to finish processing log file.
        while not packet_manager.queue.empty() or packet_manager.processing_file:
            pass

        # disabling csv logging.
        adxl_app.disable_csv_logging()
        for stream in adpd_app.get_supported_streams():
            adpd_app.disable_csv_logging(stream=stream)
        ecg_app.disable_csv_logging()
        eda_app.disable_csv_logging()
        ped_app.disable_csv_logging()
        ppg_app.disable_csv_logging(stream=ppg_app.PPG)
        ppg_app.disable_csv_logging(stream=ppg_app.SYNC_PPG)
        temp_app.disable_csv_logging()
        sqi_app.disable_csv_logging()
        bcm_app.disable_csv_logging()

        # storing initial packets in info.csv
        with open(f"{folder_name}/info.csv", 'w') as f:
            for res in info_result:
                f.write(res + " :: " + str(info_result[res]) + "\n")

        # combining adpd csv
        adpd_csv_files = []
        for i in range(1, 13):
            adpd_csv_files.append(f"{folder_name}/adpd{i}.csv")
        SDK.join_csv(*adpd_csv_files, output_filename=f"{folder_name}/adpd_streams.csv")

    def disconnect(self):
        """disconnect SDK"""
        logger.debug("----- Study Watch SDK Stopped -----")
        self._packet_manager.close()
