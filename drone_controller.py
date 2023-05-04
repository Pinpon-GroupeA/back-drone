from quart import Quart, request
from mavsdk import System
import asyncio
from drone_actions import goto_coordinates, return_to_home, goto_coordonnates_close, go_to_coordinates_open
app = Quart(__name__)
drone = System()


@app.post('/goto')
async def goto():
    coordinates = await request.get_json()  # parse arguments to dictionary
    await goto_coordinates(drone, coordinates)
    return {"coordinates": coordinates}, 200


@app.post('/closedCircuit')
async def closedCircuit():
    coordinates = await request.get_json()
    await goto_coordonnates_close(drone, coordinates)
    return {"coordinates": coordinates}, 200


@app.post('/openCircuit')
async def openCircuit():
    coordinates = await request.get_json()
    await go_to_coordinates_open(drone, coordinates)
    return {"coordinates": coordinates}, 200


@app.post('/stop')
async def stopAndGoHome():
    await return_to_home(drone)
    return {"coordinates": "home"}, 200


if __name__ == '__main__':
    print("main here")
    asyncio.run(app.run())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
