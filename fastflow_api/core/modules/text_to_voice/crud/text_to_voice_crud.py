# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted Router ===================================
from gtts import gTTS
from datetime import datetime
import os
import pyttsx3
import tempfile

# FUNGSI ONLINE
def text_to_mp3(text: str, lang: str = "id", output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"tts_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    filepath = os.path.join(output_dir, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    return filepath