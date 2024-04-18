from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean
# statistics.mean, put all the compounds of the reviews onto a list and then get the average of it

def get_compound(reviews):
    review_analysis = SentimentIntensityAnalyzer()
    compound_results = []

    for review in reviews:
        # .polarity_scores provides the sentiments of the reviews (ex: negative, positve, neutral, and compound)
        # compound score is the sum of all the ratings ranging from -1 (extremely negative) to 1 (extremely positive)
        sentiment_result = review_analysis.polarity_scores(review)
        compound_results.append(sentiment_result["compound"])
        print(review, "\n", "Rating:", sentiment_result["compound"])

    average_compound = mean(compound_results)
    print("Overall Average Rating:", average_compound)

reviews = ["tom is sooo funny","i love that movie!", "i hate that movie"]
get_compound(reviews)

