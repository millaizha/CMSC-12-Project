import PySimpleGUI as sg
import purchase

def bookMovie(movies, booked, seats, discount):
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
                    [sg.Button("Book Seats")],
                    [sg.Button("Clear")]
                    ]
    bookMovieLayout = [
                        [sg.Column(showMovieList, element_justification = "c"), sg.Column(showMovieInfo, element_justification="c")]
                        ]
    bookMovie = sg.Window("Book Movie", bookMovieLayout)

    while True:
        event, values = bookMovie.read()

        if event == sg.WIN_CLOSED:
            exit()

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in movieList if search in x]
            bookMovie['-MOVIE-'].update(new_values) 
        else:
            bookMovie['-MOVIE-'].update(movieList)

        if event == '-MOVIE-' and len(values['-MOVIE-']):
            movieKey = str(values["-MOVIE-"])[2:6]
            movieInfo = [f"Movie ID: {movieKey}", f"Movie Name: {movies[movieKey][0]}", 
                        f"Movie Genre: {movies[movieKey][1]}", f"Parental Ratings: {movies[movieKey][2]}",
                        f"Cinema Room: {movies[movieKey][3]}", f"Date and Time of Viewing: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}",
                        f"Price: P{movies[movieKey][7]}"]
            bookMovie["-MOVIEINFO-"].update(movieInfo)

        if event == "Book Seats" and bool(movieInfo):
            bookMovie.close()
            bookSeats(movieKey, movies, booked, seats, discount)

        if event == "Cancel":
            bookMovie.close()

def bookSeats(movieKey, movies, booked, seats, discount):
    bookedSeats = []

    if movies[movieKey][3] == "1":
        numSeats = len(seats) + 1
    elif movies[movieKey][3] == "2":
        numSeats = len(seats)
    elif movies[movieKey][3] == "3":
        numSeats = len(seats) - 1

    selectSeats = [
                  [sg.T("Select a seat", justification = "center")],
                  [[sg.Button(j[i], size = (4,2), key= f"-SEAT{j[i]}-") 
                  for j in seats] 
                  for i in range(numSeats)]
                  ]

    availableLegend = [[sg.Button(size = (4, 2), disabled = True)], [sg.T("Available")]]
    takenLegend = [[sg.Button(button_color = "red", size = (4, 2), disabled = True)], [sg.T("Taken")]]
    selectedLegend = [[sg.Button(button_color = "green", size = (4, 2), disabled = True)], [sg.T("Selected")]]

    buttonLegend = [
                   [sg.T("Legend")],
                   [sg.Column(availableLegend, element_justification = "c"), 
                   sg.Column(takenLegend, element_justification = "c"), 
                   sg.Column(selectedLegend, element_justification = "c")]
                   ]

    confirmation = [
                   [sg.T("Selected Seats:")],
                   [sg.T(key = "-SEATS-")],
                   [sg.T(f"Total Price: P{len(bookedSeats) * movies[movieKey][7]}", key = "-PRICE-")],
                   [sg.Button("Proceed to Payment")],
                   [sg.Button("Cancel")]              
                   ]

    bookSeatsLayout = [[selectSeats], [buttonLegend, confirmation]]

    bookSeats = sg.Window("Book seats", bookSeatsLayout, finalize = True, element_justification = "c")

    while True:
        for i in range(numSeats):
            for j in seats:
                if j[i] in booked[movieKey]:
                    bookSeats.Element(f"-SEAT{j[i]}-").update(button_color = "red", disabled = True)

        event, values = bookSeats.read()

        if event == sg.WIN_CLOSED:
            exit()

        selectedSeat = bookSeats[event].get_text()

        if selectedSeat == "Cancel":
            bookSeats.close()
            break

        if selectedSeat == "Proceed to Payment" and not bool(bookedSeats):
            pass
        elif selectedSeat == "Proceed to Payment" and bool(bookedSeats):
            bookSeats.close()
            purchase.purchaseTickets(bookedSeats, movieKey, movies, booked, discount)

        while True:
            if selectedSeat not in bookedSeats:
                if selectedSeat != "Proceed to Payment":
                    bookedSeats.append(selectedSeat)
                    bookSeats[event].update(button_color = "green")
            else:
                bookedSeats.remove(selectedSeat)
                bookSeats[event].update(button_color = "#8e8b82")
            bookedSeats.sort()
            bookSeats["-SEATS-"].update(" ".join(map(str, bookedSeats)))
            bookSeats["-PRICE-"].update(f"Total Price: P{len(bookedSeats) * movies[movieKey][7]}")

            break

    bookMovie()