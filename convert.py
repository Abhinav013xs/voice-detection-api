import base64

with open("sample.ogg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

print(encoded)
