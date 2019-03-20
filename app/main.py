import sys
import threading
import signal
from queue import Queue
from threading import Thread

from lib.qt_style_helper import Styles
from models.system_spec_model import SystemSpecModel
from services.persistence_service import PersistenceService
from flask import Flask

from services.test_worker import WorkerThread, WorkerCommandMessage, WorkerZeroMessage, WorkerDrinkMessage
from models.blackboard import Blackboard

command_queue = Queue()
output_queue = Queue()

app = Flask(__name__)


@app.route("/")
def main():
    global blackboard

    return "WEIGHT: " + str(blackboard.get('weight'))

@app.route("/zero")
def zero():
    global command_queue
    command_queue.put( WorkerZeroMessage() )
    return "Zeroing..."

# bartender:5000/drink/gin_n_tonic
@app.route("/drink/<string:name>")
def make_drink(name):
    print('requesting drink...')
    print(name)

    global command_queue
    command_queue.put( WorkerDrinkMessage(name))

    return "la la la"

@app.route("/set/<int:val>")
def main2(val):
    global command_queue
    command_queue.put( WorkerCommandMessage(val))
    return "Set to " + str(val)

# set up threads
blackboard = Blackboard()
blackboard.set('x', 0)
blackboard.set('weight', 0)

worker = WorkerThread(command_queue, output_queue, blackboard)

worker.start()

# handle application shutdown...
def signal_handler(sig, frame):
    print('Shutting down...')
    worker.join()
    print('Goodbye!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# run forever...
app.run(host= '0.0.0.0')