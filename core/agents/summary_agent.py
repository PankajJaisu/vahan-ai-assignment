from transformers import pipeline

class SummaryAgent:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def summarize(self, text):
        # Limit the text size to avoid long summarization time
        max_chars = 3000  # cap to first 3000 characters
        text = text[:max_chars]

        # Use only a single summarization call (on 1 chunk)
        summary = self.summarizer(text, max_length=360, min_length=120, do_sample=False)
        return summary[0]['summary_text']
        