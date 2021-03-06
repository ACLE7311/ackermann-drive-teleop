#!/usr/bin/env python

'''
ackermann_drive_joyop.py:
    A ros joystick teleoperation script for ackermann steering based robots 

modified by Aaron Clements for the ACFR ITS EV Program Nov 17
'''

__author__ = 'George Kouros'
__license__ = 'GPLv3'
__maintainer__ = 'George Kouros'
__email__ = 'gkourosg@yahoo.gr'

import rospy
from ackermann_msgs.msg import AckermannDrive
from sensor_msgs.msg import Joy
import sys

class AckermannDriveJoyop:

    def __init__(self):
	if rospy.has_param('max_speed'):
		self.max_speed = rospy.get_param('max_speed')
	else:
		self.max_speed = 1.0
	
	if rospy.has_param('max_steering_angle'):
		self.max_steering_angle = rospy.get_param('max_steering_angle')
	else:
		self.max_steering_angle = 0.7
	
	# what does this cmd_topic actually do? think its just the name
        cmd_topic = 'ackermann_cmd'
	self.speed = 0
        self.steering_angle = 0
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.drive_pub = rospy.Publisher(cmd_topic, AckermannDrive,
                                         queue_size=1)
        rospy.Timer(rospy.Duration(1.0/20.0), self.pub_callback, oneshot=False)
        rospy.loginfo('ackermann_drive_joyop_node initialized')

    def joy_callback(self, joy_msg):
	# Dead man switch implemented by RB1 and LB1, else 0
	if joy_msg.buttons[4] == 1 and joy_msg.buttons[5] == 1:
		# added limit to eliminate controller MODE button operation
        	if abs(joy_msg.axes[1]) != 1:
			self.speed = joy_msg.axes[1] * self.max_speed;
        	self.steering_angle = joy_msg.axes[2] * self.max_steering_angle;
	else:
		self.speed = 0
		self.seering_angle = 0

    def pub_callback(self, event):
        ackermann_cmd_msg = AckermannDrive()
        ackermann_cmd_msg.speed = self.speed
        ackermann_cmd_msg.steering_angle = self.steering_angle
        self.drive_pub.publish(ackermann_cmd_msg)
        self.print_state()

    def print_state(self):
        sys.stderr.write('\x1b[2J\x1b[H')
        rospy.loginfo('\x1b[1M\r'
                      '\033[34;1mSpeed: \033[32;1m%0.2f m/s, '
                      '\033[34;1mSteering Angle: \033[32;1m%0.2f rad\033[0m',
                      self.speed, self.steering_angle)

    def finalize(self):
        rospy.loginfo('Halting motors, aligning wheels and exiting...')
        ackermann_cmd_msg = AckermannDrive()
        ackermann_cmd_msg.speed = 0
        ackermann_cmd_msg.steering_angle = 0
        self.drive_pub.publish(ackermann_cmd_msg)
        sys.exit()

if __name__ == '__main__':
    rospy.init_node('ackermann_drive_joyop_node')
    joyop = AckermannDriveJoyop()
    rospy.spin()
