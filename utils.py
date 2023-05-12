import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from math import isclose


async def get_image(name, longitude, latitude, zoom, token):
    """
    Get an image from mapbox and save it in the assets folder.
    """
    response = requests.get(
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom}/1100x600?access_token={token}")
    image = Image.open(BytesIO(response.content))
    date = datetime.now()
    date = date.strftime("%d-%m-%Y_%H-%M-%S")
    image.save(f"assets/{name}", "png")


def is_in_coordinates(current_latitude, current_longitude, coordinates):
    """
    Check if the drone is in the coordinates.
    """
    for coordinate in coordinates:
        print("checking if in coordinates")
        lat = round(coordinate['latitude'], 6)
        long = round(coordinate['longitude'], 6)
        if isclose(long, round(current_longitude, 6), abs_tol=0.0002) and isclose(lat, float(current_latitude), abs_tol=0.0002):
            print("is in coordinates")
            return (True, lat, long)
    return (False, 0, 0)


def get_date():
    """
    Returns the current date in the format dd-mm-yyyy_hh-mm-ss.
    """
    date = datetime.now()
    date = date.strftime("%d-%m-%Y_%H-%M-%S")
    return date
