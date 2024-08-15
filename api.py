import base64
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import torch
import setuptools
import os
import shutil
import cv2
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
import requests
import json

loaded_model = PaliGemmaForConditionalGeneration.from_pretrained("Ohmmy3847/paligemma_vqav3")
loaded_processor = AutoProcessor.from_pretrained("google/paligemma-3b-pt-224")

device = "cuda" if torch.cuda.is_available() else "cpu"
loaded_model = loaded_model.to(device)

def TTS_output(text, output_path="./sound.wav"):
    url = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"
    payload = {"text":f"{text}", "speaker":"1", "volume":1, "speed":1, "type_media":"wav", "save_file": "true", "language": "th"}
    headers = {
    'Botnoi-Token': 'VWQ0YzkzM2JkZmZmZmYzNjNkZTRjMjNmYTc0YzYwMGYwNTYxODk0',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload)

    return response.json()['audio_url']

def delete_dir_contents(dir_path):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

def send_file_data(filepath):
    img = Image.open(filepath)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = buffered.getvalue()
    return img_str

def send_file_data_2(filepath):
    with open(filepath, 'rb') as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes)
    return Response(content=encoded_image, headers={"Content-Type": "image/jpg"})

def download_wav(url, output_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")
        return False

app = FastAPI()

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    prompt = "อธิบายภาพนี้เป็นภาษาไทย"
    inputs = loaded_processor(prompt, pil_image.convert("RGB"), return_tensors="pt").to(device)
    output = loaded_model.generate(**inputs, max_new_tokens=256)
    caption = loaded_processor.decode(output[0], skip_special_tokens=True)[len(prompt):]
    caption = caption.replace("\n", "")
    return {"caption": caption}

@app.post("/tts")
async def tts(text: str):
    url_sound = TTS_output(text)
    print(url_sound)
    
    output_path = "sound.wav"
    success = download_wav(url_sound, output_path)
    
    if success:
        return FileResponse(output_path, media_type='audio/wav', filename="sound.wav")
    else:
        return {"error": "Failed to download the audio file"}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)