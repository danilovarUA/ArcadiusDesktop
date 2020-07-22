class Task:
    def __init__(self, time, func, account):
        self.time = time  # none if time is not necessary
        self.status = "waiting"  # waiting, running, done, failed
        self.error = None  # error if task failed(mostly it is error from a response)
        self.func = func  # function to run
        self.account = account  # account task is running for

    # function:
    # - takes account to perform requests and store temp information and per_dict to store permanent information
    # - return result(true/false) and error_or_data(error is text of error), where data is be
    # {"scheduled_tasks": [], "regular_tasks": []}
    # 1) reads database
    # 2) sends request
    # 3) modifies database
    # 4) creates and returns new tasks
    # some steps may be skipped but order must not be changed to avoid database modifications without actually
    # performing task with request

    def run(self):
        self.status = "running"
        result, error_or_data = self.func(self.account)
        # TODO do I really need to pass it here to function or can I pass it in modules?
        if not result:
            self.status = "failed"
            self.error = error_or_data
            return None
        else:
            self.status = "done"
            return error_or_data

