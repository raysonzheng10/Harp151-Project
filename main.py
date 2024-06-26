from Scrapers.TMDB_API import CreatedTMDBAPI
from Scrapers.youtubeAPI import CreatedYoutubeAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from Scrapers.googleReviews import CreatedGoogleReviews
from VaderSentiment import *
from tkinter import *
from tkint_helper import *

# function that updates the image in the poster
def update_poster(poster_validity: bool) -> None:
    if poster_validity:
        tk_poster = get_scaled_image(path = r"images\poster.png", width = 170, height = 250)
    else:
        tk_poster = get_scaled_image(path = r"images\no_image_found.png", width = 170, height = 250)
    poster.create_image(85, 125, image = tk_poster)
    poster.image = tk_poster

# function that updates all the movie information
def update_MI_frame(movie_info: dict) -> None:
    poster_validity = movie_info['poster']
    # update image for poster
    update_poster(poster_validity)

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

# function to clear all text from the text widgets
def clear_text():
    good_review_text.delete('1.0', 'end')
    bad_review_text.delete('1.0', 'end')
    error_label.config(text = "")

# updates text boxes with reviews
def update_review_texts(good_reviews, bad_reviews):
    good_review_text.insert("1.0", "Positive Reviews\n", "bold_centered")
    bad_review_text.insert("1.0", "Negative Reviews\n", "bold_centered")

    if len(good_reviews) == 0:
        good_review_text.insert(END, "No good reviews found :(", 'review_text')
    else:
        for review in good_reviews:
            text = f"{review} \n\n"
            good_review_text.insert(END, text, 'review_text')

    if len(bad_reviews) == 0:
        bad_review_text.insert(END, "No bad reviews found :)", 'review_text')
    else:
        for review in bad_reviews:
            text = f"{review} \n\n"
            bad_review_text.insert(END, text, 'review_text')

# updates rating label
def update_rating(rating):
    rating_label.config(text=f'Rating: {rating}')

# grab reviews/rating for a specified platform
def get_reviews_ratings(platform):
    reviews = []
    rating = "N/A"

    # this is basically a bunch of if statements, check which platform we are using
    match platform:
        case "Rotten Tomatoes":
            reviews = CreatedRottenTomatoesScraper.get_critic_reviews(title)
            rating = CreatedRottenTomatoesScraper.get_review_score(title)
        case "Youtube": 
            # for youtube, we have to grab the yt trailer id first
            # we grab a list of video ids, scan through videos until we find one with comments
            video_ids = CreatedTMDBAPI.get_YoutubeTrailer_ids(title) 
            for id in video_ids:
                reviews = CreatedYoutubeAPI.get_top_comments(id)

                # try to grab rating, if unsuccessful, give default value
                try:
                    rating = CreatedYoutubeAPI.get_likes_views_ratio(id)[2] + " Likes to Views Percentage "
                except:
                    rating = 'N/A'
                    
                if len(reviews) == 0: # if this video failed, try next one
                    continue

        case "Google Reviews":
            reviews = CreatedGoogleReviews.get_google_reviews(title)
            rating = CreatedGoogleReviews.average_score
        case "TMDB":
            reviews = CreatedTMDBAPI.get_reviews(title)
            rating = str(CreatedTMDBAPI.get_average_rating(title)) + " out of 10"
        case _:
            error_label.config(text = "Invalid platform!")

    # more protection against nonetype errors
    if reviews == None:
        reviews = []
    if rating == None:
        rating = "N/A"
    
    return reviews, rating

# function that grabs reviews according to the platform on the dropdown menu
# displays reviews in the text box
def process_platformSelection(platform):
    # if the user hasn't selected a platform, give error message
    if platform == "Select a Platform":
        error_label.config(text = "Select a platform!")
        return
    
    # else, start grabbing reviews
    print(f"Grabbing reviews on {platform} for {title}....")
    # clear all review text
    clear_text()

    res = get_reviews_ratings(platform)
    reviews = res[0]
    rating = res[1]
    
    # update rating value
    update_rating(rating)

    # if reviews is empty, we weren't able to successfully grab any, so we exit and show error
    if len(reviews) == 0:
        error_label.config(text = f"No reviews found on {platform}.")
        print("Length of reviews is 0, aborting...")
        return
    
    # use vader sentiment to sort reviews into good/bad
    shortened_reviews = process_reviews(reviews)
    sorted_reviews = separate_good_bad(shortened_reviews)
    
    good_reviews = sorted_reviews[0]
    bad_reviews = sorted_reviews[1]

    # update all text widgets
    update_review_texts(good_reviews, bad_reviews)
    
    print(f"Successfully grabbed reviews on {platform} for {title}! \n")

# this function will run when the user presses the search button
def mainProcess(movie_title):
    # first we try to extract all relevant info using TMDB API
    movie_info = CreatedTMDBAPI.get_movie_info(movie_title)

    # movie_info is false if we failed, let user know of this as well
    if not movie_info:
        error_label.config(text = "Movie title is not recognized.")
        return False # return false if we failed
    error_label.config(text = "") # if it was good, reset the label to be nothing

    # use that information to update the tkinter window
    update_MI_frame(movie_info)
    
    global title
    title = movie_info['title']
    movie_name.set("")

    process_platformSelection(platform_selector.get())
    
    # return true if successful
    return True


# create Root
root = Tk()
root.geometry("1000x750")
root.title("Movie Review Compiler")

# <--------------------------------------------------------------- MAIN FRAME --------------------------------------------------------------->
main_frame = Frame(root, bg = white)
# main_frame.pack()
# don't pack it, we will reveal the main frame after

# <------------------------------------------------- HEADER FRAME ------------------------------------------------->
# header frame
header_frame = Frame(main_frame, bg = primary, height = 10)
header_frame.grid(row = 0, column = 0, sticky = "ew")

header_label = Label(header_frame, text = "Movie Review Compiler", font = (font, 15, "bold"), bg = primary, fg = white)
header_label.grid(row = 0, column = 0, padx = 12, sticky = "ew")

# search bar
movie_name = StringVar()
movie_name.set("")

movie_name_entry = Entry(header_frame, textvariable = movie_name, width = 30, font = (font, 15), bg = white, fg = primary, justify = LEFT, borderwidth = 5, relief = FLAT)
movie_name_entry.grid(row = 0, column = 1, sticky = "e", padx = (330, 10), pady = 10)

# search icon
search_icon_size = 30
tk_search_icon = get_scaled_image(r'images\search_btn.png', search_icon_size, search_icon_size)
get_movie_btn = Button(header_frame, command = lambda: mainProcess(movie_name.get()), width = search_icon_size, height=search_icon_size, bg = secondary, image = tk_search_icon)
get_movie_btn.grid(row = 0, column = 2, padx = 15)

# <------------------------------------------------- MOVIE INFORMATION FRAME ------------------------------------------------->
# movie info frame
movie_information_frame = Frame(main_frame, bg = white, height = 70)
movie_information_frame.grid(row = 1, column = 0, sticky = "ew", pady=(10, 0))

# separate into left and right sections
left_MI_frame = Frame(movie_information_frame)
left_MI_frame.grid(row = 0, column = 0)
right_MI_frame = Frame(movie_information_frame)
right_MI_frame.grid(row = 0, column = 1, padx = (5, 0))

# poster image
poster = Canvas(left_MI_frame, width = 170, height = 250, background = white)
poster.grid(row = 0, column = 0, padx = (10,0), sticky = "nw")

# elements for right MI frame
#  -------------------- top description frame --------------------
top_description_frame = Frame(right_MI_frame, bg = white, width = 770)
top_description_frame.pack_propagate(0)
top_description_frame.grid(row = 0, column = 0, pady = (15, 10))

# top left and top right 
# pack_propogate locks the size of the frame so stuff doesn't move around
description_TL_frame = Frame(top_description_frame, bg = white , width = 500, height = 50)
description_TL_frame.grid(row = 0, column = 0, padx = (0, 5))
description_TL_frame.pack_propagate(0)
description_TR_frame = Frame(top_description_frame, bg = white , width = 300, height = 50)
description_TR_frame.grid(row = 0, column = 1)
description_TR_frame.pack_propagate(0)

# elements for top left
title_label = Label(description_TL_frame, text="", background=white, font = (font, 13, "bold", "underline"), fg = primary)
title_label.pack(anchor='w')
genres_label = Label(description_TL_frame, text="", background=white, font = (font, 11), fg = primary)
genres_label.pack(anchor='w')
# elements for top right
error_label = Label(description_TR_frame, text="", background=white, fg='red', font = (font, 12, "bold"))
error_label.pack(anchor='e')

#  -------------------- bottom description frame --------------------
bottom_description_frame = Frame(right_MI_frame, bg = white, width = 770, height = 200)
bottom_description_frame.pack_propagate(0)
bottom_description_frame.grid(row = 1, column = 0,  sticky='nw')

description_label = Label(bottom_description_frame, text="", font = (font, 11), background=white, wraplength = 770, fg = primary, justify = "left", anchor = "w")
description_label.pack(anchor='w')

# <------------------------------------------------- REVIEWS FRAME ------------------------------------------------->
# reviews frame
reviews_frame = Frame(main_frame, bg = white, height = 400)
reviews_frame.grid(row = 2, column = 0, sticky = "ew", pady=(10, 0))

#  -------------------- top reviews frame --------------------
top_reviews_frame = Frame(reviews_frame, bg = white)
top_reviews_frame.grid(row = 0, column = 0, sticky = "ew", padx = (10,0), pady = (0, 10))

# top left and top right
reviews_TL_frame = Frame(top_reviews_frame, bg = white , width = 460, height = 30)
reviews_TL_frame.grid(row = 0, column = 0, padx = (0, 48))
reviews_TL_frame.pack_propagate(0)
reviews_TR_frame = Frame(top_reviews_frame, bg = white , width = 460, height = 30)
reviews_TR_frame.grid(row = 0, column = 1)
reviews_TR_frame.pack_propagate(0)

platform_selector = StringVar()
platform_selector.set("Select a Platform")
platform_dropdown = OptionMenu(reviews_TL_frame, platform_selector, *platform_selections, command = process_platformSelection)
platform_dropdown.config(bg = primary, fg = white, font = (font, 11))
platform_dropdown.pack(anchor='w')

rating_label = Label(reviews_TR_frame, text = "Rating: N/A", bg = primary, fg = white, font = (font, 11), borderwidth=5)
rating_label.pack(anchor='w')

#  -------------------- bottom reviews frame --------------------
bot_reviews_frame = Frame(reviews_frame, bg = white)
bot_reviews_frame.grid(row = 1, column = 0, padx = 10)


good_review_text = Text(bot_reviews_frame, width = 56, height = 21, padx = 5, borderwidth=3)
good_review_text.grid(row = 0, column= 0)
# configure tags
good_review_text.tag_configure("bold_centered", font=("Tahoma", 12, "bold"), justify="center")
good_review_text.tag_configure("review_text", font=("Tahoma", 10))


mid_review_frame = Frame(bot_reviews_frame, bg = white)
mid_review_frame.grid(row = 0, column = 1, padx = 20)

bad_review_text = Text(bot_reviews_frame, width = 56, height = 21, padx = 5, borderwidth=3)
bad_review_text.grid(row = 0, column= 2)
# configure tags
bad_review_text.tag_configure("bold_centered", font=("Tahoma", 12, "bold"), justify="center")
bad_review_text.tag_configure("review_text", font=("Tahoma", 10))

# <--------------------------------------------------------------- INITIAL FRAME --------------------------------------------------------------->
# this sequence forgets the initial search frame and places the main frame up
def load_main_frame():
    initial_frame.forget()
    main_frame.tkraise()

    main_frame.pack()

# this function runs when the user presses search on the intial page
def first_search(movie_title):
    # run main process
    result = mainProcess(movie_title)

    # result is false if mainProcess didn't work
    if not result:
        initial_error_label.config(text = "Movie title is not recognized")
        return
    
    # if mainProcess was successful, we load in the main frame
    load_main_frame()


initial_frame = Frame(root, bg = primary, width = 1000, height = 750)
initial_frame.pack_propagate(0)
initial_frame.pack()

# make three frames to separate our initial page
initial_header_frame = Frame(initial_frame, bg = primary, width = 1000, height = 200)
search_frame = Frame(initial_frame, bg = primary, width = 1000, height = 50)
author_frame = Frame(initial_frame, bg = primary, width = 1000, height = 50)

# grid them, they're just stacked on top of each other
initial_header_frame.grid(row = 0, column = 0, pady=(320,10), padx=(320,320))
search_frame.grid(row = 1, column = 0, pady=(0,10))
author_frame.grid(row = 2, column = 0, pady=(10, 250))


# ---------- initial header frame elements ----------
initial_header_label = Label(initial_header_frame, text = "Movie Review Compiler", font = (font, 25, "bold"), bg = primary, fg = secondary)
initial_subheader_label = Label(initial_header_frame, text = "Search for a movie", font = (font, 15, "bold"), bg = primary, fg = white)
initial_header_label.pack()
initial_subheader_label.pack()

# ---------- search frame elements ----------
initial_movie_name_entry = Entry(search_frame, textvariable = movie_name, width = 40, font = (font, 15), bg = white, fg = primary, justify = LEFT, borderwidth = 5, relief = FLAT)
initial_movie_name_entry.grid(row = 0, column = 0, sticky = "e", pady = 10)

initial_get_movie_btn = Button(search_frame, command = lambda: first_search(movie_name.get()), width = search_icon_size, height=search_icon_size, bg = secondary, image = tk_search_icon)
initial_get_movie_btn.grid(row = 0, column = 1, padx = (15,0))

# ---------- author frame elements ----------
author_label = Label(author_frame, text = "Made by Rayson, Trinity, and Jomin", font = (font, 15, "bold"), bg = primary, fg = white)
author_label.grid(row = 0, column = 0, pady = 10)

initial_error_label = Label(author_frame, text = "", font = (font, 13, "bold"), bg = primary, fg = "Red")
initial_error_label.grid(row = 1, column = 0)


root.mainloop()