import PySimpleGUI as sg
import files, change_window

# Window for showing view movie options for admin
def viewMovieAdmin(movies):
    viewMovieAdminLayout = [
                           [sg.Button("View all movies")],
                           [sg.Button("View all movies in a cinema by day")],
                           [sg.Button("View details of a movie")],
                           [sg.Button("View all movie screening by name")],
                           [sg.Button("Go back")]
                           ]

    viewMovieAdmin = sg.Window("View Movie", viewMovieAdminLayout, element_justification = "c")

    while True:
        event, values = viewMovieAdmin.read()

        if event == sg.WIN_CLOSED:
            exit()

        if event == "View all movies":
            viewAllMoviesAdmin(movies)
        elif event == "View all movies in a cinema by day":
            viewMovieInCinema(movies)
        elif event == "View details of a movie":
            viewMovieDetails(movies)
        elif event == "View all movie screening by name":
            viewMovieByName(movies)
        elif event == "Go back":
            viewMovieAdmin.close()
            change_window.goToMenu("Admin")

# Window to show all movies
def viewAllMoviesAdmin(movies):
    movieList = [f"{k} - {v[0]} [Cinema {v[3]} {v[5]}-{v[6]}]" for k, v in movies.items()]

    showMovieList = [
                    [sg.T("Movie List:")],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Go back")]
                    ]

    viewAllMoviesAdmin = sg.Window("View Movies", showMovieList, element_justification = "c")

    while True:
        event, values = viewAllMoviesAdmin.read()

        if event == sg.WIN_CLOSED:
            exit()
        if event == "Go back":
            viewAllMoviesAdmin.close()
            break

# Window to show all movies in a cinema by the chosen date
def viewMovieInCinema(movies):
    movieList = []

    searchMovie = [
                  [sg.T("Select a date:"), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton("Open Calendar", close_when_date_chosen=True,  target='-DATE-', format = "%m-%d-%y", no_titlebar=False)],
                  [sg.T("Select Cinema:"), sg.Radio("1", "CINEMA", key = "-1-", default = True), sg.Radio("2", "CINEMA", key = "-2-"), sg.Radio("3", "CINEMA", key = "-3-")],
                  [sg.Button("Search")],
                  [sg.Button("Go back")]
                  ]

    showMovieList = [
                    [sg.T("Movie Search Results")],
                    [sg.Listbox(movieList, size=(50, 7), enable_events = True, key='-MOVIELIST-')],
                    [sg.Button("Clear")]
                    ]
    
    viewMovieInCinemaLayout = [
                              [sg.Column(searchMovie, element_justification = "c"), sg.Column(showMovieList, element_justification = "c")]
                              ]

    viewMovieInCinema = sg.Window("View Movies", viewMovieInCinemaLayout)

    while True:
        event, values = viewMovieInCinema.read()

        if values["-1-"]:
            cinema = "1"
        elif values["-2-"]:
            cinema = "2"
        elif values["-3-"]:
            cinema = "3"

        date = values["-DATE-"]

        if event == sg.WIN_CLOSED:
            exit()

        if event == "Search":
            viewMovieInCinema["-MOVIELIST-"].update([])
            movieList = []

            for k, v in movies.items():
                if v[3] == cinema and v[4] == date:
                    movieList.append(f"{k} - {v[0]} [Cinema {v[3]} {v[5]}-{v[6]}]")

            # Shows popup if there is no movie on the chosen cinema on the chosen date
            if len(movieList) == 0:
                sg.popup(f"There are no movies on {date} at Cinema {cinema}")
            else:
                # Shows the movie list in the list box
                viewMovieInCinema["-MOVIELIST-"].update(movieList)
        elif event == "Clear":
            viewMovieInCinema["-MOVIELIST-"].update([])
            movieList = []
        elif event == "Go back":
            viewMovieInCinema.close()
            break

# Shows all the details of a movie
def viewMovieDetails(movies):
    movieList = [f"{k} - {v[0]}" for k, v in movies.items()]
    movieInfo = {}
    # Reload the booked seats file
    booked = files.loadBooked()

    showMovieList = [
                    [sg.T("Select a Movie:")],
                    [sg.T("Search: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                    [sg.Listbox(movieList, size=(40, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Go Back")]
                    ]

    showMovieInfo = [
                    [sg.T("Movie Information:")],
                    [sg.Listbox(movieInfo, size=(50, 8), enable_events = True, key='-MOVIEINFO-')],
                    [sg.Button("Clear")]
                    ]
    viewMovieDetailsLayout = [
                      [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                      ]
    viewMovieDetails = sg.Window("View Movie", viewMovieDetailsLayout)

    while True:
        event, values = viewMovieDetails.read()

        if event == sg.WIN_CLOSED:
            exit()

        # Will filter the movie list box depending on the text in the search bar
        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            viewMovieDetails['-MOVIE-'].update(new_values) 
        else:
            viewMovieDetails['-MOVIE-'].update(movieList)

        # Shows the movie information in the list box
        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            
            totalEarnings = 0
            
            # Will get the total earnings from the booked seats
            for i in range(len(booked[movieKey])):
                totalEarnings += float(booked[movieKey][i][1])

            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}", f"Total Earnings from Booked Seats: P{totalEarnings}"]
            viewMovieDetails["-MOVIEINFO-"].update(movieInfo)

        if event == "Clear":
            viewMovieDetails['-MOVIEINFO-'].update([])
        elif event == "Go Back":
            viewMovieDetails.close()
            break

# Window to view the movies searched by name
def viewMovieByName(movies):
    viewDict = {}
    movieList = []

    searchMovie = [
                  [sg.T("Search a Movie:"), sg.Input(key='-NAME-', size=(20,1))],
                  [sg.Button("Search")],
                  [sg.Button("Go back")]
                  ]

    showMovieList = [
                    [sg.T("Movie Search Results")],
                    [sg.Listbox(movieList, size=(50, 7), enable_events = True, key='-MOVIELIST-')],
                    [sg.Button("Clear")]
                    ]
    
    viewMovieByNameLayout = [
                              [sg.Column(searchMovie, element_justification = "c"), sg.Column(showMovieList, element_justification = "c")]
                              ]

    viewMovieByName = sg.Window("View Movies", viewMovieByNameLayout)

    while True:
        event, values = viewMovieByName.read()

        name = values["-NAME-"]

        if event == sg.WIN_CLOSED:
            exit()

        # Will search fpr movies with the same name
        if event == "Search":
            for k, v in movies.items():
                if name == v[0]:
                    viewDict[k] = v

            # Sorts the movies by date and time
            viewDict = sorted(viewDict, key = lambda k: ([viewDict[k][4]], [viewDict[k][5]]))
            movieList = [f"{k} - {movies[k][0]} [Cinema {movies[k][3]}] {movies[k][4]} {movies[k][5]} - {movies[k][6]}" for k in viewDict]

            # Shows a popup if there is no movie with the inputted name
            if len(viewDict) == 0:
                sg.popup(f"There is no movie named {name}")
            else:
                viewMovieByName["-MOVIELIST-"].update(movieList)

            viewDict = {}
            movieList = []
        
        elif event == "Clear":
            viewMovieByName["-MOVIELIST-"].update([])

        elif event == "Go back":
            viewMovieByName.close()
            break

# Window for showing view movie options for cashier
def viewMovieCashier(movies):
    viewMovieCashierLayout = [
                           [sg.Button("View all movies")],
                           [sg.Button("View all movie screening by name")],
                           [sg.Button("Go back")]
                           ]

    viewMovieCashier = sg.Window("View Movie", viewMovieCashierLayout, element_justification = "c")

    while True:
        event, values = viewMovieCashier.read()

        if event == sg.WIN_CLOSED:
            exit()

        if event == "View all movies":
            viewAllMoviesCashier(movies)
        elif event == "View all movie screening by name":
            viewMovieByName(movies)
        elif event == "Go back":
            viewMovieCashier.close()
            change_window.goToMenu("Cashier")
            break

# Window to show all movies for cashier
def viewAllMoviesCashier(movies):
    viewDict = sorted(movies, key = lambda k: ([movies[k][4]], [movies[k][5]]))
    movieList = [f"{k} - {movies[k][0]} [Cinema {movies[k][3]}] {movies[k][4]} {movies[k][5]} - {movies[k][6]}" for k in viewDict]

    showMovieList = [
                    [sg.T("Movie List:")],
                    [sg.Listbox(movieList, size=(60, 10), enable_events = True, key='-MOVIE-')],
                    [sg.Button("Go back")]
                    ]

    viewAllMoviesCashier = sg.Window("View Movies", showMovieList, element_justification = "c")

    while True:
        event, values = viewAllMoviesCashier.read()

        if event == sg.WIN_CLOSED:
            exit()
        if event == "Go back":
            viewAllMoviesCashier.close()
            break