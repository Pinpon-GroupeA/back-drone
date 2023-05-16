import asyncio
import json
import time
from supabase import create_client, Client
from mavsdk import System
from drone_actions import get_battery, get_postion, return_to_home, goto_coordonnates_close, go_to_coordinates_open
import os
from dotenv import load_dotenv
from utils import get_image, is_in_coordinates, get_date


load_dotenv()
supabase_url: str = os.environ.get('SUPABASE_URL')
supabase_key: str = os.environ.get('SUPABASE_KEY')
mapbox_key: str = os.environ.get('MAPBOX_ACCESS_TOKEN')


supabase: Client = create_client(supabase_url, supabase_key)


current_intervention_id = -111
stop_drone = False

drone_table = 'drone_data'
traject_type = 'traject_type'
traject = 'traject'
is_stopped = 'is_stopped'
intervention_id = 'intervention_id'
coordinates = []

drone = System()


async def run_drone():
    """
    Runs the drone.
    """
    global stop_drone
    response = json.loads(supabase.table(
        'drone_data').select('is_stopped').execute().json())
    stop_drone = response['data'][0]['is_stopped']
    print(stop_drone)
    while float(await get_battery(drone)) > 0.1:
        response = json.loads(supabase.table(drone_table).select(
            'id', traject_type, is_stopped, traject, 'intervention_id').execute().json())
        data = response['data'][0]
        global current_intervention_id
        global typeTrajet
        global coordinates
        current_intervention_id = data[intervention_id]
        if data != None:
            typeTrajet = data['traject_type']
            coordinates = data['traject']
            stop_drone = data['is_stopped']
            if coordinates != [] and coordinates != None and not stop_drone:
                if typeTrajet == 'CLOSED_CIRCUIT':
                    await goto_coordonnates_close(drone, coordinates)
                else:
                    await go_to_coordinates_open(drone, coordinates)

            if stop_drone:
                await return_to_home(drone)
            await update_position(current_intervention_id)


async def save_photo(path_to_save, file):
    """Save in the supabase bucket named images, we fill the name of the subsequent folders in the path of the image"""
    global current_intervention_id
    with open(file, "rb") as f:
        supabase.storage().from_("photo").upload(
            path_to_save, f)


async def save_video(filePosition):
    """Delete the file at the path filePosition in the supabase bucket named images  and replace it with the new file.
    We fill the name of the subsequent folders in the path of the image"""
    file = "assets/video/photo.png"
    with open(file, "rb") as file:
        supabase.storage().from_("video").remove(filePosition)
        supabase.storage().from_("video").upload(filePosition, file)


async def update_position(current_intervention_id):
    """
    Updates the position of the drone in the database.
    """
    global coordinates
    position = await get_postion(drone)
    latitude = position.latitude_deg
    longitude = position.longitude_deg
    is_in, lat_to_send, long_to_send = is_in_coordinates(
        latitude, longitude, coordinates)
    if is_in:
        name = f"{get_date()}.png"
        await get_image(name, longitude=longitude, latitude=latitude, zoom=19, token=mapbox_key)
        path_to_save = f"intervention_{current_intervention_id}/{lat_to_send}_{long_to_send}/{name}"
        await save_photo(path_to_save, f"assets/{name}")

    data, count = supabase.table('drone_data').update({'position': {
        'latitude': latitude, 'longitude': longitude}}).eq(intervention_id, current_intervention_id).execute()

    name_vido = "photo.png"
    await get_image(f"video/{name_vido}", longitude=longitude, latitude=latitude, zoom=19, token=mapbox_key)
    await save_video(f"intervention_{current_intervention_id}/{name_vido}")
    time.sleep(1)


if __name__ == '__main__':
    asyncio.run(run_drone())
