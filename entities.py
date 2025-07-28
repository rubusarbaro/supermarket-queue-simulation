import emoji
import functions

class Entity():
    def __init__(self,environment: object):
        self.x_location = 0
        self.y_location = 0
        self.environment = environment

class Cashier(Entity) :
    def __init__(self,environment:object,x_location:int,y_location:int,scan_speed=0.1):
        self.icon = "🛃"
        self.x_location = x_location
        self.y_location = y_location
        self.environment = environment
        self.cashier_id = 0
        self.scan_speed = scan_speed
        self.customer_queue = []
        self.current_customer = None
        self.current_customer_complete_time = 0.0
        self.scanned_items = 0
        self.status = "available"

        environment.cashiers.append(self)
        functions.generate_cashier_queue(environment.screen,self)

    def spawn(self) :
        self.environment.screen.layout[self.y_location][self.x_location] = self.icon

    def call_customer(self) :
        self.scanned_items = 0
        self.current_customer = self.customer_queue[0]
        self.current_customer_complete_time = round(self.environment.clock + self.current_customer.cart_size * self.scan_speed,1)

        self.current_customer.status = "paying"
        self.status = "busy"
    
    def release_customer(self) :
        self.status = "available"
        self.current_customer.status = "exiting"
        self.customer_queue.remove(self.current_customer)
        self.current_customer = None

class Customer(Entity) :
    def __init__(self,environment: object,customer_kind: str):
        from random import randint
        self.icon = "👤"
        self.environment = environment
        self.customer_id = 0
        self.customer_kind = customer_kind  # Tipos: regular y observer
        self.cart_size = randint(1,50)
        self.status = "spawned"  # Estatus: spawned,
        self.chosen_cashier = None

        environment.customers.append(self)
    
    def spawn(self,x_location:int,y_location:int) :
        self.x_location = x_location
        self.y_location = y_location

        self.environment.screen.layout[y_location][x_location] = self.icon

    def choose_queue(self) :
        from math import inf as infinite

        queue = None

        match self.customer_kind :
            case "regular" :
                queue_size = infinite
                for cashier in self.environment.cashiers :
                    if len(cashier.customer_queue) < queue_size :
                        queue_size = len(cashier.customer_queue)
                        queue = cashier
            case "observer" :
                items_in_queue_size = infinite
                for cashier in self.environment.cashiers :
                    cart_size = 0
                    for customer in cashier.customer_queue :
                        cart_size += customer.cart_size

                    if cart_size < items_in_queue_size :
                        items_in_queue_size = cart_size
                        queue = cashier
        queue.customer_queue.append(self)
        self.chosen_cashier = queue

        self.status = "moving to queue"
    
    def move_to_queue_clocked(self) :
        if self.x_location == self.chosen_cashier.x_location + 1 :
            self.status = "in queue"
        else :
            from elements import Queue
            Queue().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location+1,self.y_location)
    
    def move_in_queue_clocked(self) :
        if self.y_location == self.chosen_cashier.y_location :
            self.status = "ready"
        elif self.environment.screen.layout[self.y_location-1][self.x_location] == self.icon :
            pass
        else :
            from elements import Queue
            Queue().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location,self.y_location-1)
    
    def exit_store_clocked(self) :
        from elements import Void
        if self.y_location == 0 :
            Void().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.status = "finished"
        else :
            Void().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location,self.y_location-1)
