import os

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
    screen_width = environment.screen.width
    max_quantity = int((screen_width-2) // 3)
    
    if quantity > max_quantity :
        import colors
        raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La cantidad máxima de cajeros es {colors.Regular.bold}{max_quantity}{colors.Text.end}.")
    
    from entities import Cashier

    if align == "auto" :
        from itertools import zip_longest

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

def check_time_scale(self, scale) :
    if scale == 0 :
        import colors
        raise Exception(f"{colors.Bold.red}Error:{colors.Text.end} La escala debe ser igual o mayor a 0.01")
    else:
        return scale
    
def generate_cashier_queue(screen:object,cashier:object):
    from elements import Queue
    for i in range(cashier.y_location,28) :
        Queue().set_in_screen(screen,cashier.x_location+1,i)