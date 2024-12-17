    import React, { useEffect, useState } from 'react'; // useEffect 추가
    import ThemeDecorator from '@enact/sandstone/ThemeDecorator';
    import { HashRouter as Router, Route, Routes, Link } from 'react-router-dom'; // HashRouter로 변경
    import Panels from '@enact/sandstone/Panels';
    import MainPanel from '../views/Main/MainPanel'; // 메인 페이지 컴포넌트
    import HarvibotPage from '../views/Harvest/HarvestView'; // 하비봇 페이지 컴포넌트
    import CCTVPage from '../views/CCTVView/cctvview'; // CCTV 페이지 컴포넌트
    import HubotPage from '../views/Hubot/HubotView'; // 휴봇 페이지 컴포넌트
    import GraphView from '../views/Main/Graph/GraphView';
    import css from './App.module.less';
    import LS2Request from '@enact/webos/LS2Request'; // Import LS2Request

    const serviceUrl = 'luna://com.farm.app.service'; // Define service URL

    const App = (props) => {
        const [isOpen, setIsOpen] = useState(false);

        // 서버 시작 함수
        const startServer = () => {
            const bridge = new LS2Request();
            const request = {
                service: serviceUrl,
                method: 'startServer',
                parameters: {},
                onSuccess: (msg) => console.log('Server started:', msg),
                onFailure: (msg) => console.error('Failed to start server:', msg),
            };
            bridge.send(request);
        };

    // 블루투스 서비스 시작 함수
    const startBluetoothService = () => {
        const bridge = new LS2Request();
        const request = {
            service: 'luna://com.webos.service.bluetooth2',
            method: 'adapter/setState',
            parameters: {
                powered: true,
                name : 'farm',
                discoverable: true,
            },
            onSuccess: (msg) => {
                console.log('블루투스 어댑터 활성화 성공:', msg);
            },
            onFailure: (msg) => {
                console.error('블루투스 어댑터 활성화 실패:', msg);
            }
        };
        bridge.send(request);
    };

    // 앱 종료 함수
    const exitApp = () => {
        const bridge = new LS2Request();
        const request = {
            service: 'luna://com.webos.service.applicationmanager',
            method: 'closeByAppId',
            parameters: {
                id: 'com.farm.app'
            },
            onSuccess: (msg) => console.log('App closed:', msg),
            onFailure: (msg) => console.error('Failed to close app:', msg),
        };
        bridge.send(request);
    };


    // 컴포넌트 마운트 시 서버 시작
    useEffect(() => {
        startServer(); // 앱 시작과 동시에 서버 시작
        startBluetoothService(); //블루투스 어댑터 설정
    }, []);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

        return (
            <Router> {/* HashRouter로 설정 */}
                <div className={css.app}>
                    {/* 메뉴 버튼 (햄버거 아이콘) */}
                    <div className={css["menu-icon"]} onClick={toggleMenu}>
                        <img src={require('../assets/button3.png')} alt="Menu Icon" />
                    </div>


                    {/* 슬라이드 메뉴 */}
                    <div className={`${css.sidebar} ${isOpen ? css.open : ''}`}>
                        <ul className={css["menu-items"]}>
                            {/* Link 컴포넌트로 각각의 경로 연결 */}
                            <li>
                                <Link to="/" onClick={toggleMenu}>메인</Link>
                            </li>
                            <li>
                                <Link to="/cctv" onClick={toggleMenu}>CCTV</Link>
                            </li>
                            <li>
                                <Link to="/harvibot" onClick={toggleMenu}>하비봇</Link>
                            </li>
                            <li>
                                <Link to="/hubot" onClick={toggleMenu}>휴봇</Link>
                            </li>
                        </ul>
                
                        <div className={css["exit-button-container"]}>
                            <button className={css.exitButton} onClick={exitApp}>
                                <img src={require('../assets/end.png')} alt="Exit" className={css.exitIcon} />
                            </button>
                        </div>
                    </div>

                    {/* 페이지 전환을 관리하는 Routes 설정 */}
                    <Panels {...props} style={{ backgroundColor: '#a6b28f' }}>
                        <Routes>
                            <Route path="/" element={<MainPanel />} />
                            <Route path="/cctv" element={<CCTVPage />} />
                            <Route path="/hubot" element={<HubotPage />} />
                            <Route path="/harvibot" element={<HarvibotPage />} />
                            <Route path="/graphview" element={<GraphView />} />
                        </Routes>
                    </Panels>
                </div>
            </Router>
        );
    };

    export default ThemeDecorator(App);
