from gtts import gTTS
import os

class AudioAgent:
    def generate_audio(self, summary, path):
        tts = gTTS(summary)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tts.save(path)