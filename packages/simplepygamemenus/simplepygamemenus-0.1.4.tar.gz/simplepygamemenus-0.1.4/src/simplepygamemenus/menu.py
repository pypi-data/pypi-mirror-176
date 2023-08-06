"""
SIMPLE PYGAME MENU - Leonardo Ferrisi 23' 

contact: ferrisil@union.edu

A python package for simplifying the process of importing your pygame menus

Some Rules:

    - Make the main menu first!
    - If you want to be able to switch back to the previous menu, set the main parameter in Menu() to the previous menu

"""
import os
import pygame
import sys

DIRNAME = os.path.dirname(__file__)

def get_font(size:int=None, font_path:str=None) -> pygame.font.Font: # Returns Press-Start-2P in the desired size
    """
    Gets a font from a provided .ttf file indicated by `font_path`

        Parameters:
            `size`      (int): The size of the font
            `font_path` (str): Default is None. The path to a font file if applicable. 
    """
    if size is None: raise ValueError("size cannot be None")
    if font_path is not None: return pygame.font.Font(os.path.join(DIRNAME, font_path), size)
    else: return pygame.font.Font(os.path.join(DIRNAME, "font.ttf"), size)

class Button():
    """
    A button you can click on and execute functions with
    """
    def __init__(self, image:pygame.Surface, pos:tuple, text_input:str, font:pygame.font.Font, base_color:tuple, hovering_color:tuple):
        """
        Create a Button object

            Parameters:
                `image`      (pygame.Surface): An image to overlay the text on. Example: a rectangle
                `pos`                 (tuple): A tuple containing the x, y position of the button center
                `text_input`            (str): The text that goes on the button
                `font`     (pygame.font.Font): The font of the text. Use `get_font` for best functionality
                `base_color`            (str): The base color of button when not being interacted with
                `hovering_color`        (str): The hovering color of button when being interacted with
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen:pygame.Surface) -> None:
        """
        Updated the Button state

            Paramters:
                `screen` (pygame.Surface): The pygame surface object that we are composing the button onto
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position:tuple) -> bool:
        """
        Given an (x,y) position, typically provided by `pygame.mouse.get_pos()`
        tell us if the mouse is interacting with button

            Parameters:
                `position` (tuple): The x, y position provided by `pygame.mouse.get_pos()`
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position:tuple) -> None:
        """
        Given an (x,y) position, typically provided by `pygame.mouse.get_pos()`
        tell us if the mouse is above the button and change color accordingly

            Parameters:
                `position` (tuple): The x, y position provided by `pygame.mouse.get_pos()`
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class Menu:
    """
    A constructor for menus
    """
    
    def __init__(self, caption="A Simple Pygame Menu", title="MENU", x=500, y=500,world=None, background=None, displaytitle=True, main=None, useDisplayScreen=True, showESCKEYhint=True):
        """
        Creates a Menu object

        Parameters:
            `caption`            (str): The window caption of your menu
            `title`              (str): The title of your menu, is by default shown at the top of your menu, can be hidden by setting 'displayTitle' to False
            `x`                  (int): The width of your menu, leave blank if using a pygame.Surface object or using another menu as main
            `y`                  (int): The width of your menu, leave blank if using a pygame.Surface object or using another menu as main
            `world`   (pygame.Surface): A pygame surface object you can use as the base python screen. An alternative to using x, y for dimensions. 
                                        Useful for having all menus use the same display
            `background`         (str): The local path to a background file
                                        If you have an image you want to use as a background, provide the **FULL** filepath to the image here.
            `displaytitle`      (bool): A boolean to hide or show the title on your menu
            `main`              (Menu): Add a main menu to return to with ESC. Pass in another menu object to be able to return to it by clicking ESC
            `useDisplaySceen`   (bool): In the event you do not want to use the display screen passed in by `world` or `main`, set this to False. Default is True
            `showESCKEYhint`    (bool): True if you wish to show a hint at the top of all menus that have a `main` parameter that is not None. Else set to False.
        """
        self.caption          = caption
        self.title            = title
        self.buttons          = []
        self.text_to_display  = []
        self.background       = None
        self.background_color = "black"
        self.main             = main
        self.displaytitle     = displaytitle
        self.alternate_escape = None

        # TODO: make showESCKEYhint auto off it alternate_escape has been created 
        
        if main is not None and useDisplayScreen:
            if not isinstance(main, self.__class__): raise ValueError("Main Menu must be instance of Menu object")
            self.load_win_dimensions(self.main.SCREEN.get_width(),self.main.SCREEN.get_height())
            if background is not None: background_path = os.path.join(DIRNAME, background)
            else: background_path = None
            self.prepSCREEN(screen=self.main.SCREEN, background_filepath=background_path)
            if showESCKEYhint: self.add_text(text="Press ESC to return to the previous menu", x=self.center_win_width, y=10, size=10, color=(255,255,255))
        else:
            if world is not None:
                if not isinstance(world, pygame.Surface): raise ValueError("world must be a pygame.Surface object")
                self.load_win_dimensions(world.get_width(),world.get_height())
                if background is not None: background_path = os.path.join(DIRNAME, background)
                else: background_path = None
                self.prepSCREEN(screen=world, background_filepath=background_path)
            else:
                print("loading non world params")
                self.load_win_dimensions(x,y)
                if background is not None: background_path = os.path.join(DIRNAME, background)
                else: background_path=None
                self.prepSCREEN(screen=None, background_filepath=background_path)
        
        if self.displaytitle: self.add_text(text=self.title, x=self.center_win_width, y=80, size=30, color=(255,255,255))
                
    def load_win_dimensions(self, x:int, y:int) -> None:
        """
        Given an x, y input - load them as the instance variables for window height and width

            Parameters:
                `x` (int): The width of Menu window
                `y` (int): The height of Menu window
        """
        self.win_height = y # y
        self.win_width  = x  # x
        self.center_win_height = y // 2
        self.center_win_width  = x // 2

    def default_func(self) -> None:
        """
        Useless placeholder to demonstrate a thing a button can do.
        """
        print("[DEFAULT FUNC] I should do something")

    def add_button(self, label:str="button", function:callable=None, x:int=0, y:int=0, font:str=None, fontsize:int=30, basecolor:tuple=(0,0,255), hovercolor:tuple=(255,255,0)) -> None:
        """
        Add a button object to internal button storage.
        When Menu is run using `<menu name>.run_menu()`, all buttons added with this method are rendered.


            Parameters:
                `label`          (str): Text to display on the button
                `function`  (callable): A callable function for the button to execute
                        
                    NOTE : functions passed in must not be called when being passed. Do not use `()` when passing function in.

                        Proper Usage Example:
                    
                            `def callable_method():`
                                `do something`
                    
                            `menu.add_button(... , ... , function = callable_method , ... )` 

                `x`              (int): The x coordinate of the button center
                `y`              (int): The y coordinate of the button center
                `font`           (str): The filepath to a font ttf file if applicable. Leave as None to use default font
                `fontsize`       (int): The size of the label font
                `basecolor`    (tuple): RGB tuple representing the button color when mouse IS NOT hovering over it
                `hovercolor`   (tuple): RGB tuple representing the button color when mouse IS hovering over it

        """
        if function is None:
            if not isinstance(function, callable): raise TypeError("'function' parameter must be callable")
            function = self.default_func
        if font is None: font = get_font(fontsize)
        img = pygame.image.load(os.path.join(DIRNAME, "rect.png"))
        b = Button(image=img, pos=(x,y), text_input=label, font=font, base_color=basecolor, hovering_color=hovercolor)
        self.buttons.append((b, function))

    def add_text(self, text:str="default", x:int=0, y:int=0, size:int=45, color:str="#b68f40") -> None:
        """
        Add text to render for the menu

            Parameters: 
                `text`   (str): The text to add
                `x`      (int): The x coordinates for text center
                `y`      (int): The y coordinates for text center
                `size`   (int): The size of the text
                `color`  (str): A string representing color values in hexadecimal
        """
        display = (text, (x,y), size, color)
        self.text_to_display.append(display)
    
    def prepSCREEN(self, screen:pygame.Surface=None, background_filepath:str=None) -> None:
        """
        Initializes pygame and sets the screen and background where applicable

            Parameters:
                `screen` (pygame.Surface)  : Default is None. Pass in pygame.Surface object instead to use that
                `background_filepath` (str): Default is None. The filepath of an image file to use as a background.
        """
        pygame.init()
        if screen is None: self.SCREEN = pygame.display.set_mode((self.win_width, self.win_height))
        else: self.SCREEN = screen
        self.background = pygame.image.load(os.path.join(DIRNAME, background_filepath)) if background_filepath is not None else None  

    def set_background_color(self, color:str=None) -> None:
        """
        Change the background color.

            Parameters:
                `color` (str): A string representing the color.

                    Example: 
                        color = "white"
        """
        if color is None: raise ValueError("Color was None, please provided a string represented color")
        self.background_color = color

    def modify_ESC_behavior(self, function=None):
        """
        Modify what ESC does, especially if menu is present
        """
        if function is None: raise ValueError("function cannot be None")
        self.alternate_escape = function

    def run_menu(self) -> None:
        """
        Runs the menu as a loop
        """
        
        while True:
            pygame.display.set_caption(self.caption)
            self.render_background(self.background_color)
            self.render_display_texts()

            MOUSEPOS = pygame.mouse.get_pos()

            self.render_buttons(MOUSEPOS=MOUSEPOS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        if self.alternate_escape is not None:
                            self.alternate_escape()
                        elif self.main is None: 
                            if self.alternate_escape is not None:
                                self.alternate_escape()
                            else:
                                pygame.quit()
                                sys.exit()
                        else:
                            self.main.run_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle button press
                    for button_set in self.buttons:
                        button = button_set[0]
                        func  = button_set[1]
                        if button.checkForInput(MOUSEPOS):
                            func()
            pygame.display.update() # ESSENTIAL FOR CHANING MENUS!


    def render_background(self, color:str="black") -> None:
        """
        Renders the background. If self.background is not None, uses that as the background
        otherwise uses a solid color
        
            Parameters:
                `color` (str): Default is 'black'. A string representing the color.

                    Example: 
                        color = "black"
        """
        if self.background is not None:
            self.SCREEN.fill(color)
            self.load_background_coords(use_center=True)
            self.SCREEN.blit(self.background, self.background_coords)
        else:
            self.SCREEN.fill(color)

    def render_buttons(self, MOUSEPOS:tuple=None) -> None:
        """
        Renders all added Buttons onto the menu

            Parameter:
                `MOUSEPOS` (tuple[int, int]): An x, y pos extracted from pygame.mouse.get_pos
        """
        if MOUSEPOS is None: raise ValueError("MOUSEPOS cannot be None")
        assert self.SCREEN is not None
        for button_set in self.buttons:
            button = button_set[0]
            button.changeColor(MOUSEPOS)
            button.update(self.SCREEN)

    def render_display_texts(self) -> None:
        """
        Renders all added Text onto the menu
        """
        assert self.SCREEN is not None
        for text_set in self.text_to_display:
            text, pos, size, color = text_set
            self.display_text(text=text, size=size, pos=pos, color=color, custom_font=None)

    def load_background_coords(self, use_center=True) -> None:
        """
        Loads the background coordinates

            Parameters:
                `use_center` (bool): Default is True. Declares whether to center background or not
        """
        
        self.background_coords = (0,0)
        if self.background is not None:
            bg_x = self.background.get_width()
            bg_y = self.background.get_height()

            cbg_x = bg_x // 2
            cbg_y = bg_y // 2
            
            if use_center: 
                coords = ((self.center_win_width-cbg_x),(self.center_win_height-cbg_y))   
                self.background_coords = coords

    def gen_text(self, text:str="", size:str=45, color:str="#b68f40", pos:tuple=(0,0), custom_font:str=None) -> None:
        """
        Generates text to display

            Parameters:

                `text`             (str): The text to display
                `size`             (int): The size of the text. Default is 45
                `color`            (str): Color of the text as a hexadecimal code.
                `pos`  (tuple[int, int]): The position of the text in x,y format
                `custom_font`      (str): Custom font (.ttf) filepath. Default is None
        """
        TEXT = get_font(size=size, font_path=custom_font).render(text, True, color)
        TEXT_RECT = TEXT.get_rect(center=pos)
        return TEXT, TEXT_RECT

    def display_text(self, text="", size=45, color="#b68f40", pos=(0,0), custom_font=None, line_spacing=10):
        """
        Displays the text on the Menu

            Parameters:

                `text`             (str): The text to display
                `size`             (int): The size of the text. Default is 45
                `color`            (str): Color of the text as a hexadecimal code.
                `pos`  (tuple[int, int]): The position of the text in x,y format
                `custom_font`      (str): Custom font (.ttf) filepath. Default is None
                `line_spaceing`    (int): The spacing for text that uses `\n` characters

        """
        if "\n" in text:
            text = text.split("\n")
            for i, line in enumerate(text):
                y_pos = pos[1]+((size+line_spacing)*i)
                line, text_rect = self.gen_text(text=line, size=size, pos=(pos[0], y_pos ), color=color, custom_font=custom_font)
                self.SCREEN.blit(line, text_rect)
        else:
            text, text_rect = self.gen_text(text=text, size=size, pos=pos, color=color, custom_font=custom_font)
            self.SCREEN.blit(text, text_rect)

if __name__ == "__main__":


# DEFAULT: UNCOMMENT TO TRY OUT!

    # USING ANOTHER DISPLAY OBJECT (your main one perhaps?)

    mywin = pygame.display.set_mode((1000, 700))

    main = Menu(world=mywin)
    main.add_text(text="SIMPLE PYGAME MENUS", x=500, y=30, size=25)
    b_menu = Menu(main=main, title="other menu", showESCKEYhint=True)
    main.add_button(label="WHATS THIS?", x=500, y=250, fontsize=30, function=b_menu.run_menu)
    b_menu.add_button(label="exit", x=500, y=250, fontsize=30, function=sys.exit)

    next_menu = Menu(title="NEXT",main=b_menu)
    b_menu.add_button(label="next menu", x=500, y=400, fontsize=30, basecolor=(0,255,0), hovercolor=(255,255,255), function=next_menu.run_menu)

    
    main.run_menu()


# NON DEFAULT: UNCOMMENT TO TRY OUT!

    # USING DEFAULT or DEFINED local display

        # Notice that no display has been defined above, the display use is the one from the main menu

    # main = Menu(x=800, y=800)
    # main.add_text(text="SIMPLE PYGAME MENUS", x=400, y=30, size=25)
    # b_menu = Menu(main=main, title="other menu", showESCKEYhint=True)
    # main.add_button(label="WHATS THIS?", x=400, y=250, fontsize=30, function=b_menu.run_menu)
    # b_menu.add_button(label="exit", x=400, y=250, fontsize=30, function=sys.exit)

    # next_menu = Menu(title="NEXT",main=b_menu)
    # b_menu.add_button(label="next menu", x=400, y=400, fontsize=30, basecolor=(0,255,0), hovercolor=(255,255,255), function=next_menu.run_menu)

    
    # main.run_menu()




    

