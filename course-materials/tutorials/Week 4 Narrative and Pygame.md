# Topic: Narrative and pygame implementation

You may download some free assets from the following website:

[2D Game Assets Store & Free - CraftPix.net](https://craftpix.net/)

## Task 1: Follow the given example in the below to learn how to write a narrative and code it.

a. Write Storyboard Narrative

**Scene: Forest Adventure**

**Narrative:** In a forest, the player controls the main character who must navigate through the end of forest to find a diamond. Along the way, he will encounter various obstacles like river and platform.

**Storyboard:**

1. **Scene:**

   a. **Initial**: The main character stands at the edge of the forest.

   b. **Obstacle 1:** The character encounters a river.

   c. **Obstacle 2:** The character encounters a platform.

   d. **Goal:** The player(character) finally finds the diamond.

b. Download the asset.

   * You will need a character, river, platform and a diamond.

   * *A sample has been provided in the team, you may use other images if you wish too.*

c. Code it

1. Setup the game environment and GUI by typing the following code in it.

```python
import pygame
import sys

pygame.init()

#setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Adventure")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.display.flip()
    pygame.time.Clock().tick(60)

#end
pygame.quit()
sys.exit()
```

2. Load the images , if necessary, please scale it (you may refer to the previous lesson on how to do the scaling). Place the code before setup scene.

```python
backgroundImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/background.jpg")
characterWalkings = [pygame.image.load(f"C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\player\\{i}.png") for i in range(1, 5)]
riverImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/river.png")
platformImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/platforms.png")
goalImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/goal.png")
```

   a. Scaling

```python
riverImg = pygame.transform.scale_by(riverImg, (0.3))
platformImg = pygame.transform.scale_by(platformImg, (0.2))
backgroundImg = pygame.transform.scale(backgroundImg, (800, 600))
ObstacleImages = [riverImg,platformImg,goalImg]
```

3. Create a class for the main character. Please the code after scene setup.

```python
class Player(pygame.sprite.Sprite):
```

   a. Create a function to create a constructor for the main character. Load the images (array) into the images. Define the image index and create the rectangle for the object.

```python
    def __init__(self):
        super().__init__()
        self.images = characterWalkImgs
        self.currentImage = 0
        self.image = self.images[self.currentImage]
        self.rect = self.image.get_rect()
        self.rect.center = (100, 600 - 100) #sreen location (position)
        self.animationCounter = 0
```

   b. Create a function to mode the object (player) left and right. (you have learn this in the previous lesson)

```python
    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
        if direction == "right":
            self.rect.x += 5
```

   c. Create the update the image as the character move from left to right or right to left. With every key press animation counter will be + 1. Once the counter reach 5, it will change the image index back to zero (we only have 4 images here).

```python
    def update(self, keys):
        moving = False
        if keys[pygame.K_LEFT]:
            self.move("left")
            moving = True

        elif keys[pygame.K_RIGHT]:
            self.move("right")
            moving = True

        if moving:
            self.animationCounter +=1
            print(self.animationCounter)
            if self.animationCounter % 5 == 0:
                self.currentImage = (self.currentImage + 1) % len(self.images)
                self.image = self.images[self.currentImage]

        else:
            self.animationCounter = 0
            self.currentImage = 0
            self.image = self.images[self.currentImage]
```

4. Create a class for obstacle and initialise it. The obstacle will received the instructions which image to load, x and y location of the object will be placed in the different part of the scene, message to be display once the character touches the obstacle and whether that obstacle is the winning goal or not.

```python
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, index, message, isGoal=False):
        super().__init__()
        self.image = ObstacleImages[index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.message = message
        self._goal = isGoal
```

5. Now we are going to create the main character and obstacle objects.

```python
#create objects
player = Player()
obstacle1 = Obstacle(150, 450, 0, "reach the river")
obstacle2 = Obstacle(350, 500, 1, "At the platform")
goal = Obstacle(650, 500, 2, "Reach the Goal", True)
```

6. Create the sprite group.

```python
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
```

7. Add the obstacle and player into the sprite.

```python
obstacles.add(obstacle1, obstacle2, goal)
all_sprites.add(player)
all_sprites.add(obstacles)
```

8. Update the game loop with character moving , collision between the character and obstacle and updating the display.

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Check collisions
    collideObstacle = pygame.sprite.spritecollideany(player, obstacles)
    if collideObstacle:
        if collideObstacle._goal:
            print(collideObstacle.message) # Winning message
            running = False # End the game
        else:
            print(collideObstacle.message)

    screen.blit(backgroundImg, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
```

8. Now you may run the program and move your character to left / right

![](data:image/png;base64...)

**Full Code**

```python
import pygame
import sys

pygame.init()

#assets
backgroundImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/background.jpg")
characterWalkImgs = [pygame.image.load(f"C:\\Users\\maryting\\OneDrive - Asia Pacific University\\OneDrive\\Modules\\ISE\\Sample Code\\lab\\asset\\player\\{i}.png") for i in range(1, 5)]
riverImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/river.png")
platformImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/platforms.png")
goalImg = pygame.image.load("C:/Users/maryting\OneDrive - Asia Pacific University/OneDrive/Modules/ISE/Sample Code/lab/asset/goal.png")
#scale
riverImg = pygame.transform.scale_by(riverImg, (0.3))
platformImg = pygame.transform.scale_by(platformImg, (0.2))
ObstacleImages = [riverImg,platformImg,goalImg]
backgroundImg = pygame.transform.scale(backgroundImg, (800, 600))

#setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Adventure")

#main character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = characterWalkImgs
        self.currentImage = 0
        self.image = self.images[self.currentImage]
        self.rect = self.image.get_rect()
        self.rect.center = (100, 600 - 100)
        self.animationCounter = 0

    def move(self, direction):
        if direction == "left":
            self.rect.x -= 5
        if direction == "right":
            self.rect.x += 5

    def update(self, keys):
        moving = False
        if keys[pygame.K_LEFT]:
            self.move("left")
            moving = True

        elif keys[pygame.K_RIGHT]:
            self.move("right")
            moving = True

        if moving:
            self.animationCounter +=1
            print(self.animationCounter)
            if self.animationCounter % 5 == 0:
                self.currentImage = (self.currentImage + 1) % len(self.images)
                self.image = self.images[self.currentImage]

        else:
            self.animationCounter = 0
            self.currentImage = 0
            self.image = self.images[self.currentImage]
#obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, index, message, isGoal=False):
        super().__init__()
        self.image = ObstacleImages[index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.message = message
        self._goal = isGoal

#create objects
player = Player()
obstacle1 = Obstacle(150, 450, 0, "reach the river")
obstacle2 = Obstacle(350, 500, 1, "At the platform")
goal = Obstacle(650, 500, 2, "Reach the Goal", True)

# Create sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

#add object to sprites
obstacles.add(obstacle1, obstacle2, goal)
all_sprites.add(player)
all_sprites.add(obstacles)

# start the Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Check collisions
    collideObstacle = pygame.sprite.spritecollideany(player, obstacles)
    if collideObstacle:
        if collideObstacle._goal:
            print(collideObstacle.message) # Winning message
            running = False # End the game
        else:
            print(collideObstacle.message)

    screen.blit(backgroundImg, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
S
#end
pygame.quit()
sys.exit()
```

Task 2 : Add one more obstacle of your choice.

Task 3: Show the message on the screen instead of printing in the console. You have learnt it in the previous lesson.

Task 4: Add the up and down key event, add point system to calculate the total number of points collected over the time. Deduct 1 for touching the river and platform and add 1 for touching the diamond. Add the timer to end the game.

<ins>**Additional Task : Create your own narrative or enhance the previous version.**</ins>

Write a narrative to show a room environment. The obstacle will be furniture.
