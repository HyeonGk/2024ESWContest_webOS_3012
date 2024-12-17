# 2024임베디드SW경진대회(webOS부문) - ELECBRO팀
<div align="right">
<a href="https://github.com/YUNSUNGWOONG/2024ESWContest_webOS_3012"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
<a href="https://www.youtube.com/watch?v=8vGp5RCuV1c&list=PL55PqTOxkIlj9y1oz22rkJxP7jqsUbBGb&index=1"><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white"/></a>
<a href="https://velog.io/@2170004487z/series/%EC%A0%9C22%ED%9A%8C-%EC%9E%84%EB%B2%A0%EB%94%94%EB%93%9CSW%EA%B2%BD%EC%A7%84%EB%8C%80%ED%9A%8C" target="_blank"><img src="https://img.shields.io/badge/Velog_(2170004487z)-20C997?style=for-the-badge&logo=velog&logoColor=white"/></a>
</div>


<p align="center">
  <br>
 	<img src="./assets/images/README/image-20241026190510507.png" alt="elebro_logo" style="zoom:50%;" />
  <br>
</p>



# 작품 명: AGRIBOT

## ✨작품개요
**"농업의 미래를 바꾸다", 자동화 작물공정 혁신 솔루션, AGRIBOT**<br>
고령화로 인한 농업인력의 감소와 외국인 노동자의 연봉 상승에 따른 생산비 증가,
→ webOS를 활용, 작물 수확 및 분류를 원스톱으로 진행하는 자동화 솔루션을 제안,



## 💡개발환경

![image-20241026012052490](./assets/images/README/image-20241026012052490.png)

#### ▶자동수확로봇(하비봇)

- 자율주행기술로 사전에 수집한 농장부지맵을 기반으로 농장전체를 이동하면서 수확
- 트랙터와 유사한 바퀴 및 궤도시스템을 사용
- 아치형 형태로 배치된 카메랄를 통해 농작물을 감지, 프로펠러형 칼날로 수확



![image-20241026012127846](./assets/images/README/image-20241026012127846.png)

#### ▶자동분류로봇(휴봇)

- 이미지 색깔정보를 기반으로 AI에 의해 분류기를 회전시켜 분류 및 저장
- 타이밍에 맞춰, 분류기와 컨베이어 벨트의 회전을 제어



##  💻아키텍처

![brave_mzQNmdiKvy](./assets/images/README/brave_mzQNmdiKvy.webp)

## 🎮기능

### webOS

- 모니터링기능
- 작물관리기능
- 로봇제어기능
- 비전모델 관리기능



### HAVIBOT

- 자율주행/수동주행 기능
- 작물수확기 제어기능

- 실시간 영상 스트리밍 기능



### HUEBOT

- 작물 이미지 식별 기능
- 작물 분류 기능
- 실시간 영상 스트리밍 기능







## 📂파일구성

```bash
📦2024ESWContest_webOS_3012
┃📦HaviBot
┃ ┣ 📂body_module
┃ ┃ ┗ 📜body_module.c
┃ ┣ 📂catkin_ws
┃ ┃ ┗ 📂waypoint_navigation
┃ ┃ ┗ 📂rosbridge_websocket
┃ ┃ ┗ 📂turtlebot_controller
┃ ┃ ┗ 📂camera
┃ ┃ ┗ 📂vel_control
┃ ┗ 📂dc_module
┃ ┃ ┣ 📂dcmotor_control_for_linux
┃ ┃ ┃ ┗ 📜dcmotor_control.ino
┃📦HueBot
┃ ┣ 📂ConveyerBelt
┃ ┣ 📂Vision_System
┃ ┃  ┣ 📂capturing_module
┃ ┃  ┣ 📂classifing_module
┃ ┃  ┣ 📂detecting_module
┃ ┃  ┣ 📂streaming_module
┃ ┃  ┣ 📂models
┃📦webOS
┃ ┣ 📂app
┃ ┣ 📂appservice
┃ ┣ 📂arduino
┃ ┣ 📂videoserver
```



## ✔️함수구성

![image-20241026015234841](./assets/images/README/image-20241026015234841.png)







## 📋개발일정

![image-20241031033843808](./assets/images/README/image-20241031033843808.png)





## 📑업무분장

**"농업의 미래를 앞당기는 팀원들"**

| Profile | Role | Part | Tech Stack |
| ------- | ---- | ---- | ---------- |
| <div align="center"><a href="https://blog.naver.com/yhon89"><img src="./assets/images/README/hyongoon.png" width="80px;" alt=""/><br/><sub><b>김현근</b><sub></a></div> | 팀장 | webOS구축, Luna-Service 개발 | NodeJS, ReactJS, Arduino, MongoDB, Arduino |
| <div align="center"><a href="https://blog.naver.com/yhon89"><img src="./assets/images/README/sungwoong.png" width="80px;" alt=""/><br/><sub><b>윤성웅</b><sub></a></div> | 팀원 | 프로세서 설계,YOLOv5 API 개발, Vision Model 개발 | Pytorch,OpenCV,RaspberryPI,AUTOSAR |
| <div align="center"><a href="https://blog.naver.com/yhon89"><img src="./assets/images/README/jinseok.png" width="80px;" alt=""/><br/><sub><b>박진석<sub></a></div> | 팀원 | ROS개발환경 구축, Turtlebot 개발, ROS-Bridge 개발 | NodeJS, MongoDB, ROS, PointCloud |
| <div align="center"><a href="https://blog.naver.com/yhon89"><img src="./assets/images/README/jaewon.png" width="80px;" alt=""/><br/><sub><b>김재원</b><sub></a></div> | 팀원 | 데이터 수집 및 라벨링, 데이터 학습 | Python, tkinter, NodeJS, ReactJS, Arduino |
| <div align="center"><a href="https://blog.naver.com/yhon89"><img src="./assets/images/README/yongjin.png" width="80px;" alt=""/><br/><sub><b>김용진</b><sub></a></div> | 팀원 | 프로토타입 설계, 스마트팜 부지 설계 | C/C++, Arduino, Fusion360, P-Spice |



### 📣Team SLOGAN

**Accelerating the World's Transition to Sustainable Agriculture.**

**“지속가능한 농업으로의 전세계적 전환을 가속화한다” with .AGRIBOT.**



## ※Appendix

<details>
<summary><h2>&nbsp;I. Q&A </h2></summary><br/>

**❓** 스마트팜을 도입하려는 농장주의 재배 작물이 다양할 수 있는데, 사과, 딸기, 오렌지, 참외 등 다양한 작물에 대해 분류할 수 있는 방안이 있나요?

**🅰** YOLOv5 기반 비전 모델을 통해 농작물의 범주를 고려한 다양한 비전 모델을 개발할 계획이며, 농장 환경에 맞는 데이터를 확보하면 맞춤형 모델 제작이 가능해 작물 종류에 따른 제약이 없습니다.

<hr>

**❓** 작물을 재배하거나 운송, 분류할 때 작물의 손상을 줄여야 상품 가치가 높아질 텐데, 일렉브로 팀의 수확 과정에서 작물 손상이 많이 발생하지 않을까요?

**🅰** 저희는 상품 가치가 높은 작물의 손상을 줄이기 위해 로봇팔 디자인을 개선하거나, 충격 흡수에 적합한 부드러운 소재를 활용하여 손상 최소화 방안을 마련할 수 있습니다.

<hr>

**❓** 현재 webOS에서 하비봇만 제어하고 있으며, 휴봇은 별도로 제어되고 있는데, 두 로봇을 통합하여 중앙 제어할 필요는 없는가? 현재 두 로봇 간의 작업이 순조롭게 이어지고 있는가?


**🅰** 두 로봇은 하나의 시스템에 속하지만 각각 수확과 분류라는 독립적인 역할을 수행하고 있어, 개별 제어로도 작업 효율을 유지할 수 있습니다. 이 독립적인 제어 구조는 webOS 시스템의 부담을 줄이고 각 로봇의 최적 성능을 보장하며, 유지 관리 및 확장에도 유연하게 대응할 수 있어 추가 기능이 필요할 경우에도 무리가 없습니다.

<hr>

**❓** 이 시스템을 통해 수확한 데이터는 어떻게 활용하나요?

**🅰** 수확 데이터는 유동 자동화, 가격 최적화, 가격 최적화, 농장관리에 활용되어 신선도 유지와 품질관리를 돕고, 소비자 맞춤 서비스와 스마트 농업 시스템 구축에 기여할 수 있습니다.



<br/>
</details>






### &nbsp;II. Flow Chart

![image-20241026013321213](./assets/images/README/image-20241026013321213.png)

<hr>

![firefox_rsGu0FOLmr](./assets/images/README/firefox_rsGu0FOLmr.webp)

<hr>

![firefox_k7rLEkXU9k](./assets/images/README/firefox_k7rLEkXU9k.webp)



### &nbsp;IV. 논문 및 특허

- 박순용,"과수원 환경에서 로봇의 주행 제어 방법 및 이를 수행하기 위한 컴퓨팅 장치", 10-2024-0096958
- 박성호,"영상을 기반으로 한 작물재배 생육 플랫폼 구축을 통한 스마트팜 시스템", 10-2023-0088738
- 박승,"스마트팜 전동 차량의 주행방법 및 그 방법이 적용된 스마트팜 전동차량", 10-2021-0007445
