import rospy
import std_msgs
import roslib
import readline
import math
from ein.msg import EinState
from std_msgs.msg import String


def main():
	rospy.init_node("secondary_actions",anonymous=False)
	subscriber = rospy.Subscriber("/speech_recognition",String,speech_callback)
	rospy.spin()
def speech_callback(message):
	print message

main()
