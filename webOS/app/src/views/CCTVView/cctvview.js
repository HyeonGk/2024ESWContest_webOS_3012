import kind from '@enact/core/kind';
import { Component } from 'react';
import css from './CCTVView.module.less';

const CCTVView = kind({
    name: 'CCTVView',

    render: ({ streamSrc, onCaptureClick, onStopClick, onStartClick }) => (
        <div className={css.container}>
            <h1 className={css.title}>CCTV</h1>

            {/* 실시간 CCTV 화면 */}
            <div className={css.widget}>
                {streamSrc ? (
                    <iframe
                        id="cctvStream"
                        src={streamSrc}
                        title="raspicam Stream"
                        style={{ width: '100%', height: '100%', border: 'none' }}
                    />
                ) : (
                    <p>현재 스트림을 로드할 수 없습니다.</p>
                )}
            </div>
        </div>
    )
});

class CCTVContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            streamSrc: "http://192.168.43.55:4000/camera", // ESP32-CAM의 스트림 URL
            lastFrame: null
        };
    }


    render() {
        const { streamSrc, lastFrame } = this.state;
        return (
            <CCTVView
                streamSrc={streamSrc || lastFrame} // 스트리밍이 중지되면 마지막 프레임 표시
                onStartClick={this.handleStartClick}
                onStopClick={this.handleStopClick}
                onCaptureClick={this.handleCaptureClick}
            />
        );
    }
}

export default CCTVContainer;
