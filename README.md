## Installation

> ⚠️ Installtion only works for ubuntu and java 11

1. Install QGroundControl: https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html

2. Run `git clone https://github.com/PX4/PX4-Autopilot.git`

3. In a terminal run QGroundControl

4. Run `./PX4-Autopilot/Tools/setup/ubuntu.sh`

5. In a terminal
    * go to PX4-Autopilot folder
    * run this for init the simulation at ISITC location: 
        `export PX4_HOME_LON=-1.638537
        export PX4_HOME_LAT=48.115008`

6. Run `make px4_sitl jmavsim` (only work with java 11)

7. Run supabase_handler.py in BACK-DRONE
