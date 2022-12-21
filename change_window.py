import main 

# Function to switch to user menu
def goToMenu(choice):   
    if choice == "Admin":
        main.adminMain()
    elif choice == "Cashier":
        main.cashierMain()