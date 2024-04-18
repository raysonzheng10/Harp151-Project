from Scrapers.youtubeAPI import CreatedYoutubeAPI
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from tkinter import *

def get_tomatoes_reviews(movie_title):
    tomatoes_reviews = CreatedRottenTomatoesScraper.get_topCritic_reviews(movie_title)

    print(tomatoes_reviews)


root = Tk()
root.geometry("750x750")

movie_title = StringVar()
movie_title.set("")

welcome_label = Label(root, text="Enter Movie Title").pack()
movie_input = Entry(root, width=35, borderwidth=5, textvariable=movie_title).pack()




root.mainloop()