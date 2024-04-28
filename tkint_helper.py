from PIL import ImageTk, Image

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

# these are the colors/variables we use in main.py
white = "#eff0f0"
primary = "#15244B"
secondary = "#0088ca"
font = "Helvetica"

platform_selections = ["Rotten Tomatoes",
                       "Youtube",
                       "Google Reviews",
                       "TMDB"]