import pytube as pt
from uuid import uuid4
from pydub import AudioSegment
from config import PROJECT_ROOT_DIR


def download_youtube_audio(url: str) -> str:
    yt = pt.YouTube(url)
    stream = yt.streams.filter(only_audio=True)[0]
    file_name = f"{uuid4()}.mp3"
    file_path = PROJECT_ROOT_DIR / "input" / file_name
    stream.download(filename=file_path)
    return file_name


def chunk_audio(file_path, chunk_length_ms=300000):  # Set for 5 minutes
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    return chunks


if __name__ == "__main__":
    download_youtube_audio("https://www.youtube.com/watch?v=dd1kN_myNDs")