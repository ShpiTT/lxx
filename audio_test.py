#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦克风测试脚本
用于测试麦克风是否正常工作
"""

import pyaudio
import wave
import time

def test_microphone():
    """测试麦克风功能"""
    print("🎤 麦克风测试程序")
    print("=" * 40)
    
    # 音频参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    
    p = pyaudio.PyAudio()
    
    try:
        # 获取默认输入设备信息
        default_input = p.get_default_input_device_info()
        print(f"✅ 默认输入设备: {default_input['name']}")
        
        # 列出所有音频设备
        print("\n📋 可用的音频设备:")
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                print(f"  {i}: {device_info['name']}")
        
        # 开始录音
        print(f"\n🎙️ 开始录音 {RECORD_SECONDS} 秒...")
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            # 显示进度
            progress = (i + 1) / int(RATE / CHUNK * RECORD_SECONDS) * 100
            print(f"\r录音进度: {progress:.1f}%", end="", flush=True)
        
        print("\n✅ 录音完成！")
        
        # 停止录音
        stream.stop_stream()
        stream.close()
        
        # 保存录音文件
        filename = "test_recording.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"💾 录音已保存到: {filename}")
        print("🎉 麦克风测试成功！")
        
    except Exception as e:
        print(f"❌ 麦克风测试失败: {e}")
        print("请检查:")
        print("1. 麦克风是否连接")
        print("2. 麦克风权限是否开启")
        print("3. 麦克风是否被其他程序占用")
    
    finally:
        p.terminate()

if __name__ == "__main__":
    test_microphone() 