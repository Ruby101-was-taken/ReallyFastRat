import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Make sure there's at least one joystick/controller connected
if pygame.joystick.get_count() > 0:
    whichControler = 0
    if pygame.joystick.get_count() > 1:
        whichControler = int(input(f"Which Controller? 0 -> {pygame.joystick.get_count()-1}: "))
    # Get the first joystick
    joystick = pygame.joystick.Joystick(whichControler)
    joystick.init()

    # Set up the display
    screen = pygame.display.set_mode((700, 300))  # Increased height for additional text
    pygame.display.set_caption('Joystick Input')

    run = True
    # Main game loop
    while run:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Get the state of all buttons, axes, and hats
        buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]
        hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]  # Get hat values
        
        # Clear the screen
        screen.fill((255, 255, 255))

        # Display pressed buttons
        font = pygame.font.Font(None, 36)
        text = font.render("Pressed Buttons: {}".format([i for i, button in enumerate(buttons) if button]), True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Display axis values
        text = font.render("Axis Values: {}".format(axes), True, (0, 0, 0))
        screen.blit(text, (10, 50))

        # Display hat values
        text = font.render("Hat Values: {}".format(hats), True, (0, 0, 0))
        screen.blit(text, (10, 90))

        # Update the display
        pygame.display.flip()
        

        # Add a small delay to avoid flooding the display
        pygame.time.delay(100)

    pygame.quit()
    sys.exit()
