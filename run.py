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
# "Love Sandwiches", credits in README.md


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
    the info it needs to run!
    """
    try:
        if len(input_data) < 4:
            raise ValueError(f"4 values expected, you input {len(input_data)}")
        wage = input_data[0]
        carmake = input_data[1]
        months_to_finance = input_data[2]
        interest_rate = input_data[3]
        print(wage, carmake, months_to_finance, interest_rate)
        for data in input_data:
            if carmake.isnumeric():
                raise ValueError(f"Car make was entered as a {carmake}")
            elif float(interest_rate) > 30:
                raise ValueError(
                    f"Any financing with a rate above 30% should be avoided")
            elif (data == wage or data == months_to_finance) and not data.isnumeric():
                raise ValueError(
                    f"Only input whole numbers where asked, you input {data}")

            elif int(months_to_finance) > 180:
                raise ValueError(
                    f"You cannot finance cars for more than 15 years")

    except ValueError as e:
        print(f"{e}, please try again.\n")
        return False

    return True


input_data = get_user_input()
print(input_data)
