#!/usr/bin/env python



import numpy
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread




class PicoFlexxSens(Thread):

    def callback(self,data):
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
        #rospy.loginfo(data.type)
        #cv_image = bridge.imgmsg_to_cv2(image_message, desired_encoding="passthrough")
        try:
          bridge = CvBridge()
          cv_image = bridge.imgmsg_to_cv2(data, "32FC1")
          array = numpy.asarray(cv_image)
          #rospy.loginfo("columns:")
          #rospy.loginfo(len(array[70]))
          #rospy.loginfo("values:")
          #rospy.loginfo(array[70])

          self.mainclass.distances = array[70]
          #print (array[70])

        except CvBridgeError as e:
          print(e)
        #rospy.loginfo("heard something")



    def __init__(self,mainclass):
        Thread.__init__(self)

        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        self.mainclass = mainclass

        rospy.init_node('listener', anonymous=True)

        rospy.loginfo("starting")

        #rospy.Subscriber('chatter', String, callback)
        rospy.Subscriber('/pico_flexx/image_depth', Image, self.callback)

        rospy.loginfo("subscribed")



    def run(self):

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()
