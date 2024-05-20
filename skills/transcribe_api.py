from pydub import AudioSegment
import requests
from tempfile import NamedTemporaryFile
import json
import os
from tqdm import tqdm


def chunk_audio(file_path, chunk_length_ms=300000):  # Set for 5 minutes
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    return chunks


def transcribe_audio_file(audio_file_path: str) -> str:
    """
    Transcribe the audio of a file using OpenAI's Whisper model.

    :param audio_file_path: str, File path of the audio file to transcribe
    """
    api_url = "https://transcribe.whisperapi.com"
    api_key = os.getenv("WHISPER_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please set the WHISPER_API_KEY environment variable. TERMINATE")
    headers = {'Authorization': f'Bearer {api_key}'}

    sound = AudioSegment.from_file(audio_file_path, format='m4a')
    converted_file_path = audio_file_path.replace('.m4a', '.wav')
    sound.export(converted_file_path, format='wav')

    chunks = chunk_audio(converted_file_path)
    output_text_chunks = []
    for index, chunk in tqdm(enumerate(chunks)):
        with NamedTemporaryFile(delete=True, suffix='.wav') as tmp:
            chunk.export(tmp.name, format="wav")

            files = {'file': open(tmp.name, 'rb')}
            data = {
                "fileType": "wav",
                "diarization": "True",
                "task": "transcribe",
                "language": "en"
            }

            response = requests.post(api_url, headers=headers, files=files, data=data)
            response = json.loads(response.text)
            if "error" in response.keys():
                raise Exception(response.json()["error"])
            print(f"Chunk {index + 1}:")
            output_text_chunks.append(response['text'])
            print(response['text'])
            files['file'].close()

    return " ".join(output_text_chunks)
