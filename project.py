import PySimpleGUI as sg

sg.theme('DarkGrey5')

def chooseUser():
    global user
    user = sg.Window(
        "Movie Theater Booking System", 
        [[sg.T("Select a user: ")], 
        [sg.Button("Admin", s=10), sg.Button("Cashier", s=10)]])

    while True:
        event, values = user.read()
        if event == sg.WIN_CLOSED:
            break
        else:
            user.close()
            if event == "Admin":
                adminMain()
            elif event == "Cashier":
                cashierMain()

    user.close()

def adminMain():
    adminMainLayout = [
                    [sg.T("Select an option:")],
                    [sg.Button("Add movie")],
                    [sg.Button("Edit movie")],
                    [sg.Button("Delete movie")],
                    [sg.Button("View movie")],
                    [sg.Button("Go to Users")],
                    [sg.Button("Exit")]
                    ]

    adminMain = sg.Window("Admin Main Menu", adminMainLayout, modal = True)

    while True:
        event, values = adminMain.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            adminMain.close()
            if event == "Add movie":
                pass
            elif event == "Edit movie":
                pass
            elif event == "Delete movie":
                pass
            elif event == "View movie":
                pass
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

    adminMain.close()

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
            break
        else:
            cashierMain.close()
            if event == "View movie":
                pass
            elif event == "Book movie":
                pass
                pass
            elif event == "Go to Users":
                chooseUser()
            elif event == "Exit":
                exit()

    cashierMain.close()

chooseUser()
exit()