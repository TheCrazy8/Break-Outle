"""
Game Constants
"""

# Display settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
GAME_TITLE = "Break-Outle - Idle Breakout"

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

# Game area
GAME_AREA_X = 50
GAME_AREA_Y = 50
GAME_AREA_WIDTH = 700
GAME_AREA_HEIGHT = 700

# Brick settings
BRICK_ROWS = 10
BRICK_COLS = 10
BRICK_WIDTH = GAME_AREA_WIDTH // BRICK_COLS
BRICK_HEIGHT = 40
BRICK_PADDING = 2

# Ball settings
BALL_RADIUS = 8
BALL_BASE_SPEED = 200
BALL_BASE_DAMAGE = 1

# Paddle settings (optional, for manual control)
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 400
PADDLE_Y = GAME_AREA_Y + GAME_AREA_HEIGHT - 30

# UI settings
UI_PANEL_X = GAME_AREA_X + GAME_AREA_WIDTH + 20
UI_PANEL_WIDTH = WINDOW_WIDTH - UI_PANEL_X - 30
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10

# Game balance
INITIAL_GOLD = 20  # Start with some gold to buy first ball
BRICK_BASE_HP = 2  # Lower HP so manual clicks work better
BRICK_HP_SCALING = 1.3  # Less aggressive HP scaling
BRICK_BASE_GOLD = 1
MANUAL_CLICK_DAMAGE = 1
PRESTIGE_THRESHOLD = 10000  # gold needed for first prestige

# Upgrade costs
UPGRADE_DAMAGE_BASE_COST = 50
UPGRADE_SPEED_BASE_COST = 100
UPGRADE_COST_MULT = 1.3

# Ball types (matching Idle Breakout)
BALL_TYPES = {
    'basic': {
        'name': 'Basic Ball',
        'damage': 1,
        'speed_mult': 1.0,
        'color': WHITE,
        'base_cost': 10,
        'cost_mult': 1.5,
        'description': 'Simple bouncing ball'
    },
    'plasma': {
        'name': 'Plasma Ball',
        'damage': 1,
        'speed_mult': 1.2,
        'color': (0, 255, 255),
        'base_cost': 100,
        'cost_mult': 2.0,
        'special': 'splash',
        'splash_damage': 0.5,
        'description': 'Deals splash damage to nearby bricks'
    },
    'sniper': {
        'name': 'Sniper Ball',
        'damage': 2,
        'speed_mult': 0.8,
        'color': (255, 100, 100),
        'base_cost': 400,
        'cost_mult': 2.5,
        'special': 'sniper',
        'description': 'Targets the weakest brick'
    },
    'scatter': {
        'name': 'Scatter Ball',
        'damage': 1,
        'speed_mult': 1.5,
        'color': YELLOW,
        'base_cost': 1000,
        'cost_mult': 3.0,
        'special': 'scatter',
        'description': 'Splits into multiple balls periodically'
    },
    'cannon': {
        'name': 'Cannon Ball',
        'damage': 10,
        'speed_mult': 0.5,
        'color': (100, 100, 100),
        'base_cost': 5000,
        'cost_mult': 3.5,
        'special': 'cannon',
        'description': 'Slow but deals massive damage'
    },
    'poison': {
        'name': 'Poison Ball',
        'damage': 1,
        'speed_mult': 1.0,
        'color': (0, 200, 0),
        'base_cost': 12000,
        'cost_mult': 4.0,
        'special': 'poison',
        'poison_duration': 3.0,
        'poison_dps': 2,
        'description': 'Applies damage over time'
    }
}

# Brick types (simplified for Idle Breakout style)
BRICK_COLORS = [
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (100, 100, 255),  # Blue
    (255, 255, 100),  # Yellow
    (255, 100, 255),  # Pink
    (100, 255, 255),  # Cyan
    (255, 150, 100),  # Orange
    (200, 100, 255),  # Purple
]

# Save file
SAVE_FILE = 'game_save.json'
