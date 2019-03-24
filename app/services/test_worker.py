import os, time
import threading
from services.persistence_service import PersistenceService
from services.pour_service import PourService

from queue import Queue
import queue

EMULATE_HX711=True

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from services.hx711_service import HX711
    #from hx711 import HX711
else:
    from services.hx711_emulated_service import HX711
    # from emulated_hx711 import HX711

class WorkerCommandMessage:
    def __init__(self, n):
        self.n = n

class WorkerZeroMessage:
    def __init__(self):
        pass

class WorkerDrinkMessage:
    def __init__(self, drink_name):
        self.drink_name = drink_name

class WorkerThread(threading.Thread):
    def __init__(self, command_queue, output_queue, blackboard):
        super(WorkerThread, self).__init__()
        self.stoprequest = threading.Event()
        self.command_queue = command_queue
        self.output_queue = output_queue
        self.blackboard = blackboard
        self.drink = None

    def run(self):
        
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")

        self.config = PersistenceService.load_config('./app/config')

        self.pourer = PourService(self.blackboard, self.config[0], self.config[1])

        # at 128 gain.
        # 1 kg -> 458591 -> 460
        # 2.75 kg -> 1146261 -> 416


        # at 64 gain
        # 2.75 kg -> 591915 -> 215


        # 31913, 85646, with 

        self.reference_unit = 382
        self.hx.set_reference_unit(self.reference_unit)
        self.hx.reset()

        self.first_long = self.hx.read_long()
        self.hx.power_down()
        self.hx.power_up()

        while not self.stoprequest.isSet():

            val = self.hx.read_long()
            weight = 0
            weight = (val - self.first_long) / self.reference_unit
            # print(str(val) + ', ' + str(weight))

            self.blackboard.set('weight', weight)

            self.pourer.set_weight(weight)
            pin_map = self.pourer.process_pour(weight)
            for pin in pin_map:
                # for each pin returned by the pourer, set that pin's high or low.
                GPIO.output(pin, pin_map[pin])

            # To get weight from both channels (if you have load cells hooked up 
            # to both channel A and B), do something like this
            #val_A = hx.get_weight_A(5)
            #val_B = hx.get_weight_B(5)
            #print "A: %s  B: %s" % ( val_A, val_B )

            # if we are making a drink...
                # do this shit...

            # otherwise, do nothing

            self.hx.power_down()
            self.hx.power_up()
            time.sleep(0.01)
            # copy code from the example hx711 sample
            # print(self.drink)
            # increment the data.
            # self.blackboard.set('x', self.blackboard.get('x') + 1)
            # time.sleep(1)

            # # read data off the queue, or continue to next loop.
            try:
                command = self.command_queue.get(True, 0.05)
                if isinstance(command, WorkerZeroMessage):
                    self.first_long = val
                if isinstance(command, WorkerDrinkMessage):
                    self.pourer.start_pouring(command.drink_name)


            except queue.Empty:
                continue
        print('worker shutting down')

    def join(self, timeout=None):

        # TODO CLEAN UP HX711

        self.pourer.die()
        pin_map = self.pourer.process_pour(weight)
        for pin in pin_map:
            GPIO.output(pin, pin_map[pin])
            
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)
