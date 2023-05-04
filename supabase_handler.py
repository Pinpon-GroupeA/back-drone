import asyncio
import json
from supabase import create_client, Client
import time
from mavsdk import System
from drone_actions import get_battery, get_postion, return_to_home, goto_coordonnates_close, go_to_coordinates_open


url: str = "http://localhost:8000"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICAgInJvbGUiOiAiYW5vbiIsCiAgICAiaXNzIjogInN1cGFiYXNlIiwKICAgICJpYXQiOiAxNjgzMDY0ODAwLAogICAgImV4cCI6IDE4NDA5MTc2MDAKfQ.DmHNWaOzGrlmi5gDellrcCFP1fi2c_1RpY9HzaXcbNI"

supabase: Client = create_client(url, key)


# supabase.table('drone').select('id, typeTrajet , trajet->coordinates{longitude,altitude,longitude}, stop').execute()

curent_id = -111
stop_drone = False

drone = System()


async def run_drone():
    global stop_drone
    response = json.loads(supabase.table(
        'drone_data').select('is_stopped').execute().json())
    stop_drone = response['data'][0]['is_stopped']
    print(stop_drone)
    while float(await get_battery(drone)) > 0.1 and not stop_drone:
        response = json.loads(supabase.table('drone_data').select(
            'id', 'traject_type', 'is_stopped', 'traject').execute().json())
        data = response['data'][0]
        print(data)
        id = data['id']
        global curent_id
        global typeTrajet
        global coordinates
        if id != curent_id:
            curent_id = id
            typeTrajet = data['traject_type']
            coordinates = data['traject']
        stop_drone = data['is_stopped']
        if typeTrajet == 'CLOSED_CIRCUIT':
            await goto_coordonnates_close(drone, coordinates)
        else:
            await go_to_coordinates_open(drone, coordinates)
    await return_to_home(drone)


if __name__ == '__main__':
    asyncio.run(run_drone())
