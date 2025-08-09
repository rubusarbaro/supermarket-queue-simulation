## This module contains the agents to interact in the environment.


# Modules to use in this file:
from datetime import timedelta
from entities import Customer           # To create customer agents.
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
        self.screen = None
        self.clock = 0
        self.time_scale = 0.0
        self.cashiers = []
        self.inactive_cashiers = []
        self.customer_count = 0
        self.customers = []
        self.waiting_times = []

    def start(self, simulation_parameters: dict):
        """
        Start simulation. To finish the simulation press CTRL+C.
        This function only works with this specific simulation (supermarket queue).

        Args:
            simulation_parameters (dict): Dictionary containing the parameters.
        """

        match simulation_parameters["print_animation"]:
            case True:
                if functions.check_time_scale(simulation_parameters["simulation_scale"]) < 0.002 :
                    self.time_scale = 0.002
                else:
                    self.time_scale = functions.check_time_scale(simulation_parameters["simulation_scale"])
            case False:
                self.time_scale = 0.000000000000000000000001

        functions.generate_cashiers(self,simulation_parameters["cashiers_y_axis"])  # This lines were added for Letty's suggestions.
        self.inactive_cashiers = self.cashiers.copy()   # This lines were added for Letty's suggestions.
        self.cashiers = []  # This lines were added for Letty's suggestions.
        for cashier in self.inactive_cashiers:
            functions.delete_cashier_queue(self.screen, cashier)

        avg_arrival_time = simulation_parameters["customer_average_arrival_time"]

        observer_customer_p = simulation_parameters["observer_customer_probability"]

        customer_quantity = simulation_parameters["customer_quantity"]

        simulation_time = simulation_parameters["simulation_time"]

        walmart_saturday = [
            [25200,300], [28800,166], [32400,100], [36000,70], [39600,55], [43200,45],
            [46800,42], [50400,40], [54000,40], [57600,40], [61200,40], [64800,40],
            [68400,44], [72000,54], [75600,75], [79200,130], [82800,0], [86400,0]
        ] #19 34 54 78 101 120 131 135 135 135 135 135 124 101 72 41  MAX: 150

        walmart_saturday_modified = [   # Esta modificación añade corte a las 22:30h.
            [25200,300], [28800,166], [32400,100], [36000,70], [39600,55], [43200,45],
            [46800,42], [50400,40], [54000,40], [57600,40], [61200,40], [64800,40],
            [68400,44], [72000,54], [75600,75], [79200,130], [79200+1800,0], [82800,0], [86400,0]
        ] #19 34 54 78 101 120 131 135 135 135 135 135 124 101 72 41  MAX: 150

        walmart_sunday = [
            [25200,9], [28800,16], [32400,29], [36000,45], [39600,68], [43200,89],
            [46800,110], [50400,124], [54000,134], [57600,141], [61200,141], [64800,138],
            [68400,124], [72000,97], [75600,65], [79200,37], [82800,0], [86400,0]
        ] #9 16 29 45 68 89 110 124 134 141 141 138 124 97 65 37. MAX: 150

        # SUGERENCIA DE LETTY: Primeras cuatro horas son Q1; últimas 2 horas son Q3.
        cashiers_per_Q = [
            [25200, 3],
            [39600, 5],
            [75600, 2],
            [82800,0]
        ]

        for i in range(0, len(cashiers_per_Q)):
            if i + 1 < len(cashiers_per_Q):
                if cashiers_per_Q[i][1] - cashiers_per_Q[i + 1][1] > 0:
                    cashiers_per_Q[i + 1][0] += 1800
                if cashiers_per_Q[i][1] > len(self.cashiers) + len(self.inactive_cashiers):
                    raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La cantidad máxima de cajeros es {colors.Regular.bold}{len(self.cashiers) + len(self.inactive_cashiers)}{colors.Text.end}.")

        walmart_hours = walmart_saturday_modified

        #arrival_times = functions.generate_exponential_arrival_time(1000,5)    # Get a list of 1,000 customer arrival times with an average of 15 seconds.

        next_arrival = int(round(np_random.exponential(avg_arrival_time)))

        if simulation_parameters["fixed_arrival_times"] == False:
            self.clock = 25200
            avg_arrival_time = walmart_hours[0][1]
            next_arrival = self.clock + int(round(np_random.exponential(avg_arrival_time))) + 1

        start_time = round(time())

        if simulation_parameters["print_animation"]:
            self.screen.print_screen()  #Initial screen printing.

        end = False
        while True:    # Loop: This simulation will run until user press ctrl+C.
            if end == False:
                for i in range(0, len(cashiers_per_Q)):
                    if self.clock >= cashiers_per_Q[i][0] and self.clock < cashiers_per_Q[i + 1][0]:
                        if len(self.cashiers) == 0:
                            for j in range(0, cashiers_per_Q[i][1]):
                                self.cashiers.append(self.inactive_cashiers[j])
                                self.inactive_cashiers.remove(self.inactive_cashiers[j])
                                self.cashiers[j].status = "activating"
                        elif cashiers_per_Q[i][1] - len(self.cashiers) < 0:
                            for j in range(1, abs(cashiers_per_Q[i][1] - len(self.cashiers)) + 1):
                                self.cashiers[-j].open_queue = False
                        elif cashiers_per_Q[i][1] - len(self.cashiers) > 0:
                            for j in range(0, cashiers_per_Q[i][1] - len(self.cashiers)):
                                self.cashiers.append(self.inactive_cashiers[j])
                                self.inactive_cashiers[j].status = "activating"
                                self.inactive_cashiers.remove(self.inactive_cashiers[j])
            
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

            if self.customer_count < customer_quantity and self.clock < simulation_time:
                #if round(self.clock) == arrival_times[self.customer_count]:  # When internal clock is equal to the arrival time of the current customer, generate a new customer.
                if end == False:
                    if self.clock > next_arrival:
                        if simulation_parameters["fixed_arrival_times"] == False:
                
                            for i in range(0, len(walmart_hours)):
                                if self.clock >= walmart_hours[i][0] and self.clock < walmart_hours[i+1][0]:
                                    avg_arrival_time = walmart_hours[i][1]

                                    if avg_arrival_time == 0:
                                        end = True

                        customer = Customer(self, functions.random_customer_kind(observer_customer_p))  # Create a customer; "observer" customer is generated with a probability of 3%.
                        customer.customer_id = self.customer_count + 1
                        customer.spawn(0,28)    # Spawn point set in (0,28).
                        self.customer_count += 1
                        next_arrival += int(round(np_random.exponential(avg_arrival_time)))
            else:
                end = True
                
            if len(self.customers) == 0:   # If there are not customers in the simulation, do nothing.
                pass
            else :
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

            if simulation_parameters["print_animation"]:
                self.screen.print_screen()

                print(f"{colors.Regular.bold}Tiempo:{colors.Text.end} {str(timedelta(seconds=round(self.clock)))}      {colors.Regular.bold}Tiempo real:{colors.Text.end} {str(timedelta(seconds=round(time())-start_time))}")

                print(f"{colors.Regular.bold}Siguiente llegada:{colors.Text.end} {str(timedelta(seconds=round(next_arrival)))}")

                if len(self.waiting_times) > 0:
                    print(f"{colors.Regular.bold}Promedio de espera:{colors.Text.end} {str(timedelta(seconds=round(mean(self.waiting_times))))}")

                for cashier in self.cashiers:
                    print(f"{colors.Regular.bold}(Cashier {cashier.cashier_id}) Next release:{colors.Text.end} {str(timedelta(seconds=cashier.current_customer_complete_time))}")
                    if cashier.current_customer_complete_time < self.clock and cashier.current_customer != None:
                        print(f"{colors.Bold.red}Error:{colors.Text.end} Cajero {cashier.cashier_id} atascado.")

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
        for line in self.layout:
            row = ""
            for item in line:
                row += item
            print(row)