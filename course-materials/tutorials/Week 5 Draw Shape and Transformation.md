# Topic: Geometry Shape and Transformation

## Task1 : Guidelines to draw and transform Gemoetry Shape

### Part 1: Draw Shape

1. We will continue to use pygame library to draw geometry shape.

2. Setup the basic game screen and initialise it. Set the screen resolution of your choice (my size is 800X600) and background colour = white.

```python
import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry shape")

WHITE = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(WHITE)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
```

3. Now create a function to draw the polygon. The function will receive a surface, color and points data. Please the code before the program running function

```python
def drawShape(surface, color, points):
    pygame.draw.polygon(surface, color, points)
```

4. Now define the color. Place the code after the white color definition

```python
RED = (255, 0, 0)
BLUE = (0,0,255)
```

5. Define the centre of the screen. (set the coordinate according to your screen size define in step1). You can place the code anywhere before start running the program.

```python
ScreenCenterX, ScreenCenterY = 400, 300
```

6. Define 2 shapes; triangle (3 points) and rectangle (4 points). Place it after window fill function in the program running function.

```python
pointsA = [(ScreenCenterX, ScreenCenterY - 50), (ScreenCenterX - 50, ScreenCenterY + 50), (ScreenCenterX + 50, ScreenCenterY + 50)]

pointsB = [ (ScreenCenterX-50, ScreenCenterY), (ScreenCenterX-50, ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY)]
```

7. Call the drawshape function for each shape (pointA and pointB)

```python
    drawShape(window, RED, pointsA)
    drawShape(window, BLUE, pointsB)
```

Now run the program and you will see the following output.

![](data:image/png;base64...)

**Full Code**

```python
import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry shape")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)

# draw a shape
def drawShape(surface, color, points):
    pygame.draw.polygon(surface, color, points)

running = True
ScreenCenterX, ScreenCenterY = 400, 300
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(WHITE)

    pointsA = [(ScreenCenterX, ScreenCenterY - 50), (ScreenCenterX - 50, ScreenCenterY + 50), (ScreenCenterX + 50, ScreenCenterY + 50)]
    pointsB = [ (ScreenCenterX-50, ScreenCenterY), (ScreenCenterX-50, ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY)]

    drawShape(window, RED, pointsA)
    drawShape(window, BLUE, pointsB)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
```

### Part 2: Transformation

1. We are going to use math library to perform radians, cos and sine. Import math library

```python
import math
```

2. Modify the existing code by adding a function rotate the shape. The function will receive the point(X,Y) coordinate, angle and center point(middle of the screen). It will cacluate the new X,Y coordinate based on the angle provided.

```python
def rotate(point, angle, center):
    angleRadian = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    newX = x * math.cos(angleRadian) - y * math.sin(angleRadian)
    newY = x * math.sin(angleRadian) + y * math.cos(angleRadian)
    return newX + cx, newY + cy
```

3. Add the initial value for angle and scale. Angle - 0 (origin) and scale – 1 (normal size). Before program running function.

```python
angle = 0
scale = 1
```

3. Add in the keys event to trigger the shape transformation.

   * Left , right, up and down to move the shape.

   * r and a to rotate clockwise or counterclockwise.

   * s and c to scale up and down the shape

```python
        elif event.type == pygame.KEYDOWN: # transformation
            if event.key == pygame.K_LEFT:
                ScreenCenterX -= 10
            elif event.key == pygame.K_RIGHT:
                ScreenCenterX += 10
            elif event.key == pygame.K_UP:
                ScreenCenterY -= 10
            elif event.key == pygame.K_DOWN:
                ScreenCenterY += 10
            elif event.key == pygame.K_r:
                angle += 5
            elif event.key == pygame.K_a:
                angle -= 5
            elif event.key == pygame.K_s:
                scale += 0.1
            elif event.key == pygame.K_c:
                scale -= 0.1
```

4. Each time user press press a key (down), the angle / scale / center coordinate being updated, so we need to recalculate the points of each shape by calling the rotate function to update each point of a Shape. Once the points have been updated, it will redraw it shape by calling the drawshape function.

```python
TpointsA = [rotate((x * scale, y * scale), angle, (ScreenCenterX, ScreenCenterY)) for x, y in pointsA]

    drawShape(window, RED, TpointsA)

    TpointsB = [rotate((x * scale, y * scale), angle, (ScreenCenterX, ScreenCenterY)) for x, y in pointsB]
    drawShape(window, BLUE, TpointsB)
```

5. Now run the program and you will see the same screen as the part 1 exercise, you just need to press the key to view the transformation.

**Full Code**

```python
import pygame
import math

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Geometry shape")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)

# draw a shape
def drawShape(surface, color, points):
    pygame.draw.polygon(surface, color, points)

# rotate the shape
def rotate(point, angle, center):
    angleRadian = math.radians(angle)
    x, y = point
    cx, cy = center
    x -= cx
    y -= cy
    newX = x * math.cos(angleRadian) - y * math.sin(angleRadian)
    newY = x * math.sin(angleRadian) + y * math.cos(angleRadian)
    return newX + cx, newY + cy

running = True
angle = 0
scale = 1
ScreenCenterX, ScreenCenterY = 400, 300
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # transformation
            if event.key == pygame.K_LEFT:
                ScreenCenterX -= 10
            elif event.key == pygame.K_RIGHT:
                ScreenCenterX += 10
            elif event.key == pygame.K_UP:
                ScreenCenterY -= 10
            elif event.key == pygame.K_DOWN:
                ScreenCenterY += 10
            elif event.key == pygame.K_r:
                angle += 5
            elif event.key == pygame.K_a:
                angle -= 5
            elif event.key == pygame.K_s:
                scale += 0.1
            elif event.key == pygame.K_c:
                scale -= 0.1

    window.fill(WHITE)

    pointsA = [(ScreenCenterX, ScreenCenterY - 50), (ScreenCenterX - 50, ScreenCenterY + 50), (ScreenCenterX + 50, ScreenCenterY + 50)]
    pointsB = [ (ScreenCenterX-50, ScreenCenterY), (ScreenCenterX-50, ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY+50),(ScreenCenterX+50,ScreenCenterY)]

    TpointsA = [rotate((x * scale, y * scale), angle, (ScreenCenterX, ScreenCenterY)) for x, y in pointsA]
    drawShape(window, RED, TpointsA)
    # drawShape(window, RED, pointsA)

    TpointsB = [rotate((x * scale, y * scale), angle, (ScreenCenterX, ScreenCenterY)) for x, y in pointsB]
    drawShape(window, BLUE, TpointsB)
    # drawShape(window, BLUE, pointsB)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
```

## Task 2: Enhance the previous work.

a. Add 1 more shape as follow.

![](data:image/png;base64...)

b. If you have additional time, add in the mirror feature (flip – horizontal / vertical).
