# 🚗 Hand Tracking Virtual Steering

A Python-based virtual steering system that uses real-time hand tracking through a webcam to control a driving game using hand gestures.

## ✨ Features

- 🖐️ Real-time hand tracking using a webcam
- 🎮 Virtual steering using hand movements
- ➡️ Keyboard-based left and right steering controls
- 👍 Right-hand thumbs-down gesture for acceleration
- 👈 Left-hand thumbs-down gesture for braking
- ⚡ Smooth steering control for a better gaming experience

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI

## 📂 Project Structure

```text
Hand-Tracking-Virtual-Steering/
├── virtual_steering_wheel.py
├── test_hands.py
├── run.bat
├── hand_landmarker.task
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Requirements

- Python 3.11
- A working webcam
- Windows operating system
- A keyboard-controlled driving game

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/areebnasir247/Hand-Tracking-Virtual-Steering.git
```

### 2. Open the project folder

```bash
cd Hand-Tracking-Virtual-Steering
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the project

```bash
python virtual_steering_wheel.py
```

## 🎮 How It Works

1. The webcam captures hand movements in real time.
2. MediaPipe detects and tracks hand landmarks.
3. Python processes the hand positions and gestures.
4. PyAutoGUI sends keyboard inputs to control the driving game.
5. Hand movements control steering, while the configured gestures control acceleration and braking.

## 🎯 Project Goal

The goal of this project is to explore computer vision and human-computer interaction by creating a hands-free way to control a driving game using a standard webcam.

## 🔮 Future Improvements

- Improve steering smoothness and responsiveness.
- Add more customizable hand gestures.
- Support additional games and control configurations.
- Improve gesture recognition accuracy.

## 👨‍💻 Author

**Areeb Nasir**

GitHub: [@areebnasir247](https://github.com/areebnasir247)

---

⭐ If you find this project interesting, consider giving the repository a star!
