# https://docs.badge.team/esp32-app-development/api-reference/buttons/

# button definitions: python_modules/lasertag/buttons.py

# Wichtig: das menuzeug scheint buttens bereits mit der buttons.py aus dem lasertag root dir zu initialisieren. danach kann ich mit meiner eigenen buttens.py machen was ich will, die reagieren nicht. loesung: buttons.py im root dir ersetzen.

print('Test: buttons')


import buttons  # in der konsole ist es definiert, hier muss es wohl gemacht werden!?

print('A links:', buttons.value(buttons.BTN_A))
print('B mitte:', buttons.value(buttons.BTN_B))
print('C rechts:', buttons.value(buttons.BTN_C))
print('PEW:', buttons.value(buttons.BTN_PEW))


def a_btn_pressed(pushed):
    if(pushed):  # down
        print('A', pushed)
    else:  # up
        print('A', pushed)

buttons.attach(buttons.BTN_A, lambda pressed: a_btn_pressed(pressed))
buttons.attach(buttons.BTN_B, lambda pressed: print('B', pressed))
buttons.attach(buttons.BTN_C, lambda pressed: print('C', pressed))
buttons.attach(buttons.BTN_PEW, lambda pressed: print('PEW', pressed))

# buttons.pushMapping()  # alle mappings loeschen