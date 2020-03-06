# robot_arm_control
# Author: GuustFlater13

from __future__ import division

# Uncomment to enable debug output.
import logging

# Robot arm functions
import robot_arm_functions


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initialize starting point
    current_angle_arm_under = robot_arm_functions.base_arm_under()
    current_angle_arm_above = robot_arm_functions.base_arm_above()

    # If not on Base, Go direct to base (not using go_arm_by_steps because current values unknown)
    robot_arm_functions.directly_back_to_base()

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
        robot_arm_functions.go_arm2_by_steps(current_angle_arm_above, angle_arm_above)
        current_angle_arm_above = angle_arm_above
        # arm under
        robot_arm_functions.go_arm1_by_steps(current_angle_arm_under, angle_arm_under)
        current_angle_arm_under = angle_arm_under
        # gripper
        robot_arm_functions.gripper(angle_gripper)


if __name__ == "__main__":
    main()
