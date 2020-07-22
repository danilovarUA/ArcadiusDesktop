import time
from Scheduler.Task import Task


def run(account, logger, perm_dict):
    time.sleep(1)

    new_task = Task(None, run, "another run()", account)
    return [True, {"scheduled_tasks": [], "regular_tasks": [new_task]}]
