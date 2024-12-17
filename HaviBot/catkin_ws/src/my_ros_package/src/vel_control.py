#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class TurtleBotController:
    def __init__(self):
        # ROS 초기화
        rospy.init_node('turtlebot3_controller', anonymous=True)

        # /cmd_vel Publisher 생성
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

        rospy.loginfo("TurtleBotController initialized and ready to receive commands.")

    def set_velocity(self, linear_x, angular_z):
        """웹에서 받은 속도 명령을 로봇에 전송"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.cmd_vel_pub.publish(twist)
        rospy.loginfo(f"Velocity set: Linear X = {linear_x}, Angular Z = {angular_z}")

    def run(self):
        """ROS 스핀 실행"""
        rospy.spin()

if __name__ == '__main__':
    # 컨트롤러 인스턴스 생성 및 실행
    controller = TurtleBotController()
    controller.run()