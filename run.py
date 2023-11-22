""" Imports gspread which allows program to access google spreadsheet """
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

# All the code above was used during Code Institute Code along project
# "Love Sandwiches" to allow access to google API's, credits in README.md


def get_user_input():
    """
    Get input from user used to calculate the cost of the car
    """
    while True:
        print("Please enter the following information in order: ")
        print("Price of car, Wage(monthly), Car make, time for financing(in months),")
        print(" expected interest rate(if none provided 8% will be used")
        print("Example: 2000,1000,bmw,30,5")
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
    e = "Unknown error"
    try:
        if len(input_data) < 4:
            raise ValueError(f"3 values required, you input {len(input_data)}")
        if len(input_data) == 5:
            interest_rate = input_data[4]
        else:
            interest_rate = 8
            # Adds default interest rate in case user did not enter interest rate
            input_data.append(interest_rate)

        cost_of_car = input_data[0]    #Assigning values to increase readability
        wage = input_data[1]
        carmake = input_data[2]
        months_to_finance = input_data[3]
        for data in input_data:
            if carmake.isnumeric():
                raise ValueError(f"Car make was entered as a {carmake}")
            if float(interest_rate) > 30:
                raise ValueError("Financing with a rate above 30% should be avoided")
            if (data in[cost_of_car, wage ,months_to_finance]) and not data.isnumeric():
                raise ValueError(
                    f"Only input whole numbers besides for interest rate, you input {data}")
            if int(months_to_finance) > 180:
                raise ValueError("You cannot finance cars for more than 15 years")

    except ValueError as e:
        print(f"{e}, please try again.\n")
        return False

    return input_data


def check_resale_value(data):
    """
    This function will cross-check user-input car maker value with 
    some set values from spreadsheet to retrieve it's resale value after
    3 years, should the user decide to sell. 
    ***NOT BASED ON REAL VALUES, THIS PROGRAM IS FOR EDUCATIONAL USE ONLY***
    If carbrand is not found in spreadsheet the default resale value is set to 40%. 
    While not used in calculations, most car dealership provide
    a type of financing that is based on resale value 
    after 2-3 years of use. This will help an uninformed
    user what kind of value to expect in a worst case scenario.
    """
    carmake_worksheet = SHEET.worksheet("Carbrand")
    carbrands = carmake_worksheet.row_values(1)[1:6]
    carmake = data[2]
    index = 0
    resale_value = 40
    for car in carbrands:
        if car == carmake:
            resale_value = int(carmake_worksheet.cell(2, index +2).value)
            print(f"Based on our research, used {carmake}s sell for {resale_value}%")

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
    print("Your data is being updated...\n")
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
    downpayment = price*0.2
    # Calculates 20 percent of the price of the car
    data.append(downpayment)
    left_to_finance = price - downpayment
    monthly_cost = round((left_to_finance/ data[3]) * data[4])
    # Calulates cost of car divided by number of months times the interest rate
    data.append(monthly_cost)
    print(f"Most contries require at least a 20 percent downpayment, which would be {downpayment}")
    print(f"The calculated monthly cost will be: {monthly_cost}!\n")
    can_afford = ""
    if monthly_cost <= (wage * 0.3):
        print("With a 20 percent downpayment, it seems you can afford this car!")
        can_afford = "Yes"
    elif monthly_cost <= (wage*0.4):
        print("You might be able to afford this car. Please check with your car dealership,")
        print("also make sure you are financially prepared for any unexpected costs,")
        print("such as repairs or medical emergencies.")
        can_afford = "Maybe"
    else:
        print("Sorry! Looks like you cannot afford this car based on the data you entered.")
        print("try changing the length of finance or use a bigger downpayment!")
        print(f"You can always check with your local {data[2]} dealership for further assistance!")
        can_afford = "No"
    data.append(can_afford)
    return data


def main():
    """
    This is the main function that runs all the functions
    necessary to use the program
    """
    input_data = get_user_input()
    input_data.append(check_resale_value(input_data))
    update_worksheet(input_data, 'Finance')
    complete_data = calculate_costs(input_data)
    update_worksheet(complete_data, 'Result')
    print("Your results have been saved in worksheet: Result")
    print("Thanks for using CarLoanCalculator!")
    print("You can run the calculator again by pressing 'RUN PROGRAM'!")


main()
