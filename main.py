from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils.audio_utils import save_base64_audio
from model.detector import DeepfakeDetector

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()

detector = DeepfakeDetector()   # load model on startup

# Request Schema
class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.post("/detect")
async def detect_voice(
    request: AudioRequest,
    x_api_key: str = Header(None)
):

    # Validate API Key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Validate audio format
    if request.audio_format not in ["mp3", "wav", "ogg"]:
        raise HTTPException(status_code=400, detail="Invalid audio format")

    # Save base64 audio
    try:
        temp_file = save_base64_audio(request.audio_base64, request.audio_format)
    except:
        raise HTTPException(status_code=400, detail="Invalid Base64")

    # Run deepfake detection
    classification, confidence = detector.predict(temp_file)

    explanation = (
        "Prediction generated using wav2vec2 deepfake detection model "
        "analyzing spectral patterns and voice artifacts."
    )

    # Cleanup
    os.remove(temp_file)

    # Return response
    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
