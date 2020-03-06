# robot_arm_control
# Author: GuustFlater13

from __future__ import division

# Uncomment to enable debug output.
import logging

# Import the PCA9685 module.
import Adafruit_PCA9685

# Robot arm functions
import robot_arm_functions

# Configure min and max servo pulse lengths
# MG946R
servo_min_mg946r = 90  # Min pulse length out of 4096
servo_max_mg946r = 600  # Max pulse length out of 4096

# SG60
servo_min_sg90 = 146  # Min pulse length out of 4096
servo_max_sg90 = 600  # Max pulse length out of 4096

channel_gripper = 3
channel_arm_under = 7
channel_arm_above = 11

base_arm_under = 20
base_arm_above = 50

max_arm_under = 100
max_arm_above = 120

# Initialise the PCA9685 using the default address (0x40)
# Alternatively specify a different address and/or bus:
# pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm = Adafruit_PCA9685.PCA9685()


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initialize starting point
    current_angle_arm_under = base_arm_under
    current_angle_arm_above = base_arm_above

    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

    # If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
    pwm.set_pwm(channel_arm_above, 0, robot_arm_functions.angle_to_pulse_arm(base_arm_above))
    pwm.set_pwm(channel_arm_under, 0, robot_arm_functions.angle_to_pulse_arm(base_arm_under))

    while True:
        angle_arm_under = input("Enter angle of lower arm (or q to quit): ")
        if angle_arm_under == "q" or angle_arm_under == "":
            robot_arm_functions.go_to_base(current_angle_arm_under, current_angle_arm_above)
            quit()
        angle_arm_above = input("Enter angle of higher arm (or q to quit): ")
        if angle_arm_above == "q" or angle_arm_above == "":
            robot_arm_functions.go_to_base(current_angle_arm_under, current_angle_arm_above)
            quit()
        angle_gripper = input("Enter angle of gripper (or q to quit): ")
        if angle_gripper == "q" or angle_gripper == "":
            robot_arm_functions.go_to_base(current_angle_arm_under, current_angle_arm_above)
            quit()

        # Move
        # arm above
        robot_arm_functions.go_arm_by_steps(channel_arm_above, current_angle_arm_above, angle_arm_above)
        current_angle_arm_above = angle_arm_above
        # arm under
        robot_arm_functions.go_arm_by_steps(channel_arm_under, current_angle_arm_under, angle_arm_under)
        current_angle_arm_under = angle_arm_under
        # gripper
        pwm.set_pwm(channel_gripper, 0, robot_arm_functions.angle_to_pulse_gripper(angle_gripper))


if __name__ == "__main__":
    main()
