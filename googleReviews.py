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
        
        #Finds the review box and clicks into it 
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"e8eHnd"))
            )
            self.driver.find_element(By.CLASS_NAME,"e8eHnd").click()
        except:
            print("movie reviews not found")

        #Finds the more button and clicks it
        #For long movie reviews google won't initially show the whole review
        #Probably will want to make it so this clicks all the more buttons to load them
        #So they can be grabbed later?
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"tEJZ0b"))
            )
            self.driver.find_element(By.CLASS_NAME,"tEJZ0b").click()
        except:
            print("")
        
        #Finds the movie reviews
        #All review reviews are class name "T7nuU"
        WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"T7nuU"))
        )
        """
        Array of movie reviews
        Every even interval is the shortened version of the review
        The odd intervals are the full versions of the review
        However if the more button for that review isn't pressed, the review won't be loaded
        If the more button is pressed, the short review gets unloaded? and the even intervals will end up empty
        I'm not sure how to deal with the edge cases where a short review shows up
        It won't have the more option and it will throw off the indexing
        Can be put into a for loop to grab x amount of reviews
        """
        print(self.driver.find_elements(By.CLASS_NAME,"T7nuU")[1].text)
        time.sleep(5)
    
    """
    Function to get movie reviews filtered by rating (1-5 stars)
    Currently not sure how to actually click into each specific rating
    def get_movie_reviews_ratings(rating):
        #This will find the filter box and click it
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "zbTRdb"))
        )
        filter_box = driver.find_element(By.CLASS_NAME,"zbTRdb")
        filter_box.click()
    """


googleReviews = GoogleReviews()
googleReviews.get_google_reviews('the shining')