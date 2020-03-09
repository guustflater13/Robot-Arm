# Robot-Arm
I want to use an android OS to connect over ethernet with the raspberry and control the Robot Arm
Robot Arm using:

Android phone,
Raspberrry Pi with Raspbian,
PCA9685 with adafruit driver,

Robot arm: 
       
       O
      / \
arm1 /   \ arm2
    /     \
   /       O---- gripper (Remains horizontal when moving arms)    
  O              
-----
| 0 |
-----

0: Table, not yet in place (180 degrees rotation)
1: Lower arm
2: Higher arm

O = Pivot point
