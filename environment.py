###########################################
##  Saúl R. Morales © 2025 MIT License   ##
###########################################
## This module contains the agents to interact in the environment.


# Modules to use in this file:
from entities import Customer   # To create customer agents.
from time import sleep          # Regulates simulation's internal clock.
from ui import Label            # To display messages in the screen.
#import emoji       # Allows printing emojis.
import functions    # Custom module: Useful functions 

class Environment :
    """
    This class coordinates all the agents and objects in the simulation.
    The simulation runs at 0.1 seconds per step.

    Args:
        time_scale (float): Value must be greater than 0. Greater value means slower simulation.

    Attributes:
        screen (object): Screen  (layout) that displays the objects in the simulation.
        clock (float): Internal clock.
        cashiers (list): List of cashiers in the supermarket queue simulation.
        customer_count (int): Customer quantity that the simulation has created.
        customer (list): List of customer in the supermarket queue simulation.
    """

    def __init__(self,time_scale:float):
        self.screen = None
        self.clock = 0.0
        self.time_scale = functions.check_time_scale(time_scale)
        self.cashiers = []
        self.customer_count = 0
        self.customers = []

    def start(self) :
        """
        Start simulation. To finish the simulation press CTRL+C.
        This function only works with this specific simulation (supermarket queue).
        """

        arrival_times = functions.generate_exponential_arrival_time(1000,5)    # Get a list of 1,000 customer arrival times with an average of 15 seconds.

        Label("Tiempo:",Label.regular).set_in_screen(self.screen,0,30)  # Elapsed time label shown at the bottom of the simulation.
        time_label = Label(str(round(self.clock,2)),Label.regular)  # Elapsed time shown at the bottom of the simulation.

        Label("Siguiente llegada:",Label.regular).set_in_screen(self.screen,0,31)   # Label of time of next arrival shown at the bottom of the simulation.
        arrival_label = Label(str(arrival_times[self.customer_count]),Label.regular)    # Next arrival time shown at the bottom of the simulation.
        arrival_label.set_in_screen(self.screen,9,31)  # Place the next arrival time in the bottom of simulation.

        self.screen.print_screen()  #Initial screen printing.

        while True :    # Loop: This simulation will run until user press ctrl+C.
            print_screen = True # Reset print_screen to FALSE. I will let it TRUE so the time will update.

            for cashier in self.cashiers :  # Evaluates the status for each cashier in the simulation an execute a method or action according their status.
                match cashier.status :
                    case "busy" :   # If the cashier is busy (serving a customer), check if simulation's internal clock is equal to the time they finish attending the customer. If the times are the same, release the customer.
                        if round(self.clock,1) == cashier.current_customer_complete_time :
                            cashier.release_customer()
                    case "available" :  # If the cashier is available and there is someone in their queue, call them.
                        if len(cashier.customer_queue) == 0 :
                            pass
                        elif cashier.customer_queue[0].status == "ready" :  # I used elif instead of else for a technical redundance (it was on purpose).
                            cashier.call_customer()

            if round(self.clock,1) == arrival_times[self.customer_count] :  # When internal clock is equal to the arrival time of the current customer, generate a new customer.
                customer = Customer(self,functions.random_customer_kind(0.03))  # Create a customer; "observer" customer is generated with a probability of 3%.
                customer.customer_id = self.customer_count + 1
                customer.spawn(0,28)    # Spawn point set in (0,28).
                self.customer_count += 1
                arrival_label.text = str(arrival_times[self.customer_count])    # Update next arrival label.
                arrival_label.set_in_screen(self.screen,9,31)
                print_screen = True # Change print_screen to True, to print the new customer.
                

            if len(self.customers) == 0 :   # If there are not customers in the simulation, do nothing.
                pass
            else :
                for customer in self.customers :    # Evaluates the status for each customer in the simulation an execute a method or action according their status.
                    match customer.status :
                        case "exiting" :
                            customer.exit_store_clocked()
                            print_screen = True
                        case "spawned" :
                            customer.choose_queue()
                        case "moving to queue" :
                            customer.move_to_queue_clocked()
                            print_screen = True
                        case "in queue" :
                            customer.move_in_queue_clocked()
                            print_screen = True
                        case "finished" :
                            del customer

            time_label.text = str(round(self.clock,2))  # Update current time label.
            time_label.set_in_screen(self.screen,4,30)

            if print_screen :
                self.screen.print_screen()

            sleep(0.1*self.time_scale)  # Wait 0.1 second * scale before continue.
            self.clock += 0.1   # Increase 0.1 seconds the internal clock.


## SCREEN CLASS WAS RETRIEVED FROM A PAST PROJECT. It could be improved.
class Screen :
    """
    This class graphically represents the environment. The objects should be integrated in a layout.

    Args:
        environment (object): Environment that manages the simulation.
        width (int): Unit of measure is blank spaces in the command line.
        height (int): Unit of measure is blank spaces in the command line.
        border_stye (str): Character delimiting the border of the layout. If no character desired, provide double blank space "  ". Optionally, it is suggested to used Border class in ELements module.
    """

    def __init__(self, environment: object, width: int , height: int, border_style: str) :
        self.width = width
        self.height = height
        self.border_icon = border_style
        self.environment = environment

        self.environment.screen = self
        self.layout = self.build_layout()
    
    def build_layout(self) :
        """
        Build layout with the parameters provided when the object was initialized (width, height, and border). It is not necessary to call this method after the object initialization; the layout is automatically created.

        Returns:
            layout (list): List containing the layout. The layout contains y list with x double-blank spaces. An element in the layout can be called using layout[y][x].
        """

        ud_border = []  # List containing the upper border.
        for x in range(0, self.width) : # Generate the border from 0 to width.
            ud_border.append(self.border_icon)
        
        layout = [] # List containing the rest of the layout.
        layout.append(ud_border.copy())

        for y in range(0, self.height-2) :  # Generate every row (x axis) of the layout from 0 to height value.
            row = []
            row.append(self.border_icon)

            for z in range(0, self.width-2) :
                row.append("  ")
            row.append(self.border_icon)
            layout.append(row)

        layout.append(ud_border.copy())
        return layout

    def print_screen(self) :
        """
        Print the layout in the "screen" class object.
        """

        # Clean the last screen printed.    
        functions.clear_screen()

        # First, it iterates every sublist in the list "layout". Then, it iterates every item in the sublist.
        # It concatenates every item in the sublist to create a row. It prints the row.
        for line in self.layout :
            row = ""
            for item in line :
                row += item
            print(row)
