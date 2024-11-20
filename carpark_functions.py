import json 
from time import sleep
from datetime import datetime
from random import randint

def load_data(file='carpark_data.json'):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "numberplate_list": [],
            "customplate_list": [],
            "money_unpaid": [],
            "money_paid": [],
            "money_charged": []
        }

def save_data(data, file='carpark_data.json'):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def sanitize_numberplate(numberplate):
    return numberplate.upper().replace(" ", "")

def register_vehicles():
    data = load_data()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("---", current_time, '---')
    
    option1 = input('Have you entered a number plate previously? Please enter-(Yes/No) ')
    
    if option1.upper() == 'YES':
        find_vehicle = sanitize_numberplate(input('Please enter your numberplate to retrieve here: '))
        if find_vehicle in data['numberplate_list']:
            sleep(3)
            print(find_vehicle, 'has been located')
        elif find_vehicle in data['customplate_list']:
            print(find_vehicle, 'has been located')
        else:
            print('Vehicle cannot be found :/, please re-enter')
    
    elif option1.upper() == 'NO':
        vehicle_registration = sanitize_numberplate(input('Please enter your car’s numberplate here: '))
        custom_numberplate = input('Is your numberplate custom?(Yes/No) ')
        if custom_numberplate.upper() == 'YES':
            data['money_unpaid'].insert(0, vehicle_registration)
            data['customplate_list'].insert(0, vehicle_registration)
            print('Numberplate has been added in the --Custom-- numberplate database')
        elif custom_numberplate.upper() == 'NO':
            data['numberplate_list'].insert(0, vehicle_registration)
            data['money_unpaid'].insert(0, vehicle_registration)
            print(vehicle_registration, 'has been added into the database')
        else:
            print('Car details invalid :/ ')
    save_data(data)
    return "Thank you for choosing Calder Parking"

def pay_parking():
    data = load_data()
    vehicle_registration1 = sanitize_numberplate(input('Please enter your car’s numberplate here: '))
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    
    print("The current time is", current_time)
    
    if vehicle_registration1 in data['numberplate_list'] or vehicle_registration1 in data['customplate_list']:
        total_time = int(input('Please enter how long you stayed for(In Minutes) '))
        if total_time <= 30:
            total_charge = 0
        else:
            additional_time = total_time - 30
            charge_per_15_minutes = 0.33
            charge_intervals = additional_time // 15
            total_charge = charge_intervals * charge_per_15_minutes
        
        print('Your total charge is: £', round(total_charge, 2))
        payment_details = input('Please enter card number here(16 digits): ')
        
        if len(payment_details) != 16:
            print('Invalid card details given, are you trying to scam us???')
        else:
            print('Payment received!, your numberplate will now be removed from the database')
            data['money_unpaid'].remove(vehicle_registration1)
            data['money_paid'].insert(0,vehicle_registration1)
            data['money_charged'].insert(0,round(total_charge,2))

            if vehicle_registration1 in data['numberplate_list']:
                data['numberplate_list'].remove(vehicle_registration1)
            elif vehicle_registration1 in data['customplate_list']:
                data['customplate_list'].remove(vehicle_registration1)

            receipt_choice = input('Would you like a receipt? ')
            receipt = randint(0, 1234562345675454654334543234) if receipt_choice.upper() == 'YES' else None
            
            if receipt:
                print('Your receipt number:', receipt)
            else:
                print('You have opted for no receipt')

            payment_record = {
                "time": current_time,
                "numberplate": vehicle_registration1,
                "receipt": receipt if receipt else "No receipt",
                "date": current_date
            }
            
            if "payment_records" not in data:
                data["payment_records"] = []
            data["payment_records"].append(payment_record)

            print("Payment record:", payment_record)
            sleep(2)

    else:
        print('Numberplate not found, sorry')

    save_data(data)
    return "Thank you for choosing Calder Parking - Come Again!"

def admin_panel():
    data = load_data()
    pin_number = int(input('Enter the 4 digit pin code here: '))
    if pin_number == 2008:
        print('Hello! Welcome to the admin panel! Here are the following choices: ')
        print("1. Access to all time list of parked cars")
        print("2. List of cars who have not paid")
        print("3. List of money taken")
        print("4. List of currently parked cars")
        admin_choice = int(input('Please enter a number choice here: '))
        
        if admin_choice == 1:
            print(data['money_paid'], data['money_unpaid'])
        elif admin_choice == 2:
            print(data['money_unpaid'])
        elif admin_choice == 3:
            print(data['money_charged'])
        elif admin_choice == 4:
            print(data['numberplate_list'], data['customplate_list'])
    else:
        print('Incorrect PIN code guessed... try again later')

