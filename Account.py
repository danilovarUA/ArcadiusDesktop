from Requester import Requester
from Modules import TestModule
from Scheduler.Task import Task
import threading
from datetime import datetime
import time
from Constants import ACCOUNT_THREAD_IDLE_TICK, INACTIVE_THREAD_CHECK_TICK
RELATIONSHIP_NUM_TO_WORD = {"-1": "red", "1": "blue", "2": "green", "3": "orange"}


class Account(threading.Thread):
    def __init__(self, dictionary, logger, perm_dict):
        # name, server_id, server_name
        threading.Thread.__init__(self)
        self.email = dictionary["email"]
        self.password = dictionary["password"]
        self.server = {"id": dictionary["server_id"],
                       "status": None,
                       "name": dictionary["server_name"],
                       "last_login": None,
                       "urls": {"region": None, "map": None, "main": None}}

        self.data = {"player": {},
                     "player_rank": {},
                     "alliance": {},
                     "habitat": {},
                     "habitat_unit": [],
                     "report": {},
                     "transit": [],
                     "diplomacy": {"red": [], "green": [], "blue": [], "orange": []}}
        self.player_id = None
        self.player_data = {"name": dictionary["name"]}  # That is a copy of player with id == player_id for fast access

        self.requester = Requester(self)
        self.tasks = []
        self.scheduled_tasks = {}
        self.active = True
        self.last_time_idle = False

        self.logger = logger
        self.perm_dict = perm_dict

        self.add_startup_tasks()

    def perform_task(self):
        if len(self.tasks) > 0:
            task = self.tasks.pop(0)
            return task.run()

    def add_task(self, task_time, func, description):
        self.tasks.append(Task(task_time, func, description, self))

    def add_startup_tasks(self):
        self.add_task(None, TestModule.run, "some test task")
        # TODO: rewrite so that all run() functions in files in Modules folder are ran here

    def tick(self):
        # Add scheduled tasks to queue
        for scheduled_task_time in self.scheduled_tasks:
            if scheduled_task_time <= datetime.now():
                self.tasks += self.scheduled_tasks[scheduled_task_time]
                del self.scheduled_tasks[scheduled_task_time]

        new_tasks = self.perform_task()

        # Add tasks created by performed task
        if new_tasks is not None:
            self.tasks += new_tasks["regular_tasks"]
            for tasks_time in new_tasks["scheduled_tasks"]:
                tasks = new_tasks["scheduled_tasks"][tasks_time]
                if tasks_time in self.scheduled_tasks:
                    self.scheduled_tasks[tasks_time] += tasks
                else:
                    self.scheduled_tasks[tasks_time] = [tasks]
            self.idle = False
        else:
            self.idle = True

    def run(self):
        while True:
            if self.active:
                self.tick()
                if self.last_time_idle:
                    time.sleep(ACCOUNT_THREAD_IDLE_TICK)
            else:
                time.sleep(INACTIVE_THREAD_CHECK_TICK)

    def update_data(self, dict_to_parse):
        try:
            for world in dict_to_parse["loginConnectedWorlds"]:
                if world["id"].decode('ascii') == self.server["id"]:
                    self.server["last_login"] = world["lastLoginDate"]
                    self.server["status"] = world["worldStatus"]["description"].decode("ascii")
                    break
        except KeyError:
            pass
        for world in dict_to_parse["allAvailableWorlds"]:
            if world["id"].decode('ascii') == self.server["id"]:  # TODO: remove ascii decoding once all data is decoded
                self.server["name"] = world["name"]
                try:
                    self.server["url"]["region"] = world["regionDataURL"]
                except KeyError:
                    pass
                self.server["url"]["map"] = world["mapURL"]
                self.server["url"]["main"] = world["url"].decode('ascii')
                break

        # TODO: think about making a list of fields that will be saved here
        if "Data" not in dict_to_parse:
            return
        dict_to_parse = dict_to_parse["Data"]
        # Player from Rating
        try:
            for item in dict_to_parse["playerRanks"]:
                self.data["player_rank"][item["id"]] = item
        except KeyError:
            pass

        # Player
        try:
            for item in dict_to_parse["Player"]:
                self.data["player"][item["id"]] = item
        except KeyError:
            pass

        # Alliance
        try:
            for item in dict_to_parse["Alliance"]:
                self.data["alliance"][item["id"]] = item
        except KeyError:
            pass

        # Habitat
        try:
            for item in dict_to_parse["Habitat"]:
                self.data["habitat"][item["id"]] = item
        except KeyError:
            pass

        # Diplomacy
        try:
            for diplomacy_item in dict_to_parse["Data"]["Diplomacy"]:
                _, target_alliance_id = diplomacy_item['id'].split('-')
                relationship_kind = RELATIONSHIP_NUM_TO_WORD[diplomacy_item["relationship"]]
                self.data["diplomacy"][relationship_kind].append(target_alliance_id)
        except KeyError:
            pass

        # HabitatUnit
        try:
            if "HabitatUnit" in dict_to_parse["Data"]:
                self.data["habitat_unit"] = []  # TODO do I really need to reset previous info here? breaks whole point of Data class
            for item in dict_to_parse["Data"]["HabitatUnit"]:
                self.data["habitat_unit"].append(item)
        except KeyError:
            pass

        # Transit
        try:
            if "Transit" in dict_to_parse["Data"]:
                self.data["transit"] = []  # TODO do I really need to reset previous info here? breaks whole point of Data class
            for item in dict_to_parse["Data"]["Transit"]:
                self.data["transit"].append(item)
        except KeyError:
            pass

        try:
            for item in dict_to_parse["Data"]["Report"]:
                self.data["report"][item["id"]] = item
        except KeyError:
            pass
