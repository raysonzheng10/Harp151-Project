import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
class RottenTomatoesScraper:
    def __init__(self):
        self.baseURL = 'https://www.rottentomatoes.com'
        self.driver = webdriver.Chrome()
        self.audience_review_list = []
        self.critic_review_list = []
        self.review_list = []
        self.driver.get('https://www.google.com/')


    # function to format the name of a movie_title to get put into the url for bs4
    def format_movie_title(self, movie_title:str ) -> list[str]:
        return movie_title.replace(" ", "_").replace("-", "_")
    
    # returns a list of top critic reviews for a given movie title
    # TODO: be able to click the 'more reviews' button to get more of them
    def get_topCritic_reviews(self, movie_title: str ) -> list[str]:
        # type in the proper url to get the source code
        reformatted_title = self.format_movie_title(movie_title)
        url = f'{self.baseURL}/m/{reformatted_title}/reviews?intcmp=rt-scorecard_tomatometer-reviews'

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        
        #self.driver.get(url)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        self.driver.maximize_window()
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"rotten tomatoes {movie_title}" + Keys.ENTER)
        #Look for link with rotten tomatoes and movie title
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "reviews"))
            )
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Review").click()
            #print("success")
            #time.sleep(5)
            #Finds and clicks top critics reviews
            try:
                #print("waiting")
                # WebDriverWait(self.driver, 5).until(
                #     EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a'))
                # )
                # #print("found")
                # critic_reviews = self.driver.find_element(By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a')
                # critic_reviews.click()
                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews"]/div[2]/rt-button'))
                )
                
                #print("found")
                self.driver.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button').click()
                time.sleep(5)
            except:
                print("reviews not found")
        except:
            print("movie reviews not found")
        # loop through the elements and find all the review texts and compile them into a list
        reviews = []
        for element in soup.find_all('div', class_='review-row'):
            review_text = element.find('p', class_='review-text').text
            reviews.append(review_text)
        #for review in reviews:
            #print(review)
        print(len(reviews))
        return reviews
    #Getting reviews with selenium
    def get_critic_reviews(self, movie_title: str) -> list[str]:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        self.driver.maximize_window()
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"rotten tomatoes {movie_title}" + Keys.ENTER)
        #Look for link with rotten tomatoes and movie title
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "reviews"))
            )
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Review").click()
            #print("success")
            #time.sleep(5)
            #Finds and clicks top critics reviews
            try:
                #print("waiting")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a'))
                )
                #print("found")
                critic_reviews = self.driver.find_element(By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a')
                critic_reviews.click()
                #print("waiting")
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text"))
                )
                #print("found")
                reviews = self.driver.find_elements(By.CLASS_NAME, "review-text")
                for review in reviews:
                    text = review.text
                    self.critic_review_list.append(text)
                #print("done")
                #Ends up pulling 20 reviews
                #Could pull more by scrolling?

                #print(len(self.critic_review_list))
                # for review in self.critic_review_list:
                #     print(review)
                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews"]/div[2]/rt-button'))
                )
                #print("found")
                self.driver.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button').click()
                return self.critic_review_list
            except:
                print("critic reviews not found")
        except:
            print("Movie reviews not found")
    
    def get_audience_reviews(self, movie_title: str) -> list[str]:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        self.driver.maximize_window()
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"rotten tomatoes {movie_title}" + Keys.ENTER)
        #Look for link with rotten tomatoes and movie title
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "reviews"))
            )
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Review").click()
            #print("success")
            #time.sleep(5)
            #Finds and clicks all audience reviews
            try:
                #print("waiting")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/nav/ul/li[3]/a'))
                )
                #print("found")
                audience_reviews = self.driver.find_element(By.XPATH, '//*[@id="reviews"]/nav/ul/li[3]/a')
                audience_reviews.click()
                #print("waiting")
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/div[1]/div[1]/div[2]/drawer-more/p'))
                )
                #print("found")
                #print("looking for reviews")
                for i in range(20):
                    review = self.driver.find_element(By.XPATH, f'//*[@id="reviews"]/div[1]/div[{i+1}]/div[2]/drawer-more/p').text
                    #print(review)
                    self.audience_review_list.append(review)
                #Ends up pulling 20 reviews
                #Could pull more by scrolling?

                #print(len(self.audience_review_list))
                # for review in self.critic_review_list:
                #     print(review)
                #print("looking")
                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews"]/div[2]/rt-button'))
                )
                #print("found")
                self.driver.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button').click()
                time.sleep(5)
                return self.audience_review_list
            except:
                print("audience reviews not found")
        except:
            print("Movie reviews not found")


CreatedRottenTomatoesScraper = RottenTomatoesScraper()
#CreatedRottenTomatoesScraper.get_critic_reviews("The shining")
#CreatedRottenTomatoesScraper.get_audience_reviews("The Shining")
# CreatedRottenTomatoesScraper.get_topCritic_reviews("shining")