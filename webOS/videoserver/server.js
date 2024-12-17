const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// 정적 파일 경로 설정 (HTML 파일 위치)
app.use(express.static(path.join(__dirname, './public')));

// `/camera` 경로에서 HTML 파일 제공
app.get('/camera', (req, res) => {
    res.sendFile(path.join(__dirname, './public', 'camera.html'));
});

// WebSocket 연결 처리
wss.on('connection', (ws) => {
    console.log('WebSocket 연결됨.');

    let lastSentTime = 0;  // 마지막 전송 시간을 저장하는 변수
    const sendInterval = 500;  // 전송 간격 (밀리초 단위로 500ms는 0.5초)

    ws.on('message', (message, isBinary) => {
        const now = Date.now();
        if (now - lastSentTime >= sendInterval) {  // 지정된 간격이 지난 경우에만 전송
            console.log('프레임 전송 중...');

            wss.clients.forEach((client) => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send(message, { binary: isBinary });
                }
            });

            lastSentTime = now;  // 마지막 전송 시간 갱신
        }
    });

    ws.on('error', (err) => {
        console.error(`WebSocket 오류 발생: ${err.message}`);
    });

    ws.on('close', () => console.log('WebSocket 연결 종료됨.'));
});

// 서버 시작
server.listen(4000, () => {
    console.log('서버가 http://localhost:4000 에서 실행 중...');
});