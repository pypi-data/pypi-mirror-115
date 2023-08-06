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

logger = logging.getLogger(__name__)


def get_updated_timestamp(reference_time, last_ts, timestamp):
    if last_ts > timestamp:
        change = (timestamp + 2764800000.0) - last_ts
    else:
        change = timestamp - last_ts
    change = change / 32000.0
    return reference_time + change


def join_multi_length_packets(packet, sign=False, reverse=False, convert_to_hex=False):
    """
    Joins array of bytes into integer.
    """
    ans = 0
    packet_len = len(packet)
    if packet_len == 0:
        return ans
    if reverse:
        packet = list(reversed(packet))
    for i, value in enumerate(packet):
        ans += (value << (8 * i))
    bits = packet_len * 8
    if sign and ans & (1 << (bits - 1)):
        ans -= 1 << bits
    if convert_to_hex:
        return "0x%X" % ans
    return ans


def range_and_type_check(num, num_bytes=None, lower_and_upper_bound=None, type_of=None, max_len=None):
    """
    Checks num for specified type and range.
    """
    if type_of:
        if not type(num) == type_of:
            logger.error(f"{'0x%X' % num} is not of type {type_of}.")

    if num_bytes:
        lower_bound = 0
        upper_bound = 16 ** (num_bytes * 2) - 1
        if not lower_bound <= num <= upper_bound:
            logger.error(f"{'0x%X' % num} is out of range, Variable needs to be between {'0x%X' % lower_bound}"
                         f" and {'0x%X' % upper_bound}.")

    if lower_and_upper_bound:
        if not lower_and_upper_bound[0] <= num <= lower_and_upper_bound[1]:
            logger.error(f"{'0x%X' % num} is out of range, Variable needs to be greater than or equal to "
                         f"{'0x%X' % lower_and_upper_bound[0]} and less than or equal to "
                         f"{'0x%X' % lower_and_upper_bound[1]}.")

    if max_len:
        if len(num) > max_len:
            logger.error(f"{num} is out of range. Max length allowed is {max_len}.")
    return num


def split_int_in_bytes(value, length=None, reverse=False):
    """
    Breaks int into array of byte array of specified length.
    """
    result = []
    shift = 0
    base_value = 0
    if value < 0:
        base_value = 255
    while value >> shift and not (value < 0 and value >> shift == -1):
        result.append((value >> shift) & 0xff)
        shift += 8
    if length and not len(result) == length:
        result += [base_value] * abs(length - len(result))
    if reverse:
        result = list(reversed(result))
    return result


def address_range_check(address, address_range):
    """
    checks if address is in given range or not.
    """
    if not address_range[0] <= address <= address_range[1]:
        logger.warning(
            f"Address {'0x%X' % address} is out of range, it should be in range {'0x%X' % address_range[0]} "
            f"and {'0x%X' % address_range[1]} ")
    return address


def check_array_address_range(array, address_range, num_bytes, type_of=int):
    """
    checks if array address is in given range or not.
    """
    for values in array:
        if type(values) == list:
            address_range_check(values[0], address_range)
            range_and_type_check(values[1], type_of=type_of, num_bytes=num_bytes)
        else:
            address_range_check(values, address_range)
            range_and_type_check(values, type_of=type_of, num_bytes=num_bytes)


def convert_int_array_to_hex(arr):
    """
    Convert int to hex.
    """
    return ['0x%02X' % x for x in arr]


def pretty(value, tab_char='\t', next_line_char='\n', indent=0):
    """
    Print dict in clean format.
    """
    line = next_line_char + tab_char * (indent + 1)
    if type(value) is dict:
        items = [
            line + repr(key) + ': ' + pretty(value[key], tab_char, next_line_char, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + next_line_char + tab_char * indent)
    elif type(value) is list:
        items = []
        flag = " "
        for item in value:
            if type(item) is list:
                flag = line[:-1]
                items.append(line + pretty(item, tab_char, next_line_char, indent))
            elif type(item) is dict:
                flag = line[:-1]
                items.append(line + pretty(item, tab_char, next_line_char, indent + 1))
            else:
                items.append(" " + pretty(item, tab_char, " ", 0))
        return '[%s%s]' % (','.join(items), flag)
    elif type(value) is tuple:
        items = [
            line + pretty(item, tab_char, next_line_char, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + next_line_char + tab_char * indent)
    else:
        return repr(value)
