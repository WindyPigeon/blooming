# Topic: Particle System

## Using pygame

1. Create import the relevant library

```python
import pygame
import random
import math
```

**math and random library are used to calculate and configure the location and color for the particle.*

2. setup the game window and the basic running for the pygame.

```python
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Particle Example")

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

3. Create the class for the particle. Following is the examples of the particle classes, a round particle – create the particle based on mouse click, a snowflake (also round), and shard – polygon shape. Place the classes before the program running method.

* <ins>**Standard round particle.**</ins>

```python
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(4, 6)
        self.color = (255, 255, 255)
        self.velocityX = random.uniform(-1, 1)
        self.velocityY = random.uniform(-2, 0)
        self.life = random.randint(20, 50)

    def update(self):
        self.x += self.velocityX
        self.y += self.velocityY
        self.size -= 0.05
        self.life -= 1
        if self.size <= 0 or self.life <=0:
            particles.remove(self)

    def draw(self):
        pygame.draw.circle(screen, (128,100,200), (int(self.x), int(self.y)), int(self.size))
```

* **Snowflake particle – still round shape but must be white color.**

```python
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(-10, 0)
        self.size = random.randint(1, 5)
        self.speed = random.uniform(0, 3)
        self.wind = random.uniform(0, 1)
        self.color = (255, 255, 255)

    def update(self):
        self.y += self.speed
        self.x += self.wind
        if self.y > 600:
            self.y = random.randint(-10, 0)
            self.x = random.randint(0, 800)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
```

* <ins>**A shard – similar to firework idea**</ins>

```python
class Shard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 5)
        self.color = (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))
        self.life = random.randint(10, 50)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.size -= 0.1
        self.life -= 1
        if self.size <= 0 or self.life <= 0:
            shards.remove(self)

    def draw(self):
        points = [
            (self.x, self.y),
            (self.x + self.size * math.cos(self.angle + math.pi / 3), self.y + self.size * math.sin(self.angle + math.pi / 3)),
            (self.x + self.size * math.cos(self.angle - math.pi / 3), self.y + self.size * math.sin(self.angle - math.pi / 3))
        ]
        pygame.draw.polygon(screen, self.color, points)
```

4. Create a list to store these particles

```python
shards = []
particles = []
snowflakes = [Snowflake() for _ in range(50)]
```

5. Update the even code by adding the mousedown function to get the x and y positions when user click on the screen. The code will create the create 100 particles and add it to the list.

```python
elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for _ in range(100):
                particles.append(Particle(x, y))
                shards.append(Shard(x+100, y+100))
```

6. Update the program running method to keep updating and draw the particle.

```python
    for particle in particles:
        particle.update()
        particle.draw()

    for snowflake in snowflakes:
        snowflake.update()
        snowflake.draw()

    for shard in shards:
        shard.update()
        shard.draw()
```

**![A screen shot of a computer  Description automatically generated](data:image/png;base64...)**

<ins>**Full coding**</ins>

```python
import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Particle Example")

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(4, 6)
        self.color = (255, 255, 255)
        self.velocityX = random.uniform(-1, 1)
        self.velocityY = random.uniform(-2, 0)
        self.life = random.randint(20, 50)

    def update(self):
        self.x += self.velocityX
        self.y += self.velocityY
        self.size -= 0.05
        self.life -= 1
        if self.size <= 0 or self.life <=0:
            particles.remove(self)

    def draw(self):
        pygame.draw.circle(screen, (128,100,200), (int(self.x), int(self.y)), int(self.size))

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(-10, 0)
        self.size = random.randint(1, 5)
        self.speed = random.uniform(0, 3)
        self.wind = random.uniform(0, 1)
        self.color = (255, 255, 255)

    def update(self):
        self.y += self.speed
        self.x += self.wind
        if self.y > 600:
            self.y = random.randint(-10, 0)
            self.x = random.randint(0, 800)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class Shard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 5)
        self.color = (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))
        self.life = random.randint(10, 50)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.size -= 0.1
        self.life -= 1
        if self.size <= 0 or self.life <= 0:
            shards.remove(self)

    def draw(self):
        points = [
            (self.x, self.y),
            (self.x + self.size * math.cos(self.angle + math.pi / 3), self.y + self.size * math.sin(self.angle + math.pi / 3)),
            (self.x + self.size * math.cos(self.angle - math.pi / 3), self.y + self.size * math.sin(self.angle - math.pi / 3))
        ]
        pygame.draw.polygon(screen, self.color, points)

shards = []
particles = []
snowflakes = [Snowflake() for _ in range(50)]
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for _ in range(100):
                particles.append(Particle(x, y))
                shards.append(Shard(x+100, y+100))

    for particle in particles:
        particle.update()
        particle.draw()

    for snowflake in snowflakes:
        snowflake.update()
        snowflake.draw()

    for shard in shards:
        shard.update()
        shard.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

<ins>**Task:**</ins>

a. Change the colour of the particle to your desired colour

b. Change the polygon shape of the particle.

c. Create smoke effects in a new program, create a ground with a line. Placed the line for the ground at 25% from the bottom of the screen. Generate the smoke from the ground onward(source from fire). Once the smoke reaches the 25% from the top of the screen, it will disappear from the scene.
