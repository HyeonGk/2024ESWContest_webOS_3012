#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import threading
import time  # time 라이브러리 사용

class TurtleBotController:
    def __init__(self):
        # ROS 노드 초기화
        rospy.init_node('turtlebot3_controller', anonymous=True)

        # 퍼블리셔 설정
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.command_sub = rospy.Subscriber("/turtlebot_command", String, self.command_callback)

        # 상태 변수 초기화
        self.navigation_mode = False  # 네비게이션 모드 비활성화
        self.teleop_mode = True  # 처음에 수동 모드 활성화
        self.is_macro_running = False  # 매크로 실행 여부

        # 속도 설정
        self.linear_speed = 0.0  # 현재 직진 속도
        self.angular_speed = 0.0  # 현재 회전 속도
        self.max_linear_speed = 2.0  # 최대 직진 속도
        self.max_angular_speed = 2.0  # 최대 회전 속도
        self.accel_linear_step = 0.02  # 직진 속도 증가량
        self.accel_angular_step = 0.05  # 회전 속도 증가량

        # 매크로 명령어 목록
        self.macro_commands = [
            {"linear": 1.0, "angular": 0.0, "duration": 2.9},  # 4초 동안 직진
            {"linear": 0.2, "angular": -1.7, "duration": 3.2},  # 2초 동안 회전
            {"linear": 1.0, "angular": 0.0, "duration": 2},  # 2초 동안 직진
            {"linear": 0.0, "angular": 0.0, "duration": 1},  # 1초 정지
            {"linear": -1.0, "angular": 0.0, "duration": 2},  # 2초 동안 후진
            {"linear": -0.2, "angular": 1.7, "duration": 3.2},  # 2초 동안 반대 회전
            {"linear": -1.0, "angular": 0.0, "duration": 2.9},  # 4초 동안 후진
        ]
        self.current_macro_index = 0  # 첫 번째 매크로 명령어부터 시작

        # 속도를 퍼블리시할 스레드 실행
        self.is_running = True
        self.publish_speed_thread = threading.Thread(target=self.publish_speed)
        self.publish_speed_thread.start()

    def command_callback(self, msg):
        """명령어 처리 콜백 함수"""
        command = msg.data.lower().strip()
        rospy.loginfo(f"Command received: {command}")

        if command == "start_navigation":
            self.start_macro()  # 네비게이션 시작
        elif command == "end_navigation":
            self.end_macro()  # 네비게이션 종료
        elif self.teleop_mode and not self.navigation_mode:  # 수동 모드에서만 명령 처리
            self.handle_teleop_command(command)
        else:
            rospy.logwarn(f"Unknown command or incorrect mode: {command}")

    def handle_teleop_command(self, command):
        """수동 모드에서 teleop 명령어 처리"""
        if command == "front":
            self.linear_speed = min(self.linear_speed + self.accel_linear_step, self.max_linear_speed)
            rospy.loginfo(f"Accelerating forward: {self.linear_speed}")
        elif command == "back":
            self.linear_speed = max(self.linear_speed - self.accel_linear_step, -self.max_linear_speed)
            rospy.loginfo(f"Accelerating backward: {self.linear_speed}")
        elif command == "left":
            self.angular_speed = min(self.angular_speed + self.accel_angular_step, self.max_angular_speed)
            rospy.loginfo(f"Turning left: {self.angular_speed}")
        elif command == "right":
            self.angular_speed = max(self.angular_speed - self.accel_angular_step, -self.max_angular_speed)
            rospy.loginfo(f"Turning right: {self.angular_speed}")
        elif command == "neutral":
            self.linear_speed = 0
            self.angular_speed = 0
            rospy.loginfo("Stopping robot")
        else:
            rospy.logwarn(f"Unknown teleop command: {command}")

    def publish_speed(self):
        """지속적으로 속도를 퍼블리시하는 스레드"""
        rate = rospy.Rate(10)  # 10Hz로 실행
        while not rospy.is_shutdown():
            if self.teleop_mode and not self.navigation_mode and not self.is_macro_running:  # Teleop 모드에서만 속도 퍼블리시
                twist = Twist()
                twist.linear.x = self.linear_speed
                twist.angular.z = self.angular_speed
                self.cmd_vel_pub.publish(twist)
            rate.sleep()

    def start_macro(self):
        """매크로 시작"""
        if not self.navigation_mode:
            self.navigation_mode = True
            self.teleop_mode = False  # 수동 모드 비활성화
            self.is_macro_running = True
            self.current_macro_index = 0  # 매크로를 처음부터 시작
            rospy.loginfo("Starting macro execution...")
            macro_thread = threading.Thread(target=self.execute_macro)
            macro_thread.start()  # Separate thread to run macro commands
        else:
            rospy.logwarn("Macro is already running.")

    def execute_macro(self):
        """매크로 명령어를 순차적으로 실행"""
        rate = rospy.Rate(10)  # 10Hz로 실행
        while self.navigation_mode and self.is_macro_running:
            if self.current_macro_index >= len(self.macro_commands):
                self.current_macro_index = 0  # 매크로가 끝나면 다시 처음으로

            current_command = self.macro_commands[self.current_macro_index]
            linear = current_command["linear"]
            angular = current_command["angular"]
            duration = current_command["duration"]

            # 명령 시작 시 로봇 속도 설정
            self.set_velocity(linear, angular)
            rospy.loginfo(f"Executing macro {self.current_macro_index + 1}: "
                          f"Linear: {linear}, Angular: {angular}, Duration: {duration}s")

            # 주어진 시간 동안 속도를 지속적으로 퍼블리시
            start_time = time.time()
            while (time.time() - start_time) < duration and self.navigation_mode:
                # 주기적으로 같은 속도를 퍼블리시
                self.set_velocity(linear, angular)
                rate.sleep()

            self.current_macro_index += 1  # 다음 매크로로 이동

        self.is_macro_running = False  # 매크로 실행 종료 표시

    def end_macro(self):
        """매크로 중지 및 텔레오프 모드 전환"""
        self.navigation_mode = False
        self.is_macro_running = False  # 매크로 실행을 즉시 중단
        self.switch_to_teleop()
        rospy.loginfo("Macro execution stopped, switching to teleop mode.")

    def switch_to_teleop(self):
        """수동 모드로 전환"""
        rospy.loginfo("Switching to teleop mode.")
        self.set_velocity(0.0, 0.0)  # 로봇 정지
        self.teleop_mode = True  # 수동 모드 활성화
        rospy.loginfo("Teleop mode activated.")

    def set_velocity(self, linear_x, angular_z):
        """로봇 속도 설정"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.cmd_vel_pub.publish(twist)
        rospy.loginfo(f"Set velocity: Linear X: {linear_x}, Angular Z: {angular_z}")

    def run(self):
        """ROS 스핀 실행"""
        rospy.spin()

if __name__ == '__main__':
    controller = TurtleBotController()
    controller.run()

