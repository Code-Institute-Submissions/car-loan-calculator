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
        print("Wage(in USD), Car make, time for financing(in years), expected interest rate(if none provided 8% will be used")
        print("Example: 2000, Toyota, 6, 5")
        data = input("Enter your data here:\n")
        input_data = data.split(',')

        if input_data != '':
            print("Data was entered")
            break
    return input_data


data = get_user_input()
print(data)