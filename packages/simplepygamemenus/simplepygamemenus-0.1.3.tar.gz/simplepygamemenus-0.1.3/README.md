# simplepygamemenus

*A package for making simple menus for your python games!*
- By Leonardo Ferrisi

# Installation

Install using

`pip install simplepygamemenus`

----------------------------

# Documentation / API

[local](docs/documentation.md)

[webpage](https://leonardoferrisi.github.io/simplepygamemenus-gitrepo/)

### Demo / Example:

See our [Demo File](demos/simplepygamemenus_demo.py)

------------------------------------------------

## Features:

- Make simple pygame menus

## Usage:
Create a main menu using the 'Menu()' construtor

    Example:
        myMenu = Menu(title="MyMainMenu")

Add buttons using:

    myMenu.add_button(label='button text', x, y, fontsize, function=<function to perform>)

    Example:
        if you have added a second menu, you can switch to it using your new button using the:
            
        `menuName.run_menu` function

    Example2:

       myMenu = Menu(title="MyMainMenu")
       myOtherMenu = Menu(title="myOtherMenu")
       myMenu.add_button(label='button text', x, y, fontsize, function=myOtherMenu.run_main)

I'll add more soon, see the example below!

- Leonardo

### Extra Info:

- PyPI Page: https://pypi.org/project/simplepygamemenus/0.1.0/



