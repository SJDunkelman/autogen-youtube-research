from pydub import AudioSegment
import whisper
import numpy as np

model = whisper.load_model("tiny")


def chunk_audio(file_path, chunk_length_ms=60000):  # Set for 1 minute
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    return chunks


def transcribe_audio(audio_file_path: str):
    """
    Transcribe the audio of a file using OpenAI's Whisper model.

    :param audio_file_path: str, File path of the audio file to transcribe
    """
    original_audio = AudioSegment.from_file(audio_file_path, format='m4a')
    converted_file_path = audio_file_path.replace('.m4a', '.wav')
    original_audio.export(converted_file_path, format='wav')
    audio_chunks = chunk_audio(converted_file_path)

    transcriptions = []
    for chunk in audio_chunks:
        # Convert Pydub audio chunk to the appropriate format for Whisper
        audio_data = np.array(chunk.get_array_of_samples())
        if chunk.channels == 2:
            audio_data = audio_data.reshape((-1, 2))

        # Transcribe the chunk
        result = model.transcribe(audio_data, fp16=False)
        transcriptions.append(result.text)

    # Combine all transcriptions into a single string
    full_transcription = " ".join(transcriptions)
    return full_transcription

