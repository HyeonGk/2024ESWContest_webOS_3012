#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

current_index = 0
waypoints = []
client = None

def load_waypoints():
    global waypoints
    # 웨이포인트를 (x, y, z, w) 형식으로 설정합니다.
    waypoints = [
        {'x': 1.0, 'y': 1.0, 'z': 0.0, 'w': 1.0},
        {'x': 2.0, 'y': 2.0, 'z': 0.0, 'w': 1.0},
        {'x': 3.0, 'y': 3.0, 'z': 0.0, 'w': 1.0},
        {'x': 4.0, 'y': 4.0, 'z': 0.0, 'w': 1.0},
        {'x': 5.0, 'y': 5.0, 'z': 0.0, 'w': 1.0},
        {'x': 6.0, 'y': 6.0, 'z': 0.0, 'w': 1.0},
        {'x': 7.0, 'y': 7.0, 'z': 0.0, 'w': 1.0},
    ]

def move_to_waypoint(index):
    global client
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = waypoints[index]['x']
    goal.target_pose.pose.position.y = waypoints[index]['y']
    goal.target_pose.pose.orientation.z = waypoints[index]['z']
    goal.target_pose.pose.orientation.w = waypoints[index]['w']
    
    client.send_goal(goal)
    client.wait_for_result()

def waypoint_navigation():
    global current_index, waypoints
    while not rospy.is_shutdown():
        move_to_waypoint(current_index)
        current_index += 1
        if current_index >= len(waypoints):
            rospy.loginfo("All waypoints visited")
            break

if __name__ == '__main__':
    rospy.init_node('turtlebot_waypoint_navigator')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    load_waypoints()
    waypoint_navigation()
