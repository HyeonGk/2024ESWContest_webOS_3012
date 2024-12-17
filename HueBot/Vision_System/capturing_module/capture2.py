import cv2
import time
import copy

"""
OpenCV를 사용하여 주어진 라벨범위까지 사진을 찍는 매크로 코드
"""

# 카메라 초기화
cap = cv2.VideoCapture(1)

# 사진을 저장할 폴더 경로
output_folder = 'images/'

alpha = 471
omega = 480

# 사진 촬영
for i in range(alpha, omega+1):
    ret, frame = cap.read()  # 카메라에서 프레임 읽기
    if ret:
        # 1.5초 대기
        time.sleep(1.5)

        converted_frame = copy.deepcopy(frame)
        contrast_image = cv2.convertScaleAbs(converted_frame, alpha=1.5)

        # 프레임을 화면에 표시
        cv2.imshow('Webcam', contrast_image)
        
        # 프레임 저장
        cv2.imwrite(f"{output_folder}image_{i}.jpg", frame)
        print(f"Image {i} captured.")
        
        
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to capture image.")

# 카메라 해제 및 모든 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
