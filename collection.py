from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager



class SeleniumHandler:

    def __init__(self) -> None:
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
      


class GoogleSearch():

    def __init__(self) -> None:
        pass

    @staticmethod
    def search(keyword):
        sel = SeleniumHandler()
        sel.driver.get(f"https://www.google.com/search?q={keyword}")
        elements = [element for element in sel.driver.find_elements(By.CLASS_NAME, "MjjYud")]
        links = []
        for element in elements:
            a_tags = element.find_elements(By.TAG_NAME, "a")
            if len(a_tags) > 0:
                links.append(a_tags[0].get_attribute("href"))
        sel.driver.quit()
        return links
    



class YoutubeSearch():

    def __init__(self) -> None:
        pass

    @staticmethod
    def search(keyword):
        split_keyword="+".join(keyword.split(' '))
        sel=SeleniumHandler()
        url=f'https://www.youtube.com/results?search_query={split_keyword}'
        sel.driver.get(url)
        contents=sel.driver.find_elements(By.ID,'video-title')
        links=[]
        for content in contents:
            val=content.get_attribute('href')
            if val:
                links.append(val)
        return links
        
        



if __name__=='__main__':

    links=GoogleSearch.search('chapter 11 hornbill photograph summary')
    print(links)
    links=YoutubeSearch.search('chapter 11 hornbill photograph')
    print(links)
    


