import main 

def goToMenu(choice):   
    if choice == "Admin":
        main.adminMain()
    elif choice == "Cashier":
        main.cashierMain()