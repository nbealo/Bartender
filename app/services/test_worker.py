import os, time
import threading


from queue import Queue
import queue

EMULATE_HX711=False

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

class WorkerThread(threading.Thread):
    def __init__(self, command_queue, output_queue, blackboard):
        super(WorkerThread, self).__init__()
        self.stoprequest = threading.Event()
        self.command_queue = command_queue
        self.output_queue = output_queue
        self.blackboard = blackboard

    def run(self):
        
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")

        # 1 kg -> 458591 -> 460
        # 2.75 kg -> 1146261 -> 416

        self.reference_unit = 416
        self.hx.set_reference_unit(self.reference_unit)
        self.hx.reset()
        while not self.stoprequest.isSet():

            val = self.hx.read_long()
            weight = val / self.reference_unit
            print(str(val) + ', ' + str(weight))

            self.blackboard.set('weight', weight)


            # To get weight from both channels (if you have load cells hooked up 
            # to both channel A and B), do something like this
            #val_A = hx.get_weight_A(5)
            #val_B = hx.get_weight_B(5)
            #print "A: %s  B: %s" % ( val_A, val_B )

            self.hx.power_down()
            self.hx.power_up()
            time.sleep(0.01)
            # copy code from the example hx711 sample

            # increment the data.
            # self.blackboard.set('x', self.blackboard.get('x') + 1)
            # time.sleep(1)

            # # read data off the queue, or continue to next loop.
            # try:
            #     command = self.command_queue.get(True, 0.05)
            #     if isinstance(command, WorkerCommandMessage):
            #         self.blackboard.set('x', command.n)
            # except queue.Empty:
            #     continue
        print('worker shutting down')

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)
