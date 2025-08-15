# 中文语音识别系统

这是一个基于树莓派4B和Python 3.7.3的中文语音识别程序，可以将你说的话转换为文字并进行知识库问答。

## 功能特点

- 🎤 实时语音识别
- 🇨🇳 支持中文语音识别
- 💾 自动保存识别结果到文件
- 🔧 自动噪音调整
- 🎯 简单易用的交互界面
- 🧠 内置知识库问答系统
- 🍓 专为树莓派4B优化
- 🐍 基于Python 3.7.3

## 系统要求

- **硬件**: 树莓派4B（推荐4GB或8GB内存版本）
- **系统**: Raspberry Pi OS (Debian-based)
- **Python**: 3.7.3 (树莓派OS默认版本)
- **网络**: 稳定的网络连接（用于Google Speech Recognition API）
- **音频**: USB麦克风或树莓派兼容的音频设备

## 安装步骤

### 1. 更新系统（树莓派）

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. 安装系统依赖

```bash
# 安装音频相关依赖
sudo apt install -y portaudio19-dev python3-pyaudio
sudo apt install -y alsa-utils pulseaudio

# 安装Python开发工具
sudo apt install -y python3-dev python3-pip
sudo apt install -y build-essential

# 安装中文分词依赖
sudo apt install -y python3-sklearn
```

### 3. 安装Python依赖

```bash
# 升级pip
python3 -m pip install --upgrade pip

# 安装项目依赖
pip3 install -r requirements.txt

# 或者运行自动安装脚本
python3 setup_dependencies.py
```

### 4. 配置音频设备

```bash
# 查看音频设备
aplay -l
arecord -l

# 测试麦克风
python3 audio_test.py
```

### 5. 配置网络（可选）

如果遇到网络问题，可以配置代理或使用国内镜像：

```bash
# 使用清华大学PyPI镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## 使用方法

### 快速启动

```bash
# 运行主程序
python3 main.py

# 或运行语音识别程序
python3 voice_recognition_core.py

# 或运行知识库问答系统
python3 main.py
```

### 使用说明

1. 运行程序后，会看到欢迎界面
2. 程序会自动调整麦克风噪音
3. 看到 "🎤 请说话..." 提示时，开始说话
4. 说话结束后，程序会自动识别并显示结果
5. 识别结果会自动保存到 `voice_records.txt` 文件
6. 按 `Ctrl+C` 退出程序

### 示例输出

```
==================================================
🎯 中文语音识别系统
==================================================
功能：
1. 识别中文语音并转换为文字
2. 保存识别结果到文件
3. 按 Ctrl+C 退出程序
==================================================
✅ 麦克风噪音调整完成

🎤 请说话...
🔍 正在识别中...

✅ 识别结果: 你好，这是一个语音识别测试
💾 结果已保存到 voice_records.txt

------------------------------
```

## 文件说明

### 核心程序文件
- `main.py` - 知识库问答系统主程序
- `voice_recognition_core.py` - 语音识别核心程序
- `voice_recognition_full.py` - 完整版语音识别（包含语音合成功能）
- `wake_word_detector.py` - 唤醒词检测模块

### 配置和数据文件
- `requirements.txt` - Python依赖包列表
- `knowledge_base.json` - 本地知识库数据文件
- `voice_records.txt` - 识别结果保存文件（程序运行后自动生成）

### 工具和测试文件
- `setup_dependencies.py` - 自动安装依赖脚本
- `audio_test.py` - 麦克风测试程序
- `knowledge_renumber.py` - 知识库编号处理工具

## 项目架构

```
小学期项目2/
├── main.py                     # 主程序入口
├── voice_recognition_core.py   # 语音识别核心模块
├── voice_recognition_full.py   # 完整版语音识别
├── wake_word_detector.py       # 唤醒词检测模块
├── knowledge_base.json         # 本地知识库数据
├── requirements.txt            # Python依赖包
├── setup_dependencies.py       # 依赖安装脚本
├── audio_test.py              # 麦克风测试工具
├── knowledge_renumber.py       # 编号处理工具
└── voice_records.txt          # 语音识别结果（运行时生成）
```

## 技术原理

### 语音识别技术栈
- 使用 `speech_recognition` 库进行语音识别
- 使用 `pyaudio` 库进行音频输入和处理
- 调用 Google Speech Recognition API 进行中文识别
- 需要网络连接才能正常工作

### 知识库问答系统
- 使用 `jieba` 进行中文分词
- 使用 `scikit-learn` 的 TF-IDF 算法进行文本向量化
- 使用余弦相似度进行问答匹配
- 支持本地JSON知识库存储

### 树莓派优化
- 针对ARM架构进行优化
- 支持树莓派原生音频接口
- 低内存占用设计
- 适配Python 3.7.3版本

## 常见问题

### Q: 提示 "无法识别语音内容"
A: 可能的原因：
- 说话声音太小或不清楚
- 环境噪音太大
- 麦克风质量不好
- 网络连接问题

### Q: 提示 "识别服务出错"
A: 可能的原因：
- 网络连接不稳定
- Google Speech Recognition 服务暂时不可用
- 防火墙阻止了网络请求

### Q: 树莓派上安装依赖失败
A: 解决方案：
```bash
# 确保系统包管理器是最新的
sudo apt update

# 安装必要的编译工具
sudo apt install -y build-essential python3-dev

# 如果pyaudio安装失败，使用系统包管理器安装
sudo apt install -y python3-pyaudio

# 如果sklearn安装失败，使用系统包管理器安装
sudo apt install -y python3-sklearn
```

### Q: 麦克风无法工作（树莓派）
A: 检查：
```bash
# 检查音频设备
aplay -l
arecord -l

# 测试录音
arecord -D plughw:1,0 -f cd test.wav

# 调整音量
alsamixer

# 运行麦克风测试程序
python3 audio_test.py
```

### Q: 程序运行缓慢
A: 优化建议：
- 确保树莓派有足够的内存（推荐4GB+）
- 使用高速SD卡（Class 10或更高）
- 关闭不必要的系统服务
- 考虑使用轻量级的语音识别方案

### Q: 网络连接问题
A: 解决方案：
```bash
# 检查网络连接
ping google.com

# 配置DNS
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf

# 使用国内镜像安装依赖
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## 扩展功能

### 知识库问答系统
- 智能问答功能，基于本地知识库
- 支持自然语言查询
- TF-IDF算法进行语义匹配
- 可扩展的JSON知识库格式

### 完整版语音识别 (`voice_recognition_full.py`)
- 文字转语音功能
- 更详细的错误处理
- 更多的配置选项
- 增强的用户交互体验

## 树莓派性能优化建议

### 硬件优化
- 使用高质量的电源适配器（5V/3A）
- 安装散热片或风扇保持温度稳定
- 使用高速SD卡（UHS-I Class 10或更高）
- 考虑使用USB 3.0接口的麦克风

### 软件优化
```bash
# 增加交换内存
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# 设置 CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# 优化GPU内存分配
sudo raspi-config
# Advanced Options -> Memory Split -> 16

# 关闭不必要的服务
sudo systemctl disable bluetooth
sudo systemctl disable wifi-powersave
```

## 注意事项

### 树莓派使用注意
- 需要稳定的网络连接（有线连接更稳定）
- 识别准确度取决于语音质量和环境噪音
- 建议在安静的环境中使用
- 程序会自动保存所有识别结果，注意隐私保护
- 长时间运行时注意散热问题

### 数据隐私
- 语音数据通过Google API处理，请注意隐私风险
- 本地知识库数据不会上传到外部服务器
- 语音记录文件保存在本地，请妥善管理

## 开发环境信息

- **开发平台**: 树莓派4B
- **操作系统**: Raspberry Pi OS (32-bit/64-bit)
- **Python版本**: 3.7.3
- **主要依赖**: SpeechRecognition, PyAudio, scikit-learn, jieba

## 许可证

本项目仅供学习和研究使用。请遵守相关API的使用条款和隐私政策。 