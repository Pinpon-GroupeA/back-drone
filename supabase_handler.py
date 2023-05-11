import asyncio
import json
from supabase import create_client, Client
from mavsdk import System
from drone_actions import get_battery, get_postion, return_to_home, goto_coordonnates_close, go_to_coordinates_open
import os
from dotenv import load_dotenv


load_dotenv()

supabase_url: str = os.environ.get('SUPABASE_URL')
supabase_key: str = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)


current_id = -111
stop_drone = False

drone_table = 'drone_data'
traject_type = 'traject_type'
traject = 'traject'
is_stopped = 'is_stopped'

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
    while float(await get_battery(drone)) > 0.1 and not stop_drone:
        response = json.loads(supabase.table(drone_table).select(
            'id', traject_type, is_stopped, traject).execute().json())
        data = response['data'][0]
        id = data['id']
        global current_id
        global typeTrajet
        global coordinates
        if id != current_id:
            current_id = id
            typeTrajet = data['traject_type']
            coordinates = data['traject']
        stop_drone = data['is_stopped']
        if typeTrajet == 'CLOSED_CIRCUIT':
            await goto_coordonnates_close(drone, coordinates)
        else:
            await go_to_coordinates_open(drone, coordinates)
        await update_position(current_id)
    await return_to_home(drone)


async def save_photo(file):
    """Save in the supabase bucket named images, we fill the name of the subsequent folders in the path of the image"""
    # file = "assets/deusvult.png"
    with open(file, "rb") as f:
        supabase.storage().from_("images").upload(
            "interventions/123456/bite.png", f)


async def save_video(filePosition):
    """Delete the file at the path filePosition in the supabase bucket named images  and replace it with the new file.
    We fill the name of the subsequent folders in the path of the image"""
    file = "assets/deusvult.png"
    with open(file, "rb") as file:
        supabase.storage().from_("images").remove(filePosition)
        supabase.storage().from_("images").upload(filePosition, file)


async def update_position(current_id):
    """
    Updates the position of the drone in the database.
    """
    position = await get_postion(drone)
    latitude = float(position.latitude_deg)
    longitude = float(position.longitude_deg)
    data, count = supabase.table('drone_data').update({'position': {
        'latitude': latitude, 'longitude': longitude}}).eq('id', current_id).execute()


if __name__ == '__main__':
    asyncio.run(save_photo())
