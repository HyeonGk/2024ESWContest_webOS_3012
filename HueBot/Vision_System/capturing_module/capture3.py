import cv2
import time
import copy
import numpy as np

"""
영상을 테스트하는 코드
"""

# 카메라 초기화
cap = cv2.VideoCapture(1)

while 1:
    ret, frame = cap.read()  # 카메라에서 프레임 읽기
    if ret:
        brightness = 0
        bright_image = cv2.add(frame, np.ones(frame.shape, dtype=np.uint8) * brightness)
        
        converted_frame = copy.deepcopy(bright_image)
        contrast_image = cv2.convertScaleAbs(converted_frame, alpha=1.6)
        # 프레임을 화면에 표시
        cv2.imshow('Webcam', contrast_image)
        
        # 1초 대기
        time.sleep(1)
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to capture image.")

    

# 카메라 해제 및 모든 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
