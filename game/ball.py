"""
Ball entity
"""
import pygame
import math
import random
from game.constants import (
    BALL_RADIUS, BALL_BASE_SPEED,
    GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT
)


class Ball:
    """Represents a ball in the game - Idle Breakout style"""
    
    def __init__(self, x, y, ball_type='basic', type_data=None, damage_mult=1.0, speed_mult=1.0):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.ball_type = ball_type
        self.type_data = type_data or {}
        
        # Ball properties from type and upgrades
        self.base_damage = self.type_data.get('damage', 1)
        self.damage = self.base_damage * damage_mult
        self.color = self.type_data.get('color', (255, 255, 255))
        self.special = self.type_data.get('special', None)
        
        # Movement
        base_speed = BALL_BASE_SPEED * self.type_data.get('speed_mult', 1.0) * speed_mult
        
        # Special behavior for sniper (doesn't bounce randomly)
        if self.special == 'sniper':
            self.vx = 0
            self.vy = 0
            self.target_brick = None
            self.retarget_timer = 0
            self.retarget_interval = 0.5
        else:
            # Random initial direction
            angle = random.uniform(math.pi / 4, 3 * math.pi / 4)
            self.vx = base_speed * math.cos(angle)
            self.vy = base_speed * math.sin(angle)
        
        # Special properties
        self.splash_damage = self.type_data.get('splash_damage', 0)
        self.poison_dps = self.type_data.get('poison_dps', 0)
        self.poison_duration = self.type_data.get('poison_duration', 0)
        
        # Scatter ball timer
        self.scatter_timer = 0
        self.scatter_interval = 3.0
        
        # Active flag
        self.active = True
    
    def update(self, dt, game_bounds=None, bricks=None):
        """Update ball position"""
        if not self.active:
            return []
        
        spawned_balls = []
        
        # Special update for sniper ball
        if self.special == 'sniper':
            self.retarget_timer -= dt
            if self.retarget_timer <= 0 and bricks:
                # Find weakest brick
                active_bricks = [b for b in bricks if b.active]
                if active_bricks:
                    self.target_brick = min(active_bricks, key=lambda b: b.hp)
                    # Move towards target
                    if self.target_brick:
                        dx = self.target_brick.x + self.target_brick.width / 2 - self.x
                        dy = self.target_brick.y + self.target_brick.height / 2 - self.y
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist > 0:
                            speed = BALL_BASE_SPEED * self.type_data.get('speed_mult', 1.0)
                            self.vx = (dx / dist) * speed
                            self.vy = (dy / dist) * speed
                    self.retarget_timer = self.retarget_interval
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Bounce off walls
        if game_bounds is None:
            game_bounds = (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
        
        min_x, min_y, width, height = game_bounds
        max_x = min_x + width
        max_y = min_y + height
        
        # Left/right walls
        if self.x - self.radius < min_x:
            self.x = min_x + self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > max_x:
            self.x = max_x - self.radius
            self.vx = -abs(self.vx)
        
        # Top wall
        if self.y - self.radius < min_y:
            self.y = min_y + self.radius
            self.vy = abs(self.vy)
        
        # Bottom wall
        if self.y + self.radius > max_y:
            self.y = max_y - self.radius
            self.vy = -abs(self.vy)
        
        # Scatter ball spawning
        if self.special == 'scatter':
            self.scatter_timer += dt
            if self.scatter_timer >= self.scatter_interval:
                self.scatter_timer = 0
                # Spawn 2 mini balls
                for _ in range(2):
                    mini_ball = Ball(self.x, self.y, 'basic', 
                                   {'damage': self.base_damage * 0.5, 
                                    'speed_mult': 1.5, 
                                    'color': self.color},
                                   damage_mult=1.0, speed_mult=1.0)
                    spawned_balls.append(mini_ball)
        
        return spawned_balls
    
    def bounce_vertical(self):
        """Bounce vertically (hitting horizontal surface)"""
        self.vy = -self.vy
    
    def bounce_horizontal(self):
        """Bounce horizontally (hitting vertical surface)"""
        self.vx = -self.vx
    
    def check_brick_collision(self, brick):
        """Check if ball collides with brick, returns collision side if any"""
        if not self.active or not brick.active:
            return None
        
        # Simple circle-rectangle collision
        closest_x = max(brick.x, min(self.x, brick.x + brick.width))
        closest_y = max(brick.y, min(self.y, brick.y + brick.height))
        
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y
        distance_squared = distance_x * distance_x + distance_y * distance_y
        
        if distance_squared < self.radius * self.radius:
            brick_center_x = brick.x + brick.width / 2
            brick_center_y = brick.y + brick.height / 2
            
            dx = self.x - brick_center_x
            dy = self.y - brick_center_y
            
            if abs(dx / brick.width) > abs(dy / brick.height):
                return 'horizontal'
            else:
                return 'vertical'
        
        return None
    
    def get_nearby_bricks(self, bricks, radius=100):
        """Get bricks near this ball for splash damage"""
        nearby = []
        for brick in bricks:
            if not brick.active:
                continue
            brick_center_x = brick.x + brick.width / 2
            brick_center_y = brick.y + brick.height / 2
            dx = self.x - brick_center_x
            dy = self.y - brick_center_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                nearby.append(brick)
        return nearby
    
    def render(self, screen):
        """Draw the ball"""
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            
            # Draw special effect indicators
            if self.special == 'plasma':
                # Glow effect
                glow_color = tuple(min(c + 50, 255) for c in self.color)
                pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), 
                                 self.radius + 2, 2)
            elif self.special == 'sniper':
                # Crosshair effect
                pygame.draw.line(screen, self.color, 
                               (int(self.x) - 10, int(self.y)), 
                               (int(self.x) + 10, int(self.y)), 2)
                pygame.draw.line(screen, self.color, 
                               (int(self.x), int(self.y) - 10), 
                               (int(self.x), int(self.y) + 10), 2)
