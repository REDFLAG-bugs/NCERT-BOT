from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumHandler:
    def __init__(self) -> None:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
        
        chromedriver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

class GoogleSearch:
    @staticmethod
    def search(keyword, num_results=5):
        sel = SeleniumHandler()
        try:
            sel.driver.get(f"https://www.google.com/search?q={keyword}")
            elements = [element for element in sel.driver.find_elements(By.CLASS_NAME, "MjjYud")][:num_results]
            links = []
            for element in elements:
                a_tags = element.find_elements(By.TAG_NAME, "a")
                if len(a_tags) > 0:
                    links.append(a_tags[0].get_attribute("href"))
        except Exception as e:
            print(f"Google search failed: {e}")
            links = []
        finally:
            sel.__del__()
        return links

class YoutubeSearch:
    @staticmethod
    def search(keyword, num_results=5):
        split_keyword = "+".join(keyword.split(' '))
        sel = SeleniumHandler()
        try:
            url = f'https://www.youtube.com/results?search_query={split_keyword}'
            sel.driver.get(url)
            contents = sel.driver.find_elements(By.ID, 'video-title')[:num_results]
            video_ids = []
            for content in contents:
                video_url = content.get_attribute('href')
                if video_url:
                    video_id = video_url.split('v=')[-1]
                    video_ids.append(video_id)
        except Exception as e:
            print(f"YouTube search failed: {e}")
            video_ids = []
        finally:
            sel.__del__()
        return video_ids
