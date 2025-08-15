# encoding: utf-8
import os
import sys
import time
import wave
import pyaudio
import numpy as np
from ctypes import *

# 添加Snowboy库路径
SNOWBOY_DIR = "/home/pi/swig-3.0.10/snowboy"
sys.path.append(os.path.join(SNOWBOY_DIR, "swig/Python3"))
import snowboydetect

# 音频参数配置
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
MODEL_FILE = "/home/pi/swig-3.0.10/snowboy/examples/Python3/resources/models/xiaoma.pmdl"

class SnowboyWakeWordDetector:
    def __init__(self):
        """初始化Snowboy唤醒词检测器"""
        if not os.path.exists(MODEL_FILE):
            raise FileNotFoundError(f"Snowboy模型文件未找到: {MODEL_FILE}")
        
        self.detector = snowboydetect.SnowboyDetect(
            resource_filename=os.path.join(SNOWBOY_DIR, "resources/common.res").encode(),
            model_str=MODEL_FILE.encode()
        )
        self.detector.SetAudioGain(1.0)
        self.detector.SetSensitivity("0.5".encode())
        print("Snowboy唤醒检测器初始化完成")

    def detect(self, audio_data):
        """检测唤醒词"""
        return self.detector.RunDetection(audio_data)

class VoiceRecorder:
    def __init__(self):
        """初始化音频录制器"""
        self.audio = pyaudio.PyAudio()
        self.stream = None
        print("音频录制器初始化完成")

    def start_recording(self, callback):
        """开始录音"""
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=callback
        )
        print("开始录音...")

    def stop_recording(self):
        """停止录音"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("录音已停止")

def audio_callback(in_data, frame_count, time_info, status):
    """音频回调函数"""
    global wake_detector, detected
    
    # 检测唤醒词
    result = wake_detector.detect(in_data)
    
    if result > 0 and not detected:
        print("\n唤醒词检测成功!")
        detected = True
        # 在这里添加唤醒后的处理逻辑
        # 例如开始语音识别或执行特定命令
        
    return (in_data, pyaudio.paContinue)

def main():
    global wake_detector, detected
    detected = False
    
    try:
        # 初始化唤醒词检测器
        wake_detector = SnowboyWakeWordDetector()
        
        # 初始化录音器
        recorder = VoiceRecorder()
        recorder.start_recording(audio_callback)
        
        print("系统已启动，等待唤醒词... (按Ctrl+C退出)")
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n正在停止系统...")
    finally:
        if 'recorder' in locals():
            recorder.stop_recording()
        print("系统已关闭")

if __name__ == "__main__":
    main()
