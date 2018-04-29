import rospy
import std_msgs
import roslib
import readline
import math
from ein.msg import EinState
from std_msgs.msg import String
import time
from coordinate_publisher.msg import PointArray
import os
from threading import Timer
import sys

class secondary_actions:
	def __init__(self):
		rospy.init_node("secondary_actions",anonymous=False)
		self.speech = rospy.Subscriber("/recognizer/output",std_msgs.msg.String,self.speech_callback)
		#self.speech = rospy.Subscriber("/speech_recognition",String,self.speech_callback)
		self.gesture = rospy.Subscriber("/all_positions",PointArray,self.gesture_callback)
		self.head = rospy.Publisher("/ein/right/forth_commands",std_msgs.msg.String, queue_size=10)
		self.head2 = rospy.Publisher("/ein/left/forth_commands",std_msgs.msg.String, queue_size=10)
		self.gestureThreshold = 15
		self.validatingSpeech = False
		self.validatingGesture = False
		self.detonated = False
		self.timer = 10
		#self.blinkHead()
		
		#os.system("mpg123 ./speech.mp3")

		#rate = rospy.Rate(1)
		rospy.spin()
		#while not rospy.is_shutdown():
		#	rate.sleep()
	
	def baxterDone(self):
		os.system("mpg123 ./speech.mp3")
		sys.exit(0)
	def speech_callback(self,message):
		print message
		words = str(message).split( )
		wordCount = len(words)
		if (wordCount > 0):
			if self.detonated == False:
				self.detonated = True
				t = Timer(self.timer,self.baxterDone)
				t.start()
			if not self.validatingSpeech:
				self.validatingSpeech = True
				self.blinkHead()
				time.sleep(.5)
				self.validatingSpeech = False
			#self.blinkHead()
			#self.head.publish("0 1 setSonarLed")
			#print "Wordsssss"
			#time.sleep(1)
			#self.head.publish("0 0 setSonarLed")			
			#print "==================================="
	def gesture_callback(self,ar):
		lo = [ar.points[0].x,ar.points[0].y,ar.points[0].z]
		ro = [ar.points[1].x,ar.points[1].y,ar.points[1].z]
		lp = [ar.points[2].x,ar.points[2].y,ar.points[2].z]
		rp = [ar.points[3].x,ar.points[3].y,ar.points[3].z]
		ho = [ar.points[4].x,ar.points[4].y,ar.points[4].z]
		
		if ((self.isValidGesture(ho,rp) or self.isValidGesture(ho,lp))):
			print("True")
			self.head2.publish("blink_arms")
			if self.detonated == False:
				self.detonated = True
				t = Timer(self.timer,self.baxterDone)
				t.start()			
			#time.sleep(1)
			#self.validatingGesture = False
			#self.head.publish("happyFace")
		else:
			#self.head.publish("sadFace")
			print("False")
			pass
	def blinkHead(self):
		self.head.publish("blink_sonar_swoop")
		#self.head.publish("0 1 setSonarLed")
		#time.sleep(0.3)
		#self.head.publish("0 0 setSonarLed")
	
	#@origin: Origin of pointing vecctor (HEAD)
	#@target: Target location of pointing vector (HAND)
	def isValidGesture(self,origin,target):
		valid = False
		if((not(origin == [0,0,0])) and (not(target == [0,0,0]))):
			curAngle = self.angleBetween(origin,target,[0,0,0]) #The angle between pointing gesture and Baxter's Body
			ang = (curAngle*180/math.pi)
			#print ang
		if ang < self.gestureThreshold:
			#self.head.publish("happyFace");
			#self.head.publish("blink_arms");
			return True
		else:
			#self.head.publish("sadFace");
			return False
	
	def angleBetween(self,origin,p1,p2):
		v1 = [0,0,0]
		v2 = [0,0,0]

		v1[0] = p1[0] - origin[0]
		v1[1] = p1[1] - origin[1]
		v1[2] = p1[2] - origin[2]

		v2[0] = p2[0] - origin[0]
		v2[1] = p2[1] - origin[1]
		v2[2] = p2[2] - origin[2]
		
		rat = (self.dotProd(v1,v2))/(self.distance(v2,[0,0,0])*self.distance(v1,[0,0,0]))
		angle = math.acos(rat)
		if (angle <= 0):
			angle *= -1
		if (angle < math.pi-angle):
			return angle
		else:
			return math.pi - angle
		
	def dotProd(self,v1,v2):
		ret = 0
		for i in range(len(v1)):
			ret += v1[i]*v2[i]
		return ret
	def distance(self,x,y):
		sum = 0
		for i in range(len(x)):
			sum += math.pow(x[i]-y[i],2)
		return math.sqrt(sum)

sa = secondary_actions()

