#!/usr/bin/env python

import rospy
import websocket
from sensor_msgs.msg import CompressedImage

class VideoStream:
    def __init__(self, server_url):
        """WebSocket 서버 연결 초기화."""
        self.server_url = server_url
        self.ws = None
        self.connect()

    def connect(self):
        """WebSocket 서버에 연결을 시도합니다."""
        try:
            self.ws = websocket.create_connection(self.server_url)
            rospy.loginfo(f"WebSocket 서버에 연결되었습니다: {self.server_url}")
        except Exception as e:
            rospy.logerr(f"WebSocket 연결 실패: {e}. 연결을 재시도하세요.")
            self.ws = None

    def send_frame(self, data):
        """WebSocket을 통해 프레임을 전송합니다."""
        if self.ws is None or not self.ws.connected:
            rospy.logwarn("WebSocket 연결이 끊어졌습니다. 연결을 시도합니다...")
            self.connect()

        if self.ws and self.ws.connected:
            try:
                # 데이터를 그대로 바이너리 형식으로 전송
                self.ws.send(data.data, opcode=websocket.ABNF.OPCODE_BINARY)  # 바이너리 데이터 전송
                rospy.loginfo("프레임 전송 중...")
            except Exception as e:
                rospy.logerr(f"WebSocket 전송 중 오류 발생: {e}. 연결을 재시도합니다.")
                self.ws.close()
                self.ws = None
    def close(self):
        """WebSocket 연결 종료."""
        if self.ws:
            self.ws.close()
            rospy.loginfo("WebSocket 연결 종료.")

def callback(data, video_stream):
    """ROS 콜백: 프레임을 WebSocket 서버로 전송."""
    video_stream.send_frame(data)

def main():
    """ROS 노드를 초기화하고 구독 설정."""
    rospy.init_node('video_stream_node', anonymous=True)

    # WebSocket 서버 URL 설정 (Node.js 서버 IP와 포트 입력)
    server_url = "ws://192.168.183.34:4000"  # 네 Node.js 서버 IP와 포트로 수정
    video_stream = VideoStream(server_url)

    # ROS 구독 설정
    rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, callback, video_stream)

    rospy.loginfo("TurtleBot3 카메라 스트리밍 시작...")
    rospy.spin()

    # 종료 시 WebSocket 연결 종료
    video_stream.close()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

