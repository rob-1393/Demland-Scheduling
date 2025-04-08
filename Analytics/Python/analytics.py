"""
Table Analytics Script

Authors: Jackson Sievers, Robert Adams

"""

import os
import time
import pandas as pd
import calendar
from datetime import date
from datetime import time as dt_time

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

def get_column_order():
    return [
    "ClassStart", "ClassEnd", "Course", "Section", "ClassSchedDescrip", 
    "TeacherDescrip", "Days", "StartTime", "EndTime", "Cr", "Max"
    ]

def reorder_excel(excel_data) -> pd:
    """
    Cleans and reorders the columns of the Excel data.
    Returns a sorted pandas DataFrame.
    """
    
    # drop unwanted columns
    excel_data.drop(columns=["AgreementNumber", "SchedID", "DeliveryMethod", "Reg", "Email", "SecondaryTeachers"], inplace=True)

    # reorder the columns
    new_order = get_column_order()
    
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
    #current_semester = "2025-09-01"

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
    
def get_max_classes_per_semester(excel_data) -> int:
    """
    This function will create a 3d dictionary of how many classes were scheduled in each semester in each year.
    The dictionary will then be used to calculate an average amount of classes to be scheduled in our projected data.

    there is probably a much better way to write this using different functions provided with pandas, but this works...
    """

    # amount of time classes have been taught per semester (3d dictionary)
    # this will be used to calculate an average amount of classes to be scheduled
    # example: {2025 : {09 : 100} }
    classes_per_semes = {}

    # iterate through each row in the table
    # i use continues in here a lot to cut the loop off early 
    for row in excel_data.itertuples(index=False):
        
        # extracts the year and month from the ClassStart of the current item
        year = str(row.ClassStart)[:4]
        semester = str(row.ClassStart)[5:7]

        # due to summer classes having a much more sporatic schedule, excluding 
        # them from this calculation produces more consistent results
        if semester == '01' or semester == '09':
            pass
        else:
            continue

        # if no dictionary exists for the current item's year, then create one 
        # and mark that a class has been scheduled
        if classes_per_semes.get(year) is None:
            classes_per_semes.update( {year: {semester:1}} ) 
            continue
        
        # this variable is mainly created to increate readability in checks below 
        working_year = classes_per_semes.get(year)

        # within the current year dictionary, if there is no dictionary for the 
        # item's semester, create one and mark that a class has been scheduled
        if working_year.get(semester) is None:
            working_year.update( {semester: 1} ) 
            continue

        # if all previous checks have been passed, then there is a year, with a 
        # semester, with a value associated.  This variable retrieves that value
        times_scheduled = working_year.get(semester)

        # update the item and increment its value
        working_year.update( {semester: (times_scheduled + 1)} )   
   
    # variables to calculate average 
    total = 0
    num_of_semesters = 0
    
    """
    REMOVE THIS LATER !!!
    in current data, 2023 brings down the amount of classes 
    that can be scheduled by a lot and its not fun
    """
    classes_per_semes.pop('2023')

    # this basically just scans through the 3d dictionary 
    # and gets the total classes and number of semester
    for dict_year in classes_per_semes:

        current_year = classes_per_semes.get(dict_year)

        for dict_semester in current_year:
            total += current_year.get(dict_semester)
            num_of_semesters += 1
            pass
    
    # +1 because int() conversion doesn't round up, it chops off decimals
    average = int(total / num_of_semesters) + 1 
    print(f"Maximum number of classes to be scheduled per semester: {average}\n")

    return average

def create_class_database(excel_data) -> dict:
    """
    Used to figure out how many of a single class should be scheduled in a semester.

    This function creates a dictionary of lists, that then transforms to a dictionary 
    for use in a later function.

    This function only categorizes the most recent instance of a class being scheduled 
    in the excel data, nothing before that
    """
    # amount of times individual classes have been taught (regular dictionary)
    # example: {ITT321 : [3, 2024-09]}
    class_database = {}

    # reorder the excel data so that the most recent classes start at the top
    excel_data_sorted = excel_data.sort_values(by="ClassStart", ascending=False)

    # iterate through each row in the table
    for row in excel_data_sorted.itertuples(index=False):

        # retrieve course name and year & month
        course = str(row.Course)
        year_and_semes = str(row.ClassStart)[:7]

        # retrieve the current class from the class database
        current_item = class_database.get(course)

        # if class doesn't exist in the database, then create it 
        # when class is created, put 
        if current_item is None:
            class_database.update( {course : [1, year_and_semes]} )
            continue

        # this logic is how i confine the scheduled classes to the most recent instance of the class
        # i only increment and increase the class of the most recent time that its been scheduled
        # everything else gets skipped
        if current_item[1] == year_and_semes:
            increment = current_item[0] + 1

            class_database.update( {course : [increment, year_and_semes]} )
        else:
            pass

    final_database = {}

    # this just clones the class database but makes it a 1 to 1 dictionary 
    # between the classes and the amount scheduled
    for class_ in class_database:
        final_database.update( {class_ : class_database.get(class_)[0]} )

    #print(final_database)
    
    return final_database

def schedule_class(row, semester_start, semester_end, prof_name, start_time, end_time) -> list:
    """
    used in project_classes()

    This function will return a list of class data for projected_data to add to its database
    """

    return [     
            # set the start and end date to be of the new semester
            # convert the StartTime and EndTime to standard time
            # leave everything else as is

            semester_start, semester_end, row.Course, row.Section, 
            row.ClassSchedDescrip, prof_name, row.Days, start_time, 
            end_time, row.Cr, row.Max

            ]

def project_classes(excel_data, num_of_semesters) -> pd:
    """
    Project Classes Forward
    """

    projected_data = pd.DataFrame(columns=get_column_order() )

    # retrieve the current semester based on when this script is run
    semester_start = get_next_semester()

    # retrieve the maximum amount of classes that should be scheduled 
    # each semester based on previous data
    max_classes_per_semes = get_max_classes_per_semester(excel_data)

    # retrieve a dictionary of max amount of times that individual 
    # classes should be scheduled based on previous semesters
    class_database = create_class_database(excel_data)

    # set an enumerator that will be used in the loop below
    enumerator = 0
    
    #excel_data_sorted = excel_data.sort_values(by="ClassStart", ascending=False) #may not need

    # loops through the table an amount equal to num_of_semesters
    for semester in range(0, num_of_semesters):
        this_year = semester_start[0]
        this_month = semester_start[1]
        
        # retrieves semester end date based semester_start
        semester_end = get_semester_end(this_year, this_month)

        print(f"Begin semester {semester + 1} scheduling...")

        # iterate through each row in the table
        for row in excel_data.itertuples(index=False):

            # gets class start month and year from row of table
            class_year = int(str(row.ClassStart)[:4])
            class_name = str(row.Course)
            class_column = "Course"


            # if class has been taught this semester previously, then schedule it forward
            #if this_month == class_month:
                
            # this retrieves every class column in the projected data in the 
            # current year, this is used in the variable below
            filter_class = projected_data[projected_data["ClassStart"] == date_to_str(semester_start)][class_column]

            # this counts the amount of times that the current class has been scheduled in the current dataframe
            current_count = filter_class.value_counts().get(class_name, 0)

            # this retrieves the max amount of times this class has been scheduled based on the class database
            max_count = class_database.get(class_name)

            # if month is the same and year are greater than or the same then just schedule it, 
            # its already been scheduled in the excel sheet
            if this_year <= class_year:
                projected_data.loc[enumerator] = schedule_class(row, date_to_str(semester_start), date_to_str(semester_end), None, row.StartTime, row.EndTime)

            # if the amount of times the class is scheduled is less than the maxi defined before, then schedule it
            elif current_count < max_count:
                projected_data.loc[enumerator] = schedule_class(row, date_to_str(semester_start), date_to_str(semester_end), None, row.StartTime, row.EndTime)
            else:
                continue

            # increment the enumerator after class is addeds
            enumerator = enumerator + 1

            # if we reach the max number of classes per semester, then break the loop
            if enumerator % max_classes_per_semes == 0:
                print(f"Break semester {semester + 1} because it exceeded maximum classes.\n")
                break

        # if the semester is SPRING then change it to be next FALL
        if semester_start[1] == 1:
            semester_start = get_semester_start(semester_start[0], 9)

        # if the semester is FALL then change it to be next SPRING
        elif semester_start[1] == 9:
            semester_start = get_semester_start(semester_start[0] + 1, 1)
        else:
            print("error in project_history(): semester conversion failed")

    print("Finished projecting classes.\n")

    return projected_data

def create_prof_database(excel_data) -> dict:

    # example: {"ITT-123" : ["prof one", "prof two", etc]}
    prof_database = {}
    
    for row in excel_data.itertuples(index=False):
        
        semester = str(row.ClassStart)[5:7]
        course = str(row.Course)
        professor = str(row.TeacherDescrip)
        
        
        current_item = prof_database.get(course)

        if semester == '01' or semester == '09':
            pass
        else:
            continue

        if professor == "--":
            continue
        
        if current_item is None:
            prof_database.update( {course: [professor]} )
            continue
        else:
            current_item.append(professor)

    return prof_database

def assign_profs(excel_data, projected_classes) -> pd:
    
    prof_database = create_prof_database(excel_data)
    prof_schedule = pd.DataFrame(columns=get_column_order() )

    projected_classes = projected_classes.sort_values(by="Course", ascending=True)
    
    enumerator = 0

    for row in projected_classes.itertuples(index=False):
        
        class_name = str(row.Course)
        professor = prof_database.get(class_name)
        
        if professor is None:
            prof_schedule.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, "--", row.StartTime, row.EndTime)

        else:
            prof_schedule.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, professor[0], row.StartTime, row.EndTime)
            professor.append(professor[0])
            professor.pop(0)

        enumerator += 1

    # reorder the class schedule to prioritize 
    prof_schedule = prof_schedule.sort_values(by=["ClassStart", "Course", "Max"], ascending=[True, True, False])

    return prof_schedule

def get_hour(time):
    return int(str(time)[:2])

def increment_times(start_time, end_time, hours):
    new_start = list(str(start_time))
    new_end = list(str(end_time))

    start_first_two = int(f"{new_start[0]}{new_start[1]}") + hours
    end_first_two = int(f"{new_end[0]}{new_end[1]}") + hours

    if start_first_two > 17:
        start_first_two -= 8
        end_first_two -= 8

    new_start = dt_time(start_first_two, int(f"{new_start[3]}{new_start[4]}") )
    new_end = dt_time(end_first_two, int(f"{new_end[3]}{new_end[4]}") )

    return  new_start, new_end

def get_new_timeslot(class_start, class_end, previous_end):

    class_end_hour = get_hour(class_end)
    prev_end_hour = get_hour(previous_end)

    hours_to_add = get_hour(prev_end_hour - class_end_hour) + 2

    new_start, new_end = increment_times(class_start, class_end, hours_to_add)

    return new_start, new_end

def check_prof_conflicts(class_data):
    conflicts = 0

    for semester, dataset in class_data.groupby('ClassStart'):

        for professor, schedule in dataset.groupby('TeacherDescrip'):

            for days, classes in schedule.groupby('Days'):

                sorted_classes = classes.sort_values(by="StartTime", ascending=True)

                latest_end = None

                for row in sorted_classes.itertuples():

                    index = row.Index

                    end_time = row.EndTime

                    if latest_end is None:
                        latest_end = end_time
                        continue

                    elif row.StartTime < latest_end:
                        #print(f"overlap detected at {row}") # Overlap detected

                        new_start, new_end = get_new_timeslot(row.StartTime, end_time, latest_end)

                        class_data.loc[index, 'StartTime'] = new_start
                        #sorted_classes.loc[index, 'StartTime'] =  "LOOK AT ME" #"11:00:00"

                        class_data.loc[index, 'EndTime'] = new_end
                        #sorted_classes.loc[index, 'EndTime'] = "12:45:00"

                        end_time = new_end

                        conflicts += 1

                    latest_end = max(latest_end, end_time)

    final_schedule  = class_data.sort_values(by=["ClassStart", "Course", "Max"], ascending=[True, True, False])

    return final_schedule, conflicts

def generate_dots(message, how_many) -> None:
    """
    Just a cheeky little function that makes the terminal output
    more pretty before printing the preview
    """
    for dot in range(0,how_many+1):
        print(f"\r{message}", end='')
        message = message + '.'
        time.sleep(1)
    print()
    return

def convert_time(dataframe) -> pd:

    new_dataframe = pd.DataFrame(columns=get_column_order() )

    enumerator = 0

    for row in dataframe.itertuples():
        new_dataframe.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, row.TeacherDescrip, convert_std_time(row.StartTime), convert_std_time(row.EndTime) )

        enumerator += 1

    return new_dataframe

def export_xml(dataframe, xml_name) -> None:
    # get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))  

    # define XML file path to be stored
    xml_file_path = os.path.join(script_dir, "exports/XML", f"{xml_name}.xml")

    # create directory if it doesnt exist already
    os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)

    # convert the projected data to XML at that file path
    dataframe.to_xml(xml_file_path, index=False)

    return

def export_excel(dataframe, excel_name) -> None:
    # get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))  

    # define XML file path to be stored
    excel_file_path = os.path.join(script_dir, "exports/Excel", f"{excel_name}.xlsx")

    # create directory if it doesnt exist already
    os.makedirs(os.path.dirname(excel_file_path), exist_ok=True)

    # convert the projected data to excel at that file path
    dataframe.to_excel(excel_file_path, index=False)

    return

def main():

    print('\nBegin scheduling.\n')

    # Get name of the excel sheet : Fall+SpringOnly | TestTable |
    excel_sheet = "on-ground+online_tables"

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
    print(f"Project the schedule {num_of_semesters} semesters in advance.\n")

    # create a copy of the original data to avoid accidental alteration
    temp_excel_data = excel_data.copy()

    # projects the excel data forward and returns a pandas dataframe
    print("Begin projection...")
    projected_classes = project_classes(temp_excel_data, num_of_semesters)
    #export_xml(projected_classes, "step1_project_classes")
    
    # assign a professor for each class in the projected data
    print("Begin assigning professors...")
    assigned_prof_classes = assign_profs(temp_excel_data, projected_classes)
    #export_xml(assigned_prof_classes, "step2_assign_professors")
    print("Assigned professors.\n")
    
    # 
    print("Check for scheduling conflicts...")
    schedule, num_of_conflicts = check_prof_conflicts(assigned_prof_classes)
    print(f"{num_of_conflicts} conflicts resolved.\n")
    
    # convert the time from military to standard
    final_schedule = convert_time(schedule)

    generate_dots("Generating preview", 3)
    print(final_schedule)
    
    # This was something i used a lot during testing, it copied the whole output to my clipboard.
    # it did have issues when using it on Linux, so use it if you want.
    #schedule.to_clipboard(index=False)

    # export the dataframe to an XML file located under /exports
    print("\nExporting schedule to XML...")
    export_xml(final_schedule, "final_schedule")
    print("Finished exporting.\n")

    # export the dataframe to an excel file located under /exports
    print("Exporting schedule to excel...")
    export_excel(final_schedule, "final_schedule")
    print("Finished exporting.\n")

    print("Done.")
    
main()

"""
""" """ = done/to that step

# PROCESSES PLANNED:
#
# Read the data
# Look at previous dates
# Project dates forward >
#   Decide timeframe for data (3 semesters) 
#   Decide what classes should be scheduled
#   Select only most recent classes to project dates forward 
# Decide Professor > 
# Ensure professors' schedule is possible > 
#   If times overlap, set to time/day to a different one
# Convert to XML
#   Reformat data to format below (what i view to be the most important data)
# """