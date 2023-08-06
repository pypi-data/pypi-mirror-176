# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

A diagnostic test routine for a motorized linear stage using the EthMotorBoard.

See test_stage docstring for test parameters and procedure.

Copyright 2019-2022 Light Conversion
Contact: support@lightcon.com
"""
from lightcon.eth_motor_board.test_stage import test_stage

try:
    test_stage('Standa 8MT184-13', ref_travel_len=333887)
except Exception as excp:
    print("Test failed. Reason: ", excp)

input("Press any key to continue...")
