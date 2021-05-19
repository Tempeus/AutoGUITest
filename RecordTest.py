import mouse
import keyboard
import time

open('mouse.txt', 'w').close()
open('keybd.txt', 'w').close() 

def mouse_listen(e):
    mouse_events.append(e)

def log_keybd_event(e):
    f = open("keybd.txt", "a")
    a = str(e.event_type) + ", " + str(e.name) + ", " + str(e.scan_code) + ", " + str(e.time)
    f.write(a)
    f.write('\r')
    f.close

def log_mouse_event(filtered_mouse_events):
    f = open("mouse.txt", "a")
    for e in filtered_mouse_events:
        if type(e) == mouse.ButtonEvent:
            a = "CLICK: " + str(e.event_type) + ", " + str(e.button) + ", " + str(e.time)
            f.write(a)
            f.write('\r')
        elif type(e) == mouse.MoveEvent:
            a = "MOVE: (" + str(e.x) + ", " + str(e.y) + "), " + str(e.time)
            f.write(a)
            f.write('\r')

        elif type(e) == mouse.WheelEvent:
            a = "WHEEL: " + str(e.delta) + ", " + str(e.time)
    f.close

if __name__ == '__main__':
    mouse_events = []
    keyboard_events = []
    stop_recordKEY = "esc"

    mouse.hook(mouse_listen)
    keyboard.hook(log_keybd_event)

    keyboard.wait(stop_recordKEY)
    mouse.unhook(mouse_listen)
    keyboard.unhook(log_keybd_event)

    filtered_mouse_events = []

    #Scroll wheel
    for index, event in enumerate(mouse_events):
        if (index + 1 < len(mouse_events) and index - 1 >= 0): #Check bounds
            if type(event) == mouse.ButtonEvent: #If the event is a click event - record it
                if type(mouse_events[index - 1] == mouse.MoveEvent): #If the previous event is a moveEvent, 
                    filtered_mouse_events.append(mouse_events[index - 1]) #record it for the position
                filtered_mouse_events.append(event)
            elif type(event) == mouse.WheelEvent:
                filtered_mouse_events.append(event)

    log_mouse_event(filtered_mouse_events)

    #sort both even list into one big list
    