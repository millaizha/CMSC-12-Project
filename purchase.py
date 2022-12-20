import PySimpleGUI as sg
from datetime import datetime
import files, change_window

def purchaseTickets(bookedSeats, movieKey, movies, booked, discount):
    amountDue = len(bookedSeats) * movies[movieKey][7]
    selectedSeats = ""
    for seat in bookedSeats:
        selectedSeats += f"{seat[0]} "

    purchaseTicketsLayout = [
                         [sg.T("Purchase Summary", justification = "center")],
                         [sg.T("Movie\t:"), sg.T(movies[movieKey][0])],
                         [sg.T("Cinema\t:"), sg.T(movies[movieKey][3])],
                         [sg.T("Date\t:"), sg.T(f"{movies[movieKey][4]}")],
                         [sg.T("Time\t:"), sg.T(f"{movies[movieKey][5]} - {movies[movieKey][6]}")],
                         [sg.T("Seats\t:"), sg.T(selectedSeats)],
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
        pricePerTicket = movies[movieKey][7]

        event, values = purchaseTickets.read()

        if event == sg.WIN_CLOSED:
            exit()

        if values["-DISCOUNT-"] != "":
            code = values["-DISCOUNT-"]
            purchaseTickets["-OFF-"].update("\t\t    Invalid Code", visible = True)
            if code in discount:
                purchaseTickets["-OFF-"].update(f"\t\t    {discount[code]}% Off!", visible = True)
                pricePerTicket *= (100 - discount[code]) / 100
                amountDue = len(bookedSeats) * pricePerTicket
                purchaseTickets["-AMOUNT-"].update(f"{amountDue:.2f}")
            elif amountDue != len(bookedSeats) * movies[movieKey][7]:
                purchaseTickets["-OFF-"].update("\t\t    Invalid Code")
                amountDue = len(bookedSeats) * movies[movieKey][7]
                purchaseTickets["-AMOUNT-"].update(F"{amountDue:.2f}")   
        elif values["-DISCOUNT-"] == "":
            purchaseTickets["-OFF-"].update(visible = False)

        if event == "Purchase Tickets" and bool(values["-CASH-"]):
            money = float(values["-CASH-"])
            if money < amountDue:
                sg.popup("Insufficient cash.")
            else:
                for i in range(len(bookedSeats)):
                    bookedSeats[i].append(pricePerTicket)
                booked[movieKey].extend(bookedSeats)
                print(booked[movieKey])
                files.updateBooked(booked, movies)
                purchaseTickets.close()
                printReceipt(amountDue, code, money, bookedSeats, movieKey, movies, discount)

        if event == "Cancel":
            purchaseTickets.close()
            break

def printReceipt(amount, code, cash, bookedSeats, movieKey, movies, discount):
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")

    selectedSeats = ""
    for seat in bookedSeats:
        selectedSeats += f"{seat[0]} "

    printReceiptLayout = [
                         [sg.T("Booking and Payment Details", justification = "center")],
                         [sg.T(f"Booking date\t: {dtString}")],
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
                         [sg.T(F"Seat Numbers\t: {selectedSeats}")],
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
            change_window.goToMenu("Cashier")
            break