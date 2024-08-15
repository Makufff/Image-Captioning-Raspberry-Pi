# Image Captioning on Raspberry pi
Repository นี้ จัดทำขึ้นมาเพื่อแชร์โค้ด Code และแชร์เทคนิคต่างๆ หวังว่าจะเป็นประโยชน์แก่ผู้เข้าชมทุกท่านให้ได้รับความรู้กลับไปไม่มากก็น้อย
หากมีข้อผิดพลาดตัวผมขออภัยมา ณ ที่นี้ด้วยนะครับ (จาก Makufff 😀)

# PC (API)
## install Env
```bash
$ conda create --name captioning_project python=3.11.9

$ conda activate captioning_project

$ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

$ pip install -r requirements-api.txt # On PC

```

## Ngrok Foward
```bash
$ ngrok http 8000
```

## Setup API
```bash

$ conda activate captioning_project

# in PC
$ python api.py

```
# Raspberry Pi
## install Env
```bash
$ python3 -m venv myenv

$ source myenv/bin/activate

$ pip install -r requirements-pi.txt # On Raspberry

```

## Setup APP
```bash
$ source myenv/bin/activate

$ python3 app.py

```

#⭐ Special Thanks ⭐
P'ICE 🙇‍♂️ : https://github.com/Annerez
P'Arther 🙇‍♂️ : https://github.com/E27-25
P'Ohm 🙇‍♂️ : https://github.com/Ohmmy3847
P'PIM 🙇‍♂️ : https://github.com/pimsleepyy