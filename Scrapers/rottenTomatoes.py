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
        options = Options()
        options.add_argument("--headless=new")
        self.baseURL = 'https://www.rottentomatoes.com'
        self.driver = webdriver.Chrome(options = options)
        self.audience_review_list = []
        self.critic_review_list = []
        self.review_list = []
        self.driver.get('https://www.google.com/')
        self.average_score = 0
    
    # returns a list of top critic reviews for a given movie title
    #Getting reviews with selenium
    def get_critic_reviews(self, movie_title: str) -> list[str]:
        self.average_score = 0
        self.critic_review_list = []
        self.driver.get('https://www.google.com/')
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"rotten tomatoes {movie_title}" + Keys.ENTER)
        #Look for link with rotten tomatoes and movie title
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[3]/div/span[1]'))
                )
            self.average_score = self.driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[3]/div/span[1]').get_attribute("aria-label")[:-1]
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Movie Review"))
            )
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Movie Review").click()

            #Finds and clicks top critics reviews
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a'))
                )
                critic_reviews = self.driver.find_element(By.XPATH, '//*[@id="reviews"]/nav/ul/li[2]/a')
                critic_reviews.click()
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text"))
                )
                reviews = self.driver.find_elements(By.CLASS_NAME, "review-text")
                for review in reviews:
                    text = review.text
                    self.critic_review_list.append(text)

                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews"]/div[2]/rt-button'))
                )
                self.driver.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button').click()
                return self.critic_review_list
            except:
                print("critic reviews not found")
        except:
            print("Movie reviews not found")
    
    def get_audience_reviews(self, movie_title: str) -> list[str]:
        self.average_score = 0
        self.audience_review_list = []
        self.driver.get('https://www.google.com/')
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
        )
        input_element = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        input_element.clear()
        input_element.send_keys(f"rotten tomatoes {movie_title}" + Keys.ENTER)
        #Look for link with rotten tomatoes and movie title
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[3]/div/span[1]'))
                )
            self.average_score = self.driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[3]/div/span[1]').get_attribute("aria-label")[:-1]
            print(self.average_score)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Movie Review"))
            )
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Movie Review").click()

            #Finds and clicks all audience reviews
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/nav/ul/li[3]/a'))
                )
                audience_reviews = self.driver.find_element(By.XPATH, '//*[@id="reviews"]/nav/ul/li[3]/a')
                audience_reviews.click()
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews"]/div[1]/div[1]/div[2]/drawer-more/p'))
                )

                for i in range(20):
                    review = self.driver.find_element(By.XPATH, f'//*[@id="reviews"]/div[1]/div[{i+1}]/div[2]/drawer-more/p').text
                    self.audience_review_list.append(review)

                WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews"]/div[2]/rt-button'))
                )
                self.driver.find_element(By.XPATH, '//*[@id="reviews"]/div[2]/rt-button').click()
                return self.audience_review_list
            except:
                print("audience reviews not found")
        except:
            print("Movie reviews not found")


CreatedRottenTomatoesScraper = RottenTomatoesScraper()
CreatedRottenTomatoesScraper.get_audience_reviews("Dune 2")
