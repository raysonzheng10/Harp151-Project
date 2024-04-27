from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class GoogleReviewsScraper:
    def __init__(self):
        # Set up ChromeOptions for headless mode
        # options = Options()
        # options.add_argument("--headless=new")

        self.driver = webdriver.Chrome()
        self.review_list = []
        self.driver.get('https://www.google.com/')

    # TODO: Combine both functions into the same one
    # TODO: give default values to review_amount parameter and stars parameter
    # (you can look at YoutubeAPI.py for an example as well)
    # (we want to make it so that if we don't input any stars value, it will just default to grabing unordered reviews)
    # (Right now, we don't have any way of grabbing unordered reviews)
    # TODO: You can press the END key to scroll down. You need to click on the window first to select it, but you can grab a lot more reviews this way
    # TODO: Make a helper function to factor out the way we select stars reviews
    
    def get_google_reviews(self, movie: str, review_amount = 20, stars = 0) -> list[str]:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        self.driver.maximize_window()
        # the input_element represents the search bar, we clear it and send in the text 'tech with tim' and then press ENTER
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"{movie} reviews" + Keys.ENTER)
        
        #Finds the review box and clicks into it 
        try:
            WebDriverWait(self.driver,5).until(
                EC.element_to_be_clickable((By.CLASS_NAME,"e8eHnd"))
            )
            self.driver.find_element(By.CLASS_NAME,"e8eHnd").click()
            time.sleep(5)
            if stars != 0:
                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "zbTRdb"))
                )
                filter_box = self.driver.find_element(By.CLASS_NAME,"zbTRdb")
                filter_box.click()
                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH,'//*[@id="lb"]/div[2]/g-menu/g-menu-item[2]'))
                )
                if stars == 5:
                    self.driver.find_element(By.XPATH, '//*[@id="lb"]/div[2]/g-menu/g-menu-item[2]').click()
                elif stars == 4:
                    self.driver.find_element(By.XPATH, '//*[@id="lb"]/div[2]/g-menu/g-menu-item[3]').click()
                elif stars == 3:
                    self.driver.find_element(By.XPATH, '//*[@id="lb"]/div[2]/g-menu/g-menu-item[4]').click()
                elif stars == 2:
                    self.driver.find_element(By.XPATH, '//*[@id="lb"]/div[2]/g-menu/g-menu-item[5]').click()
                elif stars == 1:
                    self.driver.find_element(By.XPATH, '//*[@id="lb"]/div[2]/g-menu/g-menu-item[6]').click()
            try:
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,"tEJZ0b"))
                )
                for i in range(3):
                    for review in self.driver.find_elements(By.CLASS_NAME,"tEJZ0b"):
                        review.click()
            except:
                print("")
            time.sleep(5)
            for i in range(review_amount):
                j = 2 * i
                reviews = self.driver.find_elements(By.CLASS_NAME, "T7nuU")
            #print(reviews[i][0:10])
                if reviews[j+1].text == "":
                    self.review_list.append(reviews[j+2].text)
                else:
                    self.review_list.append(reviews[j+1].text)
            return self.review_list
        except:
            print("movie reviews not found")
            return self.review_list
        


    # function to extract youtube video id from the url
    def extract_video_id(self, url: str) -> str:
        # Split the URL at 'v=' and get everything after that
        video_id = url.split('v=')[1]

        # If there are additional parameters after the video ID, remove them
        if '&' in video_id:
            video_id = video_id.split('&')[0]

        # return the string value
        return video_id
    
    def get_YoutubeTrailer_Id(self, movie: str) -> str:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"{movie} reviews" + Keys.ENTER)

        # wait for the page to load
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[13]/div[4]/div[5]/div/div/div[2]/div/div/div/div[1]/div[1]/a'))
        )

        # Click on the youtube trailer link
        youtube_trailer_link = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[13]/div[4]/div[5]/div/div/div[2]/div/div/div/div[1]/div[1]/a')
        youtube_trailer_link.click()
        
        time.sleep(5)

        # After getting to the yt trailer, get the url
        current_url = self.driver.current_url

        # use the extact video id function to get the video id from the url, return that value
        video_id = self.extract_video_id(current_url)

        return video_id


createdGoogleReviews = GoogleReviewsScraper()
# print(googleReviews.get_google_reviews('the shining', 10, 1))
# googleReviews.get_YoutubeTrailer_Id('the dark knight')