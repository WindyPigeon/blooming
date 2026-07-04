# Topic: pygame Movement

You may download some free assets from the following website:

[2D Game Assets Store & Free - CraftPix.net](https://craftpix.net/)

## Task 1: Follow the given example in the below to learn how to auto extract multiple frames from sprite

a. Create the basic frame and structure for your pygame

```python
import pygame
import sys

pygame.init()

# setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movement example")
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
```
b. Load the sprite and extract the frames

   i. Load Sprite

```python
characterSprite = pygame.image.load(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\turtle.jpg").convert_alpha()
```

   ii. Reduce the side of the image if necessary. My image is too large, if your image is small, then you may skip this line.

```python
characterSprite = pygame.transform.scale_by(characterSprite,0.3)
```

   iii. Get the entire image (sprite) size – width and height

```python
spriteSheetWidth = characterSprite.get_width()
spriteSheetHeight = characterSprite.get_height()
```

   iv. How many frames you want to divide the images? Check out your image – how many characters are there. My example has 2 row and 4 columns.

```python
numWalkingFrames = 4
characterFrameWidth = spriteSheetWidth // numWalkingFrames
characterFrameHeight = spriteSheetHeight // 2  # 2 rows
```

   v. Write a function to extract the frame. Loop through the image to extract sub surface (rectangular) portion of the original image.

```python
def extractFrames(sheet, row, numFrames):
frames = []
for I in range(numFrames):
        frame = sheet.subsurface(pygame.Rect(I * characterFrameWidth, row * characterFrameHeight, characterFrameWidth, characterFrameHeight))
        frames.append(frame)
return frames
```

   vi. Call the function created in v) to extract the frames (walking and jumping). Row 1 for walking and row 2 for jumping

```python
walkingRightFrames = extractFrames(characterSprite, 0, numWalkingFrames)
jumpingFrame = extractFrames (characterSprite, 1, 1)[0]
```

   vii. Duplicate the previous walking frames with flip functions to create a different walking direction.

```python
walkingRightFrames = extractFrames(characterSprite, 0, numWalkingFrames)
walkingLeftFrames = [pygame.transform.flip(walkingframe, True, False) for walkingframe in walkingRightFrames]
jumpingFrame = extractFrames (characterSprite, 1, 1)[0]
```

c. Create a player class (the character) with its attributes and behaviours.

   i. Player class

```python
class Player(pygame.sprite.Sprite):
```

   ii. Create a Constructor to initialize the player object.

```python
def __init__(self):
        super().__init__()
        self.walkingRightFrames = walkingRightFrames
        self.walkingLeftFrames = walkingLeftFrames
        self.jumpingFrame = jumpingFrame
        self.image = self.walkingRightFrames[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.velocityY = 0
        self.onGround = True
        self.frameIndex = 0
        self.direction = 0
        self.facingRight = True
```

   iii. Create an update function update the character when moving right / left, jumping.

        * Based on the keyboard keys being pressed.

```python
 def update(self):
        keys = pygame.key.get_pressed()
        self.direction = 0

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direction = 1
            self.facingRight = True
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -15
            self.onGround = False
```

        * Update the y coordinate of the player (jumping drop to ground) tills reach the ground height – 50.

```python
        self.velocityY += 1
        self.rect.y += self.velocityY

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocityY = 0
            self.onGround = True
```
        * Update the frames based when character jump or move. Default is facing right direction.

```python
        if not self.onGround:
            self.image = self.jumpingFrame
        elif self.direction != 0:
            self.frameIndex = (self.frameIndex + 1) % len(self.walkingRightFrames)
            if self.facingRight:
                self.image = self.walkingRightFrames[self.frameIndex]
            else:
                self.image = self.walkingLeftFrames[self.frameIndex]
        else:
            self.image = self.walkingRightFrames[0] if self.facingRight else self.walkingLeftFrames[0]
```

**Full player class code**

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walkingRightFrames = walkingRightFrames
        self.walkingLeftFrames = walkingLeftFrames
        self.jumpingFrame = jumpingFrame
        self.image = self.walkingRightFrames[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.velocityY = 0
        self.onGround = True
        self.frameIndex = 0
        self.direction = 0
        self.facingRight = True

def update(self):
        keys = pygame.key.get_pressed()
        self.direction = 0

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direction = 1
            self.facingRight = True
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -15
            self.onGround = False

        self.velocityY += 1
        self.rect.y += self.velocityY

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocityY = 0
            self.onGround = True

        if not self.onGround:
            self.image = self.jumpingFrame
        elif self.direction != 0:
            self.frameIndex = (self.frameIndex + 1) % len(self.walkingRightFrames)
            if self.facingRight:
                self.image = self.walkingRightFrames[self.frameIndex]
            else:
                self.image = self.walkingLeftFrames[self.frameIndex]
        else:
            self.image = self.walkingRightFrames[0] if self.facingRight else self.walkingLeftFrames[0]
```

d. Create a player object and add it to the sprite group.

```python
player = Player()
allSprites = pygame.sprite.Group(player)
```

e. Now update the main function to draw the sprite and update it (30fps).

```python
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    allSprites.update()
    allSprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)
```

f. When you run the program, you can see the following screen, you can press space to jump or arrow key to move your character around.

![A cartoon turtle with a shell  Description automatically generated](data:image/png;base64...)

**Full Code**

```python
import pygame
import sys

pygame.init()

# setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movement example")

characterSprite = pygame.image.load(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\turtle.jpg").convert_alpha()

characterSprite = pygame.transform.scale_by(characterSprite,0.3)
spriteSheetWidth = characterSprite.get_width()
spriteSheetHeight = characterSprite.get_height()

numWalkingFrames = 4
characterFrameWidth = spriteSheetWidth // numWalkingFrames
characterFrameHeight = spriteSheetHeight // 2  # 2 rows

# Extract frames
def extractFrames(sheet, row, numFrames):
    frames = []
    for i in range(numFrames)
        frame = sheet.subsurface(pygame.Rect(i * characterFrameWidth, row * characterFrameHeight, characterFrameWidth, characterFrameHeight))
        frames.append(frame)
    return frames

walkingRightFrames = extractFrames (characterSprite, 0, numWalkingFrames)
walkingLeftFrames = [pygame.transform.flip(walkingframe, True, False) for walkingframe in walkingRightFrames]

jumpingFrame = extractFrames (characterSprite, 1, 1)[0]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walkingRightFrames = walkingRightFrames
        self.walkingLeftFrames = walkingLeftFrames
        self.jumpingFrame = jumpingFrame
        self.image = self.walkingRightFrames[0]
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.velocityY = 0
        self.onGround = True
        self.frameIndex = 0
        self.direction = 0
        self.facingRight = True

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = 0

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.direction = 1
            self.facingRight = True
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -15
            self.onGround = False

        self.velocityY += 1
        self.rect.y += self.velocityY

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocityY = 0
            self.onGround = True

        # Animation
        if not self.onGround:
            self.image = self.jumpingFrame
        elif self.direction != 0:
            self.frameIndex = (self.frameIndex + 1) % len(self.walkingRightFrames)
            if self.facingRight:
                self.image = self.walkingRightFrames[self.frameIndex]
            else:
                self.image = self.walkingLeftFrames[self.frameIndex]
        else:
            self.image = self.walkingRightFrames[0] if self.facingRight else self.walkingLeftFrames[0]

player = Player()
allSprites = pygame.sprite.Group(player)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    allSprites.update()
    allSprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
```

**Exercise**

a. Now add in a background (use the knowledge from previous lesson).

b. Create another player, you can download a new sprite with different characters. Use other keys (WASD) to control player movement.
