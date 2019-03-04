import os, time
import threading


from queue import Queue
import queue

from models.blackboard import BlackboardVariableMessage

class WorkerCommandMessage:
    def __init__(self, n):
        self.n = n

class WorkerThread(threading.Thread):
    def __init__(self, command_queue, output_queue, blackboard):
        super(WorkerThread, self).__init__()
        self.stoprequest = threading.Event()
        self.command_queue = command_queue
        self.output_queue = output_queue
        self.blackboard = blackboard

    def run(self):

        n = 1
        while not self.stoprequest.isSet():

            # increment the data.
            # msg = BlackboardVariableMessage('x', n)
            # self.output_queue.put(msg)
            self.blackboard.set('x', self.blackboard.get('x') + 1)
            time.sleep(1)

            # read data off the queue, or continue to next loop.
            try:
                command = self.command_queue.get(True, 0.05)
                if isinstance(command, WorkerCommandMessage):
                    self.blackboard.set('x', command.n)
            except queue.Empty:
                continue
        print('worker shutting down')

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)
