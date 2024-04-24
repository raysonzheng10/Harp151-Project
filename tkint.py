from PIL import ImageTk, Image

def get_scaled_image(path, width, height):
    original_image = Image.open(path)
    resized_image = original_image.resize((width, height))

    tk_photo = ImageTk.PhotoImage(resized_image)

    return tk_photo