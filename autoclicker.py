import pyautogui
from tkinter import *
import keyboard
import threading
import json


def callback(self, P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False


with open('settings.json') as f:
    data = json.load(f)

root = Tk()
root.geometry("300x150")
root.wm_attributes("-topmost", 1)
root.config(background="red")
root.resizable(False, False)
root.title("Autoclicker")

status = Label(root, fg="white", bg="red", text="Off", font=("Helvetica", 25))
status.pack(pady=15)

clicking = False
running = True

DELAY = data["Delay"]

CLICK_TYPE = data["Click Type"]
left_click = True if CLICK_TYPE == "Left" else False

string = "Left" if left_click else "Right"
click_type = Label(root, fg="Grey", bg="red", text=f"Mode: {string} Click", font=("Times New Roman", 18))
click_type.pack(pady=5)

delay_label = Label(root, fg="Blue", bg="red", text=f"Delay: {round(DELAY, 2)}", font=("Times New Roman", 13))
delay_label.pack(padx=15)

exit_button = "f12"
hotkey = "caps_lock"

MIN, MAX = 0.05, 1

held = False


def toggle(e):
    global clicking, status, root

    clicking = not clicking
    if clicking:
        root.config(background="lime")

        status['text'] = "On"
        status['bg'] = "lime"

        click_type['bg'] = 'lime'
    else:
        root.config(background="red")

        status['text'] = "Off"
        status['bg'] = "red"

        click_type['bg'] = 'red'


def switch_click(e):
    global left_click

    left_click = not left_click
    text = "Left Click" if left_click else "Right Click"
    click_type.config(text=f"Mode: {text}")


def QuitFunc(e):
    global running

    running = False
    root.destroy()


def increase_delay(e):
    if not e.name == 'pause': return

    global DELAY
    print('w')
    DELAY += 0.01

    if DELAY > 1: DELAY -= 0.01
    delay_label["text"] = f"Delay: {round(DELAY, 2)}"


def decrease_delay(e):
    if not e.name == 'scroll lock': return

    global DELAY

    DELAY -= 0.01

    if DELAY < 0.05: DELAY += 0.01
    delay_label["text"] = f"Delay: {round(DELAY, 2)}"


def main():
    keyboard.on_release_key("menu", lambda _: root.overrideredirect(1))
    keyboard.on_release_key("pause", switch_click)
    keyboard.on_release_key(exit_button, QuitFunc)
    keyboard.on_release_key(hotkey, toggle)

    keyboard.on_press(increase_delay)
    keyboard.on_press(decrease_delay)

    while running:
        while clicking:
            pyautogui.click(button="left" if left_click else "right")
            pyautogui.PAUSE = DELAY


def save():
    save_dict = {
        "Delay": DELAY,
        "Click Type": "Left" if left_click else "Right"
    }

    with open("settings.json", 'w') as file:
        json.dump(save_dict, file)


def on_quit():
    global running
    root.destroy()
    running = False
    save()


main_thread = threading.Thread(target=main)
main_thread.start()

root.protocol("WM_DELETE_WINDOW", on_quit)
root.mainloop()
