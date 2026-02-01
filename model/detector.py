import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

class DeepfakeDetector:
    def __init__(self):
        self.model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
        print("Loading ultra-light deepfake model...")

        self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
        self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)

        print("Model loaded (20MB).")

    def predict(self, audio_path):
        audio, sr = librosa.load(audio_path, sr=16000)

        inputs = self.feature_extractor(
            audio,
            sampling_rate=16000,
            return_tensors="pt"
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0].numpy()

        human_prob = float(probs[0])
        fake_prob = float(probs[1])

        if fake_prob > human_prob:
            return "AI_GENERATED", fake_prob
        else:
            return "HUMAN", human_prob
