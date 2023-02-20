import os
import time
import logging
import sqlite3
import datetime
from threading import Thread

from tqdm import tqdm
from dotenv import load_dotenv

import enums

""" Logging """
load_dotenv()
logger = logging.getLogger(__name__)
handler = logging.FileHandler("kettle.log")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
fmt = logging.Formatter(FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(fmt)

"""Connection to Database"""

try:
    sqlite_connection = sqlite3.connect('test.db', check_same_thread=False)
    cursor = sqlite_connection.cursor()
    sqlite_select_query = "select sqlite_version();"
    sqlite_insert_query = '''INSERT INTO logging (text, created_at)  VALUES  ('{}','{}')'''
    sqlite_connection.commit()
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
except sqlite3.Error as error:
    print("SQLite connection error", error)


class BoilingThread(Thread):
    sqlite_connection.commit()
    """
    Initialization threads to kettle object
    """

    def __init__(self, kettle):
        Thread.__init__(self)
        self.kettle = kettle

    def run(self):
        """
        Run thread for boiling kettle
        """
        progress = []
        for i in range(self.kettle.boil_time):
            progress += [i]
        self.kettle.state = enums.StateKettle.ON
        print(self.kettle.state)
        for i in tqdm(progress):
            if self.kettle.state is enums.StateKettle.OFF:
                logger.info("Boiling was unsuccessful.")
                cursor.execute(
                    sqlite_insert_query.format("Boiling was unsuccessful.", datetime.datetime.now().isoformat()))
                sqlite_connection.commit()
                break
            time.sleep(1)
        if self.kettle.state is enums.StateKettle.ON:
            logger.info("Kettle boiled successfully.")
            cursor.execute(
                sqlite_insert_query.format("Kettle boiled successfully.", datetime.datetime.now().isoformat()))
            sqlite_connection.commit()
            self.kettle.state = enums.StateKettle.OFF
            print(self.kettle.state)
            self.kettle.water_state = enums.StateKettleWater.HOT


class Kettle:
    def __init__(self):
        self.water_count = 0
        self.boil_time = int(os.getenv("BOIL_TIME"))
        print(self.boil_time)
        self.state = enums.StateKettle.OFF
        self.water_state = enums.StateKettleWater.COLD
        self.boil_temperature = int(os.getenv("BOIL_TEMPERATURE"))
        self.thread = None

    def boil(self):
        self.thread = BoilingThread(self)
        self.thread.start()

    def fill_water(self):
        max_water = float(os.getenv("WATER_COUNT"))
        count_water_to_fill = float(input("How much water you want to fill? \n"))
        self.water_count = count_water_to_fill
        if count_water_to_fill > max_water:
            print("You spilled the water but the amount of water in the kettle")
            self.water_count = max_water
        elif self.water_count == max_water:
            print("Count of water in Kettle riches maximum")
            sqlite_connection.cursor()
            cursor.execute(sqlite_insert_query.format("Count of water in Kettle riches maximum.",
                                                      datetime.datetime.now().isoformat()))
            sqlite_connection.commit()
            sqlite_connection.cursor()
        elif count_water_to_fill <= 0.0:
            logger.info("You didn't fill the water")
            sqlite_connection.cursor()
            cursor.execute(sqlite_insert_query.format("You did not fill the water.",
                                                      datetime.datetime.now().isoformat()))

            sqlite_connection.commit()
            sqlite_connection.cursor()
            return self.water_count

    def get_water_count(self):
        print(self.water_count)

    def get_kettle_state(self):
        print(self.state)

    def get_kettle_water_state(self):
        print(self.water_state)

    def turn_off(self):
        self.state = enums.StateKettle.OFF
        self.thread.join()

    def set_max_temp_boiling(self):
        count_max_temp = int(input("Which max temp do you want to install? (Max 100 C) \n"))
        self.boil_temperature = count_max_temp
        if count_max_temp > 100:
            print("You trying to set over maximum temperature. Water temp will be set to 100 C")
            self.boil_temperature = 100
        elif count_max_temp < 0:
            print("You trying to set over minimum temperature. Water temp will be set to 1 C")
            self.boil_temperature = 1
        else:
            print("Temperature installed")
            print(self.boil_temperature)

    def exit(self):
        exit()



if __name__ == '__main__':
    kettle_object = Kettle()
    while True:
        print("Choose func: \n 1: Boil \n 2: Pour the water\n 3: Get information about count of water in kettle\n "
              "4: Get state of kettle \n 5: Get state of kettle water \n 6: Turn off kettle \n 7: Set maximum "
              "temperature \n 0: Exit")
        print(kettle_object.state.name)
        choice = input("Choice - ")
        if choice == enums.Choices.BOIL.value:
            kettle_object.boil()
        if choice == enums.Choices.FILL_WATER.value:
            kettle_object.fill_water()
        if choice == enums.Choices.GET_WATER_COUNT.value:
            kettle_object.get_water_count()
        if choice == enums.Choices.GET_KETTLE_STATE.value:
            kettle_object.get_kettle_state()
        if choice == enums.Choices.GET_KETTLE_WATER_STATE.value:
            kettle_object.get_kettle_water_state()
        if choice == enums.Choices.TURN_OFF_KETTLE_BOILING.value:
            kettle_object.turn_off()
        if choice == enums.Choices.SET_MAXIMUM_TEMP_BOILING.value:
            kettle_object.set_max_temp_boiling()
        if choice == enums.Choices.EXIT.value:
            kettle_object.exit()
