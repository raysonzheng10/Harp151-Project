from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean
# statistics.mean, put all the compounds of the reviews onto a list and then get the average of it

analyzer = SentimentIntensityAnalyzer()

def get_compound(reviews):
    compound_results = []

    for review in reviews:
        # .polarity_scores provides the sentiments of the reviews (ex: negative, positve, neutral, and compound)
        # compound score is the sum of all the ratings ranging from -1 (extremely negative) to 1 (extremely positive)
        result = analyzer.polarity_scores(review)
        compound_results.append(result["compound"])

    average_compound = mean(compound_results)
    return average_compound

# function that takes in reviews and then returns a tuple separating the good/bad based on Vader
def separate_good_bad(reviews):
    # create empty lists to store reviews
    good_reviews = []
    bad_reviews = []
    
    # loop through all reviews
    for review in reviews:
        # grab the general_sentiment of the review
        result = analyzer.polarity_scores(review)
        general_sentiment = result['compound']

        # sort reviews based on negative/positive
        if general_sentiment > 0.2:
            good_reviews.append(review)
        elif general_sentiment < -0.2:
            bad_reviews.append(review)
        elif result['pos'] > result['neg']:
            good_reviews.append(review)
        else:
            bad_reviews.append(review)

    # return as a tuple
    return good_reviews, bad_reviews

