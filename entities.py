###########################################
##  Saúl R. Morales © 2025 MIT License   ##
###########################################
## This module contains the agents to interact in the environment.


# Modules to use in this file:
from math import inf as infinite    # Infinite number is used by Customer to chose Cashier.
import colors   # Custom module: Allows to modify printed text.
import elements # Custom module: Provides simulation objects that agents can interact with.
# import emoji        # Allows to print emojis.
import functions    # Custom module: Containts additional functions that are not contained in classes.

class Entity():
    """
    Agent interacting in the environment.

    Attrs:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        environment (object): Environment where the agent interact.
    """

    def __init__(self,environment: object):
        self.x_location = 0
        self.y_location = 0
        self.environment = environment


class Cashier(Entity) :
    """
    Inherited class from Entity.
    Agent that emulates the behavior of a real life cashier (scan items).

    Args:
        environment (object): Environment where this agent will interact.
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        scan_speed (float): Scanning speed of cashier. Default is 0.5 seconds per item.

    Attrs:
        icon (str): Printed icon. This is set by default as "🛃" and cannot be changed.
        cashier_id (int): Identification number. Default is 0. To assign an ID it is important to do it manually using Cashier.cashier_id = n.
        customer_queue (list): List of customers that are in the queue of this cashier.
        current_customer (object): Customer that the cashier is serving.
        current_customer_complete_time (float): When the cashier is initialized, the value is 0.0 by default. This values is automatically calculated when the method call_customer() is used.
        scanned_items (int): Quantity of items that the cashier scanned from the current customer.
        status (str): Current status; it has two options 1) "available" and 2) "busy".
    """

    def __init__(self,environment:object,x_location:int,y_location:int,scan_speed=0.5):
        self.icon = "🛃"
        self.x_location = x_location
        self.y_location = y_location
        self.environment = environment
        self.cashier_id = 0
        self.scan_speed = scan_speed
        self.customer_queue = []
        self.current_customer = None
        self.current_customer_complete_time = 0.0   # This parameter is important to release the customer according to the internal clock of the environment.
        self.scanned_items = 0
        self.status = "available"

        environment.cashiers.append(self)   # Automatically appends the cashier to the environment's cashier list.
        functions.generate_cashier_queue(environment.screen,self)   # Automatically creates the queue design for the cashier, from y_location to the main line.

    def spawn(self) :
        """
        Set the cashier in the screen's layout. It is important to execute this method before printing the screen.
        """

        self.environment.screen.layout[self.y_location][self.x_location] = self.icon    # This code change the blank space in the coordinates of Screen.layout by the agent icon.

    def call_customer(self) :
        """
        Call the first customer in the list (customer_queue).
        """

        self.scanned_items = 0  # Reset scanned items counter to 0.
        self.current_customer = self.customer_queue[0]  # Assigns the first element (customer) in the list.
        self.current_customer_complete_time = round(self.environment.clock + self.current_customer.cart_size * self.scan_speed,1)   # Calculate the time it will takes the cashier to scan all the items in the customer's cart. It multiplies the item quantity and its scan speed.

        self.current_customer.status = "paying" # Change customer's status to "paying".
        self.status = "busy"    # Change its own status to "busy".
    
    def release_customer(self) :
        """
        This releases the customer when their cart was completed scanned and remove the customer from cashier's list.
        """

        self.status = "available"   # Change own status to "available".
        self.current_customer.status = "exiting"    # Change customer's status to "exiting".
        self.customer_queue.remove(self.current_customer)   # Remove current customer from the queue.
        self.current_customer = None    # Overwrite current customer to None.


class Customer(Entity) :
    """
    Inherited class from Entity.
    Agent that emulates the behavior of a real life customer (queuing).

    Args:
        environment (object): Environment where this agent will interact.
        customer_kind (str): There are two kind of customers, "regular" that chose the queue with less customers, and "observers" who analyse the carts of other customers and chose the queue with less items.

    Attrs:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        icon (str): Printed icon. This is set by default as "👤" and cannot be changed.
        customer_id (int): Identification number. Default is 0. To assign an ID it is important to do it manually using Customer.customer_id = n.
        cart_size (int): Quantity of items in the cart. This value is randomly generated between 1 and 50.
        scanned_items (int): Quantity of items that the cashier scanned from the current customer.
        status (str): Current status; options 1) "spawned", 2) "moving to queue", 3) "in queue", 4) "paying", 5) "exiting", and 6) "finished".
    """

    def __init__(self,environment: object,customer_kind: str):
        from random import randint
        self.icon = "👤"
        self.environment = environment
        self.customer_id = 0
        self.customer_kind = customer_kind  # Tipos: regular y observer
        self.cart_size = randint(1,50)
        self.status = "spawned"
        self.chosen_cashier = None

        environment.customers.append(self)  # Assigns customer to environment list.
    
    def spawn(self,x_location:int,y_location:int) :
        """
        Set the customer in the screen's layout. It is important to execute this method before printing the screen.

        Args:
            x_location (int): Object location in the x axis of screen layout.
            y_location (int): Object location in the y axis of screen layout.
        """
        
        self.x_location = x_location
        self.y_location = y_location

        self.environment.screen.layout[y_location][x_location] = self.icon  # This code change the blank space in the coordinates of Screen.layout by the agent icon.

    def choose_queue(self) :
        """
        Customer analyses the queues according to its kind ("regular" or "observer").
        """

        queue = None    # Initialize the queue variable in blank (None type).

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
        """
        Once the customer chose their cashier, they walk to their queue.
        This function is created to work on an internal clock environment. The agent will execute one step of the action until the loop restarts.
        """

        if self.chosen_cashier == None :    # If the customer has not chosen a cashier, print a warning.
            print(f"{colors.Bold.yellow}Warning:{colors.Text.end} Customer {self.customer_id} has not chosen cashier.")
        elif self.x_location == self.chosen_cashier.x_location + 1 :   # When the customer arrives to cashier's x axis, change their status to "in queue". 
            self.status = "in queue"
        else :  # Move the customer 1 step until they arrives to cashier's x axis and restore the original sprite in the last step.
            elements.Queue().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location+1,self.y_location)
    
    def move_in_queue_clocked(self) :
        """
        Move the customer forward in the queue. If there is someone else in front of him, the customer cannot pass.
        This function is created to work on an internal clock environment. The agent will execute one step of the action until the loop restarts.
        """

        if self.y_location == self.chosen_cashier.y_location :  # If customer arrived cashier's y axis, change their status to "ready (to pay)".
            self.status = "ready"
        elif self.environment.screen.layout[self.y_location-1][self.x_location] == self.icon :  # If there is other customer in front, ignore.
            pass
        else :  # Move the customer 1 step until they arrives to cashier's y axis and restore the original sprite in the last step.
            elements.Queue().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location,self.y_location-1)
    
    def exit_store_clocked(self) :
        """
        Move the customer upwards until they disappear from the screen.
        This function is created to work on an internal clock environment. The agent will execute one step of the action until the loop restarts.
        """

        if self.y_location == 0 :
            elements.Void().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.status = "finished"
        else :
            elements.Void().set_in_screen(self.environment.screen,self.x_location,self.y_location)
            self.spawn(self.x_location,self.y_location-1)
