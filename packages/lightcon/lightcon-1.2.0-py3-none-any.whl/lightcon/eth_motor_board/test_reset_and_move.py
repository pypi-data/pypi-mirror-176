# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

A basic test routine for the EthMotorBoard.

Copyright 2019-2022 Light Conversion
Contact: support@lightcon.com
"""
from lightcon.eth_motor_board import EthMotorBoard

print("=== EthMotorBoard test ===")

MOTOR_IDX = 0
TARGET_POS = 10000

print("This test will connect an Ethernet Motor Board and move motor {:d} to "
      "{:d} ustep position".format(MOTOR_IDX, TARGET_POS))

print("Connecting to EthMotorBoard...")
motorb = EthMotorBoard()

if motorb.connected:
    motorb.reset_motor(MOTOR_IDX, speed=100000)
    motorb.move_abs(MOTOR_IDX, TARGET_POS)
    motorb.wait_until_stopped(MOTOR_IDX)
else:
    print("Could not connect to an EthMotorBoard")

input("Press any key to continue...")
