import PySimpleGUI as sg
import files
import book_movie
import add_movie, edit_movie, delete_movie, view_movie

sg.theme('DarkGrey5')

def chooseUser():
    user = sg.Window(
        "Movie Theater Booking System", 
        [[sg.T("Select a user: ")], 
        [sg.Button("Admin", s=10), sg.Button("Cashier", s=10)]])

    while True:
        event, values = user.read()
        if event == sg.WIN_CLOSED:
            exit()
        else:
            user.close()
            if event == "Admin":
                adminMain()
            elif event == "Cashier":
                cashierMain()

def adminMain():
    adminMainLayout = [
                    [sg.T("Select an option:")],
                    [sg.Button("Add Movie")],
                    [sg.Button("Edit Movie")],
                    [sg.Button("Delete Movie")],
                    [sg.Button("View Movie")],
                    [sg.Button("Add Discount Code")],
                    [sg.Button("Go to Users")],
                    [sg.Button("Exit")]
                    ]

    adminMain = sg.Window("Admin Main Menu", adminMainLayout, modal = True,  element_justification = "c")

    while True:
        event, values = adminMain.read()

        if event == sg.WIN_CLOSED:
            exit()
        else:
            adminMain.close()
            if event == "Add Movie":
                add_movie.addMovie(movies, booked)
            elif event == "Edit Movie":
                edit_movie.editMovie(movies)
            elif event == "Delete Movie":
                delete_movie.deleteMovie(movies, booked)
            elif event == "View Movie":
                view_movie.viewMovieAdmin(movies, booked)
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

def cashierMain():
    cashierMainLayout = [
                    [sg.T("Select an option:")],
                    [sg.Button("View movie")],
                    [sg.Button("Book movie")],
                    [sg.Button("Go to Users")],
                    [sg.Button("Exit")]
                    ]

    cashierMain = sg.Window("Cashier Main Menu", cashierMainLayout, modal = True)

    while True:
        event, values = cashierMain.read()

        if event == sg.WIN_CLOSED:
            exit()
        else:
            cashierMain.close()
            if event == "View movie":
                view_movie.viewMovieCashier(movies, booked)
            elif event == "Book movie":
                book_movie.bookMovie(movies, booked, seats, discount)
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

movies = files.loadMovies()
seats = files.loadSeats()
booked = files.loadBooked()
discount = {}

print(booked)
chooseUser()
