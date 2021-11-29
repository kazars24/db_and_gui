import pandas as pd
import os
import PySimpleGUI as sg

database = 'films.csv'


def create():
    global database
    data = pd.read_csv(database)
    layout = [[sg.Text("Enter new database's name")],
              [sg.InputText()],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Creation a new database', layout)

    event, values = window.read()
    window.close()

    text_input = values[0] + '.csv'
    if len(text_input) > 4:
        sg.popup('Your new database', text_input)
        database = text_input
        data.to_csv(database, index=False)
    else:
        sg.popup('Wrong name!')


def open():
    global database
    data = pd.read_csv(database, engine='python')
    header_list = list(data.columns)
    if data.empty:
        sg.popup('Database is empty')
    else:
        data = data[0:].values.tolist()
        layout = [
            [sg.Table(values=data,
                      headings=header_list,
                      font='Helvetica',
                      pad=(100, 100),
                      display_row_numbers=False,
                      auto_size_columns=True,
                      num_rows=min(25, len(data)))]
        ]

        window = sg.Window(database, layout, grab_anywhere=False)
        event, values = window.read()
        window.close()


def delete():
    global database
    database = 'films.csv'
    layout = [
        [sg.Text('Your database has been deleted')],
        [sg.Button('OK')]
    ]
    window = sg.Window('Deletion the database', layout)
    event, values = window.read()
    window.close()


def clear():
    global database
    primary = pd.read_csv('films.csv')
    if os.path.isfile(database):
        pd.DataFrame(columns=primary.columns).to_csv(database, index=False)
        sg.popup('Successfully!')
    else:
        sg.popup('There is no such file')


def add():
    global database
    data = pd.read_csv(database)
    layout = [[sg.Text("Enter a new record in format id;name;director;rus;rating")],
              [sg.InputText()],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Addition a new record', layout)

    event, values = window.read()
    window.close()

    new = values[0].split(sep=';')
    new[0] = int(new[0])
    if new[3] == 'False':
        new[3] = False
    else:
        new[3] = True
    new[4] = float(new[4])
    flag = False
    for i in data.id:
        if i == new[0]:
            flag = True
    if flag:
        sg.popup('A record with such an id already exists:(')
    else:
        data = data.append({'id': new[0],
                            'name': new[1],
                            'director': new[2],
                            'rus': new[3],
                            'rating': new[4]}, ignore_index=True)
        sg.popup('Successfully!')
        data.to_csv(database, index=False)


def del_from():
    global database

    layout = [
        [sg.Text('Enter a value'), sg.InputText()],
        [sg.Text('Then select one of the fields by which you want to delete')],
        [sg.Button('id', enable_events=True, key='id'),
         sg.Button('name', enable_events=True, key='name'),
         sg.Button('director', enable_events=True, key='director'),
         sg.Button('rus', enable_events=True, key='rus'),
         sg.Button('rating', enable_events=True, key='rating')],
    ]
    window = sg.Window('Deletion a record from the database', layout)

    event, values = window.read()
    window.close()

    if event == 'id':
        value = int(values[0])
    if event == 'rating':
        value = float(values[0])
    if event == 'rus':
        if values[0] == 'False':
            value = False
        else:
            value = True

    data = pd.read_csv(database)
    data = data[data[event] != value]
    data.to_csv(database, index=False)
    sg.popup('Successfully!')


def select():
    global database

    layout = [
        [sg.Text('Enter a value'), sg.InputText()],
        [sg.Text('Then select one of the fields by which you want to select')],
        [sg.Button('id', enable_events=True, key='id'),
         sg.Button('name', enable_events=True, key='name'),
         sg.Button('director', enable_events=True, key='director'),
         sg.Button('rus', enable_events=True, key='rus'),
         sg.Button('rating', enable_events=True, key='rating')]
    ]
    window = sg.Window('Selection records from the database', layout)

    event, values = window.read()
    window.close()

    if event == 'id':
        value = int(values[0])
    if event == 'rating':
        value = float(values[0])
    if event == 'rus':
        if values[0] == 'False':
            value = False
        else:
            value = True
    else:
        value = values[0]
    data = pd.read_csv(database)
    data = data[data[event] == value]
    header_list = list(data.columns)
    if data.empty:
        sg.popup('Database is empty')
    else:
        data = data[0:].values.tolist()
        layout = [
            [sg.Table(values=data,
                      headings=header_list,
                      font='Helvetica',
                      pad=(100, 100),
                      display_row_numbers=False,
                      auto_size_columns=True,
                      num_rows=min(25, len(data)))]
        ]

        window = sg.Window(database, layout, grab_anywhere=False)
        event, values = window.read()
        window.close()


def update():
    global database

    layout = [
        [sg.Text('Enter id of the record')],
        [sg.InputText()],
        [sg.Submit()]
    ]
    window = sg.Window('Updating a record', layout)
    event, values = window.read()
    window.close()

    id = int(values[0])
    data = pd.read_csv(database)

    layout = [
        [sg.Text('Enter a value'), sg.InputText()],
        [sg.Text('Then select one of the fields by which you want to update')],
        [sg.Button('id', enable_events=True, key='id'),
         sg.Button('name', enable_events=True, key='name'),
         sg.Button('director', enable_events=True, key='director'),
         sg.Button('rus', enable_events=True, key='rus'),
         sg.Button('rating', enable_events=True, key='rating')]
    ]
    window = sg.Window('Selection records from the database', layout)

    event, values = window.read()
    window.close()

    if event == 'id':
        value = int(values[0])
    if event == 'rating':
        value = float(values[0])
    if event == 'rus':
        if values[0] == 'False':
            value = False
        else:
            value = True
    else:
        value = values[0]

    data.loc[(data['id'] == id), event] = value
    data.to_csv(database, index=False)

    sg.popup('Successfully!')


# GUI
layout = [
    [sg.Text('     Welcome to my implementation of the file database!', justification='center', font=("Helvetica", 13))],
    [sg.Text('To interact with the database, select one of the commands:', font=("Helvetica", 13))],
    [sg.Text(' ')],
    [sg.Button('Create', enable_events=True, key='create'),
     sg.Button('Open', enable_events=True, key='open'),
     sg.Button('Delete', enable_events=True, key='delete'),
     sg.Button('Clear', enable_events=True, key='clear'),
     sg.Button('Add', enable_events=True, key='add'),
     sg.Button('Delete from', enable_events=True, key='del_from'),
     sg.Button('Select', enable_events=True, key='select'),
     sg.Button('Update', enable_events=True, key='update')],
    [sg.Text(' ')],
    [sg.Button('Exit')]
]
window = sg.Window('Laba 1', layout)
while True:  # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'create':
        create()
    if event == 'open':
        open()
    if event == 'delete':
        delete()
    if event == 'clear':
        clear()
    if event == 'add':
        add()
    if event == 'del_from':
        del_from()
    if event == 'select':
        select()
    if event == 'update':
        update()
window.close()
