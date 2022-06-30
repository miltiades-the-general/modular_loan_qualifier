# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import questionary
from pathlib import Path


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

def save_csv(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    bank_list = []
    # Lender,Max Loan Amount,Max LTV,Max DTI,Min Credit Score,Interest Rate

    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    if len(qualifying_loans) >= 1:
        csv_prompt = questionary.select("Would you like to save the loan data as a .csv file?", choices=["Yes", "No"]).ask()
    else: 
        return "There are no qualifying loans for the prospective borrower"
        

    # if the answer is yes we acquire a file path from the user
    if csv_prompt == 'Yes':
        # the path comes from an open-text prompt that we define as the subfunction
        def csv_path_prompt():
            csv_path = questionary.text("What would you like the path to the .csv file to be? (must list the entire output path, and must end in .csv)").ask()
            csv_path = Path(csv_path)
            return csv_path
        
        # We run this loop until we are given a correct .csv output path
        while True:
            csv_path = csv_path_prompt()
            # we set the csv_path to what is returned from our csv_path_prompt function
            # we check if the path includes a .csv as a quick check to make sure the user did not misspell ".csv"
            # in this step we first string the csv_path, and then we turn it into a list so that we can index the last 4 values
            # we then turn it back into a string to use the .__contains__method
            csv_path_list = list(str(csv_path))[-4:]
            csv_ending_string = "".join(csv_path_list)
            if csv_ending_string == ".csv":
                with open (csv_path, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=",")
                    csvwriter.writerow(header)
                    for item in qualifying_loans:
                        csvwriter.writerow(item)
                break

            else: 
                print("Enter a valid .csv path name")

    # if the answer is "no" we let the user know which lenders the applicant qualifies for in a list
    # the program is ended

    else: 
        for bank in qualifying_loans:
            bank_list.append(bank[0])
        print(f"Your qualifying loans are from {bank_list}")
