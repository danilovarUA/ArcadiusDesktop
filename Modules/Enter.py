import Modules.TestModule
from Scheduler.Task import Task

def run(account, logger, perm_dict):
    account.logger.add_log("Logging in", "Enter", account)
    result, data = account.requester.enter()
    if result:
        account.logger.add_log("Logged in", "Enter", account)
        new_task = Task(None, Modules.TestModule.run, account)
        return [True, {"scheduled_tasks": [], "regular_tasks": [new_task]}]
    else:
        account.logger.add_log("Error logging in: {}".format(data), "Enter", account)
        return [result, data]
