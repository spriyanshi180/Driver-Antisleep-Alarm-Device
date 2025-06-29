# 🚗 Driver Antisleep Alarm Device using Raspberry Pi

A real-time drowsiness detection system built using Raspberry Pi 4 Model B, OpenCV, and dlib. The system monitors eye blinks using a live camera feed and triggers alerts via buzzer, LED, and LCD when signs of driver sleepiness are detected.

This project aims to improve road safety and prevent accidents caused by microsleeps.

---

## 📹 Demo Videos

Click to view sample demonstrations:

- ▶️ [2.mp4](2.mp4)
- ▶️ [3.mp4](3.mp4)
- ▶️ [4.mp4](4.mp4)
- ▶️ [7.mp4](7.mp4)

> 🎥 These clips were recorded during real-time testing using Raspberry Pi and Pi Camera.

---

## 🛠 Hardware Used

| Component                | Description                          |
|--------------------------|--------------------------------------|
| Raspberry Pi 4 Model B   | 4GB RAM, running Raspberry Pi OS     |
| Pi Camera Module Rev 1.3| Used for capturing live eye feed     |
| Buzzer (5V)              | For audio alert                      |
| LED (with resistor)      | For visual alert                     |
| 16x2 LCD (I2C)           | To display warning messages          |
| Laptop Display           | Used via HDMI or VNC for monitoring  |

---

## 💻 Software & Libraries

- **Raspberry Pi OS (64-bit Bookworm)**
- **Python 3.11+**
- **OpenCV**
- **dlib (facial landmark detection)**
- **imutils**
- **RPi.GPIO / gpiozero**
- **picamera2**

---

## 📄 Project Report

📥 [Click to view Project Report](Project%20Report%20.pdf)

---

## 📁 Folder Structure
Driver-Antisleep-Alarm/

├── drowsiness_detection.py

├── README.md

├── requirements.txt

├── Project_Report.pdf

├── images/

│ ├── setup.jpg

│ └── blink_demo.png

├── media/

│ └── 2.mp4, 3.mp4, 4.mp4, 7.mp4


---

## 🚀 How to Run the Project (Two-Terminal Setup)

> ✅ Make sure your camera is connected and enabled (`sudo raspi-config`)

### 🖥 Terminal 1 – Start the Camera Stream

```bash
libcamera-vid -t 0 --width 640 --height 480 --inline --listen -o tcp://0.0.0.0:8080
```
This starts a TCP stream of the camera on port 8080.

🖥 Terminal 2 – Run the Python Detection Script
```bash
cd ~/your_script_folder/
source ~/drowsy-env/bin/activate     # Activate your virtual environment
python3 drowsiness_detection.py
```

Make sure your Python code uses:

```bash
cap = cv2.VideoCapture("tcp://127.0.0.1:8080", cv2.CAP_FFMPEG)
```

🧪 Features
Real-time blink detection using Eye Aspect Ratio (EAR)

Multi-alert system using Buzzer + LED + LCD

Runs autonomously on Raspberry Pi

Suitable for both personal and commercial vehicles

Offline system – no internet needed

📦 Installation Requirements

Install the necessary libraries with:

```bash
pip install -r requirements.txt
```

requirements.txt content:
```bash
opencv-python
dlib
imutils
numpy
RPi.GPIO
gpiozero
picamera2
```
🧑‍💻 Author

Priyanshi Singh

B.Tech – JK Institute of Applied Physics and Technology
University of Allahabad

📍 India

📧 spriyanshi180@.com

🌐 www.linkedin.com/in/spriyanshi180

📜 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute.

⭐ If you like this project, consider giving it a star on GitHub!



