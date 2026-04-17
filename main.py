import os
import subprocess
import textwrap
from pathlib import Path

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
ROTEIRO_FILE = BASE_DIR / "roteiro.txt"
SAIDA_DIR = BASE_DIR / "saida"
VIDEO_FILE = SAIDA_DIR / "videoaula.mp4"

SAIDA_DIR.mkdir(exist_ok=True)

def dividir_roteiro():
    with open(ROTEIRO_FILE, "r", encoding="utf-8") as f:
        texto = f.read()
    return [p.strip() for p in texto.split("\n") if p.strip()]

def gerar_audios(paragrafos):
    arquivos = []
    for i, p in enumerate(paragrafos, start=1):
        audio_path = SAIDA_DIR / f"slide{i}.mp3"
        gTTS(text=p, lang="pt").save(audio_path)
        arquivos.append(audio_path)
        print(f"✅ Áudio gerado: {audio_path}")
    return arquivos

def gerar_imagens(paragrafos):
    arquivos = []
    for i, p in enumerate(paragrafos, start=1):
        img_path = SAIDA_DIR / f"slide{i}.png"
        img = Image.new("RGB", (1280, 720), color="white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        wrapped = textwrap.fill(p, width=40)
        draw.text((50, 300), wrapped, fill="black", font=font)
        img.save(img_path)
        arquivos.append(img_path)
        print(f"🖼️ Imagem gerada: {img_path}")
    return arquivos

def montar_video(imagens, audios):
    videos_temp = []
    for i, (img, audio) in enumerate(zip(imagens, audios), start=1):
        video_temp = SAIDA_DIR / f"parte{i}.mp4"
        comando = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img),
            "-i", str(audio),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(video_temp)
        ]
        subprocess.run(comando)
        videos_temp.append(video_temp)
        print(f"🎞️ Vídeo parcial criado: {video_temp}")

    lista_txt = SAIDA_DIR / "lista.txt"
    with open(lista_txt, "w", encoding="utf-8") as f:
        for v in videos_temp:
            f.write(f"file '{v}'\n")

    comando_final = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(lista_txt),
        "-c", "copy", str(VIDEO_FILE)
    ]
    subprocess.run(comando_final)
    print(f"🎬 Vídeo final gerado: {VIDEO_FILE}")

if __name__ == "__main__":
    paragrafos = dividir_roteiro()
    audios = gerar_audios(paragrafos)
    imagens = gerar_imagens(paragrafos)
    montar_video(imagens, audios)
