import PySimpleGUI as sg
import files, change_window

def viewDiscount(discount):
    discountList = [f"{k}: {v}%" for k, v in discount.items()]
    discountInfo = {}
    showDiscountList = [
                        [sg.T("Search Discount Coupon: "), sg.Input(size=(20, 1), enable_events=True, key='-SEARCH-')],
                        [sg.Listbox(discountList, size=(30, 10), enable_events = True, key='-CODE-')],
                        [sg.Button("Add Discount Coupon")],
                        [sg.Button("Go back")]
                        ]
    showDiscountInfo = [
                        [sg.T("Discount Information:")],
                        [sg.Listbox(discountInfo, size=(30, 2), enable_events = True, key='-CODEINFO-')],
                        [sg.Button("Edit Coupon"), sg.Button("Delete Coupon")],
                        [sg.Button("Clear")]
                        ]
    viewDiscountLayout = [
                        [sg.Column(showDiscountList, element_justification = "c"), sg.Column(showDiscountInfo, element_justification = "c")]
                        ]
    viewDiscount = sg.Window("View Discount Coupons", viewDiscountLayout)

    while True:
        event, values = viewDiscount.read()

        if event == sg.WIN_CLOSED:
            exit()

        if values['-SEARCH-'] != '':
            search = values['-SEARCH-']
            new_values = [x for x in discountList if search in x]
            viewDiscount['-CODE-'].update(new_values) 
        else:
            viewDiscount['-CODE-'].update(discountList)

        if event == '-CODE-' and len(values['-CODE-']):
            code, off = str(values["-CODE-"])[2:-2].split(": ")
            discountInfo = [f"Coupon Code: {code}", f"Discount Off: {off}"]
            viewDiscount["-CODEINFO-"].update(discountInfo)

        if event == "Add Discount Coupon":
            viewDiscount.close()
            addDiscount(discount)
        elif event == "Edit Coupon":
            viewDiscount.close()
            editDiscount(discount, code)
        elif event == "Delete Coupon":
            viewDiscount.close()
            deleteDiscount(discount, code)
        elif event == "Clear":
            viewDiscount['-CODEINFO-'].update([])
        elif event == "Go back":
            viewDiscount.close()
            change_window.goToMenu("Admin")

def addDiscount(discount):
    addDiscountLayout = [
                        [sg.T("Enter Discount code:")],
                        [sg.Input(key = "-CODE-", do_not_clear = True, size = (20,1))],
                        [sg.T("Enter Percent Off (ex. 20):")],
                        [sg.Input(key = "-OFF-", do_not_clear = True, size = (20,1))],
                        [sg.Button("Add Discount Code"), sg.Button("Cancel")]
                        ]

    addDiscount = sg.Window("Add Discount", addDiscountLayout, modal = True, element_justification = "c")

    input_key_list = [key for key, value in addDiscount.key_dict.items()
                    if isinstance(value, sg.Input)]
    while True:
        event, values = addDiscount.read()

        if event == sg.WIN_CLOSED:
            exit()

        if event == "Add Discount Code":
            if all(map(str.strip, [values[key] for key in input_key_list])):
                discount[values["-CODE-"]] = values["-OFF-"]
                addDiscount.close()
                files.updateDiscount(discount)
                addDiscount.close()
                viewDiscount(discount)
            elif not all(map(str.strip, [values[key] for key in input_key_list])):
                    sg.popup("Some inputs are missed!")
        elif event == "Cancel":
            addDiscount.close()
            viewDiscount(discount)

def editDiscount(discount, code):
    editDiscountLayout = [
                        [sg.T("Enter Discount code:")],
                        [sg.Input(code, key = "-CODE-", do_not_clear = True, size = (20,1))],
                        [sg.T("Enter Percent Off (ex. 20):")],
                        [sg.Input(discount[code], key = "-OFF-", do_not_clear = True, size = (20,1))],
                        [sg.Button("Edit Discount Code"), sg.Button("Cancel")]
                        ]

    editDiscount = sg.Window("Edit Movie Info", editDiscountLayout, finalize = True)

    input_key_list = [key for key, value in editDiscount.key_dict.items()
                    if isinstance(value, sg.Input)]

    while True:
        event, values = editDiscount.read()

        if event == sg.WIN_CLOSED:
            exit()

        if event == "Edit Discount Code":
            if all(map(str.strip, [values[key] for key in input_key_list])):
                del discount[code]
                discount[values["-CODE-"]] = values["-OFF-"]
                editDiscount.close()
                files.updateDiscount(discount)
                editDiscount.close()
                viewDiscount(discount)
            elif not all(map(str.strip, [values[key] for key in input_key_list])):
                    sg.popup("Some inputs are missed!")
        elif event == "Cancel":
            editDiscount.close()
            viewDiscount(discount)

def deleteDiscount(discount, code):
    answer = sg.popup_yes_no(f"Are you sure to delete {code}: {discount[code]}%?")
    if answer == "Yes":
        del discount[code]
        files.updateDiscount(discount)
    viewDiscount(discount)
