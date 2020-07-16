import uuid

import eventlet
from eventlet.event import Event
from nameko.rpc import rpc
from nameko.extensions import DependencyProvider


# a simple task
def fibonacci(n):
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a+b
        if n % 50 == 0:
            eventlet.sleep()  # won't yield voluntarily since there's no i/o
    return a


class TaskProcessor(DependencyProvider):

    def __init__(self):
        self.tasks = {
            'fibonacci': fibonacci
            # add other tasks here
        }
        self.results = {}

    def start_task(self, name, args, kwargs):
        # generate unique id
        task_id = uuid.uuid4().hex

        # get the named task
        task = self.tasks.get(name)

        # execute it in a container thread and send the result to an Event
        event = Event()
        gt = self.container.spawn_managed_thread(lambda: task(*args, **kwargs))
        gt.link(lambda res: event.send(res.wait()))

        # store the Event and return the task's unique id to the caller
        self.results[task_id] = event
        return task_id

    def get_result(self, task_id):
        # get the result Event for `task_id`
        result = self.results.get(task_id)
        if result is None:
            return "missing"
        # if the Event is ready, return its value
        if result.ready():
            return result.wait()
        return "pending"

    def get_dependency(self, worker_ctx):

        class TaskApi(object):
            start_task = self.start_task
            get_result = self.get_result

        return TaskApi()


class TaskService(object):
    name = "tasks"

    processor = TaskProcessor()

    @rpc
    def start_task(self, name, *args, **kwargs):
        return self.processor.start_task(name, args, kwargs)

    @rpc
    def get_result(self, task_id):
        return self.processor.get_result(task_id)