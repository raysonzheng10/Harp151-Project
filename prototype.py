from Scrapers.youtubeAPI import CreatedYoutubeAPI
from Scrapers.TMDB_API import CreatedTMDBAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from VaderSentiment import get_compound
from tkinter import *


# rotten tomatoes and youtube

def get_tomatoes_reviews(movie_title):
    tomato_text.delete('1.0', 'end')
    tomatoes_reviews = CreatedRottenTomatoesScraper.get_critic_reviews(movie_title)
    print("Rotten Tomato Reviews")

    for review in tomatoes_reviews:
        text = f"{review} \n\n"
        tomato_text.insert(END, text)
        tomato_text.tag_config("tag_name", justify = "center")
        tomato_text.tag_add("tag_name", "1.0", "end")

    return tomatoes_reviews

def get_tmdb_reviews(movie_title):
    tmdb_text.delete('1.0','end')
    tmdb_reviews = CreatedTMDBAPI.get_reviews(movie_title)

    for review in tmdb_reviews:
        text = f"{review} \n\n"
        tmdb_text.insert(END, text)
        tmdb_text.tag_config("tag_name", justify = "center")
        tmdb_text.tag_add("tag_name", "1.0", "end")
    return tmdb_reviews

def get_reviews(movie_title):
    tmdb_reviews = get_tmdb_reviews(movie_title)
    tomatoes_reviews = get_tomatoes_reviews(movie_title)

    tmdb_score = get_compound(tmdb_reviews)
    tomatoes_score = get_compound(tomatoes_reviews)

    tmdb_rating.config(text=f"TMDB Score: {tmdb_score}")
    tomato_rating.config(text=f"tomato Score: {tomatoes_score}")



root = Tk()
root.geometry("750x750")
root.geometry("800x800")
root.title("Movie Review")

# creates a string variable
movie_title = StringVar()
movie_title.set("")


top_frame = Frame(root)
body_frame = Frame(root)

top_frame.grid(row=0, column=0)
body_frame.grid(row=1,column=0)

title_label = Label(top_frame, text='Search for a movie')
title_label.grid(row=0, column=0)
movie_input = Entry(top_frame, width=35, borderwidth=5, textvariable=movie_title)
movie_input.grid(row = 1, column=0)
button = Button(top_frame, text = "Get Reviews", command = lambda: get_reviews(movie_title.get()))
button.grid(row=2,column=0)




# creates 2 text boxes in bottom frame
tomato_text = Text(body_frame, width = 45, height = 25, padx = 5, borderwidth = 5)
tomato_text.grid(row = 1, column = 0)
tomato_rating = Label(body_frame, text="Vader Rating: ", pady=10)
tomato_rating.grid(row = 2, column = 0)

tmdb_text = Text(body_frame, width = 45, height = 25, padx = 5, borderwidth = 5)
tmdb_text.grid(row = 1, column = 2)
tmdb_rating = Label(body_frame, text="Vader Rating: ", pady=10)
tmdb_rating.grid(row = 2, column = 2)

root.mainloop()
