from functions import generate_cashiers
import environment

test = environment.Environment()
screen = environment.Screen(test, 30, 30, "  ")

generate_cashiers(test, 15)

test.inactive_cashiers = test.cashiers.copy()
test.cashiers = []

cashiers_per_Q = [
            [25200, 3],
            [39600, 5],
            [75600, 2],
            [82800,0]
        ]

clock = 25200

for i in range(0, len(cashiers_per_Q)):
    if clock >= cashiers_per_Q[i][0] and clock < cashiers_per_Q[i + 1][0]:
        if len(test.cashiers) == 0:
            for j in range(0, cashiers_per_Q[i][1]):
                print(test.inactive_cashiers[0].x_location)
                test.cashiers.append(test.inactive_cashiers[0])
                test.inactive_cashiers.remove(test.inactive_cashiers[0])
                test.cashiers[j].status = "activating"
        elif cashiers_per_Q[i][1] - len(test.cashiers) < 0:
            for j in range(1, abs(cashiers_per_Q[i][1] - len(test.cashiers)) + 1):
                test.cashiers[-j].open_queue = False
        elif cashiers_per_Q[i][1] - len(test.cashiers) > 0:
            for j in range(0, cashiers_per_Q[i][1] - len(test.cashiers)):
                test.cashiers.append(test.inactive_cashiers[0])
                test.inactive_cashiers[j].status = "activating"
                test.inactive_cashiers.remove(test.inactive_cashiers[0])

#for cashier in test.cashiers:
#    print(cashier.x_location)