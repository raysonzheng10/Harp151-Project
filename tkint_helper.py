from PIL import ImageTk, Image

# function that returns a ImageTk.PhotoImage object that is scaled
def get_scaled_image(path, width, height):
    # open the image and run the resize function
    original_image = Image.open(path)
    resized_image = original_image.resize((width, height))

    tk_photo = ImageTk.PhotoImage(resized_image)
    return tk_photo

# these are the colors/variables we use in main.py
white = "#eff0f0"
primary = "#15244B"
secondary = "#0088ca"
font = "Helvetica"

