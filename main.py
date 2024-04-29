from Scrapers.TMDB_API import CreatedTMDBAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from Scrapers.youtubeAPI import CreatedYoutubeAPI
from Scrapers.googleReviews import CreatedGoogleReviews
from VaderSentiment import *
from tkinter import *
from tkint_helper import *

# function that updates the image in the poster
def update_poster():
    tk_poster = get_scaled_image(path = r"images\poster.png", width = 200, height = 300)
    poster.create_image(100, 150, image = tk_poster)
    poster.image = tk_poster

# function that updates all the movie information
def update_MI_frame(movie_info):
    # update image for poster
    update_poster()

    # grab information from the dict
    title = movie_info['title']
    release_date = movie_info['release_date']
    overview = movie_info['overview']
    genres = movie_info['genres']
    genre_text = get_genre_text(genres)

    # update the respective labels
    title_label.config(text = f'{title} ({release_date})')
    genres_label.config(text = genre_text)
    description_label.config(text = f'{overview}')

# function that grabs reviews according to the platform on the dropdown menu
# displays reviews in the text box
def process_platformSelection(platform):
    print(f"Grabbing reviews on {platform} for {title}....")
    # clear all review text
    review_text.delete('1.0', 'end')

    # this is basically a bunch of if statements, check which platform we are using
    match platform:
        case "Rotten Tomatoes":
            reviews = CreatedRottenTomatoesScraper.get_critic_reviews(title)
        case "Youtube": 
            # for youtube, we have to grab the yt trailer id first
            video_id = CreatedTMDBAPI.get_YoutubeTrailer_id(title)
            reviews = CreatedYoutubeAPI.get_top_comments(video_id)
        case "Google Reviews":
            reviews = CreatedGoogleReviews.get_google_reviews(title)
        case "TMDB":
            reviews = CreatedTMDBAPI.get_reviews(title)
        case _:
            review_text.insert(END, "Please select a platform using the dropdown menu.")
            return
    
    # if reviews is empty, we weren't able to successfully grab any, so we exit and show error
    if len(reviews) == 0:
        review_text.insert(END, f"No reviews found on {platform}.")
        return
    
    # use vader sentiment to sort reviews into good/bad
    sorted_reviews = separate_good_bad(reviews)
    good_reviews = sorted_reviews[0]
    bad_reviews = sorted_reviews[1]

    for review in bad_reviews:
        text = f"{review} \n\n"
        review_text.insert(END, text)
        review_text.tag_config("tag_name", justify = "center")
        review_text.tag_add("tag_name", "1.0", "end")
    
    print(f"Successfully grabbed reviews on {platform} for {title}! \n")

# this function will run when the user presses the search button
def mainProcess(movie_title):
    # first we try to extract all relevant info using TMDB API
    movie_info = CreatedTMDBAPI.get_movie_info(movie_title)

    # movie_info is false if we failed, let user know of this as well
    if not movie_info:
        search_error_label.config(text = "Movie Title is not recognized. Please Try Again.")
        return
    search_error_label.config(text = "") # if it was good, reset the label to be nothing

    # use that information to update the tkinter window
    update_MI_frame(movie_info)
    
    global title
    title = movie_info['title']
    movie_name.set("")

    process_platformSelection(platform_selector.get())



# Create Root
root = Tk()
root.geometry("1000x750")
root.title("Movie Review Compiler")

# <------------------------------------------------- HEADER FRAME ------------------------------------------------->
# header frame
header_frame = Frame(root, bg = primary, height = 10)
header_frame.grid(row = 0, column = 0, sticky = "ew")


header_label = Label(header_frame, text = "Movie Review Compiler", font = (font, 15, "bold"), bg = primary, fg = white)
header_label.grid(row = 0, column = 0, padx = 12, sticky = "ew")

# search bar
movie_name = StringVar()
movie_name.set("")

movie_name_entry = Entry(header_frame, textvariable = movie_name, font = (font, 15), bg = white, fg = primary, justify = LEFT, borderwidth = 5, relief = FLAT)
movie_name_entry.grid(row = 0, column = 1, sticky = "e", padx = (450, 10), pady = 10)

# search icon
search_icon_size = 30
tk_search_icon = get_scaled_image(r'images\search_btn.png', search_icon_size, search_icon_size)
get_movie_btn = Button(header_frame, command = lambda: mainProcess(movie_name.get()), width = search_icon_size, height=search_icon_size, bg = secondary, image = tk_search_icon)
get_movie_btn.grid(row = 0, column = 2, padx = 15)

# <------------------------------------------------- MOVIE INFORMATION FRAME ------------------------------------------------->
# movie info frame
movie_information_frame = Frame(root, bg = white, height = 200)
movie_information_frame.grid(row = 1, column = 0, sticky = "ew", pady=(10, 0))

# Separete into left and right sections
left_MI_frame = Frame(movie_information_frame)
left_MI_frame.grid(row = 0, column = 0)
right_MI_frame = Frame(movie_information_frame)
right_MI_frame.grid(row = 0, column = 1)

# poster image
poster = Canvas(left_MI_frame, width = 200, height = 300, background = white)
poster.pack()

# elements for right MI frame
search_error_label = Label(right_MI_frame, text="placeholder error", background= white, fg = 'Red')
search_error_label.pack()
title_label = Label(right_MI_frame, text="placeholder title", background= white)
title_label.pack()
genres_label = Label(right_MI_frame, text="placeholder genres", background= white)
genres_label.pack()
description_label = Label(right_MI_frame, text="placeholder description", background = white)
description_label.pack()


# <------------------------------------------------- REVIEWS FRAME ------------------------------------------------->
# reviews frame
reviews_frame = Frame(root, bg = primary, height = 400)
reviews_frame.grid(row = 2, column = 0, sticky = "ew", pady=(10, 0))

top_reviews_frame = Frame(reviews_frame, bg = white)
top_reviews_frame.grid(row = 0, column = 0)

platform_selector = StringVar()
platform_selector.set("Select a Platform")
platform_dropdown = OptionMenu(top_reviews_frame, platform_selector, *platform_selections, command = process_platformSelection)
platform_dropdown.pack()

rating_label = Label(top_reviews_frame, text = "Rating: placeholder rating")
rating_label.pack()

bot_reviews_frame = Frame(reviews_frame, bg = white)
bot_reviews_frame.grid(row = 1, column = 0)

review_text = Text(bot_reviews_frame, width = 100, height = 25, padx = 5, borderwidth = 5)
review_text.pack()



root.mainloop()