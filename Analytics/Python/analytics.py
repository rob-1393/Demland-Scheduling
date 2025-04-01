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
def get_excel_sheet(sheet_name) -> pd:
    """
    Retrieves the test data Excel sheet from the repository.
    Returns a pandas DataFrame.
    """
    
    try: 
        # Determine base GIT directory (OS agnostic)
        git_directory = os.getcwd()

        # Create file path (OS agnostic)
        table_path = os.path.join(git_directory, "Tables", f"{sheet_name}.xlsx")

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
    
    # Change the order of the data
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
    # set each variable to be the respective slot in the list
    year = date_list[0]
    month = int(date_list[1])
    day = int(date_list[2])
    
    # variable:02 ensures that single numbers like 6 are displayed as "06"
    return f"{year}-{month:02}-{day:02}"

def convert_std_time(military_time) -> str:
    """
    Converts a string that is military time to be standard time

    Conversion: hh:mm:ss -> hh:mm am/pm
    """

    # takes first 5 spots from the time, its now hh:mm
    standard_time = str(military_time)[:5]

    # extracting the hour (first 2 digits) and converting to int
    hour = int(standard_time[:2])

    # logic to determine whether the hour is in the AM or PM
    if hour <= 12:
        return f"{standard_time} AM"
    elif hour > 12 and hour <= 24:
        hour = hour - 12
        standard_time = f"{hour:02}{standard_time[2:]}"
        return f"{standard_time} PM"
    else:
        print("error: time conversion failed")
        return

def project_history(temp_excel_data, num_of_semesters) -> pd:
    """
    History analytics
    """

    projected_data = pd.DataFrame(columns=[
    "ClassStart", "ClassEnd", "Course", "Section", "ClassSchedDescrip", 
    "TeacherDescrip", "Days", "StartTime", "EndTime", "Cr", "Max"
    ])

    # retrieve the current semester based on when this script is run
    semester_start = get_next_semester()

    # set an enumerator that will be used later
    enumerator = 0

    # set maximum classes that can be scheduled in each semester
    max_class_per_semes = 500
    
    # loops through the table an amount equal to num_of_semesters
    for semester in range(0, num_of_semesters):
        
        # retrieves semester end date based semester_start
        semester_end = get_semester_end(semester_start[0], semester_start[1])

        # iterate through each row in the table
        for row in temp_excel_data.itertuples(index=False):

            # gets class start month and year from row of table
            start_month = int(str(row.ClassStart)[5:7])
            start_year = int(str(row.ClassStart)[:4])

            # if class has been taught this semester previously, then schedule it
            if semester_start[1] == start_month:
                """
                TODO
                track the amount of classes that are being scheduled in a year (dictionary)
                    max 500 classes per semester
                    scan amount of time classes are scheduled in the past and prevent scheduling more than that
                
                """

                # store data at position enumerator in the dataframe
                projected_data.loc[enumerator] = [
                    
                    # set the start and end date to be of a new semester
                    # clear the professor's name for later step
                    # convert the StartTime and EndTime to standard time
                    # leave everything else as is 

                    date_to_str(semester_start), date_to_str(semester_end), row.Course, row.Section, 
                    row.ClassSchedDescrip, "", row.Days, convert_std_time(row.StartTime), 
                    convert_std_time(row.EndTime), row.Cr, row.Max
                    ]

                # increment the enumerator after class is added
                enumerator = enumerator + 1

                # if we reach the max number of classes per semester, then break the loop
                if enumerator % max_class_per_semes == 0:
                    break

        # if the semester is SPRING then change it to be next FALL
        if semester_start[1] == 1:
            semester_start = get_semester_start(semester_start[0], 9)

        # if the semester is FALL then change it to be next SPRING
        elif semester_start[1] == 9:
            semester_start = get_semester_start(semester_start[0] + 1, 1)
        else:
            print("error in project_history(): semester conversion failed")
    
    return projected_data

# might do my dumbass big table idea to select professors just to get something rolling since the database isnt setup

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

def export_xml(projected_data, xml_name):
    # get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))  

    # define XML file path to be stored
    xml_file_path = os.path.join(script_dir, "exports", f"{xml_name}.xml")

    # create directory if it doesnt exist already
    os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

    # convert the projected data to XML at that file path
    projected_data.to_xml(xml_file_path, index=False)

    return

def main():

    # Get name of the excel sheet : Fall+SpringOnly | TestTable
    excel_sheet = "on-ground+online_tables_[TestTable]"

    # Retrieve excel data and import it to a pandas dataframe
    excel_data = get_excel_sheet(excel_sheet)
    
    # Check if data exists, then reorders the data if there is
    if excel_data is not None:
        excel_data = reorder_excel(excel_data)
    else:
        print("error: No excel data found")
        return
    
    # change how many semesters we want to project in advance
    num_of_semesters = 3

    # create a copy of the original data to avoid accidental alteration
    temp_excel_data = excel_data.copy()

    # projects the excel data forward and returns a pandas dataframe
    projected_data = project_history(temp_excel_data, num_of_semesters)

    print(projected_data)

    """ NOT YET IMPLEMENTED
    # selects professors for the projected classes
    #final_schedule = select_professors(projected_data)
    """

    # define a name for XML file
    xml_name = "schedule"

    # export the protected_data dataframe to a file located under /exports
    #export_xml(projected_data, xml_name)

    print("Done.")
    
main()

"""
""" """ = done/to that step

# PROCESSES PLANNED:
#
# Read the data
# Look at previous dates
# find 
# Project dates forward >
#   Decide timeframe for data (3 semesters) """
#   Decide what classes should be scheduled
#   Select only most recent classes to project dates forward
# Decide Professor > 
#   More times taught = priority
#   No Professor?  Pull from other database of professors (not created) [optional]
# Ensure professors' schedule is possible > 
#   If times overlap, set to time/day to a different one
"""
# Convert to XML
#   Reformat data to format below (what i view to be the most important data)"""