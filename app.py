import time
import requests
import cv2
from pathlib import Path
import pygame
import RPi.GPIO as GPIO
import os
from dotenv import load_dotenv

# ENDPOINT
ENDPOINT = ''

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO_PIN = 19
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.mixer.init()

cap = cv2.VideoCapture(0)

def capture_image_and_predict():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        return

    image_path = os.getenv('IMAGE_PATH', 'test-opencv.jpg')
    cv2.imwrite(image_path, frame)
    print("Image captured")

    url = f'{ENDPOINT}/predict'
    files = {'file': open(image_path, 'rb')}

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        prediction = response.json()

        caption = prediction.get("caption")
        print("Caption: ", caption)

        if caption:
            tts_url = f"{ENDPOINT}/tts?text={caption}"
            tts_response = requests.post(tts_url)

            if tts_response.status_code == 200:
                audio_path = os.getenv('AUDIO_OUTPUT_PATH', 'response_audio.wav')
                with open(audio_path, "wb") as audio_file:
                    audio_file.write(tts_response.content)
                print(f"TTS response saved as {audio_path}")
                sound = pygame.mixer.Sound(audio_path)
                sound.play()
                time.sleep(sound.get_length())
            else:
                print("Failed to get TTS response:", tts_response.status_code, tts_response.text)
        else:
            print("No caption received to send to TTS")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

try:
    while True:
        if GPIO.input(GPIO_PIN) == False:
            capture_image_and_predict()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    cap.release()
    GPIO.cleanup()