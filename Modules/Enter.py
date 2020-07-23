import Modules.TestModule
from Scheduler.Task import Task


def run(account):
    log = account.logger.add_log("Logging in", "Enter", account)
    result, data = account.requester.enter()
    if result:
        account.logger.finish_log(log, result, None)
        new_task = Task(None, Modules.TestModule.run, account)
        return [True, {"scheduled_tasks": [], "regular_tasks": [new_task]}]
    else:
        account.logger.finish_log(log, result, data)
        return [result, data]
