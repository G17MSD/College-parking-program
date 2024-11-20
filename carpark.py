import os
import sys
from time import sleep
import carpark_functions as cp

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_menu():
    print("-------")
    print("Welcome to Calder Parking")
    print("-------")
    print(" ")
    print("1. Register/Retrieve Vehicle")
    print("2. Pay Parking")
    print("3. Admin Panel")
    print("4. Exit")
    print('Car parking fees are as follows:  30 minutes free, then every 15 minutes 33p will be charged')

def main():
    clear_screen()
    display_menu()

    try:
        action = int(input("Choose a menu item: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        sleep(2)
        main()
        return

    if action == 1:
        print(cp.register_vehicles())
        sleep(5)

    elif action == 2:
        print(cp.pay_parking())
        sleep(5)

    elif action == 3:
        print(cp.admin_panel())
        sleep(5)

    elif action == 4:
        clear_screen()
        print("Thank you for using Calder Parking")
        sys.exit()

    else:
        print("Invalid option. Please choose a valid number.")
        sleep(2)
        main()

while True:
    main()
