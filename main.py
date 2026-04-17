import os
import textwrap
from pathlib import Path

from gtts import gTTS

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
ROTEIRO_FILE = BASE_DIR / "roteiro.txt"
AUDIO_DIR = BASE_DIR / "audios"
IMG_DIR = BASE_DIR / "imagens"
VIDEO_FILE = BASE_DIR / "videoaula.mp4"

# Garantir pastas
AUDIO_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)

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
        audio_path = AUDIO_DIR / f"slide{i}.mp3"
        tts = gTTS(text=p, lang="pt")
        tts.save(audio_path)
        arquivos.append(audio_path)
        print(f"✅ Áudio gerado: {audio_path}")
    return arquivos

def montar_video(paragrafos, audios):
    """Monta o vídeo com imagens e áudios usando FFmpeg."""
    lista_txt = BASE_DIR / "lista.txt"
    with open(lista_txt, "w", encoding="utf-8") as f:
        for i, audio in enumerate(audios, start=1):
            img_path = IMG_DIR / f"slide{i}.png"
            if not img_path.exists():
                raise FileNotFoundError(f"Imagem {img_path} não encontrada.")
            f.write(f"file '{img_path}'\n")
            f.write(f"file '{audio}'\n")
    
    # FFmpeg concatenação (imagens + áudios)
    comando = (
        f'ffmpeg -y -f concat -safe 0 -i "{lista_txt}" '
        f'-c:v libx264 -c:a aac -pix_fmt yuv420p "{VIDEO_FILE}"'
    )
    os.system(comando)
    print(f"🎬 Vídeo final gerado: {VIDEO_FILE}")

if __name__ == "__main__":
    paragrafos = dividir_roteiro()
    audios = gerar_audios(paragrafos)
    montar_video(paragrafos, audios)
