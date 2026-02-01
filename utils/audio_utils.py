import base64
import uuid

def save_base64_audio(base64_string, audio_format):
    filename = f"temp_{uuid.uuid4()}.{audio_format}"
    audio_bytes = base64.b64decode(base64_string)

    with open(filename, "wb") as f:
        f.write(audio_bytes)

    return filename
