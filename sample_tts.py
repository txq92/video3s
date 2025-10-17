from google import genai
from google.genai import types
import wave
# sample tts
# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

# Thay thế 'your_api_key_here' bằng API key thực tế của bạn
API_KEY = "AIzaSyAcLoIS03oTfbMmblWt0FiyEciszIFrFac"
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="Chuyển văn bản sang lời nói có nhiều người nói",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory