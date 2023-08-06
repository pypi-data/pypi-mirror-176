# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

A diagnostic test routine for a motorized linear stage using the EthMotorBoard.

See test_stage docstring for test parameters and procedure.

Copyright 2019-2022 Light Conversion
Contact: support@lightcon.com
"""
import numpy as np
from lightcon.eth_motor_board import EthMotorBoard


def test_stage(
        stage_name=None, emb_addr=None, motor_idx=0, ref_travel_len=None,
        reset_move_speed=100000, do_reset_test=True, do_center_test=True,
        do_back_and_forth_test=True, num_back_and_forth_tests=5):
    """Test stage.

    Reset and move around a linear stage to test wether it is working properly.

    Parameters:
        emb_addr - IP address of the EthMotorBoard, set to None for autodetect
            using UDP locator
        stage_name - stage name string, e.g. 'Standa 8MT184-13'. There must be
            a json file containing the stage parameters.
        motor_idx - the port index where the motor is connected
        ref_travel_len - the reference total travel length of the stage in
            steps
        reset_move_speed - the speed at which the stage moves during reset,
            must be low enough for acurrate resets and to prevent the stage
            crashing into the limit switch
        num_back_and_forth_tests - the number of back and forth movements per
            each speed setting

    The following tests can be performed:
        - Reset: move slowly towards the limit switch and test whether the
        stage can sucessfully find it. Also test whether the available travel
        length of stage is valid.

        - Center: move the to the center of the travel range. The user can then
        visually inspect if the center position is correct.

        - Back and forth: move the stage back and forth a number of times at
        different speeds and reset the stage after each speed setting to verify
        that the stage has not lost it's position.
    """
    if stage_name is None:
        raise ValueError("No stage name given")

    print("=== {:} stage test ===".format(stage_name))

    print("This test will check the functionality of a {:} stage The stage "
          "should be connected to port {:d}) of the EthMotorBoard".format(
            stage_name, motor_idx))

    print("Connecting to EthMotorBoard...")

    motorb = EthMotorBoard(ip_address=emb_addr)

    motorb.setup_stage(motor_idx, stage_name + '.json')

    if motorb.connected:
        travel_length = ref_travel_len
        if do_reset_test:
            print("Resetting stage...", end='', flush=True)
            motorb.reset_motor(motor_idx, speed=reset_move_speed, move_dir=1)
            travel_length = np.abs(motorb.reset_motor(
                motor_idx, speed=reset_move_speed, move_dir=0).get(
                    'abs_pos_at_reset'))
            print("Done")
            print("Stage travel length: ", travel_length, end='')
            if np.abs(1 - travel_length/ref_travel_len) < 0.1:
                print(", OK")
            else:
                print(", INCORRECT")

        if do_center_test:
            print("Centering stage...", end='', flush=True)
            motorb.move_abs(motor_idx, int(travel_length/2))
            motorb.wait_until_stopped(motor_idx)
            print("OK")

        if do_back_and_forth_test:
            print("Back and forth tests, N={:} at each speed. Measuring reset "
                  "delta:".format(num_back_and_forth_tests), flush=True)
            orig_speed = motorb.get_max_speed(motor_idx)
            for speed_fac in (0.5, 1, 2, 4):
                print("\tAt {:.2f}x speed...".format(speed_fac),
                      flush=True, end='')
                motorb.set_max_speed(motor_idx, int(orig_speed*speed_fac))
                for ind in range(num_back_and_forth_tests):
                    # Move forward
                    motorb.move_abs(
                        motor_idx, int(travel_length/2 + travel_length/3))
                    motorb.wait_until_stopped(motor_idx)

                    # Move back
                    motorb.move_abs(
                        motor_idx, int(travel_length/2 - travel_length/3))
                    motorb.wait_until_stopped(motor_idx)

                    # Reset
                    motorb.run_stage(
                        motor_idx, speed=reset_move_speed, move_dir=0)
                    motorb.wait_until_stopped(motor_idx)
                    print('{:} '.format(motorb.get_abs_pos(motor_idx)), end='')

                motorb.reset_motor(
                    motor_idx, speed=reset_move_speed, move_dir=0)
                print('')

        # Reset original speed
        motorb.set_max_speed(motor_idx, int(orig_speed))

        print("Centering stage...", end='', flush=True)
        motorb.move_abs(motor_idx, int(travel_length/2))
        motorb.wait_until_stopped(motor_idx)
        print("OK")

    else:
        print("Could not connect to an EthMotorBoard")
