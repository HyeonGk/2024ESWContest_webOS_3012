import socketio
import keyboard
import time

# Flask 서버에 연결하기 위해 SocketIO 클라이언트 인스턴스 생성
sio = socketio.Client()

# 서버에 연결되었을때 호출되는 이벤트 헨들러
@sio.event
def connect():
    print('Connected to the server')

# 서버와 연결이 끊어졌을떄 호추되는 이벤트 헨들러
@sio.event
def disconnect():
    print('Disconnected from the server')

# 서버로부터 'real_time_text' 이벤트를 수신했을때 호출되는 이벤트 헨들러
@sio.on('label')
def handle_real_time_text(data):
    print(f"Received data: {data['label']}")
    #if data['label'] 


# 키보드에 인터럽트 거는 기능 넣어주기(ctrl+c)
try:
    # 서버에 연결 시도
    sio.connect('http://192.168.145.126:5000')

    # 무한 루프에서 클라이언트 실행을 유지하면서 Ctrl+F 감지
    while True:
        time.sleep(0.1)  # CPU 사용량을 줄이기 위해 약간의 대기 시간을 둠

except KeyboardInterrupt:
    print("\nProgram interrupted. Closing connection...")
    sio.disconnect()  # 소켓 연결 종료
    print("Connection closed.")