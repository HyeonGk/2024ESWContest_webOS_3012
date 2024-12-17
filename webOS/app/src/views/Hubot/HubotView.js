import React, { useState, useEffect } from 'react'; 
import css from './HubotView.module.less';
import LS2Request from '@enact/webos/LS2Request';

const webOSBridge = new LS2Request();

const showToast = (message) => {
    const params = { "message": message };
    const lsRequest = {
        "service": "luna://com.farm.app.service", 
        "method": "showToast", 
        "parameters": params,
        "onSuccess": (response) => console.log('Toast 호출 성공:', response),
        "onFailure": (error) => console.error('Toast 서비스 호출 실패:', error),
    };
    webOSBridge.send(lsRequest);
};

const putFruitData = (fruitName, harvestDate, quantity) => {
    const params = {
        "objects": [{
            "_kind": "com.farm.app:1",
            "fruitName": fruitName,
            "harvestDate": harvestDate,
            "quantity": quantity
        }]
    };

    const lsRequest = {
        "service": "luna://com.webos.service.db",
        "method": "put",
        "parameters": params,
        "onSuccess": (response) => {
            if (response.returnValue) {
                const successMessage = `등록 성공: ${harvestDate} - ${fruitName} - ${quantity}개`;
            } else {
                console.error("과일 데이터 저장 실패:", response.errorText);
                showToast("과일 데이터 저장 실패: " + response.errorText);
            }
        },
        "onFailure": (error) => {
            console.error('과일 데이터 저장 서비스 호출 실패:', error);
            showToast("과일 데이터 저장 중 오류가 발생했습니다.");
        }
    };

    webOSBridge.send(lsRequest);
};

const HubotView = () => {
    const [selectedDate, setSelectedDate] = useState('');
    const [cropCounts, setCropCounts] = useState({ red: 0, green: 0, decay: 0 });

    useEffect(() => {
        const fetchCropCounts = () => {
            const request = {
                service: 'luna://com.farm.app.service',
                method: 'getCropCounts',
                onSuccess: (response) => {
                    setCropCounts({
                        red: response.red,
                        green: response.green,
                        decay: response.decay
                    });
                },
                onFailure: (error) => {
                    console.error("Failed to receive crop counts:", error);
                }
            };
            webOSBridge.send(request);
        };

        const intervalId = setInterval(fetchCropCounts, 1000);
        return () => clearInterval(intervalId);
    }, []);

    const handleSubmit = () => {
        const totalFruits = cropCounts.red + cropCounts.green + cropCounts.decay;

        if (!selectedDate) {
            showToast("날짜를 선택해 주세요.");
            return;
        }

        if (totalFruits === 0) {
            showToast("수확된 작물이 없습니다.");
            return;
        }
        
        putFruitData("red", selectedDate, cropCounts.red);
        putFruitData("green", selectedDate, cropCounts.green);
        putFruitData("decay", selectedDate, cropCounts.decay);
        
        showToast("등록 완료");
        const resetRequest = {
            service: 'luna://com.farm.app.service',
            method: 'resetCropCounts',
            onSuccess: (response) => {
                console.log("Crop counts reset:", response);
                setCropCounts({ red: 0, green: 0, decay: 0 });
            },
            onFailure: (error) => {
                console.error("Failed to reset crop counts:", error);
            }
        };
        webOSBridge.send(resetRequest);
    };


    return (
        <div className={css.container}>
            <h1 className={css.title}>휴봇</h1>
            <div className={css.gridContainer}>
                <div className={css.widget}>
                    <iframe src="http://192.168.242.158:5000" alt="Camera Stream"></iframe>
                </div>

                <div className={css.widget}>
                    <h2>수확 작물 현황</h2>
                    <div className={css.cropCountContainer}>
                        <div className={`${css.cropCount} ${css.red}`}>
                            <span>🍎 Red</span>
                            <span>{cropCounts.red}개</span>
                        </div>
                        <div className={`${css.cropCount} ${css.green}`}>
                            <span>🍏 Green</span>
                            <span>{cropCounts.green}개</span>
                        </div>
                        <div className={`${css.cropCount} ${css.decay}`}>
                            <span>💀 Decay</span>
                            <span>{cropCounts.decay}개</span>
                        </div>
                    </div>
                    
                    <div className={css.formGroup}>
                        <label className={css.formLabel}>날짜:</label>
                        <input 
                            type="date" 
                            value={selectedDate} 
                            onChange={(e) => setSelectedDate(e.target.value)} 
                            className={css.inputBox} 
                        />
                    </div>

                    {/* 등록 버튼을 별도의 div로 감싸서 독립적으로 위치시킴 */}
                    <div className={css.buttonContainer}>
                        <button onClick={handleSubmit} className={css.submitButton}>등록</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HubotView;
