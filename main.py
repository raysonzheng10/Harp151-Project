from Scrapers.TMDB_API import CreatedTMDBAPI
# from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from Scrapers.youtubeAPI import CreatedYoutubeAPI
from VaderSentiment import get_compound
from tkinter import *
from tkint_helper import *

# this function will run when the user presses the search button
def mainProcess(movie_title):
    # first we try to extract all relevant info using TMDB API
    movie_info = CreatedTMDBAPI.get_movie_info(movie_title)

    # movie_info is false if we failed
    if not movie_info:
        print("Movie Title is not recognized. Please Try Again.")
        return
    
    # grab the title from the API call and use that title for the rest of the calls
    title = movie_info['title']
    # get the video id for the youtube trailer
    video_id = CreatedTMDBAPI.get_YoutubeTrailer_id(title)

    # grab reviews from various platforms
    tmdb_reviews = CreatedTMDBAPI.get_reviews(title)
    youtube_reviews = CreatedYoutubeAPI.get_top_comments(video_id) #use video id instead of title

    print(tmdb_reviews[0])
    print(youtube_reviews[0])



# Create Root
root = Tk()
root.geometry("1000x750")
root.title("Movie Review Compiler")

# header frame
header_frame = Frame(root, bg = primary, height = 10)
header_frame.grid(row = 0, column = 0, sticky = "ew")


header_label = Label(header_frame, text = "Movie Review Compiler", font = (font, 15, "bold"), bg = primary, fg = white)
header_label.grid(row = 0, column = 0, padx = 12, sticky = "ew")

# search bar
movie_name = StringVar()

def get_movie(movie):
    print(movie)
    movie_name.set("")

movie_name_entry = Entry(header_frame, textvariable = movie_name, font = (font, 15), bg = white, fg = primary, justify = LEFT, borderwidth = 5, relief = FLAT)
movie_name_entry.grid(row = 0, column = 1, sticky = "e", padx = (450, 10), pady = 10)

# search icon
search_icon_size = 30
tk_search_icon = get_scaled_image(r'images\search_btn.png', search_icon_size, search_icon_size)
get_movie_btn = Button(header_frame, command = lambda: get_movie(movie_name.get()), width = search_icon_size, height=search_icon_size, bg = secondary, image = tk_search_icon)
get_movie_btn.grid(row = 0, column = 2, padx = 15)

# # Create Main_frame
# main_frame = Frame(root)
# main_frame.place(x=400, y=400, anchor=CENTER)

# # Create subframes from main
# top_frame = Frame(main_frame)
# body_frame = Frame(main_frame)
# top_frame.grid(row=0, column=1)
# body_frame.grid(row=1, column=1)

# # top_frame elements
# # note the poster.png is always 2:3 ratio (width : height)
# poster = Canvas(top_frame, width = 200, height = 300 , background='white')
# poster.grid(row=0,column=0)

# title = Label(top_frame, text="", pady=10)
# title.grid(row=0, column=1)

# movie_label = Label(top_frame, text="Enter a Movie Title", pady = 10)
# movie_label.grid(row=1,column=0)

# # creates a string variable
# movie_title = StringVar()
# movie_title.set("")
# movie_input = Entry(top_frame, width=35, borderwidth=5, textvariable=movie_title)
# movie_input.grid(row=1,column=1)

# button = Button(top_frame, text = "Get Reviews", command = lambda: mainProcess(movie_title.get()))
# button.grid(row=2,column=0)


# # creates 2 text boxes in bottom frame
# tomato_text = Text(body_frame, width = 45, height = 25, padx = 5, borderwidth = 5)
# tomato_text.grid(row = 1, column = 0)
# tomato_rating = Label(body_frame, text="Vader Rating: ", pady=10)
# tomato_rating.grid(row = 2, column = 0)

# tmdb_text = Text(body_frame, width = 45, height = 25, padx = 5, borderwidth = 5)
# tmdb_text.grid(row = 1, column = 2)
# tmdb_rating = Label(body_frame, text="Vader Rating: ", pady=10)
# tmdb_rating.grid(row = 2, column = 2)



root.mainloop()