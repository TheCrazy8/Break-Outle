"""
Break-Outle - Main Game Entry Point
An overly complicated idle breakout game
"""
import pygame
import sys
from pygame.game_manager import GameManager
from pygame.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_TITLE


def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Create game manager
    game_manager = GameManager(screen)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)
        
        # Update game state
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        game_manager.update(dt)
        
        # Render
        game_manager.render()
        pygame.display.flip()
    
    # Clean up
    game_manager.save_game()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
