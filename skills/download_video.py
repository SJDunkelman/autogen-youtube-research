from pytube import YouTube
import re
from uuid import uuid4


def download_youtube_video_audio(url: str) -> str | None:
    """
    Download the audio of a YouTube video
    :param url: str, YouTube video URL
    :return: str, the file path of the downloaded audio file
    """
    try:
        # Creating a YouTube object
        yt = YouTube(url)

        if yt.length > 600:
            print("Video is too long. Please provide a video that is less than 10 minutes long.")
            return None

        # Filter streams to only those with the 'mp4a.40.2' codec
        audio_streams = [stream for stream in yt.streams.filter(only_audio=True) if stream.audio_codec == 'mp4a.40.2']
        # Sort streams by bitrate in descending order (higher quality first)
        audio_streams.sort(key=lambda x: int(x.abr.split('kbps')[0]), reverse=True)

        if audio_streams:
            # Get the highest bitrate stream available
            best_audio = audio_streams[0]
            filename = f'{uuid4()}.m4a'
            output_file = best_audio.download(filename=filename)
            print(f'Audio successfully downloaded to "{output_file}"')
            return output_file
        else:
            print("No suitable audio stream found with codec 'mp4a.40.2'")
            return None
    except Exception as e:
        print(f'An error occurred: {e}')

    return None
