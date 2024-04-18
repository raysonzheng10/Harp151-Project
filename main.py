from Scrapers.rottenTomatoes import RottenTomatoes

tomatoes = RottenTomatoes()
reviews = tomatoes.get_topCritic_reviews('spiderman')
for review in reviews:
    print(review)