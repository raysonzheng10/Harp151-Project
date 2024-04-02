# Let's scrape Wikipedia Cats
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GoogleReviews:
    def __init__(self):
        self.driver = webdriver.Chrome()

        self.driver.get('https://www.google.com/')

    def get_google_reviews(self, movie: str) -> list[str]:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )

        # the input_element represents the search bar, we clear it and send in the text 'tech with tim' and then press ENTER
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"{movie} reviews" + Keys.ENTER)

        time.sleep(20)


googleReviews = GoogleReviews()
googleReviews.get_google_reviews('the shining')