import functions

class Border :
    none = "  "
    ascii = "██"

class Environment :
    def __init__(self, time_scale=1.0):
        self.screen = None
        self.clock = 0.0
        self.time_scale = time_scale
        self.cashiers = []
        self.customer_count = 0
        self.customers = []

    def start(self) :
        from entities import Customer
        from misc import Label
        from numpy import random
        from time import sleep
        import colors

        arrival_times = []
        for i in range(1000) :
            arrival_time = random.exponential(30)
            if i == 0 :
                arrival_times.append(round(arrival_time,1))
            else :
                arrival_times.append(arrival_times[i-1]+round(arrival_time,1))

        Label("Tiempo:",Label.regular).set_in_screen(self.screen,0,30)
        time_label = Label(str(round(self.clock,2)),Label.regular)

        Label("Siguiente llegada:",Label.regular).set_in_screen(self.screen,0,31)
        arrival_label = Label(str(arrival_times[self.customer_count]),Label.regular)
        arrival_label.set_in_screen(self.screen,11,31)

        self.screen.print_screen()

        while True :
            print_screen = True

            for cashier in self.cashiers :
                match cashier.status :
                    case "busy" :
                        if round(self.clock,1) == cashier.current_customer_complete_time :
                            cashier.release_customer()
                    case "available" :
                        if len(cashier.customer_queue) == 0 :
                            pass
                        elif cashier.customer_queue[0].status == "ready" :
                            cashier.call_customer()

            if round(self.clock,1) == arrival_times[self.customer_count] :
                customer = Customer(self,"regular")
                customer.customer_id = self.customer_count
                customer.spawn(0,28)
                print_screen = True
                self.customer_count += 1
                arrival_label.text = str(arrival_times[self.customer_count])
                arrival_label.set_in_screen(self.screen,11,31)
                

            if len(self.customers) == 0 :
                pass
            else :
                for customer in self.customers :
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

            time_label.text = str(round(self.clock,2))
            time_label.set_in_screen(self.screen,4,30)

            if print_screen :
                self.screen.print_screen()

            sleep(0.1*self.time_scale)
            self.clock += 0.1

class Screen :
    def __init__(self, environment: object, width: int , height: int, border_style: str) :
        self.width = width
        self.height = height
        self.border_icon = border_style
        self.environment = environment

        self.link_environment()
        self.layout = self.build_layout()
    
    def link_environment(self) :
        self.environment.screen = self

    def build_layout(self) :
        ud_border = []
        for x in range(0, self.width) :
            ud_border.append(self.border_icon)
        
        layout = []
        layout.append(ud_border.copy())

        for y in range(0, self.height-2) :
            row = []
            row.append(self.border_icon)

            for z in range(0, self.width-2) :
                row.append("  ")
            row.append(self.border_icon)
            layout.append(row)

        layout.append(ud_border.copy())
        return layout

    def print_screen(self) :
        import emoji
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
