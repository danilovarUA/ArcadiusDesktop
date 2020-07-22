import time
from Scheduler.Task import Task


def run(account):
    time.sleep(1)
    new_task = Task(None, run, account)
    account.logger.add_log("Test Module did something {}".format(account.perm_dict["c"]), "TestModule", account)
    account.perm_dict["c"] += 1
    return [True, {"scheduled_tasks": [], "regular_tasks": [new_task]}]
