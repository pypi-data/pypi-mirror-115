import PySimpleGUI as sg

layout = [  [sg.Text('PySimpleGuy', font='_ 25')],
            [sg.Text('Hi there!  I\'m your friendly PySimpleGUI Guy.')],
            [sg.Button(image_data=sg.EMOJI_BASE64_HAPPY_HEARTS, k='Exit', button_color=sg.theme_background_color(), border_width=0)]]

window = sg.Window('PySimpleGuy', layout, element_justification='c')

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
