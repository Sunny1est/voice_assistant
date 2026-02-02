from gtts import gTTS
import os
import uuid

STATIC_AUDIO_DIR = "static/audio"

if not os.path.exists(STATIC_AUDIO_DIR):
    os.makedirs(STATIC_AUDIO_DIR)

class TTSService:
    @staticmethod
    def text_to_speech(text: str, lang: str = 'pt') -> str:
        """Converts text to speech and returns the relative path to the audio file."""
        try:
            tts = gTTS(text=text, lang=lang)
            filename = f"response_{uuid.uuid4()}.mp3"
            file_path = os.path.join(STATIC_AUDIO_DIR, filename)
            tts.save(file_path)
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"Error in TTS: {e}")
            return ""
