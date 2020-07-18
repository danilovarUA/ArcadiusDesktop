class Task:
    def __init__(self, time, func, on_fail_func, description, priority, account, prepending_tasks=None):
        self.time = time  # none if time is not necessary
        self.status = "waiting"  # waiting, running, done, failed
        self.error = None  # error if task failed(mostly it is error from a response)
        self.func = func  # function to run
        self.on_fail_func = on_fail_func  # function to run if failed
        self.priority = priority  # user, calculation, request
        self.description = description  # some text to describe
        self.prepending_tasks = prepending_tasks  # tasks to be ran before running that one
        self.account = account  # account task is running for

    # function:
    # 1) reads database
    # 2) sends request
    # 3) modifies database
    # 4) creates new tasks
    # some steps may be skipped but order must not be changed to avoid database modifications without actually
    # performing task with request

    def run(self):
        self.status = "running"
        result, error = self.func()
        if not result:
            self.status = "failed"
            self.error = error
            self.on_fail_func()
        else:
            self.status = "done"
