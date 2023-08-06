import keyboard
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Menu:
    def __init__(self, title:str, items:list, symbol:str=">", pre_selected:int=0):
        self.selected = pre_selected
        self.title = title
        self.items = items
        self.symbol = symbol

    def prepare(self):
        clear()
        print(self.title)
        for i in range(0, len(self.items)):
            print("{1} {0}. {2}".format(i + 1, "\x1b[6;30;42m{0}".format(self.symbol) if self.selected == i else " ", self.items[i] + "\x1b[0m"))

    def up(self):
        if self.selected == 0:
            return
        self.selected -= 1
        self.prepare()

    def down(self):
        if self.selected == len(self.items) - 1:
            return
        self.selected += 1
        self.prepare()

    def show_menu(self):
        self.prepare()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait("enter")
        input()
        return self.selected