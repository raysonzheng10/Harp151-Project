import requests
from bs4 import BeautifulSoup

class RottenTomatoes:
    def __init__(self):
        self.baseURL = 'https://www.rottentomatoes.com/m'

    def get_topCritic_reviews(self):
        pass


url = "https://www.rottentomatoes.com/m/the_dark_knight/reviews?intcmp=rt-scorecard_tomatometer-reviews"
user_agent = {'User-agent': 'Mozilla/5.0'}
response = requests.get(url, headers=user_agent).text
soup = BeautifulSoup(response, 'html.parser')
print(soup.prettify())

for element in soup.find_all('div', class_='review-row'):
    print(element)
print("Completed")