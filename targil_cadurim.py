import random
import sys
import threading
import time
import pygame

#gets amount of balls to draw
while True:
    user_input = input("How many balls/threads to create? ")
    #checks if the input is an int else asks again
    if user_input.isdigit():
        amount_of_balls = int(user_input)
        break
    else:
        print("Invalid input. Please enter a valid integer.")

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("cadurim koftsim")

# list of balls
balls = []


# Each thread waits its turn, spawns a ball, teleports it, and stops when done
def ball_worker(ball_id):
  # Stagger appearance
  time.sleep(ball_id * 0.4)

  ball = {
      #gives id to object in list
      "id": ball_id,
      # assigns first pos
      "x": random.randint(50, screen_width - 50),
      "y": random.randint(50, screen_height - 50),
      # give random color
      "color": (
          random.randint(0, 255),
          random.randint(0, 255),
          random.randint(0, 255),
      ),
      # gets random amount of hops
      "hops": random.randint(5, 15),
      # sets the radius
      "radius": 25,
  }
  # adds to list
  balls.append(ball)
  print(f"Ball {ball_id} added. Active balls: {len(balls)}")

  # Teleport around for the exact amount of hops it gets
  for _ in range(ball["hops"]):
    time.sleep(0.8)
    ball["x"] = random.randint(50, screen_width - 50)
    ball["y"] = random.randint(50, screen_height - 50)

  # When hops are finished, remove the ball and let the thread die
  if ball in balls:
    balls.remove(ball)
  print(
      f"Ball {ball_id} finished its hops and stopped. Active balls: {len(balls)}"
  )


# 2. Spawn all threads
threads = []
for i in range(amount_of_balls):
  t = threading.Thread(target=ball_worker, args=(i,))
  threads.append(t)
  t.start()

# 3. Main Pygame Game Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  # Clear screen
    screen.fill((0, 0, 0))

  # Draw all active balls currently in the list
    for ball in balls:
        pygame.draw.circle(screen, ball["color"], (int(ball["x"]), int(ball["y"])), ball["radius"])


    pygame.display.flip()
    clock.tick(60)
    #checks if all the balls have finished the bounces
    if not balls:
        running = False


# Wait for any remaining threads to finish before fully exiting
for t in threads:
  t.join()

pygame.quit()
sys.exit()
# 4. Safely quit Pygame
