def run(account, logger, perm_dict):
    result, data = account.requester.enter()
    account.logger.add_log("Logging in", "Enter", account)
    if result:
        account.logger.add_log("Logged in", "Enter", account)
        return [True, {"scheduled_tasks": [], "regular_tasks": []}]
    else:
        account.logger.add_log("Error logging in: {}".format(data), "Enter", account)
        return [result, data]
