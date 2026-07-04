# Topic: Animation

**Package :**

* pygame

* math – to calculate

* Opencv - dealing with image processing

* Pillow – another image library for manipulating images

## Part 1 Using basic Pygame

A. <ins>Create a simple movement from left to right</ins>
   1. Create the basic pygrame structure with 800X600 screen size as follows.

```python
import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation Part 1")

WHITE = (255, 255, 255)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

   2. Now draw the circle.
      a. Add the circle attributes before the running loop.

```python
BLUE = (0, 0, 255)
x = 0 # xposition
y = height // 2  #y pos
radius = 10
```
      b. Draw the circle in the loop. Add the code before flip function.

```python
pygame.draw.circle(screen, BLUE, (x, y), radius)
```

   3. Now add the moving from left to right.

      a. Add the attributes for speed before the running loop

```python
speed = 5
```

      b. Add in the logic to update the location of the circle everytime the screen render (updated). Place the code before draw circle function.

    x += speed #uppdate x location

    if x > width:

        x = 0   #reset to start from left

3. Now enlarge the circle as it moves from left to right. Update the Q3 code as the follows with 20% increase in size as it move.

```python
     X += speed #uppdate x location
     radius += 0.2
     if x > width:
        x = 0   #reset to start from left
        radius = 10
```

## Part 1 full code

```python
import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation Part 1")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

x = 0 # xposition
y = height // 2  #y pos
speed = 5
radius = 10

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  #movving
   x += speed #uppdate x location
   radius += 0.2
   if x > width:
        x = 0   #reset to start from left
        radius = 10

    pygame.draw.circle(screen, BLUE, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

output:

![A screen shot of a computer  Description automatically generated](data:image/png;base64...)

B. Create a wave movement from left to right

   1. Import the math library to calculate and position of the circle.

```python
import math
```

   2. Add the in attribute for the wave

```python
amplitude = 100  # wave height
frequency = 0.02  # wave width
```

   3. Calculate and update y position as the circle move from left to right. Update the circle function ycoordinate variable as well.

```python
 yPos = int(y + amplitude * math.sin(frequency * x))
 pygame.draw.circle(screen, BLUE, (x, yPos), radius)
```

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)

## Part 2 Movement with pytweening

1. Install Additional package

```bash
pip3 install pytweening
```

**Reference:**

* [piwheels - pytweening](https://www.piwheels.org/project/pytweening/)

* [GitHub - asweigart/pytweening: A set of tweening / easing functions implemented in Python.](https://github.com/asweigart/pytweening)

2. Import the libraries

```python
import pygame
import pytweening
```

3. Setup the basic game structure.

```python
pygame.init()
screen = pygame.display.set_mode((800, 600)) #wXh
pygame.display.set_caption("Animation Part 2")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

4. Define the ball attributes and configurations

```python
ballRadius = 30
ballSurface = pygame.Surface((ballRadius * 2, ballRadius * 2), pygame.SRCALPHA)
pygame.draw.circle(ballSurface, (0, 0, 255), (ballRadius, ballRadius), ballRadius)
pygame.draw.line(ballSurface, (0, 0, 0), (ballRadius, ballRadius), (ballRadius * 2, ballRadius), 4)
```

5. Define other parameters

```python
duration = 180  # frames
currentframe = 0 #start
startXPos = 30
endXPos = 770
y = 200
direction = 1     # 1 = forward, -1 = backward
```

6. Update the running function.
   a. Identify the ball status and location (create movement)

```python
    progress = currentframe / duration
    if progress > 1:
        progress = 1

    tweened = pytweening.easeInOutQuad(progress)
    x = startXPos + (endXPos - startXPos) * tweened   # update the position
```

   b. Add rotation to the ball as it move from one side to the other side of the frame.

```python
    angle = currentframe * 5  # rotate 5 degrees per frame
    rotatedBall = pygame.transform.rotate(ballSurface, angle)
    rect = rotatedBall.get_rect(center=(x, y))
```

   c. Update the ball on the screen.

```python
    screen.blit(rotatedBall, rect)
```

   d. Calculate and update the direction of the ball movement.

```python
    if currentframe < duration:
        currentframe += 1
    else: # reverse back
        startXPos, endXPos = endXPos, startXPos
        direction *= -1
        currentframe = 0
```

<ins>Full Code</ins>


```python
import pygame
import pytweening

pygame.init()
screen = pygame.display.set_mode((800, 600)) #wXh
pygame.display.set_caption("Animation Part 2")
clock = pygame.time.Clock()

ballRadius = 30
ballSurface = pygame.Surface((ballRadius * 2, ballRadius * 2), pygame.SRCALPHA)
pygame.draw.circle(ballSurface, (0, 0, 255), (ballRadius, ballRadius), ballRadius) # blue colour ball
pygame.draw.line(ballSurface, (0, 0, 0), (ballRadius, ballRadius), (ballRadius * 2, ballRadius), 4) # thick line (4)

# setup the parameters
duration = 180  # frames
currentframe = 0 #start
startXPos = 30
endXPos = 770
y = 200
direction = 1     # 1 = forward, -1 = backward

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    progress = currentframe / duration
    if progress > 1:
        progress = 1

    tweened = pytweening.easeInOutQuad(progress)
    x = startXPos + (endXPos - startXPos) * tweened   # update the position

    # Rotate the ball
    angle = currentframe * 5  # rotate 5 degrees per frame
    rotatedBall = pygame.transform.rotate(ballSurface, angle)
    rect = rotatedBall.get_rect(center=(x, y))

    screen.blit(rotatedBall, rect)
    pygame.display.flip()
    clock.tick(60)

    if currentframe < duration:
        currentframe += 1
    else: # reverse back
        startXPos, endXPos = endXPos, startXPos
        direction *= -1
        currentframe = 0

pygame.quit()
```

## Part 3 Movement - Bouncing

1. Import the library

```python
import pygame
import math
```

2. Setup the scene.

```python
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

3. Add the variables for the ball configuration – location, size, velocity and color.

```python
GroundY = 550
BallRadius = 20
gravity = 0.5
BounceDamping = 0.7
StretchDuration = 10
minBounceVelocity = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ShadowColor = (50, 50, 50, 100)
```

4. Create the ball – fill it with color and border

```python
ballSurface = pygame.Surface((BallRadius * 2, BallRadius * 2), pygame.SRCALPHA)
pygame.draw.circle(ballSurface, BLUE, (BallRadius, BallRadius), BallRadius)
pygame.draw.line(ballSurface, BLACK, (BallRadius, BallRadius), (BallRadius * 2, BallRadius), 4)
```

5. Provide the state of the ball

```python
ballXLoc = 300
ballYLoc = 100
velocityY = 0
stretchTimer = 0
stretching = False
stretchXDirection = 1.0

dragging = False
offset_x = 0
offset_y = 0
```

6. Add the following in the while running function.

   a. Add the mouse down features, where the system will capture the mouse position and start update the ball location according to the mouse position as the mouse moving across the screen.

```python
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            distance = math.hypot(mx - ballXLoc, my - ballYLoc)
            if distance <= BallRadius:
                dragging = True
                offset_x = ballXLoc - mx
                offset_y = ballYLoc - my
                velocityY = 0

         elif event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            ballXLoc = mx + offset_x
            ballYLoc = my + offset_y
```

   b. Once the user stop moving the mouse and let go of the mouse button. It will stop dragging the ball and the ball will update the position and start falling to the ground.

```python
elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                velocityY = -10  # Throw upward when released
```

   c. Add the code for bouncing physic as it touches the ground.

```python
    if not dragging:
        velocityY += gravity
        ballYLoc += velocityY

        if ballYLoc >= GroundY - BallRadius:
            ballYLoc = GroundY - BallRadius
            if abs(velocityY) > minBounceVelocity:
                velocityY = -velocityY * BounceDamping
                stretchTimer = StretchDuration
                stretching = True
            else:
                velocityY = 0
                stretching = False
```

   d. To make it more realistic, add the ball stretching effects as it touches ground.

```python
    if stretchTimer > 0:
        stretchProgress = 1 - abs((stretchTimer - StretchDuration / 2) / (StretchDuration / 2))
        stretchXDirection = 1 + 0.5 * stretchProgress
        stretchTimer -= 1
    else:
        stretchXDirection = 1.0

    scaledBall = pygame.transform.smoothscale(
        ballSurface, (int(BallRadius * 2 * stretchXDirection), BallRadius * 2)
    )
    angle = pygame.time.get_ticks() // 10 % 360
    rotatedBall = pygame.transform.rotate(scaledBall, angle)
    rect = rotatedBall.get_rect(center=(ballXLoc, ballYLoc))
```

   e. Add the ball shadow based on the ball size.

```python
    shadowScale = max(0, 1 - (ballYLoc / (GroundY - BallRadius)))
    shadowWidth = int(BallRadius * 2 * (1 + 0.5 * shadowScale))
    shadowHeight = int(BallRadius * 0.5 * shadowScale)
    shadowSurface = pygame.Surface((shadowWidth, shadowHeight), pygame.SRCALPHA)
    pygame.draw.ellipse(shadowSurface, ShadowColor, shadowSurface.get_rect())
    shadow_rect = shadowSurface.get_rect(center=(ballXLoc, GroundY))
    screen.blit(shadowSurface, shadow_rect)
```

   f. Draw the ball (render) and line (ground)

```python
    screen.blit(rotatedBall, rect)

    pygame.draw.line(screen, BLACK, (0, GroundY), (800, GroundY), 2)
```

<ins>Full Code</ins>

```python
import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()

# Constants
GroundY = 550
BallRadius = 20
gravity = 0.5
BounceDamping = 0.7
StretchDuration = 10
minBounceVelocity = 2

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ShadowColor = (50, 50, 50, 100)

# Ball surface
ballSurface = pygame.Surface((BallRadius * 2, BallRadius * 2), pygame.SRCALPHA)
pygame.draw.circle(ballSurface, BLUE, (BallRadius, BallRadius), BallRadius)
pygame.draw.line(ballSurface, BLACK, (BallRadius, BallRadius), (BallRadius * 2, BallRadius), 4)

# Ball state
ballXLoc = 300
ballYLoc = 100
velocityY = 0
stretchTimer = 0
stretching = False
stretchXDirection = 1.0

# Drag state
dragging = False
offset_x = 0
offset_y = 0

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            distance = math.hypot(mx - ballXLoc, my - ballYLoc)
            if distance <= BallRadius:
                dragging = True
                offset_x = ballXLoc - mx
                offset_y = ballYLoc - my
                velocityY = 0  # Stop motion while dragging

        # Stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                velocityY = -10  # Throw upward when released

        # Update ball position while dragging
        elif event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            ballXLoc = mx + offset_x
            ballYLoc = my + offset_y

    # Physics update only if not dragging
    if not dragging:
        velocityY += gravity
        ballYLoc += velocityY

        # Bounce
        if ballYLoc >= GroundY - BallRadius:
            ballYLoc = GroundY - BallRadius
            if abs(velocityY) > minBounceVelocity:
                velocityY = -velocityY * BounceDamping
                stretchTimer = StretchDuration
                stretching = True
            else:
                velocityY = 0
                stretching = False

    # Stretch animation
    if stretchTimer > 0:
        stretchProgress = 1 - abs((stretchTimer - StretchDuration / 2) / (StretchDuration / 2))
        stretchXDirection = 1 + 0.5 * stretchProgress
        stretchTimer -= 1
    else:
        stretchXDirection = 1.0

    # Ball transform
    scaledBall = pygame.transform.smoothscale(
        ballSurface, (int(BallRadius * 2 * stretchXDirection), BallRadius * 2)
    )
    angle = pygame.time.get_ticks() // 10 % 360
    rotatedBall = pygame.transform.rotate(scaledBall, angle)
    rect = rotatedBall.get_rect(center=(ballXLoc, ballYLoc))

    # Shadow
    shadowScale = max(0, 1 - (ballYLoc / (GroundY - BallRadius)))
    shadowWidth = int(BallRadius * 2 * (1 + 0.5 * shadowScale))
    shadowHeight = int(BallRadius * 0.5 * shadowScale)
    shadowSurface = pygame.Surface((shadowWidth, shadowHeight), pygame.SRCALPHA)
    pygame.draw.ellipse(shadowSurface, ShadowColor, shadowSurface.get_rect())
    shadow_rect = shadowSurface.get_rect(center=(ballXLoc, GroundY))
    screen.blit(shadowSurface, shadow_rect)

    # Draw ball and ground
    screen.blit(rotatedBall, rect)
    pygame.draw.line(screen, BLACK, (0, GroundY), (800, GroundY), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

Output:

![A screenshot of a computer  Description automatically generated](data:image/png;base64...)
