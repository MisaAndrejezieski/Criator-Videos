import os
import subprocess
import textwrap
from pathlib import Path

from gtts import gTTS

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
ROTEIRO_FILE = BASE_DIR / "roteiro.txt"
SAIDA_DIR = BASE_DIR / "saida"
VIDEO_FILE = SAIDA_DIR / "videoaula.mp4"

# Garantir pastas
SAIDA_DIR.mkdir(exist_ok=True)

def dividir_roteiro():
    """Divide o roteiro em parágrafos (um slide por parágrafo)."""
    with open(ROTEIRO_FILE, "r", encoding="utf-8") as f:
        texto = f.read()
    paragrafos = [p.strip() for p in texto.split("\n") if p.strip()]
    return paragrafos

def gerar_audios(paragrafos):
    """Gera um áudio MP3 para cada parágrafo."""
    arquivos = []
    for i, p in enumerate(paragrafos, start=1):
        audio_path = SAIDA_DIR / f"slide{i}.mp3"
        tts = gTTS(text=p, lang="pt")
        tts.save(audio_path)
        arquivos.append(audio_path)
        print(f"✅ Áudio gerado: {audio_path}")
    return arquivos

def gerar_imagens(paragrafos):
    """Gera uma imagem simples com texto para cada parágrafo."""
    from PIL import Image, ImageDraw, ImageFont

    arquivos = []
    for i, p in enumerate(paragrafos, start=1):
        img_path = SAIDA_DIR / f"slide{i}.png"
        # Criar imagem branca
        img = Image.new("RGB", (1280, 720), color="white")
        draw = ImageDraw.Draw(img)
        # Fonte padrão do sistema
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        # Quebrar texto em linhas
        wrapped = textwrap.fill(p, width=40)
        draw.text((50, 300), wrapped, fill="black", font=font)
        img.save(img_path)
        arquivos.append(img_path)
        print(f"🖼️ Imagem gerada: {img_path}")
    return arquivos

def montar_video(imagens, audios):
    """Monta o vídeo com imagens e áudios usando FFmpeg."""
    lista_txt = SAIDA_DIR / "lista.txt"
    with open(lista_txt, "w", encoding="utf-8") as f:
        for img, audio in zip(imagens, audios):
            f.write(f"file '{img}'\n")
            f.write(f"file '{audio}'\n")
    
    comando = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(lista_txt),
        "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
        str(VIDEO_FILE)
    ]
    subprocess.run(comando)
    print(f"🎬 Vídeo final gerado: {VIDEO_FILE}")

if __name__ == "__main__":
    paragrafos = dividir_roteiro()
    audios = gerar_audios(paragrafos)
    imagens = gerar_imagens(paragrafos)
    montar_video(imagens, audios)
