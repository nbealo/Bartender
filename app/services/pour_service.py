class PourService:

    def __init__(self, blackboard, spec, all_drinks):
        self.blackboard = blackboard
        self.ready_for_death = False
        self.spec = spec
        self.all_drinks = all_drinks
        self.drink = None
        self.component = None
        self.indegrient = None
        self.component_index = 0
        self.start_weight = 0

    def start_pouring(self, drink_name):
        try:
            self.drink = next( (d for d in self.all_drinks if d.name==drink_name) )
            self.prepare_component(0)
        except StopIteration:
            print('drink not found')
            self.stop_pouring()

    def stop_pouring(self):
        self.drink = None

    def set_weight(self, weight):
        self.weight = weight

    def update_blackboard(self):
        self.blackboard.set('pour.pouring', self.drink != None)
        self.blackboard.set('pour.drink.name', self.drink.name)
        self.blackboard.set('pour.component.index', self.component_index)
        self.blackboard.set('pour.component.name', self.component.name)
        self.blackboard.set('pour.component.startWeight', self.start_weight)
        self.blackboard.set('pour.component.stopWeight', self.stop_weight)

    def prepare_component(self, component_index):
        # TODO make sure all data exists...
        self.component_index = component_index

        if (self.component_index >= len(self.drink.components)):
            self.stop_pouring()
            return

        try:
            self.component = self.drink.components[self.component_index]
            self.indegrient = next( (i for i in self.spec.indegrients if i.name == self.component.indegrient) )
            self.start_weight = self.weight
            self.stop_weight = self.weight + (self.component.volume * self.indegrient.density)
        except:
            print('failed to prepare component')
            self.stop_pouring()

    def die(self):
        '''
        Once this method is called, the process_pour will always return a mapping of LOWS.
        '''
        self.ready_for_death = True

    def process_pour(self):
        '''
        Given the current state of the pour_service, produce a mapping on pin HIGH/LOW values,
        so that the barbot actually pours a beverage. 
        The output of this function should look like {20: False, 21: True, 22: False, 23: False}, or some-such map
        that shows pin numbers as keys, and HIGH/LOW values.
        '''
        pin_map = {}
        for indegrient in self.spec.indegrients:
            # default every pin to LOW.
            pin_map[indegrient.pin_number] = False

        if (self.drink == None or self.ready_for_death == True):
            # if there is no drink, return all zeros
            self.update_blackboard()
            return pin_map
        elif (self.weight >= self.stop_weight):
            # if the weight is greater than our stop weight, then prepare the next component.
            self.prepare_component(self.component_index + 1)
        else:
            # otherwise, write high to the current pin.
            pin_map[self.indegrient.pin_number] = True

        self.update_blackboard()
        return pin_map

