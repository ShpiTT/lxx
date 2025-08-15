import speech_recognition as sr
import pyttsx3
import time
import threading
from datetime import datetime

class ChineseVoiceRecognition:
    def __init__(self):
        """初始化语音识别器"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # 设置中文语音（如果可用）
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # 调整麦克风噪音
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("语音识别器初始化完成！")
        print("支持的识别引擎：")
        print("1. Google Speech Recognition (需要网络)")
        print("2. 离线识别 (需要额外配置)")
    
    def listen_and_recognize(self):
        """监听并识别语音"""
        try:
            print("\n🎤 请说话... (按 Ctrl+C 退出)")
            
            with self.microphone as source:
                # 动态调整噪音
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔍 正在识别中...")
            
            # 尝试使用Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language='zh-CN')
                return text
            except sr.UnknownValueError:
                return "无法识别语音内容"
            except sr.RequestError as e:
                return f"识别服务出错: {e}"
                
        except sr.WaitTimeoutError:
            return "等待超时，请重试"
        except KeyboardInterrupt:
            return None
    
    def speak_text(self, text):
        """将文字转换为语音"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"语音合成出错: {e}")
    
    def save_to_file(self, text, filename="voice_records.txt"):
        """保存识别结果到文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
    
    def run_interactive_mode(self):
        """交互模式运行"""
        print("=" * 50)
        print("🎯 中文语音识别系统")
        print("=" * 50)
        print("功能说明：")
        print("1. 说话后会自动识别并显示文字")
        print("2. 识别结果会保存到 voice_records.txt 文件")
        print("3. 按 Ctrl+C 退出程序")
        print("=" * 50)
        
        while True:
            try:
                result = self.listen_and_recognize()
                
                if result is None:
                    print("\n👋 程序已退出")
                    break
                
                if result != "无法识别语音内容" and result != "等待超时，请重试":
                    print(f"\n✅ 识别结果: {result}")
                    
                    # 保存到文件
                    self.save_to_file(result)
                    
                    # 询问是否要语音播放
                    choice = input("是否要语音播放识别结果？(y/n): ").lower()
                    if choice == 'y':
                        self.speak_text(result)
                else:
                    print(f"\n❌ {result}")
                
                print("\n" + "-" * 30)
                
            except KeyboardInterrupt:
                print("\n👋 程序已退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")

def main():
    """主函数"""
    try:
        # 创建语音识别器实例
        voice_rec = ChineseVoiceRecognition()
        
        # 运行交互模式
        voice_rec.run_interactive_mode()
        
    except Exception as e:
        print(f"程序初始化失败: {e}")
        print("请检查麦克风是否正常工作，以及是否安装了所需的依赖包。")
        print("运行命令安装依赖: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 