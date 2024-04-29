from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class GoogleReviewsScraper:
    def __init__(self):
        #Set up ChromeOptions for headless mode
        options = Options()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options = options)
        self.review_list = []
        self.driver.get('https://www.google.com/')
        self.average_score = 0

    def get_google_reviews(self, movie: str, review_amount = 20, stars = 0) -> list[str]:
        self.review_list = []
        self.average_score = 0
        self.driver.get('https://www.google.com/')

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
                EC.presence_of_element_located((By.XPATH, '//*[@id="kp-wp-tab-FilmReview"]/div[1]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]'))
            )
            self.average_score = self.driver.find_element(By.XPATH, '//*[@id="kp-wp-tab-FilmReview"]/div[1]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[1]').text
            self.average_score += " out of 5"
            WebDriverWait(self.driver,5).until(
                EC.element_to_be_clickable((By.CLASS_NAME,"e8eHnd"))
            )
            self.driver.find_element(By.CLASS_NAME,"e8eHnd").click()
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
            for i in range(review_amount):
                j = 2 * i
                reviews = self.driver.find_elements(By.CLASS_NAME, "T7nuU")
                if reviews[j+1].text == "":
                    self.review_list.append(reviews[j+2].text)
                else:
                    self.review_list.append(reviews[j+1].text)
            return self.review_list
        except:
            print("movie reviews not found")
            return self.review_list
        



CreatedGoogleReviews = GoogleReviewsScraper()
CreatedGoogleReviews.get_google_reviews('interstellar')
