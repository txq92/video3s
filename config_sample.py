# Cấu hình API key cho Google AI Gemini
# Sao chép file này thành config.py và điền API key của bạn

# Lấy API key tại: https://ai.google.dev/
GEMINI_API_KEY = "your_api_key_here"

# Các giọng nói Gemini TTS có sẵn:
AVAILABLE_VOICES = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede",
    "Callirrhoe", "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba",
    "Despina", "Erinome", "Algenib", "Rasalgethi", "Laomedeia", "Achernar",
    "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird", "Zubenelgenubi",
    "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat"
]

# Giọng nói mặc định
DEFAULT_VOICE = "Kore"