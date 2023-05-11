import requests
from PIL import Image
from io import BytesIO


def get_image(name, longitude, latitude, zoom, token):
    print(token)
    response = requests.get(
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom}/1100x600?access_token={token}")
    print(response.status_code)
    image = Image.open(BytesIO(response.content))
    image.save(name, "png")
