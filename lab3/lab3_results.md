# Names: Riley Smith and Joseph Nguyuen
# Lab: Lab3 (Advanced Prompt Engineering)
# Date: 10-17-2025

Submit:
1. Your full `lab3` directory including all the code you ran and,
2. Your `lab3_results.md` with:


## 3.2 Response
Problem (Logic):
Certainly! Let's break down the problem step-by-step to find a solution where the farmer can safely transport the goat across the river without it being eaten.

1. **Initial State**: Farmer is on one side of the river with the wolf, the goat, and the cabbage.
2. **Objective**: Transport the goat across the river without it being eaten by the wolf or the cabbage being eaten by the goat.

Here's a step-by-step solution:

### Step 1: Take the Goat Across the River
- Farmer takes the goat to the other side of the river.
- **State after Step 1**: Farmer is on the other side with the goat, and the wolf and cabbage are on the original side.

### Step 2: Return Alone to the Original Side
- Farmer goes back alone to the original side.
- **State after Step 2**: Farmer is on the original side with the wolf and the cabbage, and the goat is on the other side.

### Step 3: Take the Wolf Across the River
- Farmer takes the wolf to the other side of the river.
- **State after Step 3**: Farmer is on the other side with the wolf and the goat, and the cabbage is on the original side.

### Step 4: Bring the Goat Back to the Original Side
- Farmer goes back alone to the original side with the wolf.
- **State after Step 4**: Farmer is on the original side with the wolf and the cabbage, and the goat is on the other side.

### Step 5: Take the Cabbage Across the River
- Farmer takes the cabbage to the other side of the river.
- **State after Step 5**: Farmer is on the other side with the wolf and the cabbage, and the goat is on the original side.

### Step 6: Return Alone to the Original Side
- Farmer goes back alone to the original side with the wolf.
- **State after Step 6**: Farmer is on the original side with the wolf, and the goat and cabbage are on the other side.

### Step 7: Take the Goat Across the River Again
- Farmer takes the goat to the other side of the river.
- **Final State**: Farmer is on the other side with the wolf and the goat, and the cabbage is on the original side.

Now, all items (wolf, goat, and cabbage) are safely across the river without any of them being eaten.

## 6.1.2 Response


```python
import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (148, 0, 211)

# Define display dimensions
dis_width = 800
dis_height = 600

# Create the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Pythonist')

# Define the clock
clock = pygame.time.Clock()

snake_block = 10
initial_snake_speed = 15
snake_speed = initial_snake_speed

# Define fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    global snake_speed
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    powerup_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    powerup_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    powerup_type = random.choice(['speed', 'size'])

    obstacle_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    obstacle_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, purple, [powerup_x, powerup_y, snake_block, snake_block])
        pygame.draw.rect(dis, red, [obstacle_x, obstacle_y, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if (x1 >= foodx and x1 < foodx + snake_block) and (y1 >= foody and y1 < foody + snake_block):
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        if (x1 >= powerup_x and x1 < powerup_x + snake_block) and (y1 >= powerup_y and y1 < powerup_y + snake_block):
            if powerup_type == 'speed':
                snake_speed += 5
            elif powerup_type == 'size':
                Length_of_snake += 2
            powerup_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            powerup_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            powerup_type = random.choice(['speed', 'size'])

        if (x1 >= obstacle_x and x1 < obstacle_x + snake_block) and (y1 >= obstacle_y and y1 < obstacle_y + snake_block):
            snake_speed -= 5
            time.sleep(2)
            snake_speed = initial_snake_speed
            obstacle_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            obstacle_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
```