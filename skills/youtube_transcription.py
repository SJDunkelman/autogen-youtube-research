import pytube as pt
from uuid import uuid4


def download_youtube_audio(url: str) -> str:
    yt = pt.YouTube(url)
    stream = yt.streams.filter(only_audio=True)[0]
    file_name = f"{uuid4()}.mp3"
    stream.download(filename=file_name)
    return file_name


if __name__ == "__main__":
    download_youtube_audio("https://www.youtube.com/watch?v=dd1kN_myNDs")