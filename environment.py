## This module contains the agents to interact in the environment.


# Modules to use in this file:
from datetime import timedelta
from entities import Customer           # To create customer agents.
from math import inf as infinite
from numpy import mean
from numpy import random as np_random
from time import sleep,time             # Regulates simulation's internal clock.
import colors
#import emoji       # Allows printing emojis.
import functions    # Custom module: Useful functions

class Environment:
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

    def __init__(self):
        # Environment properties
        self.screen = None
        self.clock = 0
        self.cashiers = []
        self.inactive_cashiers = []
        self.customer_count = 0
        self.customers = []
        self.waiting_times = []

        # Running parameters
        self.print_animation = False
        self.time_scale = 0.005
        self.dynamic_arrival_time = False
        self.dynamic_cashier_generation = False
        self.dynamic_scanning_time = False
        self.customer_quantity = infinite
        self.simulation_time = infinite
        self.arrival_time_distribution = "exponential"
        self.items_in_cart_distribution = "triangular"

        # Fixed parameters
        self.arrival_time = 1
        self.scanning_time = 3
        self.observer_customer_probability = 0.1
        self.cashiers_y_axis = 15

        # Variable parameters:
        self.cashier_quantity = 5

    def define_parameters(self, simulation_parameters: dict):
        """
        Define simulation parameters.
        
        Args:
            simulation_parameters (dict): Dictionary containing the parameters listed below.

            Running parameters:
                print_animation (bool): Allow to turn on/off printing in screen the animation. Turning this feature off (False) allows to run the simulation  faster. Turning it on limits the simulation to 1 frame per 0.005 seconds (200 FPS).
        
                time_scale (float): In seconds; simulation prints a frame each t seconds. Scale is t:1 second. This parameter is only valid if "print_animation" is True. If print_animation is False, the simulation will run at the lowest time possible.

                dynamic_arrival_time (bool): If True, a list containing the distribution of arrivals must be passed, if False, a fixed arrival time must be passed. This allows to add an arrival distribution similar to a real supermarket.

                dynamic_cashier_generation (bool): If True, a list containing the times to generate a cashier must be passed, if False, a fixed quantity of cashiers from the beginning to the end must be passed.

                dynamic_scanning_time (bool): If True, scanning time for each item will be calculated using a random exponential time that must be passed as integer. If False, all items will have the same scanning time.

                customer_quantity (int): Simulate until n quantity of customers is generated. The simulation will end when all the generated customers leave the supermarket. To disable this limit, it is recommended to used infinite from math module, inf function.

                simulation_time (int): Generate customers until t seconds. The simulation will end when all the generated customers leave the supermarket. If dynamic_arrival_time is True, simulation_time must be greater than than t seconds in arrival distribution. To disable this limit, it is recommended to used infinite from math module, inf function.

                arrival_time_distribution (str): "exponential" or "poisson"

                items_in_cart_distribution (str): "triangular" or "normal"

            Fixed parameters:
                arrival_time (int|list): If dynamic_arrival_time is True, a list containing the distribution of time must be provided; format is [[t1, arrival_time], [t2, arrival_time], …, [tn, arrival_time]]. If dynamic_arrival_time is False, an integer must be passed, and all the customers will arrive at the same average arrival time, using the distribution in arrival_time_distribution.

                scanning_time (int): Average scanning time per item.

                observer_customer_probability (float): Probability that a customer is observer kind.

                cashiers_y_axis (int): All cashiers will be generated at the same y axis.

            Variable parameters:
                cashier_quantity (int|list): If dynamic_cashier_generation is True, a list containing the quantity of cashiers per hour must be provided; format is [[t1, n1], [t2, n2], …, [tn, n]]. If dynamic_cashier_generation is False, an integer must be passes and this fixed quantity of cashiers will be used from the beginning to the end of the simulation.
        """

        for key, value in simulation_parameters.items():
            setattr(self, key, value)

    def start(self):
        """
        Start simulation. To finish the simulation press CTRL+C.
        This function only works with this specific simulation (supermarket queue).
        """

        if self.dynamic_cashier_generation:
            """try:
                for i in range(0, len(self.cashier_quantity)):
                    if i + 1 < len(self.cashier_quantity):
                        if self.cashier_quantity[i][1] - self.cashier_quantity[i + 1][1] > 0:
                            self.cashier_quantity[i + 1][0] += 1800
                        if self.cashier_quantity[i][1] > len(self.cashiers) + len(self.inactive_cashiers):
                            raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La cantidad máxima de cajeros es {colors.Regular.bold}{len(self.cashiers) + len(self.inactive_cashiers)}{colors.Text.end}.")
            except:
                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} cashier_quantity debe ser una lista conteniendo la cantidad de cajeros por cuartil.")"""
            
            functions.generate_cashiers(self, self.cashiers_y_axis)
            self.inactive_cashiers = self.cashiers.copy()
            self.cashiers = []
            for cashier in self.inactive_cashiers:
                functions.delete_cashier_queue(self.screen, cashier)
        else:
            try:
                functions.generate_cashiers_n(self, self.cashier_quantity, self.cashiers_y_axis)
            except:
                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} cashier_quantity debe ser integer.")
            
        if self.dynamic_arrival_time:
            try:
                self.clock = self.arrival_time[0][0]
                avg_arrival_time = self.arrival_time[0][1]
                next_arrival = self.clock + np_random.exponential(avg_arrival_time)
            except:
                raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} arrival_time debe ser una lista conteniendo las distribuciones.")
        else:
            try:
                avg_arrival_time = self.arrival_time
            except:
               raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} arrival_time debe ser un integer.") 
            
            next_arrival = np_random.exponential(avg_arrival_time)

        start_time = round(time())

        if self.print_animation:
            if functions.check_time_scale(self.time_scale) < 0.002 :
                    self.time_scale = 0.002
            self.screen.print_screen()  #Initial screen printing.
        else:
            self.time_scale = 0

        end = False
        while True:    # Loop: This simulation will run until user press ctrl+C.
            if end == False and self.dynamic_cashier_generation:
                try:
                    for i in range(0, len(self.cashier_quantity)):
                        if self.clock >= self.cashier_quantity[i][0] and self.clock < self.cashier_quantity[i + 1][0]:
                            if len(self.cashiers) == 0:
                                for j in range(0, self.cashier_quantity[i][1]):
                                    self.inactive_cashiers[0].status = "activating"
                                    self.cashiers.append(self.inactive_cashiers[0])
                                    self.inactive_cashiers.remove(self.inactive_cashiers[0])
                            elif self.cashier_quantity[i][1] - len(self.cashiers) < 0:
                                for j in range(1, abs(self.cashier_quantity[i][1] - len(self.cashiers)) + 1):
                                    self.cashiers[-j].open_queue = False
                            elif self.cashier_quantity[i][1] - len(self.cashiers) > 0:
                                for j in range(0, self.cashier_quantity[i][1] - len(self.cashiers)):
                                    self.inactive_cashiers[0].status = "activating"
                                    self.cashiers.append(self.inactive_cashiers[0])
                                    self.inactive_cashiers.remove(self.inactive_cashiers[0])
                except:
                    raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} Se debe proporcionar la cantidad de cajeros por cuartiles en una lista en cashier_quantity.")
            
            for cashier in self.cashiers:  # Evaluates the status for each cashier in the simulation an execute a method or action according their status.
                match cashier.status:
                    case "activating" :
                        cashier.spawn()
                        functions.generate_cashier_queue(self.screen, cashier)
                        cashier.status = "available"
                        cashier.open_queue = True
                    case "busy":   # If the cashier is busy (serving a customer), check if simulation's internal clock is equal to the time they finish attending the customer. If the times are the same, release the customer.
                        if self.clock > cashier.current_customer_complete_time:
                            cashier.release_customer()
                    case "available":  # If the cashier is available and there is someone in their queue, call them.
                        if len(cashier.customer_queue) == 0 and cashier.open_queue == False:
                            functions.delete_cashier_queue(self.screen, cashier)
                            cashier.disappear()
                            self.inactive_cashiers.append(cashier)
                            self.cashiers.remove(cashier)
                        else:
                            cashier.call_customer()

            if self.customer_count < self.customer_quantity and self.clock < self.simulation_time:
                if end == False and self.clock > next_arrival:
                    if self.dynamic_arrival_time:
            
                        for i in range(0, len(self.arrival_time)):
                            if self.clock >= self.arrival_time[i][0] and self.clock < self.arrival_time[i+1][0]:
                                avg_arrival_time = self.arrival_time[i][1]

                                if avg_arrival_time == 0:
                                    end = True

                    customer = Customer(self, functions.random_customer_kind(self.observer_customer_probability))  # Create a customer; "observer" customer is generated with a probability of 3%.
                    customer.customer_id = self.customer_count + 1
                    customer.spawn(0,28)    # Spawn point set in (0,28).
                    self.customer_count += 1
                    next_arrival += np_random.exponential(avg_arrival_time)
            else:
                end = True
                
            if len(self.customers) > 0:
                for customer in self.customers:    # Evaluates the status for each customer in the simulation an execute a method or action according their status.
                    match customer.status:
                        case "exiting":
                            customer.exit_store_clocked()
                        case "spawned":
                            customer.choose_queue()
                        case "moving to queue":
                            customer.move_to_queue_clocked()
                        case "in queue":
                            customer.move_in_queue_clocked()
                            if customer == customer.chosen_cashier.customer_queue[-1] and customer.chosen_cashier.customer_queue.index(customer) != 0:
                                customer.search_different_queue()
                        case "changing queue":
                            customer.change_queue_clocked()
                        case "finished":
                            self.customers.remove(customer)

            if self.print_animation:
                self.screen.print_screen()

                print(f"{colors.Regular.bold}Tiempo:{colors.Text.end} {str(timedelta(seconds=round(self.clock)))}      {colors.Regular.bold}Tiempo real:{colors.Text.end} {str(timedelta(seconds=round(time())-start_time))}")

                print(f"{colors.Regular.bold}Siguiente llegada:{colors.Text.end} {str(timedelta(seconds=round(next_arrival)))}")

                if len(self.waiting_times) > 0:
                    print(f"{colors.Regular.bold}Promedio de espera:{colors.Text.end} {str(timedelta(seconds=round(mean(self.waiting_times))))}")

                for cashier in self.cashiers:
                    print(f"{colors.Regular.bold}(Cashier {cashier.cashier_id}) Next release:{colors.Text.end} {str(timedelta(seconds=cashier.current_customer_complete_time))}")
                    if cashier.current_customer_complete_time < self.clock and cashier.current_customer != None:
                        print(f"{colors.Bold.red}Error:{colors.Text.end} Cajero {cashier.cashier_id} atascado.")

            if self.time_scale > 0:
                sleep(1 * self.time_scale)  # Wait 0.1 second * scale before continue. 

            if end and len(self.customers) == 0:
                break

            self.clock += 1   # Increase 1 second the internal clock.
    
        print(f"{colors.Bold.green}La simulación ha finalizado.{colors.Text.end}")
        print(f"{colors.Regular.bold}Total de clientes:{colors.Text.end} {self.customer_count}")
        print(f"{colors.Regular.bold}Hora de finalización:{colors.Text.end} {str(timedelta(seconds=round(self.clock)))}")
        print(f"{colors.Regular.bold}Tiempo medio de espera:{colors.Text.end} {str(timedelta(seconds=round(mean(self.waiting_times))))}")


## SCREEN CLASS WAS RETRIEVED FROM A PAST PROJECT. It could be improved.
class Screen:
    """
    This class graphically represents the environment. The objects should be integrated in a layout.

    Args:
        environment (object): Environment that manages the simulation.
        width (int): Unit of measure is blank spaces in the command line.
        height (int): Unit of measure is blank spaces in the command line.
        border_stye (str): Character delimiting the border of the layout. If no character desired, provide double blank space "  ". Optionally, it is suggested to used Border class in ELements module.
    """

    def __init__(self, environment: object, width: int , height: int, border_style: str):
        self.width = width
        self.height = height
        self.border_icon = border_style
        self.environment = environment

        self.environment.screen = self
        self.layout = self.build_layout()
    
    def build_layout(self):
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

        for y in range(0, self.height-2):  # Generate every row (x axis) of the layout from 0 to height value.
            row = []
            row.append(self.border_icon)

            for z in range(0, self.width-2):
                row.append("  ")
            row.append(self.border_icon)
            layout.append(row)

        layout.append(ud_border.copy())
        return layout

    def print_screen(self):
        """
        Print the layout in the "screen" class object.
        """

        # Clean the last screen printed.    
        functions.clear_screen()

        # First, it iterates every sublist in the list "layout". Then, it iterates every item in the sublist.
        # It concatenates every item in the sublist to create a row. It prints the row.
        rows = []
        for line in self.layout:
            row = "".join(line)
            rows.append(row)

        output = "\n".join(rows)

        print(output, end="\n")