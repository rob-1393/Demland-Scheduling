"""
Table Analytics Script

Authors: Jackson Sievers, Robert Adams

"""

import os
import pandas as pd
import calendar
from datetime import date

#   function() -> [type] is called type hinting. It doesnt affect the code in any way, 
#   its just a way for me to communicate what the function returns
def get_excel_sheet() -> pd:
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
        print(f"error: File not found at {table_path}")
        return None
    
    except ValueError as e:
        # print any errors that may occur
        print(f"error: {e}")
        return None

def reorder_excel(excel_data) -> pd:
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

def get_semester_start(year, month) -> list:
    """
    Based on provided year and month, return the start date of that semester

    returns a list for ease of manipulation

    Currently only supports spring and fall semester
    """

    # first day of the spring and falls semesters is the 1st monday of that month
    first_day_of_month = date(year, month, 1)

    # you can try to decipher this.... but just trust me that it returns the first monday of the given month..    
    monday = str(((7 - first_day_of_month.weekday()) % 7) + 1)
    
    return [year, month, monday]

def get_semester_end(year, month) -> list:
    """
    Based on provided start date, return the end date of that semester

    returns a list for ease of manipulation

    Currently only supports spring and fall semester
    """

    # spring semester is january (1), so final month is april (4)
    if month == 1:
        month = 4
    # fall semester is september (9), so final month is december (12)
    elif month == 9:
        month = 12
    else:
        print("error: invalid semester")
        return

    sundays = []
    # monthrange() returns 2 values, so [1] gets just that last day of month
    last_day = calendar.monthrange(year, month)[1]

    # iterate through the whole month, if day is sunday then add it to the list
    for day in range(1, last_day + 1):
        if date(year, month, day).weekday() == 6: # sunday = 6
            sundays.append(str(day))

    if month == 4:
        # last day of spring semester is 4th sunday of april
        return [year, month, sundays[3]]
    elif month == 12:
        # last day of fall semester is 2nd sunday of december
        return [year, month, sundays[1]]
    else:
        print("error: something bad happened")
        return

def get_next_semester() -> list:
    """
    Returns the date of the incoming semester based on when this program is run
    """

    # gets the current date from your system
    current_semester = str(date.today())

    # can uncomment and set this date to anything for demonstration purposes
    #current_semester = "2026-09-04"

    # sets the start month of the spring and fall semesters, this can 
    # be added onto later, but the logic below will have to change
    spring_semester = 1
    fall_semester = 9

    # extracts the current month and year from the 
    current_month = int(current_semester.split('-')[1])
    current_year = int(current_semester.split('-')[0])

    # if the current month is before FALL semester starts
    if current_month >= spring_semester and current_month < fall_semester:
        # returns first day of that FALL semester
        return get_semester_start(current_year, fall_semester)

    # if current month is before SPRING semester starts
    elif current_month >= fall_semester and current_month < 13:
        # iterate the year
        current_year = current_year + 1
        # returns first day of that SPRING semester
        return get_semester_start(current_year, spring_semester)

    # if something goes awry throw an error
    else:
        print("error: current month not in range")
        return

def date_to_str(date_list) -> str:
    """
    Takes a list of 3 objects and converts it into a datetime format like so: yyyy-mm-dd
    """

    year = date_list[0]

    # insert a 0 to the beginning if number is single digits 
    if int(date_list[1]) <= 9:
        month = f"0{date_list[1]}"
    else:
        month = date_list[1]

    # ditto with above comment
    if int(date_list[2]) <= 9:
        day = f"0{date_list[2]}"
    else:
        day = date_list[2]

    return f"{year}-{month}-{day}"

def project_history(temp_excel_data, num_of_semesters) -> pd:
    """
    History analytics
    """

    projected_data = pd.DataFrame(columns=[
    "ClassStart", "ClassEnd", "Course", "Section", "ClassSchedDescrip", 
    "TeacherDescrip", "Days", "StartTime", "EndTime", "Cr", "Max"
    ])

    semester_start = get_next_semester()

    enumerator = 0
    
    for semester in range(0, num_of_semesters):
        
        semester_end = get_semester_end(semester_start[0], semester_start[1])

        for row in temp_excel_data.itertuples(index=False):
            start_month = int(str(row.ClassStart)[5:7])
            start_year = int(str(row.ClassStart)[:4])

            if semester_start[1] == start_month:
                # track the amount of classes that are being scheduled in a year (dictionary)
                    # max 500 classes per semester
                    # scan amount of time classes are scheduled in the past and prevent scheduling more than that
                    # also create military time conversion

                projected_data.loc[enumerator] = [
                    date_to_str(semester_start), date_to_str(semester_end), row.Course, row.Section, 
                    row.ClassSchedDescrip, f"John Professor #{enumerator}", row.Days, str(row.StartTime)[:5], str(row.EndTime)[:5], row.Cr, row.Max
                    ]

                enumerator = enumerator + 1

        if semester_start[1] == 1:
            semester_start = get_semester_start(semester_start[0], 9)
        elif semester_start[1] == 9:
            semester_start = get_semester_start(semester_start[0] + 1, 1)
        else:
            print("error: something bad happened")
    
    return projected_data


# might do my dumbass big table idea just to get something rolling since the database isnt setup

def professors_and_classes(excel_data) -> pd:
    # Extracts the professor names and the associated course.
    prof_and_courses = excel_data[['TeacherDescrip', 'Course']]
    
    # Replaces missing professors with filler names.
    # Due to a skill issue with manipulating the spreadsheet directly, the column is made into an array.
    i = 1
    prof_array = prof_and_courses['TeacherDescrip'].to_numpy()
    for index in range(len(prof_array)):
        if prof_array[index] == '--':
            # Function contains name of filler professors and an incremental number.
            prof_array[index] = f"Filler Professor {i}"
            i += 1

    # Places filler professors back into spreadsheet.
    prof_and_courses['TeacherDescrip'] = prof_array
    
    # Contains courses by instructor and instructors by courses, respectively.
    prof_by_courses = prof_and_courses.groupby('Course')['TeacherDescrip'].apply(lambda x: ', '.join(x)).reset_index()
    courses_by_prof = prof_and_courses.groupby('TeacherDescrip')['Course'].apply(lambda x: ', '.join(x)).reset_index()

    return prof_by_courses, courses_by_prof

def main():
    excel_data = get_excel_sheet()
    
    if excel_data is not None:
        excel_data = reorder_excel(excel_data)
    else:
        print("error: No excel data found")
        return
    
    # change how many semesters we want to project in advance
    num_of_semesters = 3

    # create a copy of the original data to avoid accidental alteration
    temp_excel_data = excel_data.copy()

    projected_data = project_history(temp_excel_data, num_of_semesters)

    print(projected_data)
    
    #print(projected_data.to_xml())

    
    #prof_by_courses, courses_by_prof = professors_and_classes(projected_data)

    
    #analyze_history(excel_data)
    #print(profByCourses)
    #print(excel_data)
    
main()

"""
Orange = done/to that step

# PROCESSES NEEDED:
#
# Read the data
# Look at previous dates
# find 
# Project dates forward >
#   Decide timeframe for data (3 semesters) """
#   Decide what classes should be scheduled
#   Select only most recent classes to project dates forward
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
