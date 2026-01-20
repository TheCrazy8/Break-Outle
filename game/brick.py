"""
Brick entity
"""
import pygame
from game.constants import BRICK_WIDTH, BRICK_HEIGHT, BRICK_PADDING, BRICK_BASE_HP, BRICK_BASE_GOLD, BRICK_HP_SCALING


class Brick:
    """Represents a brick in the game - Idle Breakout style"""
    
    def __init__(self, x, y, row, col, level=1):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.width = BRICK_WIDTH - BRICK_PADDING * 2
        self.height = BRICK_HEIGHT - BRICK_PADDING * 2
        self.level = level
        
        # Health scales with row (higher rows = more HP)
        self.max_hp = BRICK_BASE_HP * (BRICK_HP_SCALING ** row)
        self.hp = self.max_hp
        
        # Gold value based on HP
        self.gold_value = int(self.max_hp * BRICK_BASE_GOLD)
        
        # Color based on row
        from game.constants import BRICK_COLORS
        self.color = BRICK_COLORS[row % len(BRICK_COLORS)]
        
        self.active = True
        
        # Poison effect tracking
        self.poison_damage = 0
        self.poison_duration = 0
    
    def take_damage(self, damage):
        """Apply damage to brick, returns gold if destroyed"""
        if not self.active:
            return 0
        
        self.hp -= damage
        
        if self.hp <= 0:
            self.active = False
            return self.gold_value
        
        return 0
    
    def apply_poison(self, dps, duration):
        """Apply poison effect"""
        self.poison_damage = dps
        self.poison_duration = duration
    
    def update(self, dt):
        """Update brick state (poison effects)"""
        if not self.active:
            return 0
        
        gold = 0
        
        # Apply poison damage
        if self.poison_duration > 0:
            self.poison_duration -= dt
            damage = self.poison_damage * dt
            gold = self.take_damage(damage)
        
        return gold
    
    def render(self, screen, font):
        """Draw the brick with HP number"""
        if not self.active:
            return
        
        # Draw brick
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw border
        border_color = tuple(max(c - 50, 0) for c in self.color)
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)
        
        # Draw HP number in the center
        hp_text = str(int(self.hp))
        text_surface = font.render(hp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        
        # Draw text shadow for visibility
        shadow_surface = font.render(hp_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.x + self.width // 2 + 1, self.y + self.height // 2 + 1))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
        # Draw poison effect indicator
        if self.poison_duration > 0:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x + self.width - 8), int(self.y + 8)), 4)
