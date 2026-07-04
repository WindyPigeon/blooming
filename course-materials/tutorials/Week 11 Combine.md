# Topic: Combine elements

**Package :**

* pygame
* math – to calculate the distance and angle
* time – to track the time
* random – to generate random value

1. Import the libraries.

```python
import pygame
import random
import time
import math
```

2. Initialize the Pygame and mixer (for sound)

```python
pygame.init()
pygame.mixer.init()
```

3. Load the sound (background music and collision sound) and configure the setting

```python
pygame.mixer.music.load(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\backgroundMusic.mp3")
pygame.mixer.music.set\_volume(0.5)
pygame.mixer.music.play(-1)

collisionSound = pygame.mixer.Sound(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\punch.mp3")
   collisionSound.set_volume(0.5)
```

4. Basic game structure setup

```python
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("sample effect")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))  # screen background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

5. Load and scale player character image

```python
character = pygame.image.load("lab/asset/characters.svg")
updatedCharacter = pygame.transform.scale_by(character, 0.1)
charRectBlock = updatedCharacter.get_rect(center=(400, 500))
```

6. Define the speed, movement and character blinking variables

```python
velocityX, velocityY = 0, 0
acceleration, maxSpeed, friction = 0.5, 5, 0.1
movementCounts = {"left": 1, "right": 1, "up": 1, "down": 1}

blinkDuration, blinkCounter = 30, 0
isBlinking = False
```

7. Create initial enemy (the ball)

```python
enemyList = [{
    "pos": [random.randint(0, 800), random.randint(0, 600)],
    "radius": 10,
    "color": (255, 0, 0)
}]
```

8. Setup the initial state for enemy movement speed, timing, shatter effect variable

```python
enemySpeed = 2
lastCollisionTime = time.time()
lastBallAddTime = time.time()
shattered = False
fragments = []
showVictory = False
victoryDelayStart = None  #
```

9. Add the following code into the running function.

   a. Get the current time and also trace the collision time

```python
    currentTime = time.time()
    timeSinceLastCollision = currentTime - lastCollisionTime
```

   b. Add in the key presses event (left, right, up, down movement) to update the x and y location of the player character.

```python
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        velocityX -= acceleration
        movementCounts["left"] += 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        velocityX += acceleration
        movementCounts["right"] += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        velocityY -= acceleration
        movementCounts["up"] += 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        velocityY += acceleration
        movementCounts["down"] += 1
```

   c. Apply friction to calculate the updated x and y position of the character and enemy. Main purpose make it more natural (fast or slow) movement depending on the user key press as it will update the speed.

```python
    velocityX = max(-maxSpeed, min(maxSpeed, velocityX - friction * (1 if velocityX > 0 else -1)))
    velocityY = max(-maxSpeed, min(maxSpeed, velocityY - friction * (1 if velocityY > 0 else -1)))
```

   d. Update the character position based on the velocity values and clamp it to screen (stay within the screen boundary)

```python
    charRectBlock.x += int(velocityX)
    charRectBlock.y += int(velocityY)
    charRectBlock.clamp_ip(screen.get_rect())
```

   e. Read and trace the character movement (user behaviours) to predict the user movement.

```python
    totalMoves = sum(movementCounts.values())
    moveProb = {k: movementCounts[k] / totalMoves for k in movementCounts}
    predictedX = 5 * (moveProb["right"] - moveProb["left"])
    predictedY = 5 * (moveProb["down"] - moveProb["up"])
    predictedPos = [charRectBlock.centerx + predictedX, charRectBlock.centery + predictedY]
```

   f. Update the enemy position and distance to chase the character

```python
    for i, enemy in enumerate(enemyList):
        chaseX = predictedPos[0] - enemy["pos"][0]
        chaseY = predictedPos[1] - enemy["pos"][1]
        dist = max(1, math.hypot(chaseX, chaseY))
```

   g. Add in this logic (calculate the location based on the current and next enemy radius and update the distance between both enemy) to avoid the enemy from overlapping each other

```python
        for j, other in enumerate(enemyList):
            if i != j:
                dx = enemy["pos"][0] - other["pos"][0]
                dy = enemy["pos"][1] - other["pos"][1]
                d = math.hypot(dx, dy)
                if d < enemy["radius"] + other["radius"]:
                    enemy["pos"][0] += dx / d if d != 0 else 1
                    enemy["pos"][1] += dy / d if d != 0 else 1
```

   h. Update the enemy position toward the character position. The enemy position will keep moving.

```python
        enemy["pos"][0] += enemySpeed * chaseX / dist
        enemy["pos"][1] += enemySpeed * chaseY / dist
```

   i. Add new enemy(ball) every 5 second and enlarge the ball after 10 seconds of no collision. Random generate color and x and y position for new bal.

```python
    # Add new enemy ball (random color and position)
    if currentTime - lastBallAddTime > 5 and not shattered:
        newColor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        enemyList.append({
            "pos": [random.randint(0, 800), random.randint(0, 600)],
            "radius": 10,
            "color": newColor
        })
        lastBallAddTime = currentTime

#scale enemy balls size
if timeSinceLastCollision > 10:
        for enemy in enemyList:
            enemy["radius"] = min(enemy["radius"] * 1.1, 20)

    #render to update the screen with the enemy ball
    if not shattered:
        for enemy in enemyList:
            pygame.draw.circle(screen, enemy["color"], (int(enemy["pos"][0]), int(enemy["pos"][1])), int(enemy["radius"]))
```

   j. Create a rectangle for the enemy ball. So the system able to track when enemy and character rounding rectangles touching each other.

```python
  enemyRect = pygame.Rect(enemy["pos"][0] - enemy["radius"], enemy["pos"][1] - enemy["radius"], enemy["radius"] * 2, enemy["radius"] * 2)
```

   k. Add the code to check for the collision - if yes update the variable value

```python
        if charRectBlock.colliderect(enemyRect):
            collisionSound.play()
            lastCollisionTime = currentTime
            lastBallAddTime = currentTime
            shattered = False
            fragments.clear()
            isBlinking = True
            blinkCounter = blinkDuration
            enemyList = [enemyList[0]]  # Reset to original ball
```

   l. Add the character blinking effect once the character collides with the ball.

```python
    if isBlinking:
        blinkCounter -= 1
        if blinkCounter <= 0:
            isBlinking = False
        elif blinkCounter % 10 < 5:
            screen.blit(updatedCharacter, charRectBlock)
    else:
        screen.blit(updatedCharacter, charRectBlock)
```

   m. Add in the code to close the game when user press the Esc key. The key will only be active if the showVictory is set to True.

```python
        if showVictory and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
```

   n. When the player can last for 15 seconds after 3 enemy added, the game will trigger the shattering effect to end the game before displaying the victory word. Get the enemy position, color, radius to create the fragments.

```python
  if timeSinceLastCollision > 15 and not shattered:
        shattered = True
        for enemy in enemyList:
            for i in range(10):
                angle = i * (360 / 10)
                radians = math.radians(angle)
                fragments.append({
                    "x": enemy["pos"][0],
                    "y": enemy["pos"][1],
                    "vx": math.cos(radians) * 1.2,
                    "vy": math.sin(radians) * 1.2,
                    "radius": 5,
                    "color": enemy["color"]
                })
        showVictory = True
        victoryDelayStart = currentTime  #add delay
```

   o. Draw shattered fragments

```python
    if shattered:
        for frag in fragments:
            frag["x"] += frag["vx"]
            frag["y"] += frag["vy"]
            pygame.draw.circle(screen, frag["color"], (int(frag["x"]), int(frag["y"])), frag["radius"])
```

   p. Show victory text after the shattering effects. Delay for 2 seconds and then render to display the victory message.

```python
    if showVictory:
        if currentTime - victoryDelayStart >= 2:  # 2 seconds delay
            font = pygame.font.SysFont(None, 72)
            victoryText = font.render("Victory!", True, (255, 255, 0))
            screen.blit(victoryText, (300, 250))
        pygame.display.flip()
        continue
```

<ins>Full Code</ins>

```python
import pygame
import random
import time
import math

# Initialize Pygame and mixer (for sound)
pygame.init()
pygame.mixer.init()

# background music and collision sound setting
pygame.mixer.music.load(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\backgroundMusic.mp3")
pygame.mixer.music.set\_volume(0.5)
pygame.mixer.music.play(-1)

collisionSound = pygame.mixer.Sound(r"C:\Users\maryting\OneDrive - Asia Pacific University of Technology And Innovation (APU)\OneDrive\Modules\ISE\Sample Code\lab\asset\punch.mp3")
collisionSound.set\_volume(0.5)

# Set up screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("sample effect")
clock = pygame.time.Clock()

# Load and scale character image
character = pygame.image.load("lab/asset/characters.svg")
updatedCharacter = pygame.transform.scale_by(character, 0.1)
charRectBlock = updatedCharacter.get_rect(center=(400, 500))

# speed, movement and character blinking variables
velocityX, velocityY = 0, 0
acceleration, maxSpeed, friction = 0.5, 5, 0.1
movementCounts = {"left": 1, "right": 1, "up": 1, "down": 1}

blinkDuration, blinkCounter = 30, 0
isBlinking = False

# Enemy (the ball)
enemyList = [{
    "pos": [random.randint(0, 800), random.randint(0, 600)],
    "radius": 10,
    "color": (255, 0, 0)
}]
enemySpeed = 2
lastCollisionTime = time.time()
lastBallAddTime = time.time()
shattered = False
fragments = []
showVictory = False
victoryDelayStart = None  #

running = True
while running:
    screen.fill((255, 255, 255))  # screen background

    currentTime = time.time()
    timeSinceLastCollision = currentTime - lastCollisionTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if showVictory and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

   #  key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        velocityX -= acceleration
        movementCounts["left"] += 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        velocityX += acceleration
        movementCounts["right"] += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        velocityY -= acceleration
        movementCounts["up"] += 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        velocityY += acceleration
        movementCounts["down"] += 1

    # Apply friction
    velocityX = max(-maxSpeed, min(maxSpeed, velocityX - friction * (1 if velocityX > 0 else -1)))
    velocityY = max(-maxSpeed, min(maxSpeed, velocityY - friction * (1 if velocityY > 0 else -1)))

    # Move character and clamp to screen
    charRectBlock.x += int(velocityX)
    charRectBlock.y += int(velocityY)
    charRectBlock.clamp_ip(screen.get_rect())

  # add more enemy and deal with enemy logic
  # scale enemy balls size
    if timeSinceLastCollision > 10:
        for enemy in enemyList:
            enemy["radius"] = min(enemy["radius"] * 1.1, 20)

    # Add new enemy ball (random color and position)
    if currentTime - lastBallAddTime > 5 and not shattered:
        newColor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        enemyList.append({
            "pos": [random.randint(0, 800), random.randint(0, 600)],
            "radius": 10,
            "color": newColor
        })
        lastBallAddTime = currentTime

#apply probability concept to predict the character location
# and enemy will follow in that direction.
   # Predict movement
    totalMoves = sum(movementCounts.values())
    moveProb = {k: movementCounts[k] / totalMoves for k in movementCounts}
    predictedX = 5 * (moveProb["right"] - moveProb["left"])
    predictedY = 5 * (moveProb["down"] - moveProb["up"])
    predictedPos = [charRectBlock.centerx + predictedX, charRectBlock.centery + predictedY]

    # Enemy chasing - update the x and y location
    for i, enemy in enumerate(enemyList):
        chaseX = predictedPos[0] - enemy["pos"][0]
        chaseY = predictedPos[1] - enemy["pos"][1]
        dist = max(1, math.hypot(chaseX, chaseY))

        # Avoid overlapping with other enemies
        for j, other in enumerate(enemyList):
            if i != j:
                dx = enemy["pos"][0] - other["pos"][0]
                dy = enemy["pos"][1] - other["pos"][1]
                d = math.hypot(dx, dy)
                if d < enemy["radius"] + other["radius"]:
                    enemy["pos"][0] += dx / d if d != 0 else 1
                    enemy["pos"][1] += dy / d if d != 0 else 1

        # Move enemy toward the character position
        enemy["pos"][0] += enemySpeed * chaseX / dist
        enemy["pos"][1] += enemySpeed * chaseY / dist

        # Check collision - if yes update the variable value
        enemyRect = pygame.Rect(enemy["pos"][0] - enemy["radius"], enemy["pos"][1] - enemy["radius"], enemy["radius"] * 2, enemy["radius"] * 2)
        if charRectBlock.colliderect(enemyRect):
            collisionSound.play()
            lastCollisionTime = currentTime
            lastBallAddTime = currentTime
            shattered = False
            fragments.clear()
            isBlinking = True
            blinkCounter = blinkDuration
            enemyList = [enemyList[0]]  # Reset to original ball

    # trigger the Blinking effect
    if isBlinking:
        blinkCounter -= 1
        if blinkCounter <= 0:
            isBlinking = False
        elif blinkCounter % 10 < 5:
            screen.blit(updatedCharacter, charRectBlock)
    else:
        screen.blit(updatedCharacter, charRectBlock)
9

    # game over effect Shatter the ball
    if timeSinceLastCollision > 15 and not shattered:
        shattered = True
        for enemy in enemyList:
            for i in range(10):
                angle = i * (360 / 10)
                radians = math.radians(angle)
                fragments.append({
                    "x": enemy["pos"][0],
                    "y": enemy["pos"][1],
                    "vx": math.cos(radians) * 1.2,
                    "vy": math.sin(radians) * 1.2,
                    "radius": 5,
                    "color": enemy["color"]
                })
        showVictory = True
        victoryDelayStart = currentTime  #add delay

    #render the ball
    if not shattered:
        for enemy in enemyList:
            pygame.draw.circle(screen, enemy["color"], (int(enemy["pos"][0]), int(enemy["pos"][1])), int(enemy["radius"]))

    # Draw shattered fragement
    if shattered:
        for frag in fragments:
            frag["x"] += frag["vx"]
            frag["y"] += frag["vy"]
            pygame.draw.circle(screen, frag["color"], (int(frag["x"]), int(frag["y"])), frag["radius"])

    # ending  -Show victory text
    if showVictory:
        if currentTime - victoryDelayStart >= 2:  # 2 seconds delay
            font = pygame.font.SysFont(None, 72)
            victoryText = font.render("Victory!", True, (255, 255, 0))
            screen.blit(victoryText, (300, 250))
        pygame.display.flip()
        continue

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Output

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)

<ins>Enhanced the above code based on following requirements.</ins>

1. Add in Scoring start with 5, whenever the call catchup (collides) with the player, deduct 1 point from the total score.

2. Add in a timer, the timer will start with zero and count the total time the player able to stay in the gameplay. Record the result in a file.

3. When the gameover, display the message along with the time obtained on the screen.

4. Change the player to a different character( if you have sufficient time, change it to add in the movement - animated).
