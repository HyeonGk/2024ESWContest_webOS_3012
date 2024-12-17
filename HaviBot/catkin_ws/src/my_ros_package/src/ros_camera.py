#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import websocket
import cv2
import numpy as np
import base64
from cv_bridge import CvBridge

# WebSocket 서버 주소 설정
NODE_SERVER_URL = "ws://localhost:3000/camera"  # Node.js WebSocket 서버 주소

# OpenCV와 ROS 간 이미지 변환 브리지
bridge = CvBridge()

# WebSocket 연결 함수 (재연결 지원)
def connect_websocket():
    try:
        ws = websocket.WebSocket()
        ws.connect(NODE_SERVER_URL)
        rospy.loginfo("Connected to WebSocket server")
        return ws
    except Exception as e:
        rospy.logerr(f"WebSocket connection error: {e}")
        return None

# ROS 이미지 콜백 함수
def image_callback(msg):
    try:
        # ROS 이미지를 OpenCV 이미지로 변환
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 이미지를 JPEG로 인코딩 후 Base64로 변환
        _, buffer = cv2.imencode('.jpg', cv_image)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Node.js 서버로 전송
        if ws and ws.connected:
            ws.send(jpg_as_text)
        else:
            rospy.logwarn("WebSocket not connected")

    except Exception as e:
        rospy.logerr(f"Error sending image: {e}")

def main():
    rospy.init_node('ros_to_node', anonymous=True)
    rospy.Subscriber("/raspicam_node/image/compressed", CompressedImage, image_callback)
    rospy.loginfo("Subscribed to /raspicam_node/image/compressed")

    # WebSocket 연결 설정
    global ws
    ws = connect_websocket()

    rospy.spin()  # ROS 이벤트 루프

    # 종료 시 WebSocket 연결 닫기
    if ws:
        ws.close()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
