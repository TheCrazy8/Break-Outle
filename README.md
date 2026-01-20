# Break-Outle
An overly complicated idle breakout game

## Description
Break-Outle is a feature-rich remake of Idle Breakout, built with Python and Pygame. It combines classic breakout mechanics with idle/incremental game features.

## Features
- **Idle Gameplay**: Balls automatically spawn and break bricks
- **Multiple Ball Types**: Unlock different ball types with unique abilities
- **Upgrade System**: Purchase upgrades to improve ball power, speed, and spawn rates
- **Prestige System**: Reset progress for permanent bonuses
- **Special Bricks**: Different brick types with unique behaviors
- **Power-ups**: Temporary boosts and special effects
- **Achievements**: Track your progress and unlock rewards
- **Save System**: Automatic saving of game progress
- **Statistics**: Detailed tracking of your gameplay

## Requirements
- Python 3.7 or higher
- Pygame 2.5.0 or higher

## Installation

### Option 1: Download Pre-built Executable (Recommended)
Download the latest release for your platform from the [Releases](https://github.com/TheCrazy8/Break-Outle/releases) page:
- **Windows**: `Break-Outle.exe`
- **Linux**: `Break-Outle`
- **macOS**: `Break-Outle`

Just download and run!

### Option 2: Run from Source
1. Clone the repository:
```bash
git clone https://github.com/TheCrazy8/Break-Outle.git
cd Break-Outle
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

### Option 3: Build Your Own Executable
1. Clone and install dependencies (see above)

2. Build the executable:
   - **Windows**: Run `build.bat` or `python build.py`
   - **Linux/Mac**: Run `./build.sh` or `python build.py`

3. Find your executable in the `dist/` directory

## How to Play
Run the game:
```bash
python main.py
```

### Controls
- **Mouse**: Navigate menus and click upgrades
- **ESC**: Pause/Resume game
- **Arrow Keys**: Manual paddle control (optional)
- **Space**: Speed up ball spawning (costs gold)

### Gameplay
1. Watch as balls automatically spawn and break bricks
2. Earn gold from breaking bricks
3. Click the shop button to purchase upgrades
4. Unlock new ball types and abilities
5. Prestige when progress slows to gain permanent bonuses

## Game Mechanics

### Ball Types
- **Basic Ball**: Standard ball, good all-around
- **Power Ball**: Deals extra damage
- **Speed Ball**: Moves faster, hits more bricks
- **Scatter Ball**: Spawns multiple smaller balls on impact
- **Plasma Ball**: Pierces through multiple bricks

### Upgrades
- Ball damage multipliers
- Ball speed improvements
- Auto-spawn rate increases
- Ball count increases
- Critical hit chance
- Gold multipliers

### Prestige
Reset your progress to gain prestige points, which provide permanent bonuses:
- Increased base damage
- Faster gold generation
- Better upgrade efficiency
- Unlock special abilities

## License
MIT License

## Development

### Building
This project uses PyInstaller to create standalone executables. The build process is automated via GitHub Actions, which creates executables for Windows, Linux, and macOS on every push.

To build locally:
```bash
python build.py
```

The executable will be created in the `dist/` directory.

### CI/CD
The project uses GitHub Actions for continuous integration:
- Automatically builds executables for all platforms on push
- Creates releases with binaries when tags are pushed (e.g., `v1.0.0`)
- Runs on Windows, Linux, and macOS runners

