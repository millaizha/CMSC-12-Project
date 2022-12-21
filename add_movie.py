import PySimpleGUI as sg
from datetimerange import DateTimeRange
from datetime import datetime
import files
import change_window

# Function to add movie
def addMovie(movies, booked):
    addMovieLayout = [
                    [sg.T("Enter Movie name: "), sg.Input(key = "-NAME-", do_not_clear = True, size = (20,1))],
                    [sg.T("Enter Movie Genre: "), sg.Input(key = "-GENRE-", do_not_clear = True, size = (20,1))],
                    [sg.T("Choose Parental Rating: "), sg.Radio("G", "RESTRICT", key = "-G-", default = True), sg.Radio("PG", "RESTRICT", key = "-PG-"), sg.Radio("SPG", "RESTRICT", key = "-SPG-"), sg.Radio("R18", "RESTRICT", key = "-R18-")],
                    [sg.T("Choose Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                    [sg.T("Choose Date: "), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                    [sg.T("Enter Start Time: "), sg.Input(key='-STARTHOUR-', size=(5,1)), sg.T(":"), sg.Input(key='-STARTMIN-', size=(5,1)), sg.Radio("AM", "START12H", key = "-STARTAM-", default = True), sg.Radio("PM", "START12H", key = "-STARTPM-")],
                    [sg.T("Enter End Time: "), sg.Input(key='-ENDHOUR-', size=(5,1)), sg.T(":"), sg.Input(key='-ENDMIN-', size=(5,1)), sg.Radio("AM", "END12H", key = "-ENDAM-", default = True), sg.Radio("PM", "END12H", key = "-ENDPM-")],
                    [sg.T("Enter Movie Price: "), sg.Input(key = "-PRICE-", do_not_clear = True, size = (20,1))],
                    [sg.Button("Add Movie"), sg.Button("Cancel")]
                    ]

    addMovie = sg.Window("Add Movie", addMovieLayout, modal = True)

    # To check if all required boxes have inputs
    input_key_list = [key for key, value in addMovie.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:
        event, values = addMovie.read()

        if values["-G-"]:
            restrict = "G"
        elif values["-PG-"]:
            restrict = "PG"
        elif values["-SPG-"]:
            restrict = "SPG"
        elif values["-R18-"]:
            restrict = "R18"

        if values["-1-"]:
            cinema = "1"
        elif values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"
        
        startTime = values["-STARTHOUR-"].zfill(2) + ":" + values["-STARTMIN-"]
        if values["-STARTAM-"]:
            startTime += "AM"
        elif values["-STARTPM-"]:
            startTime += "PM"

        endTime = values["-ENDHOUR-"].zfill(2) + ":" + values["-ENDMIN-"]
        if values["-ENDAM-"]:
            endTime += "AM"
        elif values["-ENDPM-"]:
            endTime += "PM"

        inConflict = False

        if event == sg.WIN_CLOSED:
            exit()

        if event == "Add Movie":
            # If one input is missing
            if not all(map(str.strip, [values[key] for key in input_key_list])):
                sg.popup("Some inputs are missed!")
                continue

            # If the date is in the past or present
            if datetime.now() >= datetime.strptime(values["-DATE-"], "%m-%d-%y"):
                sg.Popup("Please provide a future date.")
                inConflict = True
            # If the time format is wrong
            try:
                bool(datetime.strptime(startTime, "%I:%M%p"))
            except ValueError:
                sg.Popup("Start time has a wrong time format.\nPlease follow the format 'HH:MM AM/PM'")
                inConflict = True
                continue
            try:
                bool(datetime.strptime(endTime, "%I:%M%p"))
            except ValueError:
                sg.Popup("End time has a wrong time format.\nPlease follow the format 'HH:MM AM/PM'")
                inConflict = True
                continue

            # If the end time is earlier than the start time
            if datetime.strptime(startTime, "%I:%M%p") > datetime.strptime(endTime, "%I:%M%p"):
                sg.Popup("End time is earlier than the start time.")
                inConflict = True
                continue

            # If there is conflict in time schedule
            for k, v in movies.items():
                if v[3] == cinema and v[4] == values["-DATE-"] and (startTime in DateTimeRange(v[5], v[6]) or endTime in DateTimeRange(v[5], v[6])):
                    sg.Popup(f"This movie will be in conflict with {k} - {v[0]} [Cinema {v[3]}]: {v[4]} {v[5]} - {v[6]}.")
                    inConflict = True
                
            # If all details are valid 
            if all(map(str.strip, [values[key] for key in input_key_list])) and not inConflict:
                addMovie.close()
                addMovieInfo(movies, booked, restrict, cinema, startTime, endTime, values)
                change_window.goToMenu("Admin")
                break
        elif event == "Cancel":
            addMovie.close()
            change_window.goToMenu("Admin")
            break

#  Function to save movie to file
def addMovieInfo(movies, booked, restrict, cinema, startTime, endTime, values):
    with open("movies.txt", "r") as f:
        intMovieID = int(f.readline()) + 1

    movieID = str(intMovieID).zfill(4)

    movies[movieID] = [values["-NAME-"], values["-GENRE-"], restrict, cinema, values["-DATE-"], startTime, endTime, int(values["-PRICE-"])]
    booked[movieID] = []

    files.addMovieToFile(movies, booked)