import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import css from './MainPanel.module.less';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import LS2Request from '@enact/webos/LS2Request';
import { useNavigate } from 'react-router-dom'; // 화면 전환을 위한 React Router import

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);
const webOSBridge = new LS2Request();

//**************** showToast 함수 ***************** */
const showToast = (message) => {
    const params = { message };

    const lsRequest = {
        service: 'luna://com.farm.app.service',
        method: 'showToast',
        parameters: params,
        onSuccess: (response) => console.log('Toast 호출 성공:', response),
        onFailure: (error) => console.error('Toast 서비스 호출 실패:', error),
    };
    webOSBridge.send(lsRequest);
};

/********************************************/

const fetchSensorData = (setTemperature, setHumidity) => {
    const lsRequest = {
        service: 'luna://com.farm.app.service',
        method: 'getSensorData',
        onSuccess: (response) => {
            if (response.returnValue) {
                setTemperature(`${response.temperature}°C`);
                setHumidity(`${response.humidity}%`);
            }
        },
        onFailure: (error) => {
            console.error('Failed to fetch sensor data:', error);
        }
    };
    webOSBridge.send(lsRequest);
};

// DB에서 데이터를 가져오는 함수 (Luna Service 호출)
const fetchCropDataFromDB = (cropName) => {
    return new Promise((resolve) => {
        const lsRequest = {
            service: 'luna://com.webos.service.db',
            method: 'find',
            parameters: {
                query: {
                    from: 'com.farm.app:1', // DB Kind ID
                    where: [{ prop: 'fruitName', op: '=', val: cropName }],
                },
            },
            onSuccess: (response) => {
                console.log('DB 데이터 조회 성공:', response);
                resolve(response);
            },
            onFailure: (error) => {
                console.error('DB 데이터 조회 실패:', error);
                resolve({ returnValue: false });
            },
        };
        webOSBridge.send(lsRequest);
    });
};

/********************************************/

const MainPanel = () => {
    const [currentDate, setCurrentDate] = useState(new Date());
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [showNewWidgets, setShowNewWidgets] = useState(false);
    const [selectedCrop, setSelectedCrop] = useState('');
    const [barData, setBarData] = useState(null);
    const [temperature, setTemperature] = useState('측정 중');
    const [humidity, setHumidity] = useState('측정 중');
    const navigate = useNavigate(); // React Router의 navigate hook 사용

    const handleCropChange = async (event) => {
        const crop = event.target.value;
        setSelectedCrop(crop);

        if (crop) {
            // DB에서 데이터 가져오기
            const response = await fetchCropDataFromDB(crop);
            if (response.returnValue && response.results.length > 0) {
                showToast(`${crop}에 대한 수확 데이터가 있습니다.`);
                updateBarData(response.results, crop);
            } else {
                showToast(`${crop}에 대한 수확 데이터가 없습니다.`);
                setBarData(null);
            }
        } else {
            setBarData(null);
        }
    };

    // 차트 데이터 업데이트 함수
    const updateBarData = (data, crop) => {
        if (data.length === 0) {
            setBarData(null);
            return;
        }

        // 날짜별로 개수 합산하기
        const dateCountMap = data.reduce((acc, item) => {
            const date = item.harvestDate;
            if (acc[date]) {
                acc[date] += item.quantity;
            } else {
                acc[date] = item.quantity;
            }
            return acc;
        }, {});

        const labels = Object.keys(dateCountMap).sort((a, b) => new Date(a) - new Date(b));
        const counts = labels.map(date => dateCountMap[date]);

        // crop 값에 따라 색상 지정
        let backgroundColor;
        if (crop === 'red') {
            backgroundColor = 'red';
        } else if (crop === 'green') {
            backgroundColor = '#98fb98';
        } else if (crop === 'decay') {
            backgroundColor = 'black';
        } else {
            backgroundColor = '#ffa500'; // 기본 색상
        }

        setBarData({
            labels,
            datasets: [
                {
                    label: `${crop} 수확량`,
                    data: counts,
                    backgroundColor: backgroundColor,
                },
            ],
        });
    };

    const toggleWidgets = () => setShowNewWidgets(!showNewWidgets);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDate(new Date());
            fetchSensorData(setTemperature, setHumidity); 
        }, 2000); 

        return () => clearInterval(timer);
    }, []);

    // 그래프 화면으로 이동하는 함수
    const goToGraphView = () => {
        navigate('/graphview'); // GraphView 경로로 이동
    };

    return (
        <div className={css.container}>
            <h1 className={css.title}>ELECBRO</h1>

            <div className={css.gridContainer}>
                {!showNewWidgets ? (
                    <>
                        <div className={css.calendar}>
                            <h2>오늘 날짜</h2>
                            <p className={css.inlineDate}>
                                {currentDate.toLocaleDateString()} {currentDate.toLocaleTimeString()}
                            </p>

                            <Calendar
                                onChange={setSelectedDate}
                                value={selectedDate}
                                locale="ko-KR"
                                className={css.customCalendar}
                            />
                        </div>

                        {/* 센서 데이터 위젯 */}
                        <div className={css.sensorData}>
                        <button onClick={goToGraphView} className={css.linkButton}>
                            <img src={require('../../assets/link.png')} alt="Go to GraphView" className={css.linkIcon} />
                        </button>
                            <h2>센서 데이터</h2>
                            <div className={css.sensorGrid}>
                                <div className={css.sensorItem}>
                                    <h3>온도</h3>
                                    <p>{temperature}</p>
                                </div>
                                <div className={css.sensorItem}>
                                    <h3>습도</h3>
                                    <p>{humidity}</p>
                                </div>
                            </div>
                        </div>          
                    </>
                ) : (
                    <div className={`${css.newWidget} ${css.fullWidthWidget}`}>
                        <h2>수확 작물 현황</h2>
                        <div className={css.selectBox}>
                            <select className={css.select} value={selectedCrop} onChange={handleCropChange}>
                                <option value="">작물 선택</option>
                                <option value="red">RED</option>
                                <option value="green">GREEN</option>
                                <option value="decay">DECAY</option>
                            </select>
                        </div>

                        {barData ? (
                            <div className={css.chartContainer}>
                                <Bar data={barData} />
                            </div>
                        ) : (
                            <p>데이터가 없습니다.</p>
                        )}
                    </div>
                )}

                <div className={css.arrowButton} onClick={toggleWidgets}>
                    {showNewWidgets ? '◀' : '▶'}
                </div>
            </div>
        </div>
    );
};

export default MainPanel;
