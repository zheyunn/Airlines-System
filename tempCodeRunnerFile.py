# Function to open the image selection dialog
def select_image():
    global image_path
    image_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select an image",
        filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("all files", "*.*"))
    )
    image_label.config(text=image_path)