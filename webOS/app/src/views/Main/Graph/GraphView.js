import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import LS2Request from '@enact/webos/LS2Request';
import css from './GraphView.module.less';
import { useNavigate } from 'react-router-dom';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

const webOSBridge = new LS2Request();

const GraphView = () => {
    const [temperatureData, setTemperatureData] = useState([]);
    const [humidityData, setHumidityData] = useState([]);
    const [labels, setLabels] = useState([]);
    const navigate = useNavigate();

    const fetchSensorData = () => {
        const lsRequest = {
            service: 'luna://com.farm.app.service',
            method: 'getSensorData',
            onSuccess: (response) => {
                if (response.returnValue) {
                    const currentTime = new Date().toLocaleTimeString();
                    setTemperatureData((prevData) => [...prevData.slice(-9), parseFloat(response.temperature)]);
                    setHumidityData((prevData) => [...prevData.slice(-9), parseFloat(response.humidity)]);
                    setLabels((prevLabels) => [...prevLabels.slice(-9), currentTime]);
                }
            },
            onFailure: (error) => {
                console.error('Failed to fetch sensor data:', error);
            }
        };
        webOSBridge.send(lsRequest);
    };

    useEffect(() => {
        const intervalId = setInterval(fetchSensorData, 2000);
        return () => clearInterval(intervalId);
    }, []);

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Temperature (°C)',
                data: temperatureData,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                yAxisID: 'y1',
                fill: false,
                tension: 0.3,
            },
            {
                label: 'Humidity (%)',
                data: humidityData,
                borderColor: 'blue',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                yAxisID: 'y2',
                fill: false,
                tension: 0.3,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: '온도와 습도 실시간 데이터',
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time',
                },
            },
            y1: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Temperature (°C)',
                },
                suggestedMin: 20, 
                suggestedMax: 30,
            },
            y2: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Humidity (%)',
                },
                beginAtZero: true,
                suggestedMax: 100,
                grid: {
                    drawOnChartArea: false,
                },
            },
        },
    };

    return (
        <div className={css.container}>
            <button className={css.backButton} onClick={() => navigate('/')}>
                <img src={require('../../../assets/back.png')} alt="Back" className={css.backIcon} />
            </button>

            <h1 className={css.title}>Graph View</h1>
            <div className={css.widget}>
                <Line data={data} options={options} />
            </div>
        </div>
    );
};

export default GraphView;