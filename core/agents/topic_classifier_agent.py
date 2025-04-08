from transformers import pipeline

class TopicClassificationAgent:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification")

    def classify(self, text, labels):
        result = self.classifier(text, labels)
        return result["labels"][0]  # return top topic

