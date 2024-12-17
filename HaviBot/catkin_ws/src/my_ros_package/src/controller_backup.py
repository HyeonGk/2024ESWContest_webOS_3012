#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, PoseStamped
from move_base_msgs.msg import MoveBaseActionResult
from std_msgs.msg import String
import actionlib
from move_base_msgs.msg import MoveBaseAction
import threading
import subprocess

class TurtleBotController:
    def __init__(self):
        # ROS 노드 초기화
        rospy.init_node('turtlebot3_controller', anonymous=True)

        # 퍼블리셔 및 서브스크라이버 설정
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.goal_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        self.result_sub = rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.result_callback)
        self.command_sub = rospy.Subscriber("/turtlebot_command", String, self.command_callback)

        # 상태 변수 초기화
        self.current_waypoint = 1  # 첫 웨이포인트부터 시작
        self.navigation_mode = False  # 네비게이션 모드 비활성화
        self.teleop_mode = True  # 처음에 수동 모드 활성화

        # move_base 클라이언트 설정
        self.move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_base_client.wait_for_server()

        # 속도 설정
        self.linear_speed = 0.0  # 현재 직진 속도
        self.angular_speed = 0.0  # 현재 회전 속도
        self.max_linear_speed = 0.2  # 최대 직진 속도
        self.max_angular_speed = 0.5  # 최대 회전 속도
        self.accel_linear_step = 0.02  # 직진 속도 증가량
        self.accel_angular_step = 0.05  # 회전 속도 증가량

        # 마지막 퍼블리시 속도 값 초기화
        self.last_linear_speed = 0.0
        self.last_angular_speed = 0.0

        # 현재 방향 명령어 상태 변수
        self.current_command = None

        # 시작 시 로봇 정지
        self.set_velocity(0, 0)

        # 스레드로 속도를 계속 퍼블리시하기 위한 변수
        self.is_running = True
        self.publish_speed_thread = threading.Thread(target=self.publish_speed)
        self.publish_speed_thread.start()

    def command_callback(self, msg):
        """명령어 처리 콜백 함수"""
        command = msg.data.lower().strip()  # 명령어를 소문자로 변환하고 공백 제거
        if not command:
            rospy.logwarn("Received an empty command.")
            return
        rospy.loginfo(f"Command received: {command}")  # 수신한 명령어를 명확히 출력

        # 명령어 처리
        if command == "start_navigation":
            self.start_navigation()  # 네비게이션 시작
        elif command == "end_navigation":
            self.end_navigation()  # 네비게이션 종료
        elif self.teleop_mode and not self.navigation_mode:  # 수동 모드이고 네비게이션 모드가 아닐 때만 명령 처리
            self.handle_teleop_command(command)
        else:
            rospy.logwarn(f"Unknown command or navigation mode active: {command}")  # 알 수 없는 명령어 경고

    def handle_teleop_command(self, command):
        """수동 모드에서 teleop 명령어 처리"""
        if command == "front":
            self.linear_speed = min(self.linear_speed + self.accel_linear_step, self.max_linear_speed)
            self.current_command = "front"
            rospy.loginfo(f"Accelerating forward: {self.linear_speed}")
        elif command == "back":
            self.linear_speed = max(self.linear_speed - self.accel_linear_step, -self.max_linear_speed)
            self.current_command = "back"
            rospy.loginfo(f"Accelerating backward: {self.linear_speed}")
        elif command == "left":
            self.angular_speed = min(self.angular_speed + self.accel_angular_step, self.max_angular_speed)
            self.current_command = "left"
            rospy.loginfo(f"Turning left: {self.angular_speed}")
        elif command == "right":
            self.angular_speed = max(self.angular_speed - self.accel_angular_step, -self.max_angular_speed)
            self.current_command = "right"
            rospy.loginfo(f"Turning right: {self.angular_speed}")
        elif command == "neutral":
            self.linear_speed = 0
            self.angular_speed = 0
            self.current_command = None  # Reset current command
            rospy.loginfo("Stopping robot")
        else:
            rospy.logwarn(f"Unknown teleop command: {command}")
            return  # 잘못된 명령어일 경우 동작하지 않음

    def publish_speed(self):
        """지속적으로 속도를 퍼블리시하는 스레드"""
        while self.is_running:
            if self.teleop_mode and not self.navigation_mode:  # Teleop 모드에서만 속도 퍼블리시
                twist = Twist()
                twist.linear.x = self.linear_speed
                twist.angular.z = self.angular_speed
                self.cmd_vel_pub.publish(twist)
                rospy.loginfo(f"Teleop mode - Published /cmd_vel: {twist.linear.x}, {twist.angular.z}")
            rospy.sleep(0.1)  # 10Hz로 퍼블리시

    def start_navigation(self):
        """네비게이션 모드 시작"""
        if not self.navigation_mode:
            self.navigation_mode = True
            self.teleop_mode = False  # 네비게이션 시작 시 수동 모드 비활성화
            self.linear_speed = 0  # 네비게이션 시작 시 속도 초기화
            self.angular_speed = 0
            rospy.loginfo("Navigation mode started. Moving to waypoint 1.")
            self.move_to_waypoint(self.current_waypoint)  # 첫 번째 웨이포인트로 이동

    def move_to_waypoint(self, waypoint):
        """지정된 웨이포인트로 이동"""
        if not self.navigation_mode:
            rospy.loginfo("Not in navigation mode.")
            return

        # 목표 설정 및 퍼블리시
        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.header.stamp = rospy.Time.now()

        # 각 웨이포인트의 좌표 설정
        waypoints = {
            1: (0.40609, -0.71288, -0.61567,0.788),
            2: (0.256273,-0.868197,0.96805,-0.25076),
            3: (-0.020254,-1.1084, 0.96767, -0.25223),
            4: (0.256273,-0.868197,0.96805,-0.25076),
            5: (0.40609, -0.71288, -0.61567,0.788),
            6: (0.05037, -0.001242, -0.52292, 0.85238)
        }

        if waypoint in waypoints:
            pos_x, pos_y, orient_z, orient_w = waypoints[waypoint]
            goal.pose.position.x = pos_x
            goal.pose.position.y = pos_y
            goal.pose.orientation.z = orient_z
            goal.pose.orientation.w = orient_w

            self.goal_pub.publish(goal)  # 목표 퍼블리시
            rospy.loginfo(f"Published goal to waypoint {waypoint}")
        else:
            rospy.loginfo("Invalid waypoint.")

    def result_callback(self, result):
        """네비게이션 결과 콜백"""
        if result.status.status == 3:  # 목표 도달 확인
            rospy.loginfo(f"Reached waypoint {self.current_waypoint}")

            # 다음 웨이포인트로 이동
            self.current_waypoint += 1
            if self.current_waypoint > 6:  # 마지막 웨이포인트에 도달하면 다시 웨이포인트 1로 돌아감
                self.current_waypoint = 1  # 웨이포인트 1로 다시 설정
                rospy.loginfo("Restarting from waypoint 1.")
            self.move_to_waypoint(self.current_waypoint)  # 다음 웨이포인트로 이동

    def end_navigation(self):
        """네비게이션 종료 및 Rviz 종료, teleop 모드 활성화"""
        rospy.loginfo("Ending navigation and switching to teleop mode...")

        # 네비게이션 목표 모두 취소
        self.cancel_navigation_goals()

        # 로봇을 정지시킴
        self.set_velocity(0, 0)  # 로봇 정지

        # move_base와 rviz 프로세스를 종료
        self.shutdown_move_base()
        self.shutdown_rviz()

        # teleop 모드 활성화
        self.switch_to_teleop()  # 수동 모드로 전환
        rospy.loginfo("Switched to teleop mode.")

    def cancel_navigation_goals(self):
        """move_base에서 모든 목표를 취소"""
        rospy.loginfo("Canceling all navigation goals...")
        self.move_base_client.cancel_all_goals()  # 모든 목표 취소
        self.navigation_mode = False  # 네비게이션 모드 비활성화

    def shutdown_move_base(self):
        """move_base 노드 종료"""
        rospy.loginfo("Shutting down move_base...")
        try:
            subprocess.call(["rosnode", "kill", "/move_base"])  # move_base 종료
            rospy.loginfo("move_base has been successfully shut down.")
        except Exception as e:
            rospy.logwarn(f"Failed to shut down move_base: {e}")

    def shutdown_rviz(self):
        """이미 실행 중인 Rviz 종료"""
        rospy.loginfo("Shutting down Rviz...")
        try:
            subprocess.call(["pkill", "rviz"])  # 이미 실행 중인 모든 Rviz 프로세스 종료
            rospy.loginfo("Rviz has been successfully shut down.")
        except Exception as e:

            rospy.logwarn(f"Failed to shut down Rviz: {e}")

    def switch_to_teleop(self):
        """수동 모드로 전환"""
        rospy.loginfo("Switching to teleop mode.")
        self.set_velocity(0, 0)  # 로봇 정지
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
        ros_thread = threading.Thread(target=lambda: rospy.spin())
        ros_thread.start()

if __name__ == '__main__':
    controller = TurtleBotController()
    controller.run()

