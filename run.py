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
            print("Data was entered successfully")
            break
    wage = int(input_data[0]) 
    carmake = input_data[1].upper()
    finance_length = int(input_data[2])
    interest_rate = float(input_data[3])
    final_data = [wage, carmake, finance_length,interest_rate]
    return final_data


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


def check_resale_value(data):
    """
    This function will cross-check user-input car maker value with 
    some set values from spreadsheet to retrieve it's resale value after
    3 years, should the user decide to sell. If carbrand is not found in spreadsheet 
    the default resale value is set to 40%.
    """
    carmake_worksheet = SHEET.worksheet("Carbrand")
    carbrands = carmake_worksheet.row_values(1)[1:6]
    carmake = data[1]
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



def main():
    input_data = get_user_input()
    print(input_data)
    input_data.append(check_resale_value(input_data))
    print(input_data)
    update_worksheet(input_data, 'Finance')

main()