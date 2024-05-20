import cloudscraper
from bs4 import BeautifulSoup
import urllib.parse
import re


def get_channel_stats(username: str) -> tuple[dict[str, str], str | None]:
    """
    Get the stats for a YouTube channel via the channel username

    :param username: str, YouTube channel username
    :return: tuple[dict[str, str], str | None], dictionary of channel stats and channel ID
    """
    scraper = cloudscraper.create_scraper()

    # URL of the channel page
    encoded_username = urllib.parse.quote(username)
    html = scraper.get(f"https://socialblade.com/youtube/s/?q={encoded_username}").text
    soup = BeautifulSoup(html, 'lxml')

    banner_image = soup.find('div', id='YouTubeUserTopHeaderBackground')
    channel_id_match = re.search(r'(?<=https://www\.banner\.yt/)(.+)(?=\?)',banner_image['style'])

    # Select all divs with class "YouTubeUserTopInfo"
    data_divs = soup.select('div.YouTubeUserTopInfo')
    data = {}
    for idx, div in enumerate(data_divs):
        text = div.text.strip()
        cleaned_text = text.split('\n')[0]
        if "Uploads" in text:
            data['Uploads'] = cleaned_text.split('Uploads')[1].strip()
        elif "Subscribers" in text:
            data['Subscribers'] = cleaned_text.split('Subscribers')[1].strip()
        elif "Video Views" in text:
            data['Video Views'] = cleaned_text.split('Video Views')[1].strip()
        elif "Country" in text:
            data['Country'] = cleaned_text.split('Country')[1].strip()
        elif "Channel Type" in text:
            data['Channel Type'] = cleaned_text.split('Channel Type')[1].strip()
        elif "User Created" in text:
            data['User Created'] = cleaned_text.split('User Created')[1].strip()

    # for key, value in data.items():
    #     print(f"{key}: {value}")

    if channel_id_match:
        channel_id = channel_id_match.group(0)
    else:
        channel_id = None

    return data, channel_id
