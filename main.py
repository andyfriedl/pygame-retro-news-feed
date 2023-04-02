import datetime
import time
import sys
import random
import json

import pygame

from functions import return_news


pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set icon
gameIcon = pygame.image.load('images/icon.png')
pygame.display.set_icon(gameIcon)

# Set up the window
screen = pygame.display.set_mode()

# get the default screen size
screen_x, screen_y = screen.get_size()
screen = pygame.display.set_mode((screen_x, screen_y))

# Load the background images
bg_images = ["images/bg1.png", "images/bg.png", "images/bg2.png", "images/bg3.png", "images/bg4.png"]
bg_index = 0
bg_image = pygame.image.load(bg_images[bg_index])

# Type Speed
type_speed_index = 0
type_speed_number = [round(random.uniform(0.01, 0.18), 2),
           round(random.uniform(0.005, 0.058), 2)]
type_speed = type_speed_number[0]

# Set font
font = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 42)

# Define the maximum number of lines that can be displayed on the screen
MAX_LINES = 20

# Define the position of the typewriter text
x = 20
y = 20

url = "https://www.reuters.com/world/"


def create_line(sentences):
    # Initialize the list of lines to display on the screen
    lines = []
    # Loop through each sentence and add it to a line
    for sentence in sentences:
        # Skip empty sentences
        if not sentence:
            continue

        # Split the sentence into words
        words = sentence.split()
        # Initialize the current line with the first word
        current_line = words[0]
        # Loop through each subsequent word in the sentence
        for word in words[1:]:
            # Add the current word to the current line
            current_text = current_line + " " + word
            text_surface = font.render(current_text, True, WHITE)
            if text_surface.get_rect().width > screen_x - x:
                # If adding the current word to the current line will exceed the width of the screen, add the current line to the list of lines and start a new line with the current word
                lines.append(current_line)
                current_line = word
            else:
                # If adding the current word to the current line will not exceed the width of the screen, add the current word to the current line
                current_line = current_text
        # Add the current line to the list of lines
        lines.append(current_line)
    return lines


def key_input():
    global bg_index, bg_image, type_speed_number, type_speed_index
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_b:
                bg_index = (bg_index + 1) % len(bg_images)
                bg_image = pygame.image.load(bg_images[bg_index])

done = False

# loop
while True:
    key_input()

    # get news - news is stale for 1 hour
    lines = create_line(return_news(url))

    # Add last updated news date to caption
    with open("news.txt", "r") as f:
        data = json.load(f)
        pygame.display.set_caption(
            '>> Latest News from around the Earth. Last updated: ' + str(data["date"]))

    for i, line in enumerate(lines):
        key_input()
        # Loop through each character in the line
        for j in range(len(line)):
            # Handle events
            key_input()

            # Draw the background
            screen.fill(BLACK)
            screen.blit(bg_image, (0, 0))

            # Draw the lines of text that have already been printed
            for k in range(max(0, i - MAX_LINES + 1), i):
                key_input()
                text_surface = font.render(lines[k], True, WHITE)
                screen.blit(text_surface, (x, y + (k - i + MAX_LINES - 1)
                                           * text_surface.get_rect().height))

            # Draw the current line up to the current character
            current_text = line[:j+1]
            text_surface = font.render(current_text, True, WHITE)
            screen.blit(text_surface, (x, y + (MAX_LINES - 1)
                                       * text_surface.get_rect().height))

            # Update the screen
            pygame.display.flip()

            # Pause briefly to create the typewriter effect or type speed
            time.sleep(round(random.uniform(0.01, 0.18), 2))

            if done:
                break
        # wait 1 second between lines
        # time.sleep(1)

    if done:
        break

# Quit Pygame
pygame.quit()
