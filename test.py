# import os
# os.system("cls")
# from jsonParse import *

# #from tiles import *


# levelInfo = parseJsonFile(f"levels/levels/1-1.json")

# lvl = [[] for i in range(20)]
# print(lvl)


# print(levelInfo["height"])
# for info in levelInfo["layers"][0]["chunks"]:
#     print(info["x"])
#     #print(f"x: {levelInfo['layers'][0]['chunks'][0]['x']}, y: {levelInfo['layers'][0]['chunks'][0]['y']}")
    
    
    
# testMap = {}

# print(True if "Joe" in testMap else False)


# testMap["Joe"] = {int: 100}


# print(True if "Joe" in testMap else False)


# print(testMap["Joe"][int])


# # testTile = createTile(0, 1, 0)
# # testTile2 = createTile(0, 1, 16)


# # print(type(testTile) == type(testTile2))



# # x:int = 5
# # y:int = -5

# # print(-x)
# # print(-y)


# import pygame
# import math

# # Initialize Pygame
# pygame.init()

# # Screen setup
# screen_width, screen_height = 800, 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# clock = pygame.time.Clock()

# # Load your image
# image = pygame.image.load("player/player.png")  # Replace with your image file path
# image_rect = image.get_rect()

# # Define the point around which you want to rotate (e.g., center of the screen)
# rotate_point = (90, 50)  # Change this to the desired rotation point

# angle = 0  # Starting angle for rotation

# # Function to rotate an image around a point
# def rotate_image(image, angle, pivot):
#     # Rotate the image
#     rotated_image = pygame.transform.rotate(image, angle)
#     rotated_rect = rotated_image.get_rect()

#     # Calculate the offset from pivot to the center of the original image
#     offset_center_to_pivot = pygame.math.Vector2(image.get_rect().center) - pivot

#     # Create a vector from the pivot to the center of the rotated image
#     rotated_offset = offset_center_to_pivot.rotate(-angle)

#     # Position the rotated image so that its pivot is at the desired point
#     rotated_rect.center = (pivot[0] + rotated_offset.x, pivot[1] + rotated_offset.y)

#     return rotated_image, rotated_rect

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear screen
#     screen.fill((255, 255, 255))

#     # Increase the rotation angle
#     angle += 90  # Change the value to control rotation speed

#     # Rotate the image around the specified point
#     rotated_image, rotated_rect = rotate_image(image, angle, rotate_point)

#     # Draw the rotated image on the screen
#     screen.blit(rotated_image, (400, 300))

#     # Update the display
#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()



# d = {":3":1, ":2" :2, ":1" :3}

# print(list(d.keys())[0])


# for a,b in d.items():
#     print(f"{a} -> {b}")


