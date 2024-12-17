import React, { useState, useEffect, useRef } from 'react';  
import css from './HarvestView.module.less';
import LS2Request from '@enact/webos/LS2Request';
import { Buffer } from 'buffer';

const bridge = new LS2Request();
const serviceUrl = 'luna://com.farm.app.service';
let currentChannelId = "001"; 
let channelCounter = 1;
//***********************showToast ************************//
const showToast = (message) => {
    const params = {
        "message": message  
    };

    const lsRequest = {
        "service": "luna://com.farm.app.service", 
        "method": "showToast", 
        "parameters": params,
        "onSuccess": onToastSuccess,
        "onFailure": onToastFailure
    };
    bridge.send(lsRequest);
};

const onToastSuccess = (response) => {
    console.log('Toast 호출 성공:', response);
};

const onToastFailure = (error) => {
    console.error('Toast 서비스 호출 실패:', error);
};
//****************************************************//

//************************  log  *************************//
const HubotView = () => {
    const [logs, setLogs] = useState([]);
    const logEndRef = useRef(null);

    // Scroll to the bottom whenever new log is added
    useEffect(() => {
        if (logEndRef.current) {
            logEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [logs]);

    useEffect(() => {
        const originalLog = console.log;
        const originalError = console.error;

        // Override console.log to capture logs
        console.log = (message) => {
            setLogs((prevLogs) => [...prevLogs, `LOG: ${message}`]);
            originalLog(message);
        };

        // Override console.error to capture errors
        console.error = (message) => {
            setLogs((prevLogs) => [...prevLogs, `ERROR: ${message}`]);
            originalError(message);
        };

        return () => {
            console.log = originalLog;
            console.error = originalError;
        };
    }, []);



//******************SPP 채널 열기 ********************** */
//*******************아두이노랑 연결하면 자동? 으로 채널이 열리는듯? 잘 모르겠다..****************** */
const createSPPChannelAndConnect = () => {
    const createChannelRequest = {
        service: 'luna://com.webos.service.bluetooth2',
        method: 'spp/createChannel',
        parameters: {
            "name": "farm",
            "uuid": "00001101-0000-1000-8000-00805f9b34fb",
            "subscribe": true
        },
        onSuccess: (msg) => {
            console.log('SPP 채널 생성 성공:', msg);
            showToast('SPP 채널 생성 성공');
            currentChannelId = msg.channelId;
            connectToArduino(msg.channelId);
        },
        onFailure: (msg) => {
            console.error('SPP 채널 생성 실패:', msg);
            showToast('SPP 채널 생성 실패');
        }
    };
    bridge.send(createChannelRequest);
};


//******************아두이노 블루투스 연결 ********************** */
const connectToArduino = () => {
    const connectRequest = {
        service: 'luna://com.webos.service.bluetooth2',
        method: 'spp/connect',
        parameters: {
            "address": "98:da:60:0a:92:df",
            "uuid": "00001101-0000-1000-8000-00805f9b34fb",
            "subscribe": true
        },
        onSuccess: (msg) => {
            console.log('아두이노 연결 성공:', msg);
            showToast('아두이노 연결 성공');
        },
        onFailure: (msg) => {
            console.log('아두이노 연결 실패:', msg);
            if (msg.errorText) {
                console.error('Error Text:', msg.errorText);
            }
            if (msg.errorCode) {
                console.error('Error Code:', msg.errorCode);
            }
            showToast('아두이노 연결 실패: ' + (msg.errorText || 'Unknown error'));
        }
    };
    bridge.send(connectRequest);
}; //이게 왜 되는지 모르겠음... 아두이노 연결 실패 뜨는데 채널 id가 그냥 1씩 오른 상태로 연결이 되어있음....

// ******************** SPP 채널 닫기 ****************** //
const closeSPPChannel = (channelId) => {
    const closeChannelRequest = {
        service: 'luna://com.webos.service.bluetooth2',
        method: 'spp/disconnect',
        parameters: {
            "channelId": channelId
        },
        onSuccess: (msg) => {
            console.log('SPP 채널 닫기 성공:', msg);
            showToast('SPP 채널 닫기 성공');
        },
        onFailure: (msg) => {
            console.error('SPP 채널 닫기 실패:', msg);
            showToast('SPP 채널 닫기 실패');
        }
    };
    bridge.send(closeChannelRequest);
};

const handleBluetoothConnect = () => {
    console.log("Bluetooth 연결 시도");
    connectToArduino();  // 기존 SPP 채널에 연결 시도
};

// ******************** 아두이노 명령 전달 ****************** //
const handleArduinoCommand = (command) => {

    console.log(`Sending command to Arduino. Channel ID: ${currentChannelId}, Command: ${command}`); // 채널 ID와 명령 로그
    
    const request = {
        service: 'luna://com.webos.service.bluetooth2',
        method: 'spp/writeData',
        parameters: {
            "channelId": currentChannelId,
            "data": Buffer.from(command).toString('base64')
        },
        onSuccess: (msg) => {
            console.log('Command executed:', msg);
        },
        onFailure: (msg) => console.error('Failed to execute command:', msg),
    };

    bridge.send(request);
};

//************************  log  *************************//

    // 속도 업데이트 함수
    const handleSpeedChange = (direction) => {
        const message = {
            direction: direction, // "front", "back", "left", "right", "neutral"
        };

        const request = {
            service: serviceUrl,
            method: 'executeCommand2',
            parameters: message,
            onSuccess: (msg) => console.log('Speed command sent:', msg),
            onFailure: (msg) => console.error('Failed to send speed command:', msg),
        };

        bridge.send(request);
    };

//************************  ros 명령 처리  *************************//
    const handleCommand = (command) => {
        const message = {
            command: command,
        };

        const request = {
            service: serviceUrl,
            method: 'executeCommand',
            parameters: message,
            onSuccess: (msg) => {
                console.log('Command executed:', msg);
                showToast(`로봇이 ${command === 'start_navigation' ? '이동을 시작합니다.' : command === 'stop_navigation' ? '이동을 중지합니다.' : command === 'resume_navigation' ? '이동을 재개합니다.' : '이동을 종료합니다.'}`);
            },
            onFailure: (msg) => console.error('Failed to execute command:', msg),
        };

        bridge.send(request);
    };

    const handleStartStop = (rosCommand, arduinoCommand) => {
        handleCommand(rosCommand);  // ROS 명령 전송
        handleArduinoCommand(arduinoCommand);  // 아두이노 명령 전송
    };


    return (
        <div className={css.container}>
        <div className={css.header}>
            <h1 className={css.title}>
                하비봇
                <button className={css.bluetoothButton} onClick={handleBluetoothConnect}>
                    <img src={require('../../assets/bluetooth.png')} alt="Bluetooth" className={css.bluetoothIcon} />
                </button>
            </h1>
        </div>
            <div className={css.mainContent}>
                <div className={css.widgetContainer} >
                    <div className={css.widget}>
                        <iframe src="http://192.168.242.34:4000/camera" alt="Camera Stream"></iframe>
                    </div>
                </div>

                <div className={css.logArea}>
                    <h2>로봇 로그</h2>
                    <div className={css.logContent}>
                        {logs.map((log, index) => (
                            <p key={index}>{log}</p>
                        ))}
                        <div ref={logEndRef} />
                    </div>
                </div>
            </div>

            <div className={css.lowerSection}>
                <div className={css.commandArea}>
                    <button className={css.commandButton} onClick={() => handleStartStop('start_navigation', '2')}>시작</button>
                    <button className={css.commandButton} onClick={() => handleArduinoCommand('2')}>수확기 작동</button>
                    <button className={css.commandButton} onClick={() => handleArduinoCommand('1')}>수확기 정지</button>
                    <button className={css.commandButton} onClick={() => handleStartStop('end_navigation', '1')}>종료</button>
                </div>

                <div className={css.directions}>
                    <button className={css.directionButton} onClick={() => handleSpeedChange('front')}>▲</button>
                    <div className={css.horizontalButtons}>
                        <button className={css.directionButton} onClick={() => handleSpeedChange('left')}>◀</button>
                        <button className={css.directionButton} onClick={() => handleSpeedChange('neutral')}>•</button>
                        <button className={css.directionButton} onClick={() => handleSpeedChange('right')}>▶</button>
                    </div>
                    <button className={css.directionButton} onClick={() => handleSpeedChange('back')}>▼</button>
                </div>
            </div>
        </div>
    );
};

export default HubotView;
