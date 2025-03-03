"""
Table Analytics Script

Author: jackson sievers

"""

import os
import pandas as pd

def getExcelSheet():
    current_directory = os.getcwd() # Gets the current working directory
    table_path = f'{current_directory}/Tables/on-ground+online_tables_[TestTable].xlsx'   # retrieves the table
    sheet_name = 'on-ground' # Sheet name (currently default) [either will be "on-ground" or "online"].

    excel_data = pd.read_excel(table_path, sheet_name)

    return excel_data

def main():
    excel_data = getExcelSheet()

    print(excel_data)


# process needed:
#
# Read the data
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
# Convert to XML
#   Reformat data to format below (what i view to be the most important data)

# Export an XML document that looks something like this:
# | ClassStart | ClassEnd  | Course  | Section | ClassSchedDescription (name) | Professor    | Days | StartTime   | EndTime     | Cr (credits) | Max (students) |
# | 5/6/2024   | 6/23/2024 | ITT-307 | TR1100A | Cybersecurity Foundations    | Albert Kelly | W F  | 11:00:00 AM | 12:45:00 PM | 4            | 32             |

# NOTES:
# unsure if i want to modify the data given directly from the excel sheet, or insert each class into another "database"
# may conduct analysis in python and export to other database for storage

main()
