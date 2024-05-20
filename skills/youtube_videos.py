from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up Chrome options
options = Options()
options.add_argument('start-maximized')  # Maximize the window to simulate a real user's screen
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
# User agent string of a commonly used browser
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')


# Initialize WebDriver
def get_recent_channel_videos(channel_id: str) -> list[tuple[str, str]]:
    """
    Get the recent channel videos for a YouTube channel via the channel ID

    :param channel_id: str, YouTube channel ID (this is not the same as the username)
    :return: list[tuple[str, str]], list of tuples containing video title and video link
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL of the channel page
    url = f'https://socialblade.com/youtube/channel/{channel_id}/videos'
    driver.get(url)

    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    time.sleep(10)  # Adding a sleep to ensure all scripts are loaded and button is clickable
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="SP Consent Message"]')))
    driver.switch_to.frame(iframe)
    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    accept_button.click()

    # Switch back to the main document to continue with other operations
    driver.switch_to.default_content()

    # Ensure the div is scrolled into view and loaded
    videos_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'YouTube-Video-Wrap')))
    driver.execute_script("arguments[0].scrollIntoView();", videos_div)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    video_wrap = soup.find('div', id='YouTube-Video-Wrap')
    video_child_divs = video_wrap.find_all('div', recursive=False)
    videos_info = []
    for div in video_child_divs:
        a_tags = div.find_all('a')
        if len(a_tags) >= 2:
            video_a_tag = a_tags[0]
            href = video_a_tag.get('href', None)
            text = video_a_tag.text.strip()
            videos_info.append({'text': text, 'href': href})

    output = []
    for video in videos_info:
        # print(f"Video Title: {video['text']}, Link: {video['href']}")
        output.append((video['text'], video['href']))

    # Close the browser
    driver.quit()
    return output
