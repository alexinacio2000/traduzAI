from flask import Flask, request, jsonify
from google.cloud import speech, translate_v2 as translate
import base64

app = Flask(__name__)

# Inicialize os clientes das APIs
speech_client = speech.SpeechClient()
translate_client = translate.Client()

@app.route("/process_audio", methods=["POST"])
def process_audio():
    audio_data = request.json.get("audio_data")
    language = request.json.get("language", "en")
    
    # Decodifica o áudio
    audio_bytes = base64.b64decode(audio_data)

    # Configuração do reconhecimento de fala
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language,
    )

    # Reconhecimento
    response = speech_client.recognize(config=config, audio=audio)
    if not response.results:
        return jsonify({"error": "No speech detected"}), 400
    
    # Tradução
    transcript = response.results[0].alternatives[0].transcript
    translation = translate_client.translate(transcript, target_language="pt")

    return jsonify({"transcript": transcript, "translation": translation["translatedText"]})

if __name__ == "__main__":
    app.run(debug=True)
