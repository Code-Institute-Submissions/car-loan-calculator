import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('carloancalculator')

# Code above was used during Code Institute Code along project
# "Love Sandwiches" to allow access to google API's, credits in README.md


def get_user_input():
    """
    Get input from user used to calculate the cost of the car
    """
    while True:
        print("Please enter the following information in order: ")
        print("Price of car, Wage(monthly), Car make, time for financing(in months),")
        print(" expected interest rate(if none provided 8% will be used")
        print("Example: 2000,200,Toyota,6,5")
        data = input("Enter your data here:\n")
        input_data = data.split(',')

        if validate_input(input_data):
            print("\nData was entered successfully")
            break
    cost_of_car = int(input_data[0])
    wage = int(input_data[1]) 
    carmake = input_data[2].upper()
    finance_length = int(input_data[3])
    interest_rate = float(input_data[4])
    valid_data = [cost_of_car, wage, carmake, finance_length, interest_rate]
    return valid_data


def validate_input(input_data):
    """
    Validates users input data to make sure the program has all
    the correct data it needs to run!
    """
    try:
        if len(input_data) < 4:
            raise ValueError(f"3 values required, you input {len(input_data)}")
        elif len(input_data) == 5:
            interest_rate = input_data[4]
        else: 
            interest_rate = 8
            input_data.append(interest_rate)    # Adds default interest rate in case user did not enter interest rate

        cost_of_car = input_data[0]    #Assigning values to increase readability
        wage = input_data[1]
        carmake = input_data[2]
        months_to_finance = input_data[3]
        
        for data in input_data:
            index = 0
            if carmake.isnumeric():
                raise ValueError(f"Car make was entered as a {carmake}")
            elif float(interest_rate) > 30:
                raise ValueError(
                    f"Any financing with a rate above 30% should be avoided")
            elif (data == cost_of_car or data == wage or data == months_to_finance) and not data.isnumeric():
                raise ValueError(
                    f"Only input whole numbers for cost, wage and months to finance, you input {data}")
            elif int(months_to_finance) > 180:
                raise ValueError(
                    f"You cannot finance cars for more than 15 years")
        
    except ValueError as e:
        print(f"{e}, please try again.\n")
        return False

    return input_data


def check_resale_value(data):
    """
    This function will cross-check user-input car maker value with 
    some set values from spreadsheet to retrieve it's resale value after
    3 years, should the user decide to sell. If carbrand is not found in spreadsheet 
    the default resale value is set to 40%.
    """
    carmake_worksheet = SHEET.worksheet("Carbrand")
    carbrands = carmake_worksheet.row_values(1)[1:6]
    carmake = data[2]
    index = 0
    resale_value = 40
    for car in carbrands:
        if car == carmake:
            resale_value = int(carmake_worksheet.cell(2, index +2).value)

        else:
            index += 1
    if resale_value == 40:
        print(f"{carmake} is not among our known car brands, resale value is set to 40%")
    return resale_value
            

def update_worksheet(data, worksheet):
    """
    This function updates the specified worksheet with information provided. 
    Will be used to update worksheets "Finance" as well as "Results".
    """
    print(f"{worksheet} is being updated...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"Data was added to {worksheet}\n")

def calculate_costs(data):
    """
    Purpose of this function is to check what the cost of the car will be to calculate 
    how much the car will cost per month and see if the user can actually afford this car.
    """
    price = data[0]
    wage = data[1]
    downpayment = price*0.2 # Calculates 20 percent of the price of the car 
    left_to_finance = price - downpayment
    monthly_cost = round((left_to_finance/ data[3]) * data[4]) # Calulates cost of car divided by number of months times the interest rate
    data.append(monthly_cost)
    print(f"Most contries require at least a 20 percent downpayment, which would be {downpayment}.\n")
    print(f"The calculated monthly cost will be: {monthly_cost}!\n")
    if monthly_cost <= (wage * 0.3):
        print(f"With a 20 percent downpayment, it seems you can afford this car!")
        
        
    elif monthly_cost <= (wage*0.4):
        print("You might be able to afford this car. Please check with your car dealership,")
        print("also make sure you are financially prepared for any unexpected costs, such as repairs or medical emergencies.")
    else:
        print("Sorry! Looks like you cannot afford this car based on the data you entered.")
        print("try changing the length of finance or use a bigger downpayment!")
        print(f"You can always check with your local {data[2]} dealership for further assistance!")


def main():
    input_data = get_user_input()
    print(input_data)
    input_data.append(check_resale_value(input_data))
    print(input_data)
    update_worksheet(input_data, 'Finance')
    calculate_costs(input_data)

main()