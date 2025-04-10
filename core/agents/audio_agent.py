from gtts import gTTS
import os
class AudioAgent:
    def generate_audio(self, summary, path, topic=None):
        intro = f"Welcome to today's podcast on {topic}. " if topic else "Welcome to today's research summary. "
        outro = "Thanks for listening to this episode. Stay tuned for more insightful research breakdowns."
        full_script = f"{intro}{summary} {outro}"

        tts = gTTS(text=full_script)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tts.save(path)