import PySimpleGUI as sg
import files, main, change_window

def deleteMovie(movies, booked):
    deleteMovieLayout = [
                        [sg.Button("Delete a movie by ID")],
                        [sg.Button("Delete all movies in a Cinema by Day")],
                        [sg.Button("Delete all movies in all cinema by name")],
                        [sg.Button("Go Back")],
                        ]

    deleteMovie = sg.Window("Delete Movie", deleteMovieLayout, element_justification = "c")

    while True:
        event, values = deleteMovie.read()

        if event == sg.WIN_CLOSED:
            exit()
        else:
            deleteMovie.close()
            if event == "Delete a movie by ID":
                deleteMovieByID(movies, booked)
            if event == "Delete all movies in a Cinema by Day":
                deleteMovieByDay(movies, booked)
            if event == "Delete all movies in all cinema by name":
                deleteMovieByName(movies, booked)
            if event == "Go Back":
                change_window.goToMenu("Admin")
                break
        

def deleteMovieByID(movies, booked):
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
                    [sg.Button("Delete Movie")]
                    ]

    deleteMovieByIDLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    deleteMovieByID = sg.Window("Delete Movie", deleteMovieByIDLayout)

    while True:
        event, values = deleteMovieByID.read()

        if event == sg.WIN_CLOSED:
            exit()

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            deleteMovieByID['-MOVIE-'].update(new_values) 
        else:
            deleteMovieByID['-MOVIE-'].update(movieList)

        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}"]
            deleteMovieByID["-MOVIEINFO-"].update(movieInfo)

        if event == "Delete Movie" and bool(movieInfo):
            answer = sg.popup_yes_no(f"Are you sure to delete {movieKey} - {movies[movieKey][0]}?")
            if answer == "Yes":
                del movies[movieKey]
                del booked[movieKey]
                files.updateMovie(movies)
                files.updateBooked(booked, movies)
                deleteMovieByID['-MOVIEINFO-'].update([])
                deleteMovieByID['-MOVIE-'].update(movieList)
        elif event == "Cancel":
            deleteMovieByID.close()
            deleteMovie(movies, booked)

def deleteMovieByDay(movies, booked):
    moviesDel = []

    deleteMovieByDayLayout = [
                             [sg.T("Select a Date: "), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                             [sg.T("Select a  Cinema Venue: "), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                             [sg.Button("Search Movies")],
                             [sg.Button("Cancel")]
                             ]

    deleteMovieByDay = sg.Window("Delete Movie", deleteMovieByDayLayout, modal = True, element_justification = "c")

    input_key_list = [key for key, value in deleteMovieByDay.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:
        event, values = deleteMovieByDay.read()
        cinema = "1"
        if values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"

        date = values["-DATE-"]

        if event == sg.WIN_CLOSED:
            exit()
        if event == "Search Movies":
            for k, v in movies.items():
                if cinema == v[3] and date == v[4]:
                    moviesDel.append(k)

            if all(map(str.strip, [values[key] for key in input_key_list])):
                if len(moviesDel) == 0:
                    sg.popup(f"There are no movies on {date} in Cinema {cinema}")
                    continue
                else:
                    answer = deletePopup(moviesDel, movies)
                    if answer == "Yes":
                        for k in moviesDel:
                            if k in movies:
                                del movies[k]
                                del booked[k]
                        files.updateMovie(movies)
                        files.updateBooked(booked, movies)
                    deleteMovieByDay.close()
            else:
                sg.popup("Some inputs are missed!")   
        elif event == "Cancel":
            deleteMovieByDay.close()
        
        deleteMovie(movies, booked)   

def deleteMovieByName(movies, booked):
    moviesDel = []

    deleteMovieByNameLayout = [
                              [sg.T("Search movie name to delete:")],
                              [sg.Input(key = "-NAME-", do_not_clear = True, size = (20,1))],
                              [sg.Button("Search")],
                              [sg.Button("Cancel")]
                              ]

    deleteMovieByName = sg.Window("Delete movie", deleteMovieByNameLayout, element_justification = "c")

    while True:
        event, values = deleteMovieByName.read()

        name = values["-NAME-"]

        if event == sg.WIN_CLOSED:
            exit()
        if event == "Search" and name != "":
            for k, v in movies.items():
                if values["-NAME-"] == v[0]:
                    moviesDel.append(k)
            if len(moviesDel) == 0:
                sg.popup(f"There is no movie named {name}")
            else:
                answer = deletePopup(moviesDel, movies)
                if answer == "Yes":
                    for k in moviesDel:
                        if k in movies:
                            del movies[k]
                            del booked[k]
                    files.updateMovie(movies)
                    files.updateBooked(booked, movies)
                deleteMovieByName.close()
                break
        elif event == "Cancel":
            deleteMovieByName.close()

    deleteMovie(movies, booked)

def deletePopup(data, movies):
    layout =[
            [sg.T("Are you sure to delete the following movie/s?")],
            [[sg.T(f"{k} - {movies[k][0]}")] for k in data],
            [sg.Button("Yes"), sg.Button("No")]
            ]
    
    window = sg.Window("Delete movie", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "No":
            break
        else:
            window.close()
            return "Yes"