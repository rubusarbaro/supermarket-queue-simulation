###########################################
##  Saúl R. Morales © 2025 MIT License   ##
###########################################
## This module contains additional functions needed to simplify this simulation.

# Modules to use in this file:
from itertools import zip_longest       # Merge list of different sizes.
from numpy import random as np_random   # To generate a random number using exponential average.
from random import random   # To create random values.
import colors               # To print in colors.
import os                   # To access system commands.

def clear_screen() :
    """
    Clear all text in the terminal.
    """

    # If system is macOS or Linux, it will use "clear" command.
    if os.name == "posix" :
        os.system("clear")
    # Else, if it's Windows, it will use "CLS".
    elif os.name == "nt" :
         os.system("CLS")
    # If a system doesn't match any of this conditions, it will display an error.
    else :
        print("Function not compatible with the current os.")

def generate_cashiers(environment:object,quantity:int,y_axis:int,x_locations=[],align="auto") :
    """
    Generates the specified quantity of cashiers.

    Args:
        environment (object): Environment where the cashiers will interact.
        quantity (int): Quantity of cashiers.
        y_axis (int): Y axis position in the layout where the cashiers will be located.
        x_locations (list): List of locations in x axis where each cashier will be located.
        algin (str): "auto" generate automatically the x positions for each cashier based in the size of the the screen. This paramentes is "auto" by default. If it is changed, it will be necessary to provide x_locations list.
    """

    from entities import Cashier    # Agent
    screen_width = environment.screen.width
    max_quantity = int((screen_width-2) // 3)   # Calculates the maximum quantity that is possible in for the current layout.
    
    if quantity > max_quantity :    # If the requested quantity is higher than the capacity, it prints a color warning for user and stops the execution.
        raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La cantidad máxima de cajeros es {colors.Regular.bold}{max_quantity}{colors.Text.end}.")

    if align == "auto" :    # If user selected "auto", generates x positions.
        n = (screen_width//2)
        left_list = []
        while n > 0 :
            left_list.append(int(n)-1)
            n -= 3

        n = (screen_width//2) + 3
        right_list = []
        while n < screen_width-1 :
            right_list.append(int(n)-1)
            n += 3

        x_locations = [x for pair in zip_longest(left_list, right_list) for x in pair if x is not None]

    for i in range(0,quantity) :
        cashier = Cashier(environment,x_locations[i],y_axis)
        cashier.cashier_id = i+1
        cashier.spawn()

def check_time_scale(scale:float) :
    """
    Check if the time scale for environment execution is valid. If not, print a warning and stop execution. A valid a scale is greater than 0, but not less or equal than 0.

    Args:
        scale (float):  Scale

    Returns:
        scale (float)
    """
    if scale == 0 :
        raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La escala debe ser igual o mayor a 0.01")
    else:
        return scale

def generate_exponential_arrival_time(n:int,m:int):
    """
    Generate a list of arrival times using numpy.random.exponential.

    Args:
        n (int): Number of times to generate.
        m (int): Average arrival time in seconds.

    Returns:
        arrival_times (list): List of arrival times.
    """
    arrival_times = []
    for i in range(n) :
        arrival_time = np_random.exponential(m)
        if i == 0 :
            arrival_times.append(round(arrival_time,1))
        else :
            arrival_times.append(round(arrival_times[i-1]+arrival_time,1))
    return arrival_times

def generate_cashier_queue(screen:object,cashier:object):
    from elements import Queue  # Queue class generates the queue tiles as object.
    for i in range(cashier.y_location,28) :
        Queue().set_in_screen(screen,cashier.x_location+1,i)

def random_customer_kind(p_observer_kind:float) :
    if random() < p_observer_kind :
        return "observer"
    else :
        return "regular"