import PySimpleGUI as sg
import datetime
import files

def purchaseTickets(bookedSeats, movieKey, movies, booked, discount):
    amountDue = len(bookedSeats) * movies[movieKey][7]

    purchaseTicketsLayout = [
                         [sg.T("Purchase Summary", justification = "center")],
                         [sg.T("Movie\t:"), sg.T(movies[movieKey][0])],
                         [sg.T("Cinema\t:"), sg.T(movies[movieKey][3])],
                         [sg.T("Date\t:"), sg.T(f"{movies[movieKey][4]}")],
                         [sg.T("Time\t:"), sg.T(f"{movies[movieKey][5]} - {movies[movieKey][6]}")],
                         [sg.T("Seats\t:"), sg.T(" ".join(map(str, bookedSeats)))],
                         [sg.T()],
                         [sg.T(f"Amount\ndue\t:"), sg.T(f"{amountDue:.2f}", key = "-AMOUNT-")],
                         [sg.T("Enter\ndiscount code\t:"), sg.Input(size = 10, enable_events = True, key = "-DISCOUNT-")],
                         [sg.T(visible = False, key = "-OFF-")],
                         [sg.T("Enter cash\t:"), sg.Input(size = 10, enable_events = True, key = "-CASH-")],
                         [sg.Button("Purchase Tickets")],
                         [sg.Button("Cancel")]
                         ]
    
    purchaseTickets = sg.Window("Purchase Tickets", purchaseTicketsLayout, finalize = True)

    while True:
        code = ""

        event, values = purchaseTickets.read()

        if event == sg.WIN_CLOSED:
            exit()

        if values["-DISCOUNT-"] != "":
            code = values["-DISCOUNT-"]
            if code in discount:
                purchaseTickets["-OFF-"].update(f"\t\t    {discount[code]}% Off!", visible = True)
                amountDue = ((len(bookedSeats) * movies[movieKey][7]) * (100 - discount[code])) / 100
                purchaseTickets["-AMOUNT-"].update(F"{amountDue:.2f}")
            elif amountDue != len(bookedSeats) * movies[movieKey][7]:
                purchaseTickets["-OFF-"].update(visible = False)
                amountDue = len(bookedSeats) * movies[movieKey][7]
                purchaseTickets["-AMOUNT-"].update(F"{amountDue:.2f}")     

        if event == "Purchase Tickets" and bool(values["-CASH-"]):
            money = float(values["-CASH-"])
            if money < amountDue:
                sg.popup("Insufficient cash.")
                print(code)
            else:
                booked[movieKey].extend(bookedSeats)
                files.updateFiles()
                purchaseTickets.close()
                printReceipt(amountDue, code, money, bookedSeats, movieKey, movies, discount)

        if event == "Cancel":
            purchaseTickets.close()
            break

def printReceipt(amount, code, cash, bookedSeats, movieKey, movies, discount):
    printReceiptLayout = [
                         [sg.T("Booking and Payment Details", justification = "center")],
                         [sg.T(f"Booking date\t: {datetime.strftime(datetime.now(), '%m-%d-%y %I:%M%p')}")],
                         [sg.T(f"Amount Due\t: {amount:.2f}")],
                         [sg.T(f"Cash\t\t: {cash:.2f}")],
                         [sg.T(f"Change\t\t: {(cash - amount):.2f}")],
                         [sg.T(visible = False, key = "-DISCOUNT-")],
                         [sg.T("Movie Details", justification = "center")],
                         [sg.T(f"Movie\t\t: {movies[movieKey][0]}")],
                         [sg.T(f"Date and\nTime\t\t: {movies[movieKey][4]} {movies[movieKey][5]} - {movies[movieKey][6]}")],
                         [sg.T(f"Genre\t\t: {movies[movieKey][1]}")],
                         [sg.T(f"Parental Rating\t: {movies[movieKey][2]}")],
                         [sg.T(f"Cinema\t\t: Cinema {movies[movieKey][3]}")],
                         [sg.T(f"Number of\nTickets\t\t: {len(bookedSeats)}")],
                         [sg.T("Seat Numbers\t: " + ", ".join(map(str, bookedSeats)))],
                         [sg.T("\nThank you and enjoy your movie!")],
                         [sg.Button("OK")]
                         ]

    printReceipt = sg.Window("Receipt", printReceiptLayout, finalize = "True")

    while True:
        if code in discount:
            printReceipt.Element("-DISCOUNT-").update(f"Discount\t\t: {discount[code]}%", visible = True)

        event, values = printReceipt.read()

        if event == sg.WIN_CLOSED:
            exit()

        if event == "OK":
            printReceipt.close()
            break