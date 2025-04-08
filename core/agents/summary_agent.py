from transformers import pipeline

class SummaryAgent:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text):
        chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
        return " ".join(self.summarizer(chunk)[0]['summary_text'] for chunk in chunks)
