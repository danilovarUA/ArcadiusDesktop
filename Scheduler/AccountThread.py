from datetime import datetime
from Scheduler.Task import Task
import threading
import time
from Constants import ACCOUNT_THREAD_IDLE_TICK, INACTIVE_THREAD_CHECK_TICK
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
        self.running = True

        self.add_startup_tasks()

    def perform_task(self):
        if len(self.tasks) > 0:
            task = self.tasks.pop(0)
            return task.run()

    def tick(self):
        # Add scheduled tasks to queue
        for scheduled_task_time in self.scheduled_tasks:
            if scheduled_task_time == datetime.now():
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

    def add_task(self, task_time, func, description):
        self.tasks.append(Task(task_time, func, description, self.account, self.perm_dict, self.logger))

    def run(self):
        while True:
            if self.running:
                self.tick()
                if self.idle:
                    time.sleep(ACCOUNT_THREAD_IDLE_TICK)
            else:
                time.sleep(INACTIVE_THREAD_CHECK_TICK)

    def add_startup_tasks(self):
        self.add_task(None, TestModule.run, "some test task")
        # TODO: rewrite so that all run() functions in files in Modules folder are ran here
