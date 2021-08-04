import pyautogui
from tkinter import *
import keyboard
import threading
import json

# Main Class
class Main():
    def __init__(self):
        self.exit_button = "f12"
        self.hotkey = "caps_lock"

        self.increase_key = "scroll lock"
        self.decrease_key = "f4"

        self.default_info = {
            'Delay': 0.05,
            'Click Type': "Left"
        }

    def check(self):
        try:
            with open('settings.json') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:

            with open('settings.json', 'w') as file:
                json.dump(self.default_info, file)
            return self.default_info
        except json.decoder.JSONDecodeError:

            with open('settings.json', 'w') as file:
                json.dump(self.default_info, file)
                return self.default_info



    def toggle(self, _):
        global clicking, status, root, delay_label

        clicking = not clicking
        if clicking:
            root.config(background="lime")

            status['text'] = "On"
            status['bg'] = "lime"

            click_type['bg'] = 'lime'
            delay_label['bg'] = 'lime'
        else:
            root.config(background="red")

            status['text'] = "Off"
            status['bg'] = "red"

            click_type['bg'] = 'red'
            delay_label['bg'] = 'red'

    def switch_click(self, _):
        global left_click

        left_click = not left_click
        text = "Left Click" if left_click else "Right Click"
        click_type.config(text=f"Mode: {text}")

    def QuitFunc(self, _):
        global running

        running = False
        root.destroy()

    def handle(self, key):
        if key.name == self.increase_key:
            self.increase_delay()
        if key.name == self.decrease_key:
            self.decrease_delay()

    def increase_delay(self):
        global DELAY

        DELAY += 0.01

        if DELAY >= 1: DELAY -= 0.01
        delay_label["text"] = f"Delay: {round(DELAY, 2)}"

    def decrease_delay(self):
        global DELAY

        DELAY -= 0.01

        if DELAY <= 0.05: DELAY += 0.01
        delay_label["text"] = f"Delay: {round(DELAY, 2)}"

    def main(self):
        keyboard.on_release_key("menu", lambda _: root.overrideredirect(1))
        keyboard.on_release_key("pause", self.switch_click)
        keyboard.on_release_key(self.exit_button, self.QuitFunc)
        keyboard.on_release_key(self.hotkey, self.toggle)

        keyboard.on_press(self.handle)

        while running:
            while clicking:
                pyautogui.click(button="left" if left_click else "right")
                pyautogui.PAUSE = DELAY

    def save(self):
        save_dict = {
            "Delay": DELAY,
            "Click Type": "Left" if left_click else "Right"
        }

        with open("settings.json", 'w') as file:
            json.dump(save_dict, file)

    def on_quit(self):
        global running
        running = False

        root.destroy()
        self.save()


# Main System Variables
clicking = False
running = True
MainClass = Main()

data = MainClass.check()

DELAY = data["Delay"]

CLICK_TYPE = data["Click Type"]
left_click = True if CLICK_TYPE == "Left" else False

# GUI Elements
root = Tk()
root.geometry("300x150")
root.wm_attributes("-topmost", 1)
root.config(background="red")
root.resizable(False, False)
root.title("Autoclicker")

string = "Left" if left_click else "Right"
click_type = Label(root, fg="Grey", bg="red", text=f"Mode: {string} Click", font=("Times New Roman", 18))
click_type.pack(pady=5)

delay_label = Label(root, fg="Blue", bg="red", text=f"Delay: {round(DELAY, 2)}", font=("Times New Roman", 13))
delay_label.pack(padx=15)

status = Label(root, fg="white", bg="red", text="Off", font=("Helvetica", 25))
status.pack(pady=15)

MIN, MAX = 0.05, 1

held = False

main_thread = threading.Thread(target=MainClass.main)
main_thread.start()

root.protocol("WM_DELETE_WINDOW", MainClass.on_quit)
root.mainloop()
