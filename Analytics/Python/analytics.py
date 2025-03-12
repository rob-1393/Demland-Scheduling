"""
Table Analytics Script

Author: jackson sievers

"""

import os
import pandas as pd

def get_excel_sheet():
    """
    Retrieves the test data Excel sheet from the repository.
    Returns a pandas DataFrame.
    """
    
    try: 
        # Determine base GIT directory (OS agnostic)
        git_directory = os.path.abspath(os.path.join(os.getcwd()))
        
        # Create file path (OS agnostic)
        table_path = os.path.join(git_directory, "Tables", "on-ground+online_tables_[TestTable].xlsx")
        
        # Sheet name (currently default) [either will be "on-ground" or "online"].
        sheet_name = 'on-ground'

        # Read the excel file
        excel_data = pd.read_excel(table_path, sheet_name, engine='openpyxl')
        
        return excel_data
    
    except FileNotFoundError:
        print(f"Error: File not found at {table_path}")
        return None
    
    except ValueError as e:
        # print any errors that may occur
        print(f"Error: {e}")
        return None


def reorder_excel(excel_data):
    """
    Cleans and reorders the columns of the Excel data.
    Returns a sorted pandas DataFrame.
    """
    
    # drop unwanted columns
    excel_data.drop(columns=["AgreementNumber", "SchedID", "DeliveryMethod", "Reg", "Email", "SecondaryTeachers"], inplace=True)

    # reorder the columns
    new_order = [
    "ClassStart", "ClassEnd", "Course", "Section", "ClassSchedDescrip", 
    "TeacherDescrip", "Days", "StartTime", "EndTime", "Cr", "Max"
    ]
    
    excel_data = excel_data[new_order]
    
    # sort the values by classStart
    excel_data = excel_data.sort_values(by="ClassStart", ascending=True)
    
    return excel_data

def analyze_history(excel_data):
    """
    History analytics
    """
    
    
    return excel_data

def main():
    excel_data = get_excel_sheet()
    
    if excel_data is not None:
        excel_data = reorder_excel(excel_data)
    
    
    print(excel_data)
    #print(excel_data.to_xml())

main()

"""
Orange = done/to that step

# PROCESSES NEEDED:
#
# Read the data """
# Look at previous dates
# Project dates forward >
#   Decide timeframe for data (3 semesters)
#   Decide what classes should be scheduled
#   Fix entries where single classes are listed twice under the 2 diff days
# Decide Professor > 
#   More times taught = priority
#   No Professor?  Pull from other database of professors (not created) [optional]
# Ensure professors' schedule is possible > 
#   If times overlap, set to time/day to a different one
"""
# Convert to XML
#   Reformat data to format below (what i view to be the most important data)"""

# | ClassStart | ClassEnd  | Course  | Section | ClassSchedDescription     | Professor    | Days | StartTime   | EndTime     | Cr | Max |
# | 5/6/2024   | 6/23/2024 | ITT-307 | TR1100A | Cybersecurity Foundations | Albert Kelly | W F  | 11:00:00 AM | 12:45:00 PM | 4  | 32  |


# NOTES:
# unsure if i want to modify the data given directly from the excel sheet, or insert each class into another "database"
# may conduct analysis in python and export to other database for storage
# when displaying time, may chop off the extra :00 and convert back from military time 