from datetime import datetime
from Scheduler.Task import Task
import threading
import time
from Constants import ACCOUNT_THREAD_IDLE_TICK
from Modules import TestModule


class AccountThread(threading.Thread):
    def __init__(self, account, logger, perm_dict):
        threading.Thread.__init__(self)
        self.account = account
        self.tasks = []
        self.scheduled_tasks = {}
        self.logger = logger
        self.perm_dict = perm_dict
        self.idle = False
        self.add_startup_tasks()
        self.running = True

    def perform_task(self):
        if len(self.tasks) > 0:
            task = self.tasks.pop(0)
            self.logger.add_log("performing task {}".format(task.description), "account thread task performer",
                                self.account)
            return task.run()

    def tick(self):
        # Add scheduled tasks to queue
        for scheduled_task_time in self.scheduled_tasks:
            if scheduled_task_time == datetime.now():
                self.tasks += self.scheduled_tasks[scheduled_task_time]
                del self.scheduled_tasks[scheduled_task_time]
                # TODO: check if that removes tasks from memory completely

        new_tasks = self.perform_task()

        # Add tasks created by performed task
        if new_tasks is not None:
            self.tasks += new_tasks["regular_tasks"]
            self.scheduled_tasks += new_tasks["scheduled_tasks"]
            self.idle = False
        else:
            self.idle = True

    def add_task(self, time, func, description):
        self.tasks.append(Task(time, func, description, self.account, self.perm_dict))

    def run(self):
        while True:
            if self.running:
                self.tick()
                if self.idle:
                    time.sleep(ACCOUNT_THREAD_IDLE_TICK)
            else:
                time.sleep(1)  # TODO: move to constants

    def add_startup_tasks(self):
        self.add_task(None, TestModule.run(self.account, self.logger, self.perm_dict), "some test task")
        # TODO: rewrite so that all run() functions in files in Modules folder are ran here
