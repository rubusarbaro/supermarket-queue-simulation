simulation_parameters = {
    # Running parameters
    "print_animation": True,                    # Listo
    "time_scale": 0.005,                        # Listo
    "dynamic_arrival_time": True,               # Listo
    "dynamic_cashier_generation": True,         # Listo
    "dynamic_scanning_time": True,
    "customer_quantity": infinite,              # Listo
    "simulation_time": infinite,                # Listo
    "arrival_time_distribution": "exponential",
    "items_in_cart_distribution": "triangular",

    # Fixed parameters
    "arrival_time": market.Popular_Hours.saturday_modified, # Listo
    "scanning_time": 3,
    "observer_customer_probability": 0.1,                   # Listo
    "cashiers_y_axis": 15,                                  # Listo

    # Variable parameters:
    "cashier_quantity": market.Quartiles.saturday   # Listo
}

"""
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