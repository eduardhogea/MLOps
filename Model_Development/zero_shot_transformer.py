from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import bentoml
import os

class ZeroShotClassifier:
    def __init__(self, model_name="typeform/distilbert-base-uncased-mnli", save_dir="model"):
        self.model_name = model_name
        self.save_dir = save_dir
        self.classifier = self.load_model()

    def load_model(self):
        if os.path.exists(self.save_dir):
            model = AutoModelForSequenceClassification.from_pretrained(self.save_dir)
            tokenizer = AutoTokenizer.from_pretrained(self.save_dir)
        else:
            model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model.save_pretrained(self.save_dir)
            tokenizer.save_pretrained(self.save_dir)

        return pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

    def classify(self, text, candidate_labels):
        return self.classifier(text, candidate_labels)

def save_model(zero_shot_classifier, model_name):
    bentoml.transformers.save_model(model_name, zero_shot_classifier.classifier.model, zero_shot_classifier.classifier.tokenizer)

def load_model(model_name):
    classifier = bentoml.transformers.load_model(model_name)
    return classifier

if __name__ == "__main__":
    zero_shot_classifier = ZeroShotClassifier()

    save_model(zero_shot_classifier, "my_zero_shot_classifier")

    loaded_classifier = load_model("my_zero_shot_classifier")
    print("Model loaded successfully.")
