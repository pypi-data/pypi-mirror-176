# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

API for controlling Ethernet-connected motor boards (EthMotorBoard).

A working IPv4 connection to the EthMotorBoard is needed to control it.
EthMotorBoards get assigned either a fixed IP address in the
10.1.1.x space or an auto-generated one in the 10.x.x.x at the factory. You
will need an Ethernet adapter with a static IP address in the 10.x.x.x space to
connected to the EthMotorBoard. The use of a dedicated Ethernet adatper is
recomended.

If you do not know the IP address of the EthMotorBoard you want to control you
can use the "Manage Eth motor boards" feature in WinTopas4. You can also use
the UDP locator feature included in this library.

Copyright 2019-2022 Light Conversion
Contact: support@lightcon.com
"""
import socket
import time
import string
import json
from pathlib import Path

from ..common.leprecan_base import LepreCanBase
from ..common.udp_locator import UdpLocator


class EthMotorBoardCan:
    def __init__(self, emb):
        self.emb = emb

    def send(self, base_id, data):
        msb = (int.from_bytes(data, 'big') & 0xffffffff00000000) >> 32
        lsb = int.from_bytes(data, 'big') & 0xffffffff
        message = "CAN_TRANSMIT {:} {:} {:}\r\n".format(base_id,  msb, lsb)
        # print ('>', base_id, data)
        self.received = self.emb.send(message)

    def receive(self):
        if (self.received):
            recv_array = [int(item) for item in self.received.split(' ')]
            base_id = recv_array[0]
            msb = recv_array[1]
            lsb = recv_array[2]
            bytes_array = [(msb >> 24) & 0xff,
                           (msb >> 16) & 0xff,
                           (msb >>  8) & 0xff,
                           (msb >>  0) & 0xff,
                           (lsb >> 24) & 0xff,
                           (lsb >> 16) & 0xff,
                           (lsb >>  8) & 0xff,
                           (lsb >>  0) & 0xff
                           ]
            # print('<', base_id, bytes_array)
            return bytes_array


class EthMotorBoard(LepreCanBase):
    """Class to control EthMotorBoards."""

    BUFFER_SIZE = 1024
    sock = None
    connected = False
    name = None
    timeout = 100
    fv = None
    ip_address = None
    max_position = 2**21-1
    
    reg_dict = { 'HardHiZ' : ('HIZ {:} HARD', 0x00A8),
                'AbsPos' : ('',0x0001),
                'Stop' : ('',0x00B8),
                'GoTo' : ('', 0x0060),
                'RunForward' : ('RUN {:} 0', 0x0051),
                'RunReverse' : ('RUN {:} 1', 0x0050),
                'Acc' : ('ACC', 0x0005), 
                 'Dec' : ('DEC', 0x0006),
                 'FnSlpAcc' : ('FN_SLP_ACC', 0x000F),
                 'FnSlpDec' : ('FN_SLP_DEC', 0x0010),
                 'IntSpeed' : ('INT_SPEED', 0x000D),
                 'KTherm' : ('K_THERM', 0x0011), 
                 'KvalAcc' : ('KVAL_ACC', 0x000B),
                 'KvalDec' : ('KVAL_DEC', 0x000C),
                 'KvalHold' : ('KVAL_HOLD', 0x0009),
                 'KvalRun' : ('KVAL_RUN', 0x000A),
                 'MaxSpeed' : ('MAX_SPEED', 0x0007),
                 'MinSpeed' : ('MIN_SPEED', 0x0008),
                 'OcdTh' : ('OCD_TH', 0x0013),
                 'StSlp' : ('ST_SLP', 0x000E),
                 'StallTh' : ('STALL_TH', 0x0014),
                 'StepMode' : ('STEP_MODE', 0x0016),
                 'LSStatus': ('', 0x0100),
                 'LSEnable': ('', 0x0103)}

    status_registers = [
        (0x01, 0x01, 'HiZ'), (0x02, 0x0, 'BUSY'), (0x04, 0x04, 'SW_F'),
        (0x08, 0x08, 'SW_ENV'), (0x60, 0x00, 'Stopped'),
        (0x60, 0x20, 'Acceleration'), (0x60, 0x40, 'Deceleration'),
        (0x60, 0x60, 'Constant speed'), (0x80, 0x80, 'NOTPERF_CMD'),
        (0x100, 0x100, 'WRONG_CMD'), (0x200, 0x0, 'OVLO'),
        (0x400, 0x0, 'TH_WRN'), (0x800, 0x0, 'TH_SD'), (0x1000, 0x0, 'OCD'),
        (0x2000, 0x0, 'STEP_LOSS_A'), (0x4000, 0x0, 'STEP_LOSS_B'),
        (0x8000, 0x8000, 'SCK_MOD')]

    ls_registers = [
        (0x01, 0x01, 'Left LS reached'), (0x02, 0x02, 'Right LS reached')]

    def __init__(self, ip_address=None):
        """Create an EthMotorBoard control instance."""

        if ip_address is None:
            loc = UdpLocator()
            devices = loc.locate('EthMotorBoard', verbose=True)

            if len(devices) > 1:
                print("A total of {:} EthMotorBoard devices were found, using "
                      "the first one".format(len(devices)))

            ip_address = devices[0].get('IpAddress')

        if ip_address is None:
            raise RuntimeError("No EthMotorBoard devices found")

        self.ip_address = ip_address

        self.name = self.send('GET BOARD_NAME')
        self.fv = self.send('FIRMWARE_VERSION')

        self.connected = self.fv is not None

        if self.connected:
            print("Successfully connected to EthMotorBoard {:} at address {:},"
                  " firmware version: {:}".format(
                    self.name, self.ip_address, self.fv))

            self.can_service = EthMotorBoardCan(self)

        else:
            raise RuntimeError(
                "Motor board not found at {:}".format(self.ip_address))

    def setup_motor(self, index, file_name):                
        try:
            with open(file_name, 'r') as f:
                motor_info = json.loads(f.read())            
                
        except FileNotFoundError:
            print ('Configuration not found')
            return        
    
        response = self.send(self.reg_dict['HardHiZ'][0].format(1 << index))
        time.sleep(1)    
        
        for key in motor_info.keys():
            if self.reg_dict.get(key):
                
                response = self.send('SET ' + self.reg_dict[key][0], [index, motor_info[key]])
                print ('<', response, 'for', key)
                
    def send(self, message, args=None):
        """Send a command to the board and get a response.

        TODO: This should probably be called a querry.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout/1000)
            self.sock.connect((self.ip_address, 80))

            if args is None:
                self.sock.send((str(message)+'\r\n').encode('UTF-8'))
            else:
                self.sock.send((
                    str(message) + ' '
                    + ' '.join([str(arg) for arg in args])
                    + '\r\n').encode('UTF-8'))

            data = self.sock.recv(self.BUFFER_SIZE)
            self.sock.close()
            return data[:-2].decode()
        except socket.timeout:
            return None

    def get_status(self, motor_index=0):
        """Get board status."""
        status = int(self.send('GET STATUS', [motor_index]))
        ls_result = self.send('GET LIMIT_SWITCH', [motor_index])
        ls_status = eval(ls_result)['Logical']
        return [stat for mask, val, stat in self.status_registers
                if status & mask == val] \
            + [stat for mask, val, stat in self.ls_registers
                if ls_status & mask == val]

    def wait_until_stopped(self, motor_index=0):
        """Wait until motor stops."""
        repeat = True
        while repeat:
            status = self.send('GET STATUS ' + str(motor_index))
            repeat = int(status) & 0x60 != 0
            time.sleep(0.05)

    def get_abs_pos(self, motor_index=0):
        """Get absolute position in steps."""
        return int(self.send('GET ABS_POS ' + str(motor_index)))

    def move_rel(self, motor_index=0, move_dir=0, pos_delta=0):
        """Move motor a given distance from the current position."""
        ret_code = self.send('MOVE {:d} {:d} {:d}'.format(
            motor_index, move_dir, pos_delta))

        self.check_error(ret_code)

    def move_abs(self, motor_index=0, abs_pos=0):
        """Move motor to an absolute position."""
        ret_code = self.send('GOTO {:d} {:d}'.format(motor_index, abs_pos))
        self.check_error(ret_code)

    def run_stage(self, motor_index=0, move_dir=0, speed=10000):
        """Run stage continuously.

        Run the stage continuously in the given direction until stopped or a
        limit switch is activated.
        """
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        return self.check_error(ret_code)

    def get_max_speed(self, motor_index=0):
        """Get maximum speed."""
        return int(self.send('GET MAX_SPEED ' + str(motor_index)))

    def set_max_speed(self, motor_index=0, speed=100):
        """Set maximum speed."""
        if speed < 0:
            raise ValueError("Speed has to be positive")
        if speed > 1024:
            raise ValueError("Speed has to be less than 1024")

        ret_code = self.send('SET MAX_SPEED {:d} {:d}'.format(
            motor_index, speed))
        self.check_error(ret_code)

    def check_error(self, ret_code):
        """Check the return value.

        'ERR0' means that everything is fine. 'ERR4' means that a limit switch
        has been reached. These two codes can be ignored in most cases.
        Anything else indicates an error.
        """
        ret_code = strip_whitespace(ret_code)

        if ret_code not in ['ERR0', 'ERR4']:
            print("Error: " + ret_code)

    def reset_motor(self, motor_index=0, move_dir=0, speed=10000):
        """Reset motor and set current position to 0.

        Move motor in the given direction until a limit switch has been
        reached and set the current position there to 0.
        """
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        self.check_error(ret_code)

        self.wait_until_stopped(motor_index)

        pos = self.get_abs_pos(motor_index)

        ret_code = self.send('RESET_POS {:d}'.format(motor_index))
        self.check_error(ret_code)

        return {'abs_pos_at_reset': pos}

    def setup_motor(self, motor_index=0, cfg_file_name=None, verbose=False):
        info_dict = {
            'Acc': 'ACC', 'Dec': 'DEC', 'FnSlpAcc': 'FN_SLP_ACC',
            'FnSlpDec': 'FN_SLP_DEC', 'IntSpeed': 'INT_SPEED',
            'KTherm': 'K_THERM', 'KvalAcc': 'KVAL_ACC', 'KvalDec': 'KVAL_DEC',
            'KvalHold': 'KVAL_HOLD', 'KvalRun': 'KVAL_RUN',
            'MaxSpeed': 'MAX_SPEED', 'MinSpeed': 'MIN_SPEED',
            'OcdTh': 'OCD_TH', 'StSlp': 'ST_SLP', 'StallTh': 'STALL_TH',
            'StepMode': 'STEP_MODE'}

        if cfg_file_name is None:
            print("Configuration file not specified for motor ", motor_index)

        try:
            cfg_path = \
                str(Path(__file__).parent) + '\\config\\' + cfg_file_name
            with open(cfg_path, 'r') as f:
                motor_cfg = json.loads(f.read())

        except FileNotFoundError:
            print("Motor configuration not found")
            return

        except Exception as excpt:
            print("Error while reading motor configuration file")
            print(excpt)
            return

        print("Configuring motor '{:s}' on port {:d}".format(
            Path(cfg_file_name).stem, motor_index))

        self.send('HIZ {:} HARD'.format(1 << motor_index))
        time.sleep(1)

        for key in motor_cfg.keys():
            if info_dict.get(key):
                message = 'SET {:} {:} {:}'.format(
                    info_dict[key], motor_index, motor_cfg[key])
                response = self.send(message)
                if verbose:
                    print(response, 'for', message)

    def setup_stage(self, motor_index=0, cfg_file_name=None, verbose=False):
        try:
            cfg_path = \
                str(Path(__file__).parent) + '\\config\\' + cfg_file_name
            with open(cfg_path, 'r') as f:
                stage_cfg = json.loads(f.read())

        except FileNotFoundError:
            print("Stage configuration not found")
            return

        except Exception as excpt:
            print("Error while reading stage configuration file")
            print(excpt)
            return

        print("Configuring stage '{:s}' on port {:d}".format(
            Path(cfg_file_name).stem, motor_index))

        self.setup_motor(motor_index, stage_cfg.get('motor_config_file_name'),
                         verbose=verbose)

        ls_keys = {'ls_enable', 'ls_invert', 'ls_swap'}

        for key in ls_keys:
            message = 'SET {:} {:} {:}'.format(
                key.upper(), motor_index, stage_cfg[key])
            response = self.send(message)
            if verbose:
                print(response, 'for', message)


# === Helper functions ===
def strip_whitespace(s):
    return s.translate(str.maketrans('', '', string.whitespace))
