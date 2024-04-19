from Scrapers.TMDB_API import tmdb_API
from Scrapers.rottenTomatoes import CreatedRottenTomatoesScraper
from VaderSentiment import get_compound
from tkinter import *


# rotten tomatoes and youtube

def get_tomatoes_reviews(movie_title):
    tomato_text.delete('1.0', 'end')
    tomatoes_reviews = CreatedRottenTomatoesScraper.get_topCritic_reviews(movie_title)
    print("Rotten Tomato Reviews")

    for review in tomatoes_reviews:
        text = f"{review} \n\n"
        tomato_text.insert(END, text)
        tomato_text.tag_config("tag_name", justify = "center")
        tomato_text.tag_add("tag_name", "1.0", "end")

    return tomatoes_reviews

def get_tmdb_reviews(movie_title):
    tmdb_text.delete('1.0','end')
    tmdb_reviews = tmdb_API.get_reviews_from_title(movie_title)

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
root.geometry("800x800")
root.title("Movie Review")

# creates a string variable
movie_title = StringVar()
movie_title.set("")

# creates entry frame
entry_frame = Frame(root)
entry_frame.grid(row = 0, column = 0)

# elements in the entry frame
movie_label = Label(entry_frame, text="Enter a Movie Title", pady = 10).pack()
movie_input = Entry(entry_frame, width=35, borderwidth=5, textvariable=movie_title).pack()
button = Button(entry_frame, text = "Get Reviews", command = lambda: get_reviews(movie_title.get()))
button.pack(pady = 10)


# creates 2 text boxes in bottom frame
tomato_text = Text(root, width = 45, height = 25, padx = 5, borderwidth = 5)
tomato_text.grid(row = 1, column = 0)
tomato_rating = Label(root, text="Vader Rating: ", pady=10)
tomato_rating.grid(row = 2, column = 0)

tmdb_text = Text(root, width = 45, height = 25, padx = 5, borderwidth = 5)
tmdb_text.grid(row = 1, column = 2)
tmdb_rating = Label(root, text="Vader Rating: ", pady=10)
tmdb_rating.grid(row = 2, column = 2)



root.mainloop()