import requests
from PIL import Image
from io import BytesIO

HARPER_COLLINS_LOGO = r".\media\HarperCollins_logo_no_text.png"

def get_logo() -> Image:
    image = Image.open(HARPER_COLLINS_LOGO)
    return image

def merge_images(background: Image, foreground: Image, filepath: str) -> str:
    """
    Takes a background image and overlays a transparent foreground image.
    foreground is resized to fit the dimensions of the background image.
    """
    thumb_size = (background.size[0] // 4, background.size[1] // 4)

    # Resize foreground to fit
    foreground.thumbnail(thumb_size)
    fg_size = foreground.size

    fg_postion = (0, background.size[1] - fg_size[1]) ## bottom-left corner

    background.paste(foreground, fg_postion, foreground.convert("RGBA"))
    background.save(f"{filepath}.png", "PNG")

    return f"{filepath}.png"

def load_image_from_url(url: str) -> Image:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    return image