# Let's scrape Wikipedia Cats
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

class GoogleReviews:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.review_list = []
        self.driver.get('https://www.google.com/')
    
    # TODO: make the function compile the reviews into a list of strings. Right now we only get one review, make the function have the ability to get all of them
    # The end of this function should return a list.
    # TODO: make this function take in 2 additional parameters: number_limit:int, number_stars:int
    # the number_limit should limit the number of reviews we get (default should be 100?)
    # the number_stars indicates the type of review we want (ie 1 star/2 star/etc.), default value will be none, so we grab all reviews unordered
    # feel free to factor some functions out, just do what you think is best

    # ? I had issues trying to scroll down the reviews window
    # ? It might be possible that not all the reviews will get loaded if you don't scroll the page
    # ? Might end up not grabbing enough reviews if not enough reviews are loaded/available?


    def get_google_reviews(self, movie: str, review_amount: int) -> list[str]:
        self.driver.maximize_window()
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
            for review in self.driver.find_elements(By.CLASS_NAME, "tEJZ0b"):
                review.click()
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
        for i in range(review_amount):
            j = 2 * i
            review = self.driver.find_elements(By.CLASS_NAME, "T7nuU")[j+1].text
            self.review_list.append(review)
            #print(f"This is review {i}\n " + review)
        #print(self.driver.find_elements(By.CLASS_NAME,"T7nuU")[1].text)
        return self.review_list
        time.sleep(5)

    def get_google_reviews(self, movie: str, review_amount: int, stars:int) -> list[str]:
        self.driver.maximize_window()
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
                EC.element_to_be_clickable((By.CLASS_NAME,"e8eHnd"))
            )
            self.driver.find_element(By.CLASS_NAME,"e8eHnd").click()
        except:
            print("movie reviews not found")
        
        
        WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "zbTRdb"))
        )
        filter_box = self.driver.find_element(By.CLASS_NAME,"zbTRdb")
        filter_box.click()
        #Wait for dropdown menu
        WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="lb"]/div[2]/g-menu/g-menu-item[2]'))
        )
        #Select an option from dropdown
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
        
        #Finds the more button and clicks it
        #For long movie reviews google won't initially show the whole review
        #Probably will want to make it so this clicks all the more buttons to load them
        #So they can be grabbed later?
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"tEJZ0b"))
            )
            for i in range (3):
                for review in self.driver.find_elements(By.CLASS_NAME, "tEJZ0b"):
                    review.click()
        except:
            print("")
        
        #Finds the movie reviews
        #All review reviews are class name "T7nuU"
        # WebDriverWait(self.driver,10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME,"T7nuU"))
        # )

        

        time.sleep(5)
        for i in range(review_amount):
            j = 2 * i
            review = self.driver.find_elements(By.CLASS_NAME, "T7nuU")[j+1].text
            self.review_list.append(review)
            #print(f"This is review {i}\n " + review)
        #print(self.driver.find_elements(By.CLASS_NAME,"T7nuU")[1].text)
        return self.review_list
        time.sleep(5)



googleReviews = GoogleReviews()
googleReviews.get_google_reviews('the shining', 10, 1)