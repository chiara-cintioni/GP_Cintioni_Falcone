import PySimpleGUI as sg
import os.path



def second_window():

    layout = [
        [sg.Text('Insert the path of the directory that contains the csv files of the rna sequences: ')],
        []
    ]

    window = sg.Window('Second Form', layout)
    event, values = window.read()
    window.close()


def menu():
    elements_to_center = [
        [sg.Text("Welcome, what would you like to do?")],
        [sg.Button("Insert a csv file into mongodb")],
        [sg.Button("Modify a single rna sequence")],
        [sg.Button("Delete a single rna sequence")],
        [sg.Button(" Change the taxonomy folder ")],
        [sg.Button("Exit")],
    ]

    layout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(elements_to_center, element_justification='c'), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("Main page", layout, margins=(150,50))

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Insert a csv file into mongodb":
            second_window()

    window.close()

menu()