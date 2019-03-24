import os, time
import json
import threading

class Blackboard:
    def __init__(self):
        self.state = {}
        self.lock = threading.Lock()

    def set(self, key, value):
        self.lock.acquire()
        self.state[key] = value
        self.lock.release()
        return self

    def get(self, key):
        self.lock.acquire()
        value = self.state[key]
        self.lock.release()
        return value

    def as_json(self):
        self.lock.acquire()
        data = json.dumps(self.state)
        self.lock.release()
        return data