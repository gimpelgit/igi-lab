def define_task(text_task: str):
    """
        A decorator for displaying the task description on the screen.
    """
    def actual_decorator(func):
        def task():
            print("===================")
            print(text_task)
            func()
            print("===================\n")
        return task
    return actual_decorator