from PIL import ImageTk, Image
import html

# function that returns a ImageTk.PhotoImage object that is scaled
def get_scaled_image(path, width, height):
    # open the image and run the resize function
    original_image = Image.open(path)
    resized_image = original_image.resize((width, height))

    tk_photo = ImageTk.PhotoImage(resized_image)
    return tk_photo

# format the genre text 
def get_genre_text(genres):
    genre_text = ""
    # loop through each genre and add it to the end of the string
    for genre in genres:
        genre_text += f" {genre} |"

    # remove the space at the beginning and the '|' at the end
    genre_text = genre_text[1:-1]
    return genre_text

def shorten_reviews(reviews, character_length = 500):
    shortened_reviews = []

    for review in reviews:
        revised_review = ""

        # this process gets rid of any line breaks and makes one big review
        split_lines = review.splitlines()
        for line in split_lines:
            revised_review += line + " "


        if len(revised_review) > character_length:
            revised_review = revised_review[:character_length] + '...'

        shortened_reviews.append(revised_review)
    
    return shortened_reviews

def decode_reviews(reviews):
    decoded_reviews = []
    removal_characters = ['<br>', '</br>', '<b>', '</b>']

    for review in reviews:
        decoded_review = html.unescape(review)

        for character in removal_characters:
            decoded_review = decoded_review.replace(character, "")

        decoded_reviews.append(decoded_review)

    return decoded_reviews

def process_reviews(reviews):
    short_reviews = shorten_reviews(reviews)
    decoded_reviews = decode_reviews(short_reviews)

    return decoded_reviews


# these are the colors/variables we use in main.py
white = "#eff0f0"
primary = "#15244B"
secondary = "#0088ca"
font = "Helvetica"

platform_selections = ["Rotten Tomatoes",
                       "Youtube",
                       "Google Reviews",
                       "TMDB"]