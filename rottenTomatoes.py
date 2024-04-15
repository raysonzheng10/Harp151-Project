import requests
from bs4 import BeautifulSoup

class RottenTomatoes:
    def __init__(self):
        self.baseURL = 'https://www.rottentomatoes.com'

    # function to format the name of a movie_title to get put into the url for bs4
    def format_movie_title(self, movie_title:str ) -> str:
        return movie_title.replace(" ", "_").replace("-", "_")
    
    # returns a list of top critic reviews for a given movie title
    # TODO: be able to click the 'more reviews' button to get more of them
    def get_topCritic_reviews(self, movie_title: str ) -> list[str]:
        reformatted_title = self.format_movie_title(movie_title)
        url = f'{self.baseURL}/m/{reformatted_title}/reviews?intcmp=rt-scorecard_tomatometer-reviews'

        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        
        reviews = []

        for element in soup.find_all('div', class_='review-row'):
            review_text = element.find('p', class_='review-text').text
            reviews.append(review_text)

        return reviews

tomatoes = RottenTomatoes()
reviews = tomatoes.get_topCritic_reviews('the dark knight')
for review in reviews:
    print(review)