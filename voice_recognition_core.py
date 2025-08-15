import speech_recognition as sr
import time
from datetime import datetime

def setup_recognizer():
    """设置语音识别器"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # 调整麦克风噪音
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ 麦克风噪音调整完成")
    
    return recognizer, microphone

def listen_and_recognize(recognizer, microphone):
    """监听并识别语音"""
    try:
        print("\n🎤 请说话...")
        
        with microphone as source:
            # 动态调整噪音
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        print("🔍 正在识别中...")
        
        # 使用Google Speech Recognition识别中文
        text = recognizer.recognize_google(audio, language='zh-CN')
        return text
        
    except sr.UnknownValueError:
        return "无法识别语音内容"
    except sr.RequestError as e:
        return f"识别服务出错: {e}"
    except sr.WaitTimeoutError:
        return "等待超时，请重试"
    except KeyboardInterrupt:
        return None

def save_result(text, filename="voice_records.txt"):
    """保存识别结果到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")

def main():
    """主函数"""
    print("=" * 50)
    print("🎯 中文语音识别系统")
    print("=" * 50)
    print("功能：")
    print("1. 识别中文语音并转换为文字")
    print("2. 保存识别结果到文件")
    print("3. 按 Ctrl+C 退出程序")
    print("=" * 50)
    
    try:
        # 设置识别器
        recognizer, microphone = setup_recognizer()
        
        while True:
            try:
                # 识别语音
                result = listen_and_recognize(recognizer, microphone)
                
                if result is None:
                    print("\n👋 程序已退出")
                    break
                
                if result != "无法识别语音内容" and result != "等待超时，请重试":
                    print(f"\n✅ 识别结果: {result}")
                    
                    # 保存到文件
                    save_result(result)
                    print("💾 结果已保存到 voice_records.txt")
                else:
                    print(f"\n❌ {result}")
                
                print("\n" + "-" * 30)
                
            except KeyboardInterrupt:
                print("\n👋 程序已退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                
    except Exception as e:
        print(f"程序初始化失败: {e}")
        print("请检查：")
        print("1. 麦克风是否正常工作")
        print("2. 是否安装了依赖包: pip install -r requirements.txt")
        print("3. 网络连接是否正常（Google Speech Recognition需要网络）")

if __name__ == "__main__":
    main() 