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
def print_logo() -> None:
    '''
    Prints some ascii art to the terminal.  
    This is just something for me.
    '''

    return print('''
      ::::::::       ::::::::      :::    ::: 
    :+:    :+:     :+:    :+:     :+:    :+:  
   +:+            +:+            +:+    +:+   
  :#:            +#+            +#+    +:+    
 +#+   +#+#     +#+            +#+    +#+     
#+#    #+#     #+#    #+#     #+#    #+#      
########       ########       ########        
''')

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

def get_next_semester(provided_date) -> list:
    """
    Returns the date of the incoming semester based on when this program is run
    """

    # gets the current date from your system
    current_semester = str(date.today())

    # can uncomment and set this date to anything for demonstration purposes
    if provided_date is not None:
        current_semester = provided_date

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

    # this basically just scans through the 3d dictionary 
    # and gets the total classes and number of semester
    for dict_year in classes_per_semes:

        current_year = classes_per_semes.get(dict_year)

        for dict_semester in current_year:
            total += current_year.get(dict_semester)
            num_of_semesters += 1
            pass
    
    # +1 because python's int() conversion doesn't round up, it chops off decimals
    average = int(total / num_of_semesters) + 1 
    print(f"Maximum number of classes to be scheduled per semester: {average}\n")

    return average

def create_class_database(excel_data) -> dict:
    """
    Used to figure out how many of each individual class should be scheduled in a semester.

    This function creates a dictionary of lists, with one item being the amount of times taught, 
    and the other being the semester that the class was added to this "database"

    This function only stores the most recent instance of a class appearing in the data.

    This function could be made more robust by counting EVERY semester that the class is held and taking 
    an average, but this is what I was able to implement
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
    Used to insert classes into a pandas dataframe.  
    
    Generally this is just used to clean up the input field when inserting something into the table
    """

    return [     
            # set the start and end date to be of the new semester
            # convert the StartTime and EndTime to standard time
            # leave everything else as is

            semester_start, semester_end, row.Course, row.Section, 
            row.ClassSchedDescrip, prof_name, row.Days, start_time, 
            end_time, row.Cr, row.Max

            ]

def project_classes(excel_data, num_of_semesters, provided_date) -> pd:
    """
    This process is the cumulation of many functions written previously.

    This function will take in the data from the previous classes and 
    schedule the classes a num_of_semesters amount into the future.
    """

    projected_data = pd.DataFrame(columns=get_column_order() )

    # retrieve the current semester based on when this script is run
    semester_start = get_next_semester(provided_date)

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


            """
            UNIMPLEMENTED
            i wanted to have this to keep it so that a class is only scheduled forward if 
            the class is normally scheduled in that semester period

            I ran into some bugs when using it, but i didnt have time to iron them out. 
            """
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

    return projected_data

def create_prof_database(excel_data) -> dict:
    """
    Creates a "database" of classes and their associated professors

    if a professor has taught a class, it gets put into that class's associated list

    this dictionary : list relationship is used later to determine what professor 
    should teach a class

    BIG THING TO NOTE:
    this database allows the same prof to be added to the database multiple times.
    this was my basic solution to incorporate professor weighting (if a professor 
    has taught class more times, then prefer them over another prof)
    """
    # this is how our professor "database" will be formatted:
    # it is a dictionary of lists
    # example: {"ITT-123" : ["prof one", "prof two", etc]}
    prof_database = {}


    for row in excel_data.itertuples(index=False):
        
        semester = str(row.ClassStart)[5:7]
        course = str(row.Course)
        professor = str(row.TeacherDescrip)
        
        # retrieve the dictionary at position {course}, it will 
        # return None if there is no associated item
        current_item = prof_database.get(course)

        # if the class is spring/fall then let it through, ignore exceptions
        if semester == '01' or semester == '09':
            pass
        else:
            continue 
        
        # if class doesn't exist in our dictionary then create it
        if current_item is None:
            prof_database.update( {course: []} )
            current_item = prof_database.get(course)

        # "--" is the placeholder professor name within the database and excel sheet 
        # add extra handling here if there are more cases
        if professor == "--" or professor == None:
            continue
        
        # if all other conditions clear, then add the professor to the list
        current_item.append(professor)

    return prof_database

def assign_profs(excel_data, projected_classes) -> pd:
    """
    using the data given from the projected classes function,
    this function aims to assign a professor to each class
    
    it creates a new table and iterates through a database 
    of professors to decide who to assign to each class.

    SOMETHING TO NOTE:
    the way the professor is selected will follow a predetermined 
    path every time it is run in the program's current state. 
    This is because it just cycles through a list created in 
    create_prof_database().  a way to make it more random could be 
    to select a random entry through this list.
    """
    
    prof_database: dict[str : list] = create_prof_database(excel_data)
    # creates a new dataframe with the columns that we have used previously  
    prof_schedule = pd.DataFrame(columns=get_column_order() )

    # sort values by course to allow the function to run smoother
    projected_classes = projected_classes.sort_values(by="Course", ascending=True)
    
    # enumerator is created to assign an index for each item in the table
    enumerator = 0

    # iterate through our projected list  
    for row in projected_classes.itertuples(index=False):
    
        class_name = str(row.Course)
        # uses the class_name as a key to search the created dictionary
        professor = prof_database.get(class_name)
        
        # if there is no professor, just assign the class and mark the professor as "--"
        if professor is None:
            prof_schedule.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, "--", row.StartTime, row.EndTime)

        else:
            # note that professor[0] is what is being passed, this is explained below
            prof_schedule.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, professor[0], row.StartTime, row.EndTime)
            
            # once a professor is selected, then cycle through the list by appending
            # the current prof to the end and removing its entry at position [0]
            professor.append(professor[0])
            professor.pop(0)

        # wether the prof exists or not, increment the enumerator
        enumerator += 1

    # reorder the class schedule to prioritize 
    prof_schedule = prof_schedule.sort_values(by=["ClassStart", "Course", "Max"], ascending=[True, True, False])

    return prof_schedule

def get_hour(time) -> int:
    """
    from the format: hh:mm:ss return the hour as an int
    """
    return int(str(time)[:2])

def increment_times(start_time, end_time, hours) -> time:
    """
    this function takes 2 times and increments them each by the amount {hours}

    it will roll back any times that exceed 5pm to 9am

    i made this function before i knew how to use datetime objects properly,
    so this code isn't great and could be a lot better....

    IMPORTANT TO NOTE:
    this function assumes that the latest start time for a class is 5pm as seen in the if statement

    If this ever changes then this function will have to change accordingly
    """

    # convert objects to a string, and from there convert to a list... 
    new_start = list(str(start_time))
    new_end = list(str(end_time))

    # take the first two items of the list (the hours), convert them to an int, 
    # and add the determined amount of hours to both
    start_first_two = int(f"{new_start[0]}{new_start[1]}") + hours
    end_first_two = int(f"{new_end[0]}{new_end[1]}") + hours

    # roll back the hours to 9am if the start time exceeds 5pm
    if start_first_two > 17:
        start_first_two -= 8
        end_first_two -= 8

    # take the hour and concatenate it into the remaining parts of that original time 
    new_start = dt_time(start_first_two, int(f"{new_start[3]}{new_start[4]}") )
    new_end = dt_time(end_first_two, int(f"{new_end[3]}{new_end[4]}") )

    return  new_start, new_end

def get_new_timeslot(class_start, class_end, previous_end):
    """
    takes class start and end time for a class, and based on the previous 
    class's end time will get a new time.

    since GCU's classes tend to work in 2 hour blocks i decided to increment the time by 2 hours 
    """

    class_end_hour = get_hour(class_end)
    prev_end_hour = get_hour(previous_end)

    # incorporates logic to ensure that the previous class's end time cannot 
    # overlap with the new class's start time
    hours_to_add = get_hour(prev_end_hour - class_end_hour) + 2

    new_start, new_end = increment_times(class_start, class_end, hours_to_add)

    return new_start, new_end

def check_prof_conflicts(class_data):
    """
    This function will take a completed list of professors and check for conflicts in their schedules.

    it completes this task by going through the following process:
        for every semester,
        for every professor,
        for every day of the week that professor is scheduled to teach,
        iterate through every class
    """

    # this variable is purely to display how many conflicts arise within the function, not required
    conflicts = 0

    for semester, dataset in class_data.groupby('ClassStart'):

        for professor, schedule in dataset.groupby('TeacherDescrip'):

            for days, classes in schedule.groupby('Days'):
                # sort each prof's schedule by StartTime, the plan is to iterate through the classes 
                # and increment the times forward and KEEP incrementing them until there are no more conflicts
                sorted_classes = classes.sort_values(by="StartTime", ascending=True)

                # This value will contain the latest end time and compare it to the future end time
                latest_end = None

                for row in sorted_classes.itertuples():
                    
                    index = row.Index
                    end_time = row.EndTime

                    # if no latest_end, then assign one
                    if latest_end is None:
                        latest_end = end_time
                        continue

                    # if the incoming class's StartTime is greater than the prev class' end time, then 
                    elif row.StartTime < latest_end:
                        # if conflict arrises, get a new timeslot
                        new_start, new_end = get_new_timeslot(row.StartTime, end_time, latest_end)

                        # reschedule the class at its previous position, but with the new time
                        class_data.loc[index, 'StartTime'] = new_start
                        class_data.loc[index, 'EndTime'] = new_end

                        # reassign the end time for 
                        end_time = new_end

                        # increment conflict when conflict
                        conflicts += 1

                    # whichever time is bigger becomes the new latest_end for comparison
                    latest_end = max(latest_end, end_time)

    # reorder the dataframe to become the final schedule
    final_schedule  = class_data.sort_values(by=["ClassStart", "Course", "Max"], ascending=[True, True, False])

    return final_schedule, conflicts

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

def convert_time(dataframe) -> pd:
    """
    recreates a dataframe and converts the military time into standard time

    everything else stays the same

    not a necessary function, but just one to make it look nice
    """
    new_dataframe = pd.DataFrame(columns=get_column_order() )

    enumerator = 0

    for row in dataframe.itertuples():
        new_dataframe.loc[enumerator] = schedule_class(row, row.ClassStart, row.ClassEnd, row.TeacherDescrip, convert_std_time(row.StartTime), convert_std_time(row.EndTime) )

        enumerator += 1

    return new_dataframe

def generate_dots(message, how_many) -> None:
    """
    Just a cheeky little function that makes the preview look
    like it takes more time to load, this was kinda just used for the showcase

    GENUINELY NOT NEEDED I JUST MADE THIS FOR FUN 
    """
    for dot in range(0,how_many+1):
        print(f"\r{message}", end='')
        message = message + '.'
        time.sleep(0.5)
    print()
    return

def export_xml(dataframe, xml_name) -> None:
    """
    Takes a pandas dataframe and exports it as an XML file
    """
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
    """
    Takes a pandas dataframe and exports it as an excel file
    """
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
    print_logo()

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
    
    # create a copy of the original data to avoid accidental alteration
    temp_excel_data = excel_data.copy()

    # change how many semesters we want to project in advance
    num_of_semesters = 3
    print(f"Project the schedule {num_of_semesters} semesters in advance.\n")

    # Provide a date for the program to run in, 
    # mainly used for testing purposes
    provided_date = None

    # projects the excel data forward and returns a pandas dataframe
    print("Begin projection...")
    projected_classes = project_classes(temp_excel_data, num_of_semesters, provided_date)
    #export_xml(projected_classes, "step1_project_classes")
    print("Finished projecting Professors")
    
    # assign a professor for each class in the projected data
    print("Begin assigning professors...")
    assigned_prof_classes = assign_profs(temp_excel_data, projected_classes)
    #export_xml(assigned_prof_classes, "step2_assign_professors")
    print("Assigned professors.\n")
    
    # resolve any conflicts that may have arrisen since the class was scheduled
    print("Check for scheduling conflicts...")
    schedule, num_of_conflicts = check_prof_conflicts(assigned_prof_classes)
    print(f"{num_of_conflicts} conflicts resolved.\n")
    
    # convert the time from military to standard
    final_schedule = convert_time(schedule)

    generate_dots("Generating preview", 3)
    print(final_schedule)
    
    # This was something i used a lot during testing, it copied the whole output to my clipboard.
    # it did have issues when using it on Linux, so use it if you want.
    '''schedule.to_clipboard(index=False)'''

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