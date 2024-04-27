from Scrapers.TMDB_API import CreatedTMDBAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from VaderSentiment import get_compound
from tkinter import *
from tkint import get_scaled_image
from PIL import Image, ImageTk


# rotten tomatoes and youtube

# def get_tomatoes_reviews(movie_title):
#     tomato_text.delete('1.0', 'end')
#     tomatoes_reviews = CreatedRottenTomatoesScraper.get_topCritic_reviews(movie_title)

#     for review in tomatoes_reviews:
#         text = f"{review} \n\n"
#         tomato_text.insert(END, text)
#         tomato_text.tag_config("tag_name", justify = "center")
#         tomato_text.tag_add("tag_name", "1.0", "end")

#     return tomatoes_reviews

# def get_tmdb_reviews(movie_title):
#     tmdb_text.delete('1.0','end')
#     tmdb_reviews = CreatedTMDBAPI.get_reviews(movie_title)

#     for review in tmdb_reviews:
#         text = f"{review} \n\n"
#         tmdb_text.insert(END, text)
#         tmdb_text.tag_config("tag_name", justify = "center")
#         tmdb_text.tag_add("tag_name", "1.0", "end")

#     return tmdb_reviews

# def update_image():
#     tk_photo = get_scaled_image(path = r"poster.png", width = 200, height = 300)
#     poster.create_image(100, 150, image=tk_photo)
#     poster.image = tk_photo

# def update_movie_info(movie_info):
#     title.config(text=movie_info['title'])




#     print('finished updating')

# def mainProcess(movie_title):
#     tmdb_reviews = get_tmdb_reviews(movie_title)
#     tomatoes_reviews = get_tomatoes_reviews(movie_title)

#     tmdb_score = get_compound(tmdb_reviews)
#     tomatoes_score = get_compound(tomatoes_reviews)

#     tmdb_rating.config(text=f"TMDB Score: {tmdb_score}")
#     tomato_rating.config(text=f"tomato Score: {tomatoes_score}")
    
#     movie_info = CreatedTMDBAPI.get_movie_info(movie_title)
#     update_image()
#     update_movie_info(movie_info)



# Create Root
root = Tk()
root.geometry("1000x750")
root.title("Movie Review Compiler")

white = "#eff0f0"
primary = "#15244B"
secondary = "#0088ca"
font = "Helvetica"

# header frame
header = Frame(root, bg = primary, height = 10)
header.grid(row = 0, column = 0, sticky = "ew")

header_label = Label(header, text = "Movie Review Compiler", font = (font, 15, "bold"), bg = primary, fg = white)
header_label.grid(row = 0, column = 0, padx = 12, sticky = "ew")

# search bar
movie_name = StringVar()

def get_movie():
    movie = movie_name.get()

    print(movie)
    movie_name.set("")

movie_name_entry = Entry(header, textvariable = movie_name, font = (font, 15), bg = white, fg = primary, justify = LEFT, borderwidth = 5, relief = FLAT)
movie_name_entry.grid(row = 0, column = 1, sticky = "e", padx = (450, 10), pady = 10)

# search icon
search_icon_size = 30
tk_search_icon = get_scaled_image(r'search_btn.png', search_icon_size, search_icon_size)
get_movie_btn = Button(header, command = get_movie, width = search_icon_size, height=search_icon_size, bg = secondary, image = tk_search_icon)
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