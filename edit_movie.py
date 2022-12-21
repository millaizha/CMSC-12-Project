import PySimpleGUI as sg
from datetimerange import DateTimeRange
from datetime import datetime
import files, change_window

# Function to show movie list to edit 
def editMovie(movies):
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
    movieInfo = {}

    showMovieList = [
                    [sg.T("Select a Movie:")],
                    [sg.T("Search: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Cancel")]
                    ]

    showMovieInfo = [
                    [sg.T("Movie Information:")],
                    [sg.Listbox(movieInfo, size=(50, 7), enable_events = True, key='-MOVIEINFO-')],
                    [sg.Button("Edit Movie Information")],
                    [sg.Button("Clear")]
                    ]
    editMovieLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    editMovie = sg.Window("Edit Movie", editMovieLayout)

    while True:
        event, values = editMovie.read()

        if event == sg.WIN_CLOSED:
            exit()

        # Will filter the movie list box depending on the text in the search bar
        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            editMovie['-MOVIE-'].update(new_values) 
        else:
            editMovie['-MOVIE-'].update(movieList)

        # Adds the information of the movie to the movie information list box
        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}"]
            editMovie["-MOVIEINFO-"].update(movieInfo)

        # Shows the edit information window
        if event == "Edit Movie Information" and bool(movieInfo):
            editMovieInfo(movies, movieKey)
            editMovie['-MOVIEINFO-'].update([])
            movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
            editMovie['-MOVIE-'].update(movieList)
        elif event == "Clear":
            editMovie['-MOVIEINFO-'].update([])
        elif event == "Cancel":
            editMovie.close()
            change_window.goToMenu("Admin")
            break

# Function to edit movie information
def editMovieInfo(movies, movieKey):
    editMovieInfoLayout = [
                    [sg.T("Enter Movie name: "), sg.Input(movies[movieKey][0], key = "-NAME-", do_not_clear = True, size = (20,1))],
                    [sg.T("Enter Movie Genre: "), sg.Input(movies[movieKey][1], key = "-GENRE-", do_not_clear = True, size = (20,1))],
                    [sg.T("Choose Parental Rating: "), sg.Radio("G", "RESTRICT", key = "-G-", default = True), sg.Radio("PG", "RESTRICT", key = "-PG-"), sg.Radio("SPG", "RESTRICT", key = "-SPG-"), sg.Radio("R18", "RESTRICT", key = "-R18-")],
                    [sg.T("Choose Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default=True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-"              )],
                    [sg.T("Choose Date: "), sg.Input(movies[movieKey][4], key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                    [sg.T("Enter Start Time: "), sg.Input(movies[movieKey][5][:2], key='-STARTHOUR-', size=(5,1)), sg.T(":"), sg.Input(movies[movieKey][5][3:5], key='-STARTMIN-', size=(5,1)), sg.Radio("AM", "START12H", key = "-STARTAM-", default = True), sg.Radio("PM", "START12H", key = "-STARTPM-")],
                    [sg.T("Enter End Time: "), sg.Input(movies[movieKey][6][:2], key='-ENDHOUR-', size=(5,1)), sg.T(":"), sg.Input(movies[movieKey][6][3:5], key='-ENDMIN-', size=(5,1)), sg.Radio("AM", "END12H", key = "-ENDAM-", default = True), sg.Radio("PM", "END12H", key = "-ENDPM-")],
                    [sg.T("Enter Movie Price: "), sg.Input(movies[movieKey][7], key = "-PRICE-", do_not_clear = True, size = (20,1))],
                    [sg.Button("Finish Editing Movie"), sg.Button("Cancel")]
                    ]

    editMovieInfo = sg.Window("Edit Movie Info", editMovieInfoLayout, finalize = True)

    input_key_list = [key for key, value in editMovieInfo.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:        
        if movies[movieKey][2] == "PG":
            editMovieInfo.Element("-PG-").update(value = True)
        elif movies[movieKey][2] == "SPG":
            editMovieInfo.Element("-SPG-").update(value = True)
        elif movies[movieKey][2] == "R18":
            editMovieInfo.Element("-R18-").update(value = True)

        if movies[movieKey][3] == "2":
            editMovieInfo.Element("-2-").update(value = True)
        elif movies[movieKey][3] == "3":
            editMovieInfo.Element("-3-").update(value = True)

        if movies[movieKey][5][-2:] == "PM":
            editMovieInfo.Element("-STARTPM-").update(value = True)
        if movies[movieKey][6][-2:] == "PM":
            editMovieInfo.Element("-ENDPM-").update(value = True)

        event, values = editMovieInfo.read()

        inConflict = False

        if event == sg.WIN_CLOSED:
            exit()
        else:
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
        
            startTime = values["-STARTHOUR-"] + ":" + values["-STARTMIN-"]
            if values["-STARTAM-"]:
                startTime += "AM"
            elif values["-STARTPM-"]:
                startTime += "PM"

            endTime = values["-ENDHOUR-"] + ":" + values["-ENDMIN-"]
            if values["-ENDAM-"]:
                endTime += "AM"
            elif values["-ENDPM-"]:
                endTime += "PM"
                
            if event == "Finish Editing Movie":
                if not all(map(str.strip, [values[key] for key in input_key_list])):
                    sg.popup("Some inputs are missed!")
                    continue
                
                if datetime.now() >= datetime.strptime(values["-DATE-"], "%m-%d-%y"):
                    sg.Popup("Please provide a future date.")
                    inConflict = True
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
                if datetime.strptime(startTime, "%I:%M%p") > datetime.strptime(endTime, "%I:%M%p"):
                    sg.Popup("End time is earlier than the start time.")
                    inConflict = True
                    continue
                for k, v in movies.items():
                    if k != movieKey and v[3] == cinema and v[4] == values["-DATE-"] and (
                        startTime in DateTimeRange(v[5], v[6]) or endTime in DateTimeRange(v[5], v[6])):
                        sg.Popup(f"This movie will be in conflict with {k} - {v[0]} [Cinema {v[3]}]: {v[4]} {v[5]} - {v[6]}.")
                        inConflict = True
                if all(map(str.strip, [values[key] for key in input_key_list])) and not inConflict:
                    movies[movieKey] = [values["-NAME-"], values["-GENRE-"], restrict, cinema, values["-DATE-"], startTime, endTime, int(values["-PRICE-"])]
                    editMovieInfo.close()
                    files.updateMovie(movies)
                    break
            elif event == "Cancel":
                editMovieInfo.close()
                break