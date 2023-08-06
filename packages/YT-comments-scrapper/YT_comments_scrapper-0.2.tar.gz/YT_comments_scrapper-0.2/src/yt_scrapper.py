import time
import requests
import re
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YtScrapper:
    def __init__(self,video_url,no_of_comments,chromedriverpath) -> None:
        self.video_url = video_url
        self.no_of_comments = no_of_comments
        self.chromedriverpath = chromedriverpath


    def checkinput(self, object, instance) -> None:
        """
        Validates that the number of comments is an integer type
        """
        if not isinstance(object, instance):
            raise ValueError(f"Expected {instance} instead of {object}")

    def match_youtube_url(self):
        """
        Checks that url is a youtube url
        """
        yt_url = re.compile('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$')

        if(re.search(yt_url, self.video_url)):
            return True
        else:
            raise AttributeError("Expected a Youtube url")
 


    def check_video_url(self):
        """
        Checks that the video returns a 200 response
        """
        self.checkinput(self.no_of_comments,int)
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}
        request = requests.get(self.video_url,headers = headers)

        if request.status_code != 200:
            raise OSError("Invalid response")
        return 200
        
                    
    def scrape_comments(self) -> pd.DataFrame:
        """
        Scrapes the comments from the YouTube link url
        """
        data=[]
        if self.match_youtube_url() == True and self.check_video_url() == 200:

            with Chrome(executable_path=self.chromedriverpath) as driver:
                wait = WebDriverWait(driver,15)
                driver.get(self.video_url)

                for item in range(self.no_of_comments): 
                    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                    time.sleep(15)

                for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
                    data.append(comment.text)
        else:
            raise ValueError("Expected a Youtube url")
        df = pd.DataFrame(data, columns=['comment'])
        return df
