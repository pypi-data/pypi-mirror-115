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

from enum import Enum, unique

from .ad7156_enums import AD7156Command
from .adpd_enums import ADPDCommand
from .adxl_enums import ADXLCommand
from .bcm_enums import BCMCommand
from .dcb_enums import DCBCommand, DCBStatus
from .display_enums import DisplayCommand
from .ecg_enums import ECGCommand
from .eda_enums import EDACommand
from .fs_enums import FSCommand, FSStatus
from .low_touch_enum import LTCommand
from .pedometer_enums import PedometerCommand
from .pm_enums import PMCommand, PMStatus
from .ppg_enums import PPGCommand
from .sqi_enum import SQICommand
from .. import utils


class Command:
    """
    Helper method for decoding commands.
    """

    def __init__(self, command, source):
        self._enum = None
        self._source = None
        if command == CommonCommand.STREAM_DATA.value:
            self._source = Stream(source)
            self._enum = CommonCommand(command)
        elif source == Stream.FS.value and command in [FSCommand.DOWNLOAD_LOG_RES.value,
                                                       FSCommand.CHUNK_RETRANSMIT_RES.value]:
            self._source = Stream(source)
            self._enum = FSCommand(command)
        else:
            self._source = Application(source)
            if command[0] < CommonCommand.HIGHEST.value[0]:
                self._enum = CommonCommand(command)
            elif command in [DCBCommand.READ_CONFIG_RES.value, DCBCommand.WRITE_CONFIG_RES.value,
                             DCBCommand.ERASE_CONFIG_RES.value, DCBCommand.QUERY_STATUS_RES.value]:
                self._enum = DCBCommand(command)
            elif self._source == Application.PM:
                self._enum = PMCommand(command)
            elif self._source == Application.ADPD:
                self._enum = ADPDCommand(command)
            elif self._source == Application.ADXL:
                self._enum = ADXLCommand(command)
            elif self._source == Application.FS:
                self._enum = FSCommand(command)
            elif self._source == Application.PPG:
                self._enum = PPGCommand(command)
            elif self._source == Application.SQI:
                self._enum = SQICommand(command)
            elif self._source == Application.DISPLAY:
                self._enum = DisplayCommand(command)
            elif self._source == Application.AD7156:
                self._enum = AD7156Command(command)
            elif self._source == Application.BCM:
                self._enum = BCMCommand(command)
            elif self._source == Application.EDA:
                self._enum = EDACommand(command)
            elif self._source == Application.LT_APP:
                self._enum = LTCommand(command)
            elif self._source == Application.ECG:
                self._enum = ECGCommand(command)
            elif self._source == Application.PEDOMETER:
                self._enum = PedometerCommand(command)
            else:
                self._enum = CommonCommand(command)

    def get_enum(self):
        return self._enum

    def get_source(self):
        return self._source


class Status:
    """
    Helper method for decoding status.
    """

    def __init__(self, status, source, command):
        self._enum = None
        if command == CommonCommand.STREAM_DATA.value:
            self._enum = CommonStatus(status)
        elif source == Stream.FS.value and command in [FSCommand.DOWNLOAD_LOG_RES.value,
                                                       FSCommand.CHUNK_RETRANSMIT_RES.value]:
            self._enum = FSStatus(status)
        else:
            source = Application(source)
            if status[0] < CommonStatus.HIGHEST.value[0]:
                self._enum = CommonStatus(status)
            elif command in [DCBCommand.READ_CONFIG_RES.value, DCBCommand.WRITE_CONFIG_RES.value,
                             DCBCommand.ERASE_CONFIG_RES.value]:
                self._enum = DCBStatus(status)
            elif source == Application.PM:
                self._enum = PMStatus(status)
            elif source == Application.FS:
                self._enum = FSStatus(status)
            else:
                self._enum = CommonStatus(status)

    def get_enum(self):
        return self._enum


@unique
class CommonCommand(Enum):
    """
    CommonCommand Enum
    """
    NO_RESPONSE = [-1]
    GET_VERSION_REQ = [0x0]
    GET_VERSION_RES = [0x1]
    START_SENSOR_REQ = [0x4]
    START_SENSOR_RES = [0x5]
    STOP_SENSOR_REQ = [0x6]
    STOP_SENSOR_RES = [0x7]
    SUBSCRIBE_STREAM_REQ = [0xC]
    SUBSCRIBE_STREAM_RES = [0xD]
    UNSUBSCRIBE_STREAM_REQ = [0xE]
    UNSUBSCRIBE_STREAM_RES = [0xF]
    GET_SENSOR_STATUS_REQ = [0x10]
    GET_SENSOR_STATUS_RES = [0x11]
    GET_LCFG_REQ = [0x12]
    GET_LCFG_RES = [0x13]
    SET_LCFG_REQ = [0x14]
    SET_LCFG_RES = [0x15]
    READ_LCFG_REQ = [0x16]
    READ_LCFG_RES = [0x17]
    WRITE_LCFG_REQ = [0x18]
    WRITE_LCFG_RES = [0x19]
    PING_REQ = [0x1A]
    PING_RES = [0x1B]
    REGISTER_READ_REQ = [0x21]
    REGISTER_READ_RES = [0x22]
    REGISTER_WRITE_REQ = [0x23]
    REGISTER_WRITE_RES = [0x24]
    GET_DCFG_REQ = [0x25]
    GET_DCFG_RES = [0x26]
    STREAM_DATA = [0x28]
    GET_STREAM_DEC_FACTOR_REQ = [0x29]
    GET_STREAM_DEC_FACTOR_RES = [0x2A]
    SET_STREAM_DEC_FACTOR_REQ = [0x2B]
    SET_STREAM_DEC_FACTOR_RES = [0x2C]
    HIGHEST = [0x40]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class CommonStatus(Enum):
    """
    CommonStatus Enum
    """
    NO_RESPONSE = [-1]
    OK = [0x0]
    ERROR = [0x1]
    STREAM_STARTED = [0x2]
    STREAM_STOPPED = [0x3]
    STREAM_IN_PROGRESS = [0x4]
    STREAM_DEACTIVATED = [0x5]
    STREAM_COUNT_DECREMENT = [0x6]
    STREAM_NOT_STARTED = [0x7]
    STREAM_NOT_STOPPED = [0x8]
    SUBSCRIBER_ADDED = [0x9]
    SUBSCRIBER_REMOVED = [0xA]
    SUBSCRIBER_COUNT_DECREMENT = [0xB]
    HIGHEST = [0x20]
    NEW_STREAM_STATUS = [0x43]  # some stream such as EDA has 0x43 as status instead of 0x0

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class Stream(Enum):
    """
    Stream Enum
    """
    NULL = [0x00, 0x00]
    ADPD1 = [0xc2, 0x11]
    ADPD2 = [0xc2, 0x12]
    ADPD3 = [0xc2, 0x13]
    ADPD4 = [0xc2, 0x14]
    ADPD5 = [0xc2, 0x15]
    ADPD6 = [0xc2, 0x16]
    ADPD7 = [0xc2, 0x17]
    ADPD8 = [0xc2, 0x18]
    ADPD9 = [0xc2, 0x19]
    ADPD10 = [0xc2, 0x1a]
    ADPD11 = [0xc2, 0x1b]
    ADPD12 = [0xc2, 0x1c]
    ADXL = [0xc2, 0x02]
    BCM = [0xC4, 0x07]
    ECG = [0xc4, 0x01]
    EDA = [0xc4, 0x02]
    FS = [0xC6, 0x01]
    PEDOMETER = [0xc4, 0x04]
    PPG = [0xC4, 0x00]
    TEMPERATURE = [0xc4, 0x06]
    SYNC_PPG = [0xC4, 0x05]
    SQI = [0xC8, 0x0D]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))


@unique
class Application(Enum):
    """
    Application Enum.
    """
    ADXL = [0xc1, 0x02]
    ADPD = [0xc1, 0x10]
    PPG = [0xC3, 0x00]
    ECG = [0xc3, 0x01]
    EDA = [0xc3, 0x02]
    PEDOMETER = [0xc3, 0x04]
    TEMPERATURE = [0xc3, 0x06]
    BCM = [0xC3, 0x07]
    FS = [0xC5, 0x01]
    PS = [0xc5, 0x80]
    PM = [0xc5, 0x00]
    DISPLAY = [0xC5, 0x03]
    APP_USB = [0xc7, 0x05]
    SQI = [0xC8, 0x0C]
    AD7156 = [0xC8, 0x0B]
    APP_BLE = [0xC8, 0x08]
    LT_APP = [0xC8, 0x0A]
    NULL = [0x0, 0x0]

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, utils.convert_int_array_to_hex(self._value_))
