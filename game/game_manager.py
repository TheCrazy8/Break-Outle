"""
Game Manager - Main game logic coordinator
"""
import pygame
import json
import os
import random
from game.constants import *
from game.ball import Ball
from game.brick import Brick


class GameManager:
    """Manages the main game state and logic"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        
        # Game state
        self.gold = INITIAL_GOLD
        self.total_gold_earned = 0
        self.prestige_points = 0
        self.prestige_mult = 1.0
        
        # Ball inventory (count of each type owned)
        self.ball_counts = {ball_type: 0 for ball_type in BALL_TYPES.keys()}
        self.ball_counts['basic'] = 0  # Start with 0 balls
        
        # Upgrade levels
        self.damage_upgrade_level = 0
        self.speed_upgrade_level = 0
        
        # Active balls and bricks
        self.balls = []
        self.bricks = []
        
        # UI state
        self.paused = False
        self.show_shop = False
        self.shop_scroll = 0
        
        # Buttons
        self.buttons = {}
        self.create_buttons()
        
        # Initialize game
        self.create_brick_grid()
        self.load_game()
    
    def create_buttons(self):
        """Create UI buttons"""
        self.buttons['shop'] = pygame.Rect(UI_PANEL_X, 50, UI_PANEL_WIDTH, BUTTON_HEIGHT)
        self.buttons['stats'] = pygame.Rect(UI_PANEL_X, 100, UI_PANEL_WIDTH, BUTTON_HEIGHT)
        self.buttons['prestige'] = pygame.Rect(UI_PANEL_X, 150, UI_PANEL_WIDTH, BUTTON_HEIGHT)
    
    def create_brick_grid(self):
        """Create the initial brick grid"""
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = GAME_AREA_X + col * BRICK_WIDTH + BRICK_PADDING
                y = GAME_AREA_Y + row * BRICK_HEIGHT + BRICK_PADDING
                brick = Brick(x, y, row, col)
                self.bricks.append(brick)
    
    def respawn_bricks(self):
        """Respawn broken bricks after delay"""
        for brick in self.bricks:
            if not brick.active:
                brick.active = True
                brick.hp = brick.max_hp
    
    def get_damage_multiplier(self):
        """Calculate current damage multiplier from upgrades and prestige"""
        base = 1.0 + self.damage_upgrade_level * 0.1
        return base * self.prestige_mult
    
    def get_speed_multiplier(self):
        """Calculate current speed multiplier from upgrades"""
        return 1.0 + self.speed_upgrade_level * 0.05
    
    def buy_ball(self, ball_type):
        """Purchase a ball of given type"""
        if ball_type not in BALL_TYPES:
            return False
        
        type_data = BALL_TYPES[ball_type]
        count = self.ball_counts[ball_type]
        
        # Calculate cost with exponential scaling
        cost = int(type_data['base_cost'] * (type_data['cost_mult'] ** count))
        
        if self.gold >= cost:
            self.gold -= cost
            self.ball_counts[ball_type] += 1
            
            # Spawn the ball
            x = GAME_AREA_X + GAME_AREA_WIDTH // 2
            y = GAME_AREA_Y + GAME_AREA_HEIGHT - 100
            ball = Ball(x, y, ball_type, type_data, 
                       self.get_damage_multiplier(), 
                       self.get_speed_multiplier())
            self.balls.append(ball)
            
            return True
        return False
    
    def upgrade_damage(self):
        """Purchase damage upgrade"""
        cost = int(UPGRADE_DAMAGE_BASE_COST * (UPGRADE_COST_MULT ** self.damage_upgrade_level))
        if self.gold >= cost:
            self.gold -= cost
            self.damage_upgrade_level += 1
            # Update all existing balls
            for ball in self.balls:
                ball.damage = ball.base_damage * self.get_damage_multiplier()
            return True
        return False
    
    def upgrade_speed(self):
        """Purchase speed upgrade"""
        cost = int(UPGRADE_SPEED_BASE_COST * (UPGRADE_COST_MULT ** self.speed_upgrade_level))
        if self.gold >= cost:
            self.gold -= cost
            self.speed_upgrade_level += 1
            # Update all existing balls
            speed_mult = self.get_speed_multiplier()
            for ball in self.balls:
                if ball.special != 'sniper':
                    current_speed = (ball.vx ** 2 + ball.vy ** 2) ** 0.5
                    if current_speed > 0:
                        ball.vx = (ball.vx / current_speed) * BALL_BASE_SPEED * ball.type_data.get('speed_mult', 1.0) * speed_mult
                        ball.vy = (ball.vy / current_speed) * BALL_BASE_SPEED * ball.type_data.get('speed_mult', 1.0) * speed_mult
            return True
        return False
    
    def handle_brick_click(self, pos):
        """Handle manual clicking on bricks"""
        for brick in self.bricks:
            if brick.active:
                if (brick.x <= pos[0] <= brick.x + brick.width and
                    brick.y <= pos[1] <= brick.y + brick.height):
                    # Apply manual click damage
                    gold = brick.take_damage(MANUAL_CLICK_DAMAGE * self.get_damage_multiplier())
                    if gold > 0:
                        self.gold += gold
                        self.total_gold_earned += gold
                    return True
        return False
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_s:
                self.show_shop = not self.show_shop
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = event.pos
                
                # Check UI buttons
                if self.buttons['shop'].collidepoint(pos):
                    self.show_shop = not self.show_shop
                elif self.buttons['prestige'].collidepoint(pos):
                    if self.total_gold_earned >= PRESTIGE_THRESHOLD:
                        self.prestige()
                
                # Check shop purchases
                if self.show_shop:
                    self.handle_shop_click(pos)
                else:
                    # Manual brick clicking
                    self.handle_brick_click(pos)
        
        elif event.type == pygame.MOUSEWHEEL:
            if self.show_shop:
                self.shop_scroll += event.y * 20
                self.shop_scroll = max(0, min(self.shop_scroll, 500))
    
    def handle_shop_click(self, pos):
        """Handle clicks in the shop"""
        shop_x = UI_PANEL_X
        shop_y = 200 - self.shop_scroll
        
        # Ball purchase buttons
        y_offset = 0
        for ball_type, type_data in BALL_TYPES.items():
            button_rect = pygame.Rect(shop_x, shop_y + y_offset, UI_PANEL_WIDTH, 60)
            if button_rect.collidepoint(pos):
                self.buy_ball(ball_type)
                return
            y_offset += 70
        
        # Upgrade buttons
        y_offset += 20
        damage_button = pygame.Rect(shop_x, shop_y + y_offset, UI_PANEL_WIDTH, 50)
        if damage_button.collidepoint(pos):
            self.upgrade_damage()
            return
        
        y_offset += 60
        speed_button = pygame.Rect(shop_x, shop_y + y_offset, UI_PANEL_WIDTH, 50)
        if speed_button.collidepoint(pos):
            self.upgrade_speed()
            return
    
    def prestige(self):
        """Prestige: reset progress for permanent bonuses"""
        # Calculate prestige points (simplified)
        new_pp = int(self.total_gold_earned / PRESTIGE_THRESHOLD)
        if new_pp <= self.prestige_points:
            return  # No benefit
        
        self.prestige_points = new_pp
        self.prestige_mult = 1.0 + self.prestige_points * 0.1
        
        # Reset progress
        self.gold = INITIAL_GOLD
        self.total_gold_earned = 0
        self.ball_counts = {ball_type: 0 for ball_type in BALL_TYPES.keys()}
        self.balls = []
        self.damage_upgrade_level = 0
        self.speed_upgrade_level = 0
        self.create_brick_grid()
    
    def update(self, dt):
        """Update game state"""
        if self.paused:
            return
        
        # Update balls
        new_balls = []
        for ball in self.balls[:]:
            spawned = ball.update(dt, bricks=self.bricks)
            new_balls.extend(spawned)
            
            # Check collisions with bricks
            for brick in self.bricks:
                if not brick.active:
                    continue
                
                collision_side = ball.check_brick_collision(brick)
                if collision_side:
                    # Apply damage
                    gold = brick.take_damage(ball.damage)
                    if gold > 0:
                        self.gold += gold
                        self.total_gold_earned += gold
                    
                    # Apply special effects
                    if ball.special == 'plasma' and brick.active:
                        # Splash damage to nearby bricks
                        nearby = ball.get_nearby_bricks(self.bricks, radius=80)
                        for nearby_brick in nearby:
                            if nearby_brick != brick:
                                splash_gold = nearby_brick.take_damage(ball.damage * ball.splash_damage)
                                if splash_gold > 0:
                                    self.gold += splash_gold
                                    self.total_gold_earned += splash_gold
                    
                    elif ball.special == 'poison':
                        # Apply poison effect
                        brick.apply_poison(ball.poison_dps * ball.damage, ball.poison_duration)
                    
                    # Bounce ball (unless it's sniper which retargets)
                    if ball.special != 'sniper':
                        if collision_side == 'vertical':
                            ball.bounce_vertical()
                        else:
                            ball.bounce_horizontal()
                    break
        
        # Add spawned balls
        self.balls.extend(new_balls)
        
        # Update bricks (poison damage, etc.)
        for brick in self.bricks:
            gold = brick.update(dt)
            if gold > 0:
                self.gold += gold
                self.total_gold_earned += gold
        
        # Respawn bricks if all are destroyed
        if all(not brick.active for brick in self.bricks):
            self.respawn_bricks()
    
    def render(self):
        """Render the game"""
        self.screen.fill(BLACK)
        
        # Draw game area border
        pygame.draw.rect(self.screen, WHITE, 
                        (GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                         GAME_AREA_WIDTH + 4, GAME_AREA_HEIGHT + 4), 2)
        
        # Draw bricks
        for brick in self.bricks:
            brick.render(self.screen, self.small_font)
        
        # Draw balls
        for ball in self.balls:
            ball.render(self.screen)
        
        # Draw UI
        self.render_ui()
        
        # Draw pause overlay
        if self.paused:
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))
            
            text = self.large_font.render("PAUSED", True, WHITE)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(text, rect)
    
    def render_ui(self):
        """Render UI elements"""
        # Gold display
        gold_text = f"Gold: ${int(self.gold)}"
        text_surface = self.large_font.render(gold_text, True, YELLOW)
        self.screen.blit(text_surface, (UI_PANEL_X, 10))
        
        # Buttons
        for name, rect in self.buttons.items():
            color = LIGHT_GRAY if rect.collidepoint(pygame.mouse.get_pos()) else GRAY
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 2)
            
            text = self.font.render(name.upper(), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        # Shop overlay
        if self.show_shop:
            self.render_shop()
        else:
            # Show quick stats
            stats_y = 220
            stats = [
                f"Balls: {len(self.balls)}",
                f"Damage: x{self.get_damage_multiplier():.2f}",
                f"Speed: x{self.get_speed_multiplier():.2f}",
                f"Prestige: {self.prestige_points}",
                "",
                "Click bricks to break!",
                "Buy balls to automate!"
            ]
            for stat in stats:
                text = self.font.render(stat, True, WHITE)
                self.screen.blit(text, (UI_PANEL_X, stats_y))
                stats_y += 30
    
    def render_shop(self):
        """Render the shop interface"""
        # Shop background
        shop_rect = pygame.Rect(UI_PANEL_X - 10, 200, UI_PANEL_WIDTH + 20, 580)
        pygame.draw.rect(self.screen, DARK_GRAY, shop_rect)
        pygame.draw.rect(self.screen, WHITE, shop_rect, 2)
        
        shop_x = UI_PANEL_X
        shop_y = 210 - self.shop_scroll
        
        # Ball purchase options
        for ball_type, type_data in BALL_TYPES.items():
            count = self.ball_counts[ball_type]
            cost = int(type_data['base_cost'] * (type_data['cost_mult'] ** count))
            
            # Button background
            button_rect = pygame.Rect(shop_x, shop_y, UI_PANEL_WIDTH, 60)
            can_afford = self.gold >= cost
            color = (0, 100, 0) if can_afford else DARK_GRAY
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, type_data['color'], button_rect, 3)
            
            # Ball info
            name_text = self.font.render(type_data['name'], True, WHITE)
            self.screen.blit(name_text, (shop_x + 5, shop_y + 5))
            
            cost_text = self.small_font.render(f"${cost} (Own: {count})", True, YELLOW)
            self.screen.blit(cost_text, (shop_x + 5, shop_y + 30))
            
            desc_text = self.small_font.render(type_data['description'], True, LIGHT_GRAY)
            self.screen.blit(desc_text, (shop_x + 5, shop_y + 45))
            
            shop_y += 70
        
        # Upgrades section
        shop_y += 20
        title = self.font.render("UPGRADES", True, YELLOW)
        self.screen.blit(title, (shop_x, shop_y))
        shop_y += 30
        
        # Damage upgrade
        damage_cost = int(UPGRADE_DAMAGE_BASE_COST * (UPGRADE_COST_MULT ** self.damage_upgrade_level))
        damage_button = pygame.Rect(shop_x, shop_y, UI_PANEL_WIDTH, 50)
        can_afford = self.gold >= damage_cost
        color = (100, 0, 0) if can_afford else DARK_GRAY
        pygame.draw.rect(self.screen, color, damage_button)
        pygame.draw.rect(self.screen, RED, damage_button, 2)
        
        damage_text = self.small_font.render(f"Damage +10% (Lv.{self.damage_upgrade_level})", True, WHITE)
        self.screen.blit(damage_text, (shop_x + 5, shop_y + 5))
        cost_text = self.small_font.render(f"${damage_cost}", True, YELLOW)
        self.screen.blit(cost_text, (shop_x + 5, shop_y + 28))
        shop_y += 60
        
        # Speed upgrade
        speed_cost = int(UPGRADE_SPEED_BASE_COST * (UPGRADE_COST_MULT ** self.speed_upgrade_level))
        speed_button = pygame.Rect(shop_x, shop_y, UI_PANEL_WIDTH, 50)
        can_afford = self.gold >= speed_cost
        color = (0, 0, 100) if can_afford else DARK_GRAY
        pygame.draw.rect(self.screen, color, speed_button)
        pygame.draw.rect(self.screen, CYAN, speed_button, 2)
        
        speed_text = self.small_font.render(f"Speed +5% (Lv.{self.speed_upgrade_level})", True, WHITE)
        self.screen.blit(speed_text, (shop_x + 5, shop_y + 5))
        cost_text = self.small_font.render(f"${speed_cost}", True, YELLOW)
        self.screen.blit(cost_text, (shop_x + 5, shop_y + 28))
    
    def save_game(self):
        """Save game state to file"""
        save_data = {
            'gold': self.gold,
            'total_gold_earned': self.total_gold_earned,
            'prestige_points': self.prestige_points,
            'ball_counts': self.ball_counts,
            'damage_upgrade_level': self.damage_upgrade_level,
            'speed_upgrade_level': self.speed_upgrade_level
        }
        
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self):
        """Load game state from file"""
        if not os.path.exists(SAVE_FILE):
            return
        
        try:
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)
            
            self.gold = save_data.get('gold', INITIAL_GOLD)
            self.total_gold_earned = save_data.get('total_gold_earned', 0)
            self.prestige_points = save_data.get('prestige_points', 0)
            self.prestige_mult = 1.0 + self.prestige_points * 0.1
            self.ball_counts = save_data.get('ball_counts', {ball_type: 0 for ball_type in BALL_TYPES.keys()})
            self.damage_upgrade_level = save_data.get('damage_upgrade_level', 0)
            self.speed_upgrade_level = save_data.get('speed_upgrade_level', 0)
            
            # Respawn owned balls
            for ball_type, count in self.ball_counts.items():
                if ball_type in BALL_TYPES:
                    type_data = BALL_TYPES[ball_type]
                    for _ in range(count):
                        x = GAME_AREA_X + random.randint(100, GAME_AREA_WIDTH - 100)
                        y = GAME_AREA_Y + random.randint(100, GAME_AREA_HEIGHT - 100)
                        ball = Ball(x, y, ball_type, type_data,
                                  self.get_damage_multiplier(),
                                  self.get_speed_multiplier())
                        self.balls.append(ball)
            
            print(f"Game loaded: {len(self.balls)} balls, ${int(self.gold)} gold")
        except Exception as e:
            print(f"Error loading game: {e}")
