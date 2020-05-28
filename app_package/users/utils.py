from flask import current_app

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8) # Create a random 8 digit hexadecial to use as the file name
#     f_name, f_ext = os.path.splitext(form_picture.filename) # This os function returns 2 parameters: the filename without extension, and the filename extension
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/images', picture_fn) # This creates the full file path to the image.

#     output_size = (125, 125) # x/y size of picture
#     i = Image.open(form_picture) # use the PIL library to open image object
#     i.thumbnail(output_size) # resize the image.
#     i.save(picture_path) # This saves the file to the newly created path.
#     return picture_fn # return the new hexadecial filename we created.