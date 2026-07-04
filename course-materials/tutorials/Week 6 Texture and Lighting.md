# Topic : Texture and Lighting

## Task 1: Draw Circle

1. Initialize and create the pygame window.

```python
import pygame

screen = pygame.display.set\_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255)) #white background

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

2. Create a function to draw the circle. The function will receive the coordinate (center location and radius of the circle). Fill the circle with red color.

```python
def drawCircle(x, y, radius):
    pygame.draw.circle(screen, (255,0,0), (x, y), radius)
```

3. Update the DrawCircle function by add in the lighting effect by calculating the direction of the light based on the mouse distance from the center and the intensity of the light changes.

   a. Update the function signature to receive the light position

```python
def drawCircle(x, y, radius, lightPosition):
```

   b. Calculate the new X and Y coordinate of the light radius (edge)

```python
for angle in range(360):
        radians = math.radians(angle)
        newX = x + radius \* math.cos(radians)
        newY = y + radius \* math.sin(radians)
```

   c. Calculate the distance of the light and the color intensity.

```python
        distanceLight = math.hypot(lightPosition[0] - newX, lightPosition[1] - newY) #Calculates the distance from the light source. (square root of the sum of squares)
        intensity = max(0, 255 - distanceLight) # calculate the light intensity
```

   d. Update the colour according to the intensity.

```python
        updateColor = (max(0, min(255 + intensity, 255)),
                            max(0, min(0 + intensity, 255)),
                            max(0, min(0 + intensity, 255)))
```

   e. Update the circle

```python
pygame.draw.circle(screen, updateColor, (x,y), radius)
```

**Full drawCircle function**

```python
def drawCircle(x, y, radius, lightPosition):

    pygame.draw.circle(screen, (255,0,0), (x, y), radius)

    for angle in range(360):
        radians = math.radians(angle)
        newX = x + radius * math.cos(radians)
        newY = y + radius * math.sin(radians)

        distanceLight = math.hypot(lightPosition[0] - newX, lightPosition[1] - newY) #Calculates the distance from the light source. (square root of the sum of squares)
        intensity = max(0, 255 - distanceLight) # calculate the light intensity

        # change the red color intensity
        updateColor = (max(0, min(255 + intensity, 255)),
                            max(0, min(0 + intensity, 255)),
                            max(0, min(0 + intensity, 255)))

pygame.draw.circle(screen, updateColor, (x,y), radius)
```

4. Get the mouse position and call the drawcircle function while running program.

```python
    mousePos = pygame.mouse.get\_pos()
    drawCircle(400, 300, 100, mousePos) #draw at the center
```

**![](data:image/png;base64...)**

**Full Code**

```python
import pygame
import math

screen = pygame.display.set\_mode((800, 600))
clock = pygame.time.Clock()

def drawCircle(x, y, radius, lightPosition):

    pygame.draw.circle(screen, (255,0,0), (x, y), radius)

    for angle in range(360):
        radians = math.radians(angle)
        newX = x + radius \* math.cos(radians)
        newY = y + radius \* math.sin(radians)

        distanceLight = math.hypot(lightPosition[0] - newX, lightPosition[1] - newY) #Calculates the distance from the light source. (square root of the sum of squares)
        intensity = max(0, 255 - distanceLight) # calculate the light intensity

        # change the red color intensity
        updateColor = (max(0, min(255 + intensity, 255)),
                            max(0, min(0 + intensity, 255)),
                            max(0, min(0 + intensity, 255)))

    pygame.draw.circle(screen, updateColor, (x,y), radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255)) #white background

    mousePos = pygame.mouse.get\_pos()
    drawCircle(400, 300, 100, mousePos) #draw at the center

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## Task 2: Using lines to draw the circle.

1. Update the existing drawcircle function by removing both drawing circle before looping to get the new x and y coordinate.

2. Add a new statement to draw the line inside the loop. Draw the line from center to the edges.

```python
        pygame.draw.line(screen, updateColor, (x,y), (newX, newY))
```

**Updated code**

```python
def drawCircle(x, y, radius, lightPosition):

    for angle in range(360):
        radians = math.radians(angle)
        newX = x + radius \* math.cos(radians)
        newY = y + radius \* math.sin(radians)

        distanceLight = math.hypot(lightPosition[0] - newX, lightPosition[1] - newY) #Calculates the distance from the light source. (square root of the sum of squares)
        intensity = max(0, 255 - distanceLight) # calculate the light intensity

        # change the red color intensity
        updateColor = (max(0, min(255 + intensity, 255)),
                            max(0, min(0 + intensity, 255)),
                            max(0, min(0 + intensity, 255)))

        pygame.draw.line(screen, updateColor, (x,y), (newX, newY))
```

3. when you run the code, you will see the circle with lines (not solid)

**![](data:image/png;base64...)**

## Task 3: Fill the shape (circle / square / rectangle) with an image

1. Google and download any texture image.

2. Fill up the shape with the image you have downloaded.

3. Now apply lighting effect

**Example**

**![](data:image/png;base64...)**
