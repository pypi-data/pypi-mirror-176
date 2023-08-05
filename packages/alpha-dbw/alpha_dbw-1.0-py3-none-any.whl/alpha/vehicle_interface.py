#!/usr/bin/env python

#############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.                    #
#                                                                           #
# Created by Nikolay Dema <ndema2301@gmail.com>                             #
#                                                                           #
# Licensed under the Apache License, Version 2.0 (the "License");           #
# you may not use this file except in compliance with the License.          #
# You may obtain a copy of the License at                                   #
#                                                                           #
# http://www.apache.org/licenses/LICENSE-2.0                                #
#                                                                           #
# Unless required by applicable law or agreed to in writing, software       #
# distributed under the License is distributed on an "AS IS" BASIS,         #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
# See the License for the specific language governing permissions and       #
# limitations under the License.                                            #
#############################################################################

import sys
import io

from serial import *

from . import log
from .loops import Spinner
from .asp import *


SERIAL_WRITE_RATE = 100.
SERIAL_READ_RATE  = 100.


class SerialVehicleInterface:
    '''
    Serial communication interface.
    Directly ask Protocol for what data is needed to send and update.
    '''
    def __init__(self, protocol, port):

        self._protocol = protocol
        self._serial_read_buffer = bytearray()
        self._serial = Serial(port=port, baudrate=115200, bytesize=EIGHTBITS)

        self._receive_spinner = Spinner(self._receive_by_protocol, SERIAL_READ_RATE)
        self._send_spinner    = Spinner(self._send_by_protocol,    SERIAL_WRITE_RATE)


    def _send_by_protocol(self):
        # TODO: max size data constraints (serial buf on receiver side has limited size)
        alpha_can_raw_data_array = self._protocol.get_raw_data_to_send()
        for raw_data in alpha_can_raw_data_array:
            raw_serial = create_raw_serial_from_raw_alpha_data(raw_data)
            self._serial.write(raw_serial)


    def _receive_by_protocol(self):

        # TODO: check and clear if buffer too big
        self._serial_read_buffer += self._serial.read(self._serial.in_waiting)

        read_time = time.time()
        buffer_len = len(self._serial_read_buffer)
        end_buffer_check_pose = buffer_len - SERIAL_PKG_LEN
        alpha_can_raw_data_array = []
        left_buffer_pose = 0

        i = 0
        while (i <= end_buffer_check_pose):
            # TODO: not optimal
            pkg = get_pkg_from_raw_serial(self._serial_read_buffer[i:i+SERIAL_PKG_LEN])

            if pkg:
                i += SERIAL_PKG_LEN
                left_buffer_pose = i
                oscar_can_raw_data_array.append(pkg)
            else:
                i += 1


        if alpha_can_raw_data_array:
            self._protocol.update_data_from_raw(alpha_can_raw_data_array, read_time)
            self._serial_read_buffer = self._serial_read_buffer[left_buffer_pose:]


    def start_communication(self):
        return (self.start_sender() and self.start_receiver())


    def stop_communication(self):
        return (self.stop_sender() and self.stop_receiver())


    def start_sender(self):
        self._send_spinner.start()
        return self._send_spinner.is_active()


    def stop_sender(self):
        self._send_spinner.stop()
        return not self._send_spinner.is_active()


    def start_receiver(self):
        self._receive_spinner.start()
        return self._receive_spinner.is_active()


    def stop_receiver(self):
        self._receive_spinner.stop()
        return not self._receive_spinner.is_active()


    def __del__(self):
        if hasattr(self, 'serial'):
            self._serial.flush()
            self._serial.close()
