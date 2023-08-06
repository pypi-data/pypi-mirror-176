# kiwi menu

## Example
```py
from kiwi_menu import Menu

fruits = ["apple", "banana", "kiwi"]
menu = Menu(
    "Choose a fruit",
    fruits
)
selected = menu.show_menu()
print("You choosed", fruits[selected])
```