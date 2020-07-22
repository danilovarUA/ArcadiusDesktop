import time
from Scheduler.Task import Task


def run(account, logger, perm_dict):
    if "c" not in perm_dict:
        perm_dict["c"] = 0
    time.sleep(1)
    new_task = Task(None, run, "another run()", account)
    logger.add_log("Test Module did something {}".format(perm_dict["c"]), "TestModule", account)
    perm_dict["c"] += 1
    return [True, {"scheduled_tasks": [], "regular_tasks": [new_task]}]
