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
def get_channel_stats(channel_url: str):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL of the channel page
    url = 'https://socialblade.com/youtube/channel/UCigUBIf-zt_DA6xyOQtq2WA/videos'
    driver.get(url)

    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    time.sleep(10)  # Adding a sleep to ensure all scripts are loaded and button is clickable
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="SP Consent Message"]')))
    driver.switch_to.frame(iframe)
    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    accept_button.click()

    # Switch back to the main document to continue with other operations
    driver.switch_to.default_content()

    # Extract specific data points
    soup = BeautifulSoup(driver.page_source, 'lxml')

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


    for key, value in data.items():
        print(f"{key}: {value}")


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

    for video in videos_info:
        print(f"Video Title: {video['text']}, Link: {video['href']}")

    # Close the browser
    driver.quit()
