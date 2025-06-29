import os 
import cv2 
import dlib 
import time 
import RPi.GPIO as GPIO 
from scipy.spatial import distance as dist 
from RPLCD.i2c import CharLCD 
# Set Qt backend to xcb to avoid Wayland issues 
os.environ["QT_QPA_PLATFORM"] = "xcb" 
# Constants 
EAR_THRESHOLD = 0.25 
CONSECUTIVE_FRAMES = 20 
COUNTER = 0 
# GPIO Pins 
LED_PIN = 17     
  # Pin 11 
BUZZER_PIN = 18    # Pin 12 
# GPIO Setup 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(LED_PIN, GPIO.OUT) 
GPIO.setup(BUZZER_PIN, GPIO.OUT) 

# LCD Setup (use correct I2C address, 0x27 is common) 
lcd = CharLCD('PCF8574', 0x27) 
# EAR calculation function 
def eye_aspect_ratio(eye): 
A = dist.euclidean(eye[1], eye[5]) 
B = dist.euclidean(eye[2], eye[4]) 
C = dist.euclidean(eye[0], eye[3]) 
return (A + B) / (2.0 * C) 
# Load dlib face detector and landmark predictor 
try: 
print("[INFO] Loading facial landmark predictor...") 
detector = dlib.get_frontal_face_detector() 
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 
print("[INFO] Model loaded successfully.") 
except Exception as e: 
print(f"[ERROR] Could not load predictor: {e}") 
exit() 
# Eye landmark indexes 
LEFT_EYE_IDX = list(range(42, 48)) 
RIGHT_EYE_IDX = list(range(36, 42)) 
# Start video stream from TCP 
cap = cv2.VideoCapture("tcp://127.0.0.1:8080", cv2.CAP_FFMPEG) 

time.sleep(2) 
if not cap.isOpened(): 
print("[ERROR] Could not open video stream") 
exit() 
cv2.namedWindow("Driver Drowsiness Monitor", cv2.WINDOW_NORMAL) 
cv2.startWindowThread() 
try: 
while True: 
ret, frame = cap.read() 
if not ret: 
print("[ERROR] Failed to grab frame") 
break 
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
faces = detector(gray, 0) 
for face in faces: 
shape = predictor(gray, face) 
landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)] 
left_eye = [landmarks[i] for i in LEFT_EYE_IDX] 
right_eye = [landmarks[i] for i in RIGHT_EYE_IDX] 
left_EAR = eye_aspect_ratio(left_eye) 
right_EAR = eye_aspect_ratio(right_eye) 
ear = (left_EAR + right_EAR) / 2.0 

# Draw eye landmarks 
for (x, y) in left_eye + right_eye: 
cv2.circle(frame, (x, y), 2, (0, 255, 0), -1) 
# Drowsiness detection 
if ear < EAR_THRESHOLD: 
COUNTER += 1 
if COUNTER >= CONSECUTIVE_FRAMES: 
cv2.putText(frame, "DROWSINESS DETECTED!", (20, 100), 
cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3) 
GPIO.output(LED_PIN, GPIO.HIGH) 
GPIO.output(BUZZER_PIN, GPIO.HIGH) 
lcd.clear() 
lcd.write_string("Drowsy Detected!") 
else: 
COUNTER = 0 
GPIO.output(LED_PIN, GPIO.LOW) 
GPIO.output(BUZZER_PIN, GPIO.LOW) 
lcd.clear() 
lcd.write_string("Status: Awake") 
# Display EAR on frame 
cv2.putText(frame, f"EAR: {ear:.2f}", (20, 30), 
cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2) 
cv2.imshow("Driver Drowsiness Monitor", frame) 

if cv2.waitKey(1) == ord("q"): 
break 
except KeyboardInterrupt: 
print("[INFO] Interrupted by user") 
finally: 
cap.release() 
cv2.destroyAllWindows() 
GPIO.output(LED_PIN, GPIO.LOW) 
GPIO.output(BUZZER_PIN, GPIO.LOW) 
GPIO.cleanup() 
lcd.clear() 
lcd.write_string("System Stopped")