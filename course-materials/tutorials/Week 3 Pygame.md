# Week 3 : Create a simple game using pygame

Objective: Learn how to create a simple basic game with pygame library.

Package: pygame

Documentation: [Pygame Front Page — pygame v2.6.0 documentation](https://www.pygame.org/docs/)

1. Install the package, if you have not done so previously.

2. Create a simple empty screen.

   The following code will create a 1000X800 blue colour background game window.

   Click ‘X’ to quite the game.

   a. Import the required library

```python
import pygame
import sys
```

   b. initiate the pygame object

```python
pygame.init()
```

   c. setup the pygame screen (the scene size) and choose the background color

```python
screen = pygame.display.set_mode((1000, 800)) #size 1000 (width) X 800(height)
background_color = (0, 128, 255) #RGB => blue
pygame.display.set_caption("my Game Windows")
```

   d. Start the game loop, the window will continue to loop and updating (rendering), click (‘x’) window close icon to closed the screen.

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color) # fill the screen with blue color
    # Update the screen
    pygame.display.flip() # render / update the screen after each update
```

   e. Stop the game.

```python
pygame.quit()
sys.exit()
```

   f. Now you may test to run the game.

![](data:image/png;base64...)

**Full Code**

```python
import pygame
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 800))
background_color = (0, 128, 255) #RGB => blue
pygame.display.set_caption("my Game Windows")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color) # fill the screen with blue color
    # Update the screen
    pygame.display.flip() # render / update the screen after each update

print("closing...")
pygame.quit()
sys.exit()
```

3. Add the background image and character.

   a. Go online and download your desire background image and one character.

   b. Load the images into the memory. Place the code after set the window caption

```python
background = pygame.image.load("C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\background.svg")
character = pygame.image.load("C:/Users/maryting/OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/characters.svg")
```

   c. Draw one image onto another surface, can draw on top of each other. Use the blit function to draw the image. Choose the desired coordinate where you want to place the image on the screen (X,Y). Place the code after the color the background

```python
    screen.blit(background, (0, 0))
    screen.blit(character, (400, 200))
```

   d. Run the program and check the UI. My images is too big…

![](data:image/png;base64...)

4. Scale the background and character

   a. Create a function to resize / scale the image. Place the code before initialize the game.

```python
def resizeObject(originObject, scaledFactor):
    scaledObject = pygame.transform.scale_by(originObject, scaledFactor)
    return (scaledObject)
```

   b. Resize the background to fit with the frame size (1000X800). Place the code after loading the images.

```python
UpdatedBackground = pygame.transform.scale(background, (1000, 800)) # Adjust the size to fit the screen
```

   c. Resize the character by percentage, calling the function. Place the code after the updated background.

```python
updatedcharacter = resizeObject(character, 0.5)
```

   d. Update the drawing with the updated images (scaled image) instead of the original image.

```python
  screen.blit(UpdatedBackground, (0, 0))
    screen.blit(updatedcharacter, (400, 500))
```

   e. Run the program, now both images are smaller and fit into the entire screen.

![](data:image/png;base64...)

5. Move the character around the screen.
   a. Create the rectangular area of the character and set the coordinate where the rectangular of the character should be. We will used back the previous location of the character. Place the code before the game start looping

```python
charRectBlock = updatedcharacter.get_rect()
charRectBlock.center = (400, 500)
```
   b. Now update the blid function for the drawing character. Change the coordinate to the rectangular block. The location will remain the same, instead of fixing the location to one constant location, we will keep drawing and updating the location of the character on the screen based on the location of the charRectBlock.

```python
    screen.blit(updatedcharacter, charRectBlock)
```

   c. Now add on the keyhandler to detect user pressing the key to move the charRectBlock around the screen. Place the code within the running loop (outside the event loop)

Reference: [pygame.key — pygame v2.6.0 documentation](https://www.pygame.org/docs/ref/key.html)

```python
  keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        charRectBlock.x -= 5
    if keys[pygame.K_RIGHT]:
        charRectBlock.x += 5
    if keys[pygame.K_UP]:
        charRectBlock.y -= 5
    if keys[pygame.K_DOWN]:
        charRectBlock.y += 5
```

   d. Now run the program, you may move the character around the screen using up, down, left and right key.

<ins>**Full Code**</ins>

```python
import pygame
import sys

def resizeObject(originObject, scaledFactor):
    scaledObject = pygame.transform.scale_by(originObject, scaledFactor)
    return (scaledObject)

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 800)) #x,y
background_color = (0, 128, 255) #RGB => blue
pygame.display.set_caption("my Game Windows")

background = pygame.image.load("C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\background.svg")
character = pygame.image.load("C:/Users/maryting/OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/characters.svg")

UpdatedBackground = pygame.transform.scale(background, (1000, 800)) # Adjust the size to fit the screen
updatedcharacter = resizeObject(character, 0.5)
* charRectBlock = updatedcharacter.get_rect() # get the rectagular surround the character
* charRectBlock.center = (400, 500)
* # Main game loop
* running = True
* while running:
* for event in pygame.event.get():
* if event.type == pygame.QUIT:
* running = False
* keys = pygame.key.get_pressed()
* if keys[pygame.K_LEFT]:
* charRectBlock.x -= 5
* if keys[pygame.K_RIGHT]:
* charRectBlock.x += 5
* if keys[pygame.K_UP]:
* charRectBlock.y -= 5
* if keys[pygame.K_DOWN]:
        charRectBlock.y += 5

    screen.fill(background_color)
    # screen.blit(background, (0, 0))
    # screen.blit(character, (400, 200))

    screen.blit(UpdatedBackground, (0, 0))
    screen.blit(updatedcharacter, charRectBlock)

    # Update the screen
    pygame.display.flip() # render / update the screen after each update

print("closing...")
pygame.quit()
sys.exit()
```

6. Add the text (narrative) onto the screen. Please the following code before the game looping.
   a. Setup the font size and create a variable with text content.

```python
font = pygame.font.Font(None, 36)
content= "Now the story begin...."
```

   b. Create another variable to show the text (text surface) – font size, content and color.

```python
contentSurface = font.render(content, True, ((255, 0, 0))) #red color
```

   c. Get the rectangular (border) for the text surface.

```python
textRect = contentSurface.get_rect(center=(200, 50))
```

   d. Draw the text on the screen. Place the code after character drawing.

```python
 screen.blit(contentSurface, textRect)
```

   e. Run the program and you will see the following output

![](data:image/png;base64...)

7. Enhance the narrative to make it into a dialogues which will loop through a sequence a text with 3 second interval. Please the following code before the game looping.

   a. Replace the existing content (single line) with a dialogue (list).

```python
dialogue = [
    "Welcome to the ISE class!",
    "It is Christmas time....",
    "Greeting....",
    "Lets have fun."
]
```

   b. Setup the dialogue timing, first line, and animation (text changing) interval.

```python
currLine = 0
diaTime = 0 # dialogue time
diaInterval = 3000  # milliseconds (3 seconds)
```

   c. Setup the clock to control the dialogue sequence. (create the timer object to keep track of the time)

```python
clock = pygame.time.Clock()
```

   d. Create a function to display the dialogue, you need to move the old code (set the content color, font size, get rectangular, drawing) into the function. We are going to loop through the dialogue list and display the content on the screen line by line.

```python
def renderDialogue():
    global currLine
    if currLine < len(dialogue):
        contentSurface = font.render(dialogue[currLine], True, (255,0,0))
        textRect = contentSurface.get_rect(center=(200, 50))
        screen.blit(contentSurface , textRect)
```

   e. Add in the control in the game running to get the time, and keep getting the time and add into the dialogue time, once it reach 3 seconds, the current line will increase by one (to change the line).

```python
   # Update the timer
    diaTime += clock.get_time()
    if diaTime >= diaInterval:
        currLine += 1
        diaTime = 0  # Reset the timer
```

   f. Replace the old code blit function in the loop with calling the render dialogue function.

```python
    renderDialogue()
```

   g. Add the clock tick function to run the game with max 60 frame per second.

```python
clock.tick(60)
```

   h. Run the program and you will notice the looping of the dialogue content. Every 3 second the line will be updated

![](data:image/png;base64...)

Full Code

```python
import pygame
import sys

def resizeObject(originObject, scaledFactor):
    scaledObject = pygame.transform.scale_by(originObject, scaledFactor)
    return (scaledObject)

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 800)) #x,y
background_color = (0, 128, 255) #RGB => blue
pygame.display.set_caption("my Game Windows")

background = pygame.image.load("C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\background.svg")
character = pygame.image.load("C:/Users/maryting/OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/characters.svg")
UpdatedBackground = pygame.transform.scale(background, (1000, 800)) # Adjust the size to fit the screen
updatedcharacter = resizeObject(character, 0.5)
charRectBlock = updatedcharacter.get_rect() # get the rectagular surround the character
charRectBlock.center = (400, 500)

#setup the text font size and text content
font = pygame.font.Font(None, 36)
#content = "Now the story begin...."

dialogue = [
    "Welcome to the ISE class!",
    "It is Christmas time....",
    "Greeting....",
    "Lets have fun."
]
currLine = 0
diaTime = 0 # dialogue time
diaInterval = 3000  # milliseconds (3 seconds)
clock = pygame.time.Clock()

def renderDialogue():
    global currLine
    if currLine < len(dialogue):
        contentSurface = font.render(dialogue[currLine], True, (255,0,0))
        textRect = contentSurface.get_rect(center=(200, 50))
        screen.blit(contentSurface , textRect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        charRectBlock.x -= 5
    if keys[pygame.K_RIGHT]:
        charRectBlock.x += 5
    if keys[pygame.K_UP]:
        charRectBlock.y -= 5
    if keys[pygame.K_DOWN]:
        charRectBlock.y += 5

    # Update the timer
    diaTime += clock.get_time()
    if diaTime >= diaInterval:
        currLine += 1
        diaTime = 0  # Reset the timer

    screen.fill(background_color)
    # screen.blit(background, (0, 0))
    # screen.blit(character, (400, 200))

    screen.blit(UpdatedBackground, (0, 0))
    screen.blit(updatedcharacter, charRectBlock)
    #screen.blit(contentSurface, textRect)
    renderDialogue()
    # Update the screen
    pygame.display.flip() # render / update the screen after each update

    clock.tick(60)

print("closing...")
pygame.quit()
sys.exit()
```

8. Let’s add the timer on the screen.
   a. Setup the information for the timer.

```python
GameTime = 60  # init seconds
countdownEvent = pygame.USEREVENT + 1 # id 1-24 is for internal used, 25 is userevent, for unique own even +1 => 26
pygame.time.set_timer(countdownEvent, 1000)  # Trigger event every second
```

   b. Create a function to display the timer. Use the previous font size, set the content (time) and colour for the time. Place the timer position on the top right side of the screen and display the timer.

```python
def displayTimer():
    TimerSurface = font.render(f"Time: {GameTime}", True, (0,0,0))
    TimerRect = TimerSurface.get_rect(topright=(950, 50))
    screen.blit(TimerSurface, TimerRect)
```

   c. Modify the function created in b) to add a rectangular to surround the timer. The background set to white color.

```python
def displayTimer():
    TimerSurface = font.render(f"Time: {GameTime}", True, (0,0,0))
    TimerRect = TimerSurface.get_rect(topright=(950, 50))
    TimerBackground = pygame.Rect(TimerRect.left - 2, TimerRect.top - 2, TimerRect.width + 2, TimerRect.height + 2)
    pygame.draw.rect(screen, (255,255,255), TimerBackground)
    screen.blit(TimerSurface, TimerRect)
```

   d. Check the control flow of the countdownEvent defined previously in the game loop, the program will trigger the event every 1 second to deduct the time from 60 seconds to zero seconds.

```python
   elif event.type == countdownEvent:
            GameTime -= 1
            if GameTime <= 0:
                GameTime = 0  # Stop
```

   e. Add the display timer function in the game loop.

```python
    displayTimer()
```

   f. Run the program and you will notice the timer countdown in the game.

![](data:image/png;base64...)

**Full Code**

```python
import pygame
import sys

def resizeObject(originObject, scaledFactor):
    scaledObject = pygame.transform.scale_by(originObject, scaledFactor)
    return (scaledObject)

pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 800)) #x,y
background_color = (0, 128, 255) #RGB => blue
pygame.display.set_caption("my Game Windows")

background = pygame.image.load("C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\background.svg")
character = pygame.image.load("C:/Users/maryting/OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/characters.svg")
UpdatedBackground = pygame.transform.scale(background, (1000, 800)) # Adjust the size to fit the screen
updatedcharacter = resizeObject(character, 0.5)
charRectBlock = updatedcharacter.get_rect() # get the rectagular surround the character
charRectBlock.center = (400, 500)

#setup the text font size and text content
font = pygame.font.Font(None, 36)
#content = "Now the story begin...."

dialogue = [
    "Welcome to the ISE class!",
    "It is Christmas time....",
    "Greeting...."
    "Lets have fun."
]
currLine = 0
diaTime = 0 # dialogue time
diaInterval = 3000  # milliseconds (3 seconds)
clock = pygame.time.Clock()

def renderDialogue():
    global currLine
    if currLine < len(dialogue):
        contentSurface = font.render(dialogue[currLine], True, (255,0,0))
        textRect = contentSurface.get_rect(center=(200, 50))
        screen.blit(contentSurface , textRect)

# Render the text
# contentSurface = font.render(content, True, ((255, 0, 0))) #red color
# textRect = contentSurface.get_rect(center=(200, 50))

# Set up the countdown timer
GameTime = 60  # init seconds
countdownEvent = pygame.USEREVENT + 1 # id 1-24 is for internal used, 25 is userevent, for unique own even +1 => 26
pygame.time.set_timer(countdownEvent, 1000)  # Trigger event every second

def displayTimer():
    TimerSurface = font.render(f"Time: {GameTime}", True, (0,0,0))
    TimerRect = TimerSurface.get_rect(topright=(950, 50))
    TimerBackground = pygame.Rect(TimerRect.left - 2, TimerRect.top - 2, TimerRect.width + 2, TimerRect.height + 2)
    pygame.draw.rect(screen, (255,255,255), TimerBackground)
    screen.blit(TimerSurface, TimerRect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == countdownEvent:
            GameTime -= 1
            if GameTime <= 0:
                GameTime = 0  # Stop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        charRectBlock.x -= 5
    if keys[pygame.K_RIGHT]:
        charRectBlock.x += 5
    if keys[pygame.K_UP]:
        charRectBlock.y -= 5
    if keys[pygame.K_DOWN]:
        charRectBlock.y += 5

    # Update the timer
    diaTime += clock.get_time()
    if diaTime >= diaInterval:
        currLine += 1
        diaTime = 0  # Reset the timer

    screen.fill(background_color)
    # screen.blit(background, (0, 0))
    # screen.blit(character, (400, 200))

    screen.blit(UpdatedBackground, (0, 0))
    screen.blit(updatedcharacter, charRectBlock)
    #screen.blit(contentSurface, textRect)
    renderDialogue()
    displayTimer()
    # Update the screen
    pygame.display.flip() # render / update the screen after each update

    clock.tick(60)

print("closing...")
pygame.quit()
sys.exit()
```

**Exercise**

Write a narrative for APU students’ academic Journey. Create a simple narrative (10 lines) into the game. Set the dialogue interval to 5 seconds per line. The game will auto closed when the timer reach <ins>**zero**</ins> seconds. Make sure the background is related to the education environment. Update the character with the student character (make sure transparent background).
