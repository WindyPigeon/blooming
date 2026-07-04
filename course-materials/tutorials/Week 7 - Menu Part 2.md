# Week 7 - Menu Part 2:

## Create Menu without any package.

1. You may use the week7page1 and week7page2 python files.

2. You may start with creating the basic window for the pygame.

```python
import pygame
import sys
from week7page1 import page1
from week7page2 import page2
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    pygame.display.flip()
    clock.tick(60)
```

3. Since we are going to create many buttons, hence we will define a number of colors for button (2 each-hover and normal colours)

```python
GRAY = (200, 200, 200)
LIGHTBLUE = (160, 200, 210)
HOVER_LIGHTBLUE = (180, 220, 230)
GREEN = (34, 139, 34)
HOVER_GREEN = (46, 204, 113)
RED = (200, 30, 30)
HOVER_RED = (240, 50, 50)
```

4. Define the default value for global variables ; player name, dropdown button status and game level.

```python
playerName = ""
dropdownEnable = False
selectedLevel = "1"  # Default level
```

5. Since the button is customized, you need to define the location, size, color (image if necessary), text caption and its font colour, type and size, and action (behaviour). First you need to create a Button class along with the constructor.

```python
class Button:
    def __init__(self, text, x, y, width, height, normalColor, hoverColor, action=None, radius=0):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normalColor
        self.hover_color = hoverColor
        self.action = action
        self.border_radius = radius
        self.font = pygame.font.SysFont(None, 30)
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
```

6. Now define the function to update the text of the button (optional).

```python
def update(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
```

7. Now define the Button behaviour (what happens when mouse clicked). The function will check for the mouse clicked on the button.

```python
    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()
```

8. Create a function to draw the button. When the mouse hover the button, the colour will change to hover color else it will remain the normal color or back to normal color once the mouse left the button surface.

```python
def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        surface.blit(self.text_surf, self.text_rect)
```

<ins>**Full Code for the button class**</ins>

```python
class Button:
    def __init__(self, text, x, y, width, height, normalColor, hoverColor, action=None, radius=0):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normalColor
        self.hover_color = hoverColor
        self.action = action
        self.border_radius = radius

        # Font setup
        self.font = pygame.font.SysFont(None, 30)
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def update(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        surface.blit(self.text_surf, self.text_rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()
```

9. Now code the game start function. The game will redirect to the right function along with player name based on the chosen game level.

```python
def startGame():
    if selectedLevel == "1":
        page1(playerName)
    else:
        page2(playerName)
    pygame.display.set_caption("Main Menu")
```

10. Now code the end function, where the menu will trigger the endgame function whenever the quit button is click.

```python
def endGame():
    pygame.quit()
    sys.exit()
```

11. Now create a function to set the game level. The function will refer to the dropdown button status variable set previously and change it to true.

```python
def setLevel():
    global dropdownEnable
    dropdownEnable = True
```

12. Now update the game level by creating the selectlevel function. The function will received a value from main programme and update game level. Once the new game level is chosen, it will call the button object to update the button text caption based on the selected level.

```python
def selectLevel(num):
    global selectedLevel, dropdownEnable
    selectedLevel = str(num)
    dropdownEnable = False
    buttons[1].update(f"Level: {selectedLevel}")
```

13. Now we will create a textbox / textfield for user to enter the name using rectangle function.

```python
userTextbox = pygame.Rect(200, 150, 200, 40) #left, top, width , height
font = pygame.font.SysFont(None, 28)
userTextBoxEnable = False
```

14. Create all the buttons. Lets use 2 lists, one for the main buttons; Play Game, Set Level and also the quit game button. And another one list for the sub-buttons (list of drop down buttons). Create an object for each button, starting with setting the button text caption, X, Y location, width and height, color – normal and hover, function and also the border radius)

```python
buttons = [
    Button("Play Game", 200, 200, 200, 35, GREEN, HOVER_GREEN, startGame,10),
    Button("Set Level", 200, 250, 200, 35, LIGHTBLUE, HOVER_LIGHTBLUE, setLevel,10),
    Button("Quit", 200, 300, 200, 35, RED, HOVER_RED, endGame,10)
]

dropdownButtons = [
    Button("Level 1", 200, 300, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(1),30),
    Button("Level 2", 200, 350, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(2),30),
    Button("Level 3", 200, 400, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(3),30)
]
```

15. Now updates the game main loop, as follows.

```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
```

16. Add new code for the mouseclick on the buttons, the following logic will check which button is being clicked, it can be either one of the following.

* If the select game level button is clicked, the program will loop through each drop down buttons to determine which is being clicked (**collidepoint**) – then it will trigger the button behaviour to update the main button caption (select level), update game level variable.
* If textbox is being clicked, then it will enable user to enter data in the field.
* If normal button is being clicked, then it will trigger to execute the button behaviour.

```python
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dropdownButtonclicked = False
                if dropdownEnable:
                    for db in dropdownButtons:
                        if db.rect.collidepoint(event.pos):
                            db.check_click(event.pos)
                            dropdownButtonclicked = True
                            break

                if not dropdownButtonclicked:
                    for button in buttons:
                        button.check_click(event.pos)

                if userTextbox.collidepoint(event.pos):
                    userTextBoxEnable = True
                else:
                    userTextBoxEnable = False
```

17. Continue to add code for the typing behaviour in the player name textbox, where a backspace will remove the character from the playername, enter button will set the enable to false and continue typing will add characters to the existing playername.

```python
        if event.type == pygame.KEYDOWN and userTextBoxEnable:
                if event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                elif event.key == pygame.K_RETURN:
                    userTextBoxEnable = False
                else:
                    if len(playerName) >= 0 and event.unicode.isprintable():
                        playerName += event.unicode
```

18. Now add the code to render the user label as the instruction to the user. Start with rendering the font and update it to the screen.

```python
    prompt = font.render("Enter Player Name:", True, BLACK)
    screen.blit(prompt, (200, 120))
```

19. Continue with creating drawing the rectangle by setting the background and border colours

```python
    TextBoxbordercolor = LIGHTBLUE if userTextBoxEnable else GRAY
    pygame.draw.rect(screen, WHITE, userTextbox, 0, 10) # Filled background
    pygame.draw.rect(screen, BLACK, userTextbox, 2,10)     # Border
```

20. Follow up with additional code to render the font in the textbox to show the player name, size and colour.

```python
    namefont = font.render(playerName, True, BLACK)
    screen.blit(namefont, (userTextbox.x + 10, userTextbox.y + 10))
```

21. Now update the last part to draw all the buttons.

```python
    for button in buttons:
        button.draw(screen)

    if dropdownEnable:
        for db in dropdownButtons:
            db.draw(screen)

    pygame.display.flip()
    clock.tick(60)
```

<ins>**Drop down button list to select the game level.**</ins>

![A screenshot of a game  Description automatically generated](data:image/png;base64...)

<ins>**The main menu UI**</ins>

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)

Full Code

```python
import pygame
import sys
from week7page1 import page1
from week7page2 import page2

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHTBLUE = (160, 200, 210)
HOVER_LIGHTBLUE = (180, 220, 230)
GREEN = (34, 139, 34)
HOVER_GREEN = (46, 204, 113)
RED = (200, 30, 30)
HOVER_RED = (240, 50, 50)

playerName = ""
dropdownEnable = False
selectedLevel = "1"  # Default level

class Button:
    def __init__(self, text, x, y, width, height, normalColor, hoverColor, action=None, radius=0):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normalColor
        self.hover_color = hoverColor
        self.action = action
        self.border_radius = radius

        # Font setup
        self.font = pygame.font.SysFont(None, 30)
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def update(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        surface.blit(self.text_surf, self.text_rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

def startGame():
    if selectedLevel == "1":
        page1(playerName)
    else:
        page2(playerName)
    pygame.display.set_caption("Main Menu")

def endGame():
    pygame.quit()
    sys.exit()

def setLevel():
    global dropdownEnable
    dropdownEnable = True

def selectLevel(num):
    global selectedLevel, dropdownEnable
    selectedLevel = str(num)
    dropdownEnable = False
    buttons[1].update(f"Level: {selectedLevel}")

clock = pygame.time.Clock()

userTextbox = pygame.Rect(200, 150, 200, 40) #left, top, width , height
font = pygame.font.SysFont(None, 28)
userTextBoxEnable = False

buttons = [
    Button("Play Game", 200, 200, 200, 35, GREEN, HOVER_GREEN, startGame,10),
    Button("Set Level", 200, 250, 200, 35, LIGHTBLUE, HOVER_LIGHTBLUE, setLevel,10),
    Button("Quit", 200, 300, 200, 35, RED, HOVER_RED, endGame,10)
]

dropdownButtons = [
    Button("Level 1", 200, 300, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(1),30),
    Button("Level 2", 200, 350, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(2),30),
    Button("Level 3", 200, 400, 200, 40, LIGHTBLUE, HOVER_LIGHTBLUE, lambda: selectLevel(3),30)
]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dropdownButtonclicked = False
                if dropdownEnable:
                    for db in dropdownButtons:
                        if db.rect.collidepoint(event.pos):
                            db.check_click(event.pos)
                            dropdownButtonclicked = True
                            break

                if not dropdownButtonclicked:
                    for button in buttons:
                        button.check_click(event.pos)

                if userTextbox.collidepoint(event.pos):
                    userTextBoxEnable = True
                else:
                    userTextBoxEnable = False

        if event.type == pygame.KEYDOWN and userTextBoxEnable:
                if event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                elif event.key == pygame.K_RETURN:
                    userTextBoxEnable = False
                else:
                    if len(playerName) >= 0 and event.unicode.isprintable():
                        playerName += event.unicode

    screen.fill(WHITE)

    prompt = font.render("Enter Player Name:", True, BLACK)
    screen.blit(prompt, (200, 120))

    TextBoxbordercolor = LIGHTBLUE if userTextBoxEnable else GRAY
    pygame.draw.rect(screen, WHITE, userTextbox, 0, 10) # Filled background
    pygame.draw.rect(screen, BLACK, userTextbox, 2,10)     # Border

    namefont = font.render(playerName, True, BLACK)
    screen.blit(namefont, (userTextbox.x + 10, userTextbox.y + 10))

    for button in buttons:
        button.draw(screen)

    if dropdownEnable:
        for db in dropdownButtons:
            db.draw(screen)

    pygame.display.flip()
    clock.tick(60)
```
