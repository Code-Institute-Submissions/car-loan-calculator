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
        print("Wage(in USD), Car make, time for financing(in years), ")
        print("expected interest rate(if none provided 8% will be used")
        print("Example: 2000, Toyota, 6, 5")
        data = input("Enter your data here:\n")
        input_data = data.split(',')

        if validate_input(input_data):
            print("Data was entered")
            break
    return input_data


def validate_input(input_data):
    """
    Validates users input data to make sure the program has all
    the correct data it needs to run!
    """
    try:
        if len(input_data) < 3:
            raise ValueError(f"3 values required, you input {len(input_data)}")
        elif len(input_data) == 4:
            interest_rate = input_data[3]
        else: 
            interest_rate = 8
            input_data.append(interest_rate)    # Adds default interest rate in case user did not enter interest rate

        wage = input_data[0]    #Assigning values to increase readability
        carmake = input_data[1]
        months_to_finance = input_data[2]
        
        for data in input_data:
            index = 0
            if carmake.isnumeric():
                raise ValueError(f"Car make was entered as a {carmake}")
            elif float(interest_rate) > 30:
                raise ValueError(
                    f"Any financing with a rate above 30% should be avoided")
            elif (data == wage or data == months_to_finance) and not data.isnumeric():
                raise ValueError(
                    f"Only input nhole umbewrs where asked, you input {data}")

            elif int(months_to_finance) > 180:
                raise ValueError(
                    f"You cannot finance cars for more than 15 years")
        
    except ValueError as e:
        print(f"{e}, please try again.\n")
        return False

    return input_data

def check_resale_value(carmake):
    """
    This function will cross-check user-input car maker value with 
    some set values from spreadsheet to retrieve it's resale value after
    3 years, should the user decide to sell.
    """
    carmake_worksheet = SHEET.worksheet("Carbrand")
    carbrands = carmake_worksheet.row_values(1)[1:6]
    print(carbrands)
    index = 0
    for car in carbrands:
        if car.upper() == carbrands[index]:
            resale_value = []
            resale_value.append(carmake_worksheet.row_values(2)[index])
            print(resale_value, index)

        else:
            print("Not listed")
            index + 1
            


def main():
    input_data = get_user_input()
    print(input_data)
    wage = input_data[0]
    carmake = input_data[1]
    finance_length = input_data[2]
    interest_rate = input_data[3]
    check_resale_value(carmake)

main()