# Topic : Menu page

Library: pygame-menu

Url Link: [pygame-menu — pygame-menu 4.5.4 Documentation](https://pygame-menu.readthedocs.io/en/latest/index.html)

Install the package : pip install pygame-menu

1. We will be using pygame and pygame menu package in this exercise.

2. Start with creating the basic frame for the game.

```python
import pygame
import pygame_menu as pyMenu
from pygame_menu import themes

pygame.init()
surface = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
           running = False
    surface.fill((0, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

3. Start with creating the global variables

```python
MENU, LOADING, GAME, PAGE2 = "menu", "loading", "game", "page2"
state = MENU
player = "User"
selected_difficulty = 1
updateLoading = pygame.USEREVENT + 1
```

4. Now we will add the menu; add the player name, play, difficulty level, history and quit game buttons.

```python
mainMenu = pyMenu.Menu('Welcome Page \n Main Menu', 600, 600, theme=themes.THEME_SOLARIZED)
mainMenu.add.text_input('Name: ', default='', onchange=setPlayerName)
mainMenu.add.button('Play', startGame) # call the startGame function when user press the button
mainMenu.add.button('Levels', gameLevelMenu)
mainMenu.add.button('History', gameHistory)
mainMenu.add.button('Quit', pygame.quit)

loadingMenu = pyMenu.Menu('Loading...', 600, 600, theme=themes.THEME_DARK)
progress = loadingMenu.add.progress_bar("Progress", progressbar_id="pb1", default=0, width=300)
levelMenu = pyMenu.Menu('Select a Difficulty', 600, 600, theme=themes.THEME_BLUE)
levelMenu.add.selector('Difficulty :', [('EASY', 1), ('MEDIUM', 2), ('HARD', 3)], onchange=setDifficulty)

historyMenu = pyMenu.Menu('History', 600, 600, theme=themes.THEME_SOLARIZED)
historyMenu.add.button("Back", lambda: setMenuState())
```

5. Now add the function when these button is click / selected.

```python
def startGame():
    global state
    state = LOADING
    progress.set_value(0)
    pygame.time.set_timer(updateLoading, 20)

def setDifficulty(value, difficulty):
    global selected_difficulty
    selected_difficulty = difficulty
    print(f"Difficulty set to {value[0]} ({difficulty})")

def gameLevelMenu():
    mainMenu._open(levelMenu)

def gameHistory():
    global state
    state = "history"

    historyMenu.clear()
    historyMenu.add.label("History")

    try:
        with open(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\history.txt", "r") as f:
            for line in f:
                historyMenu.add.label(line.strip())
    except FileNotFoundError:
        historyMenu.add.label("No history found.")

    historyMenu.add.button("Back", lambda: setMenuState())

def setPlayerName(name):
    global player
    player = name

def setMenuState():
    global state
    state = MENU
```

6. Update in the main game loop function to update the state of the game and screen after user select the button from the menu. Place the following code after the surface.fill function.

```python
if state == MENU:
        mainMenu.update(events)
        mainMenu.draw(surface)

    elif state == LOADING:
        loadingMenu.update(events)
        loadingMenu.draw(surface)

    elif state == GAME:
        page1(player)
        state = MENU

    elif state == PAGE2:
        page2(player)
        state = MENU

    elif state == "history":
        historyMenu.update(events)
        historyMenu.draw(surface)
```

7. Insert the following code into the main game loop function to update the state of the progress bar (game play). And also page that it suppose to load.

```python
   if state == LOADING and event.type == updateLoading:
            val = progress.get_value()
            progress.set_value(val + 1)
            if val + 1 >= 100:
                pygame.time.set_timer(updateLoading, 0)
                if selected_difficulty == 1:
                    state = GAME  # Hard
                elif selected_difficulty == 2:
                    state = PAGE2   # Medium
                elif selected_difficulty == 3:
                    print("Hard mode selected. your implementation.")
                    state = MENU
```

8. Copy and paste the following code into two additional files; week7page1 and week7page2.

<ins>**week7page1**</ins>

```python
import pygame

def page1(player_name):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Page 1 (Easy Level)")
    background_color = (0, 128, 255)

    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Player: {player_name} (Easy)", True, (255, 255, 255))

    # Player settings
    player_rect = pygame.Rect(300, 300, 50, 50)
    player_color = (255, 255, 0)
    player_speed = 5

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # ESC to return to menu

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # Screen boundaries
        player_rect.x = max(0, min(player_rect.x, 600 - player_rect.width))
        player_rect.y = max(0, min(player_rect.y, 600 - player_rect.height))

        screen.fill(background_color)
        screen.blit(text_surface, (20, 20))
        pygame.draw.rect(screen, player_color, player_rect)

        pygame.display.flip()
        clock.tick(60)

    return
```

<ins>**week7page2**</ins>

```python
import pygame

def page2(player_name):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Page - Medium Level")
    background_color = (200, 0, 0)

    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Player: {player_name} - Medium MODE", True, (255, 255, 255))

    player_rect = pygame.Rect(300, 300, 50, 50)
    player_color = (255, 255, 255)
    player_speed = 7

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]: player_rect.x += player_speed
        if keys[pygame.K_UP]: player_rect.y -= player_speed
        if keys[pygame.K_DOWN]: player_rect.y += player_speed

        player_rect.x = max(0, min(player_rect.x, 600 - player_rect.width))
        player_rect.y = max(0, min(player_rect.y, 600 - player_rect.height))

        screen.fill(background_color)
        screen.blit(text_surface, (20, 20))
        pygame.draw.rect(screen, player_color, player_rect)

        pygame.display.flip()
        clock.tick(60)
```

9. Now link the page, by placing these code at the top of the screen.

```python
from week7page1 import page1  # Easy level page
from week7page2 import page2  # Medium level page
```

10. Now run the code and you will see the following.

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)

<ins>**Full code (main)**</ins>

```python
import pygame
import pygame_menu as pyMenu
from pygame_menu import themes
from week7page1 import page1  # Easy level page
from week7page2 import page2  # Medium level page

pygame.init()
surface = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

MENU, LOADING, GAME, PAGE2 = "menu", "loading", "game", "page2"
state = MENU
player = "User"
selected_difficulty = 1

updateLoading = pygame.USEREVENT + 1

def startGame():
    global state
    state = LOADING
    progress.set_value(0)
    pygame.time.set_timer(updateLoading, 20)

def setDifficulty(value, difficulty):
    global selected_difficulty
    selected_difficulty = difficulty
    print(f"Difficulty set to {value[0]} ({difficulty})")

def gameLevelMenu():
    mainMenu._open(levelMenu)

def gameHistory():
    global state
    state = "history"

    historyMenu.clear()
    historyMenu.add.label("History")

    try:
        with open(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\history.txt", "r") as f:
            for line in f:
                historyMenu.add.label(line.strip())
    except FileNotFoundError:
        historyMenu.add.label("No history found.")

    historyMenu.add.button("Back", lambda: setMenuState())

def setPlayerName(name):
    global player
    player = name

def setMenuState():
    global state
    state = MENU

# --- Menus ---
mainMenu = pyMenu.Menu('Welcome Page \n Main Menu', 600, 600, theme=themes.THEME_SOLARIZED)
mainMenu.add.text_input('Name: ', default='', onchange=setPlayerName)
mainMenu.add.button('Play', startGame)
mainMenu.add.button('Levels', gameLevelMenu)
mainMenu.add.button('History', gameHistory)
mainMenu.add.button('Quit', pygame.quit)

loadingMenu = pyMenu.Menu('Loading...', 600, 600, theme=themes.THEME_DARK)
progress = loadingMenu.add.progress_bar("Progress", progressbar_id="pb1", default=0, width=300)

levelMenu = pyMenu.Menu('Select a Difficulty', 600, 600, theme=themes.THEME_BLUE)
levelMenu.add.selector('Difficulty :', [('EASY', 1), ('MEDIUM', 2), ('HARD', 3)], onchange=setDifficulty)

historyMenu = pyMenu.Menu('History', 600, 600, theme=themes.THEME_SOLARIZED)
historyMenu.add.button("Back", lambda: setMenuState())

# --- Main Loop ---
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if state == LOADING and event.type == updateLoading:
            val = progress.get_value()
            progress.set_value(val + 1)
            if val + 1 >= 100:
                pygame.time.set_timer(updateLoading, 0)
                if selected_difficulty == 1:
                    state = GAME  # EASY
                elif selected_difficulty == 2:
                    state = PAGE2   # Medium
                elif selected_difficulty == 3:
                    print("Hard mode selected. your implementation.")
                    state = MENU

    surface.fill((0, 0, 0))

    if state == MENU:
        mainMenu.update(events)
        mainMenu.draw(surface)

    elif state == LOADING:

        loadingMenu.update(events)

        loadingMenu.draw(surface)

    elif state == GAME:
        page1(player)
        state = MENU

    elif state == PAGE2:
        page2(player)
        state = MENU

    elif state == "history":
        historyMenu.update(events)
        historyMenu.draw(surface)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**Exercise:**

Add the code for the page3 (Hard level).

Now you may pass the data back to the main menu / store it in the history file
