import pygame
import json
import os
import copy

# Initialize Pygame
pygame.init()

# Save File Name
SAVE_FILE = "savegame.json"

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tile properties
TILE_SIZE = 32

# Tile Types
FLOOR_TILE_TYPE = 0 # Renamed for clarity if needed elsewhere
WALL_TILE_TYPE = 1
KEY_TILE = 2
POTION_TILE = 3
SWORD_TILE = 4
SHIELD_TILE = 5
DOOR_TILE = 6
STAIRS_UP_TILE = 7
STAIRS_DOWN_TILE = 8
SUPER_POTION_TILE = 9
STEEL_SWORD_TILE = 10
STEEL_SHIELD_TILE = 11
NPC_WISE_MAN_TILE = 12
SHOPKEEPER_TILE = 13

# Map Definitions
map_floor0 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1], # Key and Potion
    [1, 0, 1, 1, 0, 1, 1, 1, SHOPKEEPER_TILE, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1], # Shop at (2,8)
    [1, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, STAIRS_UP_TILE, 1], # Door at (3,6), Stairs Up at (3,18)
    [1, 0, 1, 1, 0, 1, 0, 1, NPC_WISE_MAN_TILE, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], # NPC at (4,8)
    [1, 0, 4, 0, 0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 1], # Sword, Super Potion at (5,6), Shield
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1], # Another key at (7,14)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Floor 1: New layout, includes arrival and departure stairs, and a boss arena
map_floor1 = [ # Col:0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #0
    [1, 0, STAIRS_DOWN_TILE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #1 Stairs Down (arrival from F0) at (1,2)
    [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1], #2
    [1, 0, 1, 0, 10, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], #3 Steel Sword at (3,4)
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], #4 Boss arena walls
    [1, 0, 1, 0, 0, STAIRS_DOWN_TILE, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1], #5 Stairs Down (to F0) at (5,5). Boss entry at (5,15)
    [1, 0, 1, 1, 1, 1, 0, 11, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1], #6 Steel Shield at (6,7). Boss at (6,15)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1], #7 Boss arena walls
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #8
]
all_floor_maps = [map_floor0, map_floor1]
# map_floor0[5][6] = SUPER_POTION_TILE (row 5, col 6)
# map_floor1[4][4] = STEEL_SWORD_TILE (Original subtask placement: map_floor1[3][4] is the actual placement for (row 3, col 4))
# map_floor1[7][7] = STEEL_SHIELD_TILE (Original subtask placement: map_floor1[6][7] is the actual placement for (row 6, col 7))

# Stair Positions (map_col, map_row)
F0_STAIRS_UP_POS = (18, 3)
F1_STAIRS_DOWN_ARRIVAL_POS = (2, 1) # This is where player arrives on F1 (map_floor1[1][2])
F1_STAIRS_DOWN_POS = (5, 5)         # This is a different stair on F1 to go back to F0 (map_floor1[5][5])
F0_STAIRS_DOWN_ARRIVAL_POS = (3, 3) # This is where player arrives on F0 from F1's F1_STAIRS_DOWN_POS

# Update maps with correct stair tile types based on definitions
map_floor0[F0_STAIRS_UP_POS[1]][F0_STAIRS_UP_POS[0]] = STAIRS_UP_TILE
map_floor1[F1_STAIRS_DOWN_ARRIVAL_POS[1]][F1_STAIRS_DOWN_ARRIVAL_POS[0]] = STAIRS_DOWN_TILE
map_floor1[F1_STAIRS_DOWN_POS[1]][F1_STAIRS_DOWN_POS[0]] = STAIRS_DOWN_TILE
# Note: F0_STAIRS_DOWN_ARRIVAL_POS is an arrival point, tile type on map_floor0 at this point should be floor or specific visual if needed.
# For this subtask, we assume arrival points are just regular floor tiles unless specified as a stair tile.
# The original description was slightly confusing on F0_STAIRS_UP_ARRIVAL_POS, simplifying to defined arrival coords.

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Magic Tower")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0) # Player color, also potion color
FLOOR_COLOR = (100, 100, 100)  # Gray
WALL_COLOR = (50, 50, 50)    # Dark Gray
KEY_COLOR = (255, 255, 0)    # Yellow
POTION_COLOR = (255, 0, 0)   # Red (Regular Potion)
SWORD_COLOR = (173, 216, 230) # Light Blue (Regular Sword)
SHIELD_COLOR = (128, 128, 128) # Gray (Regular Shield)
DOOR_COLOR = (139, 69, 19)   # Brown
STAIRS_COLOR = (138, 43, 226) # BlueViolet
SUPER_POTION_COLOR = (255, 105, 180) # Hot Pink
STEEL_SWORD_COLOR = (192, 192, 192) # Silver
STEEL_SHIELD_COLOR = (112, 128, 144) # Slate Gray
NPC_COLOR = (0, 0, 200)      # Dark Blue
SHOP_COLOR = (34, 139, 34)   # Forest Green


# Item Effects
POTION_HEAL_AMOUNT = 20       # Regular Potion
SWORD_ATK_BOOST = 5           # Regular Sword
SHIELD_DEF_BOOST = 2          # Regular Shield

SUPER_POTION_HEAL_AMOUNT = 50
STEEL_SWORD_ATK_BOOST = 10
STEEL_SHIELD_DEF_BOOST = 5

# NPC Dialogue
NPC_DIALOGUE = {
    NPC_WISE_MAN_TILE: "Greetings, traveler! The path ahead is perilous. Seek the Steel Sword on the next floor to aid you."
}

# Enemy Definitions & Colors (centralized for reference)
# Green Slime: color: (0, 200, 0) -> Adjusted Green Slime color
# Goblin Archer: color: (150, 150, 0) (Yellowish-Green)
# Orc Warrior: color: (0, 100, 0) (Dark Green)
# Shadow Mage: color: (75, 0, 130) (Indigo)
# BOSS_GUARDIAN: color: (139, 0, 0) (Dark Red)

BOSS_GUARDIAN_DATA = {'name': 'Tower Guardian', 'hp': 150, 'atk': 25, 'def': 10, 'color': (139, 0, 0), 'gold_drop': 100, 'xp_yield': 100}

enemies_floor0 = [
    {'id': 0, 'name': 'Green Slime', 'hp': 30, 'atk': 8, 'def': 2, 'map_x': 5, 'map_y': 3, 'color': (0, 200, 0), 'gold_drop': 5, 'xp_yield': 10},
    {'id': 100, 'name': 'Goblin Archer', 'hp': 20, 'atk': 12, 'def': 1, 'map_x': 7, 'map_y': 3, 'color': (150, 150, 0), 'gold_drop': 8, 'xp_yield': 15},
    {'id': 101, 'name': 'Goblin Archer', 'hp': 20, 'atk': 12, 'def': 1, 'map_x': 10, 'map_y': 5, 'color': (150, 150, 0), 'gold_drop': 8, 'xp_yield': 15},
    {'id': 102, 'name': 'Shadow Mage', 'hp': 25, 'atk': 15, 'def': 0, 'map_x': 15, 'map_y': 2, 'color': (75, 0, 130), 'gold_drop': 12, 'xp_yield': 20},
    {'id': 103, 'name': 'Green Slime', 'hp': 30, 'atk': 8, 'def': 2, 'map_x': 2, 'map_y': 6, 'color': (0, 200, 0), 'gold_drop': 5, 'xp_yield': 10},
]
enemies_floor1 = [
    {'id': 200, 'name': 'Orc Warrior', 'hp': 50, 'atk': 10, 'def': 5, 'map_x': 5, 'map_y': 3, 'color': (0, 100, 0), 'gold_drop': 15, 'xp_yield': 25},
    {'id': 202, 'name': 'Goblin Archer', 'hp': 20, 'atk': 12, 'def': 1, 'map_x': 12, 'map_y': 4, 'color': (150, 150, 0), 'gold_drop': 8, 'xp_yield': 15},
    {'id': 203, 'name': 'Green Slime', 'hp': 30, 'atk': 8, 'def': 2, 'map_x': 15, 'map_y': 2, 'color': (0, 200, 0), 'gold_drop': 5, 'xp_yield': 10},
    {'id': 204, 'name': 'Shadow Mage', 'hp': 25, 'atk': 15, 'def': 0, 'map_x': 12, 'map_y': 6, 'color': (75, 0, 130), 'gold_drop': 12, 'xp_yield': 20},
    {
        'id': 250, 
        'name': BOSS_GUARDIAN_DATA['name'], 
        'hp': BOSS_GUARDIAN_DATA['hp'], 
        'atk': BOSS_GUARDIAN_DATA['atk'], 
        'def': BOSS_GUARDIAN_DATA['def'], 
        'map_x': 15, 
        'map_y': 6,  
        'color': BOSS_GUARDIAN_DATA['color'],
        'gold_drop': BOSS_GUARDIAN_DATA['gold_drop'],
        'xp_yield': BOSS_GUARDIAN_DATA['xp_yield']
    }
]
all_enemies_on_floors = [enemies_floor0, enemies_floor1]

# Player properties
player_start_pixel_x = TILE_SIZE * 1.5
player_start_pixel_y = TILE_SIZE * 1.5
player = {
    "x": player_start_pixel_x,
    "y": player_start_pixel_y,
    "map_x": int(player_start_pixel_x // TILE_SIZE),
    "map_y": int(player_start_pixel_y // TILE_SIZE),
    "width": 32,
    "height": 32,
    "speed": 5, 
    "hp": 100,
    "max_hp": 100,
    "atk": 10,
    "def": 5,
    "keys": 0,
    "gold": 0,
    "level": 1,
    "experience": 0,
    "xp_to_next_level": 100
}

# Initialize Font
pygame.font.init() # Explicitly initialize font module, good practice
STATS_FONT = pygame.font.Font(None, 28) # Default system font, size 28
MESSAGE_FONT = pygame.font.Font(None, 24) # Slightly smaller for messages
GAME_OVER_FONT = pygame.font.Font(None, 74) # Font for Game Over message
WHITE = (255, 255, 255)
GREY = (200, 200, 200) # For message log text

# UI and Game State Variables
current_floor = 1
message_log = []
MAX_LOG_MESSAGES = 5

# Shop State
in_shop_menu = False
shop_message = ""
SHOP_INVENTORY = [
    {'id': 'potion', 'name': 'Health Potion', 'cost': 15, 'effect_type': 'HEAL', 'amount': POTION_HEAL_AMOUNT},
    {'id': 'super_potion', 'name': 'Super Potion', 'cost': 40, 'effect_type': 'HEAL', 'amount': SUPER_POTION_HEAL_AMOUNT},
    {'id': 'key', 'name': 'Key', 'cost': 50, 'effect_type': 'ADD_KEY', 'amount': 1},
    {'id': 'atk_boost_small', 'name': 'ATK Boost (+2)', 'cost': 100, 'effect_type': 'ATK_BOOST', 'amount': 2, 'permanent': True},
    {'id': 'def_boost_small', 'name': 'DEF Boost (+1)', 'cost': 80, 'effect_type': 'DEF_BOOST', 'amount': 1, 'permanent': True}
]
SHOP_UI_BACKGROUND_COLOR = (50, 50, 70) # Dark Slate Blue for shop background

# Create player surface
player_surface = pygame.Surface((player["width"], player["height"]))
player_surface.fill(RED)

# Function to check collision with walls
def check_collision(player_rect, current_map_data, tile_size): # Takes current_map_data
    # Get the map coordinates of the player's corners
    left_col = player_rect.left // tile_size
    right_col = player_rect.right // tile_size
    top_row = player_rect.top // tile_size
    bottom_row = player_rect.bottom // tile_size

    # Check all tiles the player might be overlapping with
    for r in range(top_row, bottom_row + 1):
        for c in range(left_col, right_col + 1):
            # Check if the tile is within map boundaries
            if 0 <= r < len(current_map_data) and 0 <= c < len(current_map_data[0]):
                # Treat walls (1), closed doors (6), NPCs (12), and Shopkeepers (13) as collidable.
                tile_val = current_map_data[r][c]
                if tile_val == WALL_TILE_TYPE or tile_val == DOOR_TILE or \
                   tile_val == NPC_WISE_MAN_TILE or tile_val == SHOPKEEPER_TILE:  
                    obstacle_rect = pygame.Rect(c * tile_size, r * tile_size, tile_size, tile_size)
                    if player_rect.colliderect(obstacle_rect):
                        return True  # Collision detected
    return False # No collision

# Function to draw the map
def draw_map(screen, current_map_data, tile_size): # Takes current_map_data
    for row_index, row in enumerate(current_map_data):
        for col_index, tile_type in enumerate(row):
            rect_x = col_index * tile_size
            rect_y = row_index * tile_size
            tile_rect = pygame.Rect(rect_x, rect_y, tile_size, tile_size)
            
            # Draw floor first for all walkable/special tiles
            if tile_type == FLOOR_TILE_TYPE or tile_type == KEY_TILE or tile_type == POTION_TILE or \
               tile_type == SWORD_TILE or tile_type == SHIELD_TILE or tile_type == DOOR_TILE or \
               tile_type == STAIRS_UP_TILE or tile_type == STAIRS_DOWN_TILE or \
               tile_type == SUPER_POTION_TILE or tile_type == STEEL_SWORD_TILE or tile_type == STEEL_SHIELD_TILE or \
               tile_type == NPC_WISE_MAN_TILE or tile_type == SHOPKEEPER_TILE: # NPC/Shop tile also gets a floor base
                pygame.draw.rect(screen, FLOOR_COLOR, tile_rect)

            # Draw specific items, walls, doors or stairs
            if tile_type == WALL_TILE_TYPE:
                pygame.draw.rect(screen, WALL_COLOR, tile_rect)
            elif tile_type == KEY_TILE:
                pygame.draw.rect(screen, KEY_COLOR, tile_rect)
            elif tile_type == POTION_TILE:
                pygame.draw.rect(screen, POTION_COLOR, tile_rect)
            elif tile_type == SWORD_TILE:
                pygame.draw.rect(screen, SWORD_COLOR, tile_rect)
            elif tile_type == SHIELD_TILE:
                pygame.draw.rect(screen, SHIELD_COLOR, tile_rect)
            elif tile_type == DOOR_TILE:
                pygame.draw.rect(screen, DOOR_COLOR, tile_rect)
            elif tile_type == STAIRS_UP_TILE or tile_type == STAIRS_DOWN_TILE:
                pygame.draw.rect(screen, STAIRS_COLOR, tile_rect)
            elif tile_type == SUPER_POTION_TILE:
                pygame.draw.rect(screen, SUPER_POTION_COLOR, tile_rect)
            elif tile_type == STEEL_SWORD_TILE:
                pygame.draw.rect(screen, STEEL_SWORD_COLOR, tile_rect)
            elif tile_type == STEEL_SHIELD_TILE:
                pygame.draw.rect(screen, STEEL_SHIELD_COLOR, tile_rect)
            elif tile_type == NPC_WISE_MAN_TILE:
                pygame.draw.rect(screen, NPC_COLOR, tile_rect)
            elif tile_type == SHOPKEEPER_TILE:
                pygame.draw.rect(screen, SHOP_COLOR, tile_rect)
            # No need for 'elif tile_type == FLOOR_TILE_TYPE:' here if floor is drawn as base

# Function to draw player stats
def draw_player_stats(screen, player_stats, font, position, current_floor_num): # Changed 'player' to 'player_stats' for clarity
    stats_texts = [
        f"Floor: {current_floor_num}",
        f"Level: {player_stats['level']}",
        f"XP: {player_stats['experience']} / {player_stats['xp_to_next_level']}",
        f"HP: {player_stats['hp']} / {player_stats['max_hp']}",
        f"ATK: {player_stats['atk']}",
        f"DEF: {player_stats['def']}",
        f"Keys: {player_stats['keys']}",
        f"Gold: {player_stats['gold']}"
    ]
    
    start_x, start_y = position
    line_height = font.get_height() + 5

    for i, text in enumerate(stats_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (start_x, start_y + i * line_height))

# Helper function to add messages to the log
def add_message(text):
    message_log.append(text)
    if len(message_log) > MAX_LOG_MESSAGES:
        del message_log[0]

# Function to draw the message log
def draw_message_log(screen, log, font, position, color):
    start_x, start_y = position
    line_height = font.get_height() + 3

    for i, message_text in enumerate(log):
        message_surface = font.render(message_text, True, color)
        screen.blit(message_surface, (start_x, start_y + i * line_height))

# Function to draw enemies
def draw_enemies(screen, enemies_list, tile_size):
    for enemy in enemies_list:
        enemy_rect_x = enemy['map_x'] * tile_size
        enemy_rect_y = enemy['map_y'] * tile_size
        # Draw a simple rectangle for the enemy, slightly smaller than a full tile
        enemy_visual_rect = pygame.Rect(enemy_rect_x + tile_size * 0.1, 
                                        enemy_rect_y + tile_size * 0.1, 
                                        tile_size * 0.8, 
                                        tile_size * 0.8)
        pygame.draw.rect(screen, enemy['color'], enemy_visual_rect)

# Function to handle combat
def handle_combat(current_player, current_enemy):
    # Player attacks enemy
    player_damage = max(0, current_player['atk'] - current_enemy['def'])
    current_enemy['hp'] -= player_damage
    add_message(f"You hit {current_enemy['name']} for {player_damage} damage.")

    if current_enemy['hp'] > 0:
        # Enemy attacks player (if still alive)
        enemy_damage = max(0, current_enemy['atk'] - current_player['def'])
        current_player['hp'] -= enemy_damage
        add_message(f"{current_enemy['name']} hits you for {enemy_damage} damage.")
    else:
        add_message(f"Defeated {current_enemy['name']}.")
    
    return current_enemy

# --- Level Up Function ---
def check_level_up(player_obj):
    leveled_up_this_check = False
    if player_obj['experience'] >= player_obj['xp_to_next_level']:
        leveled_up_this_check = True
        player_obj['level'] += 1
        excess_xp = player_obj['experience'] - player_obj['xp_to_next_level']
        player_obj['experience'] = excess_xp
        player_obj['xp_to_next_level'] = int(player_obj['xp_to_next_level'] * 1.5) # Or other scaling factor
        
        hp_boost = 20
        atk_boost = 2
        def_boost = 1
        
        player_obj['max_hp'] += hp_boost
        player_obj['atk'] += atk_boost
        player_obj['def'] += def_boost
        player_obj['hp'] = player_obj['max_hp'] # Full heal
        
        add_message(f"Level Up! Reached Level {player_obj['level']}.")
        add_message(f"MaxHP+{hp_boost}, ATK+{atk_boost}, DEF+{def_boost}. Fully healed.")
    return leveled_up_this_check

# --- Save and Load Functions ---
def save_game():
    game_state = {
        'player_data': player, # Player dict is fine as a shallow copy for JSON dump
        'current_floor_index': current_floor,
        'all_floor_map_data': copy.deepcopy(all_floor_maps),
        'all_enemies_data': copy.deepcopy(all_enemies_on_floors),
        'message_log_data': list(message_log) # shallow copy for list of strings
    }
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_state, f, indent=4)
        add_message("Game Saved.")
    except IOError:
        add_message("Error saving game.")

def load_game():
    global player, current_floor, all_floor_maps, all_enemies_on_floors, message_log
    if not os.path.exists(SAVE_FILE):
        add_message("No save file found.")
        return False
    
    try:
        with open(SAVE_FILE, 'r') as f:
            loaded_data = json.load(f)
        
        # Restore game state
        player.clear()
        player.update(loaded_data['player_data'])
        
        current_floor = loaded_data['current_floor_index']
        
        # Ensure lists are properly replaced content-wise
        all_floor_maps[:] = loaded_data['all_floor_map_data']
        all_enemies_on_floors[:] = loaded_data['all_enemies_data']
        message_log[:] = loaded_data['message_log_data']

        # Recalculate player pixel coordinates
        player['x'] = player['map_x'] * TILE_SIZE + (TILE_SIZE - player['width']) // 2
        player['y'] = player['map_y'] * TILE_SIZE + (TILE_SIZE - player['height']) // 2
        
        add_message("Game Loaded.")
        return True
    except (IOError, json.JSONDecodeError) as e:
        add_message(f"Error loading game: {e}")
        return False

# --- Initial Game Setup ---
# Define default game state variables first
# (player, current_floor, all_floor_maps, all_enemies_on_floors, message_log are already defined globally)

# Attempt to load game at the start
game_loaded_successfully = load_game()
if not game_loaded_successfully:
    # If load failed or no save file, use/re-initialize with default values
    # (These are already set up globally, so this block can be for any specific re-init if needed)
    add_message("Starting a new game.")


# Main game loop
running = True
game_over = False # Game over flag (already defined, ensure it's reset for new game if not loaded)
if not game_loaded_successfully: # If starting a new game, ensure game_over is False
    game_over = False


while running:
    # Unified Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_shop_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_shop_menu = False
                    add_message("Exited shop.")
                    shop_message = "" 
                
                item_index_to_buy = -1
                if event.key == pygame.K_1: item_index_to_buy = 0
                elif event.key == pygame.K_2: item_index_to_buy = 1
                elif event.key == pygame.K_3: item_index_to_buy = 2
                elif event.key == pygame.K_4: item_index_to_buy = 3
                elif event.key == pygame.K_5: item_index_to_buy = 4

                if 0 <= item_index_to_buy < len(SHOP_INVENTORY):
                    selected_item = SHOP_INVENTORY[item_index_to_buy]
                    if player['gold'] >= selected_item['cost']:
                        player['gold'] -= selected_item['cost']
                        if selected_item['effect_type'] == 'HEAL':
                            player['hp'] = min(player['max_hp'], player['hp'] + selected_item['amount'])
                        elif selected_item['effect_type'] == 'ADD_KEY':
                            player['keys'] += selected_item['amount']
                        elif selected_item['effect_type'] == 'ATK_BOOST':
                            player['atk'] += selected_item['amount']
                        elif selected_item['effect_type'] == 'DEF_BOOST':
                             player['def'] += selected_item['amount']
                        shop_message = f"Bought {selected_item['name']}."
                        add_message(f"Bought {selected_item['name']} for {selected_item['cost']} gold.")
                    else:
                        shop_message = "Not enough gold!"
        
        # elif game_over: # game_over loop handles its own QUIT
            # pass 
        
        else: # Normal gameplay event handling (not in shop, not effectively in game_over's own loop)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_game()
                # Other normal gameplay KEYDOWN events can go here
    
    # Main Game Logic (runs if not in shop menu)
    if not in_shop_menu:
        # Centralize current map and enemy data access for the current frame
        current_map_data = all_floor_maps[current_floor]
        current_enemies_list = all_enemies_on_floors[current_floor]

        # --- Drawing Game World (This part is always active if not in shop, game_over handles its own drawing) ---
        screen.fill(BLACK)
        # Use the centrally defined current_map_data and current_enemies_list for drawing
        draw_map(screen, current_map_data, TILE_SIZE)
        draw_enemies(screen, current_enemies_list, TILE_SIZE)
        screen.blit(player_surface, (player["x"], player["y"]))
        
        stats_position = (650, 20) 
        draw_player_stats(screen, player, STATS_FONT, stats_position, current_floor + 1) # Display 1-indexed floor
        message_log_position = (650, 180)
        draw_message_log(screen, message_log, MESSAGE_FONT, message_log_position, GREY)

        if game_over:
            # Ensure game_over_text_surface is created here, inside the if game_over block
            game_over_text_surface = GAME_OVER_FONT.render("Game Over", True, RED)
            text_rect = game_over_text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            
            # Optional: Add a semi-transparent overlay to make text more readable
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,128)) # Black with 50% alpha
            screen.blit(overlay, (0,0))
            
            screen.blit(game_over_text_surface, text_rect)
            pygame.display.flip()
            # Event loop for game over to allow closing, but prevent other actions
            while game_over: # This inner loop will now correctly use the 'game_over' variable from the outer scope
                for event_gm_over in pygame.event.get():
                    if event_gm_over.type == pygame.QUIT:
                        running = False
                        game_over = False # To exit this inner loop
                pygame.time.wait(100) # Prevent high CPU usage in game over state
            if not running: # If QUIT was detected in game over loop
                continue
        else:
            # If not game_over, flip the display for normal game rendering
            pygame.display.flip()

        # --- Start of Game Logic Block (only if not game_over and not in_shop_menu) ---
        if not game_over: 
            action_taken_this_turn = False 

            # Get pressed keys
            keys = pygame.key.get_pressed()
            print(f"DEBUG: Keys - L:{keys[pygame.K_LEFT]}, R:{keys[pygame.K_RIGHT]}, U:{keys[pygame.K_UP]}, D:{keys[pygame.K_DOWN]}")
            
            original_x = player["x"]
            original_y = player["y"]
            
            prospective_x = original_x
            prospective_y = original_y

            if keys[pygame.K_LEFT]: prospective_x -= player["speed"]
            if keys[pygame.K_RIGHT]: prospective_x += player["speed"]
            if keys[pygame.K_UP]: prospective_y -= player["speed"]
            if keys[pygame.K_DOWN]: prospective_y += player["speed"]

            if prospective_x < 0: prospective_x = 0
            elif prospective_x > SCREEN_WIDTH - player["width"]: prospective_x = SCREEN_WIDTH - player["width"]
            if prospective_y < 0: prospective_y = 0
            elif prospective_y > SCREEN_HEIGHT - player["height"]: prospective_y = SCREEN_HEIGHT - player["height"]

            target_center_x = prospective_x + player["width"] / 2
            target_center_y = prospective_y + player["height"] / 2
            target_map_col = int(target_center_x // TILE_SIZE)
            target_map_row = int(target_center_y // TILE_SIZE)
            print(f"DEBUG: Original Pos (pixels): ({original_x}, {original_y}), Prospective Pos (pixels): ({prospective_x}, {prospective_y})")
            print(f"DEBUG: Target Grid Cell: ({target_map_col}, {target_map_row})")

            # --- Stair Interaction Logic ---
            # current_map_data and current_enemies_list are already defined at the start of the 'if not in_shop_menu:' block
            player_is_moving_to_new_tile = (int(original_x // TILE_SIZE) != target_map_col or int(original_y // TILE_SIZE) != target_map_row)
            print(f"DEBUG: Player attempting to move to new tile: {player_is_moving_to_new_tile}")

            print("DEBUG: Checking Stairs Interaction")
            if player_is_moving_to_new_tile and 0 <= target_map_row < len(current_map_data) and 0 <= target_map_col < len(current_map_data[0]):
                tile_type_at_target = current_map_data[target_map_row][target_map_col] 

                if tile_type_at_target == STAIRS_UP_TILE:
                    if current_floor == 0 and (target_map_col, target_map_row) == F0_STAIRS_UP_POS:
                        current_floor = 1; player['map_x'], player['map_y'] = F1_STAIRS_DOWN_ARRIVAL_POS
                        action_taken_this_turn = True; add_message(f"Moved to Floor {current_floor + 1}.")
                        # Update map/enemy data immediately after floor change for this frame
                        current_map_data = all_floor_maps[current_floor]
                        current_enemies_list = all_enemies_on_floors[current_floor]
                elif tile_type_at_target == STAIRS_DOWN_TILE:
                    if current_floor == 1:
                        new_floor_idx = -1
                        new_player_map_coords = (-1,-1)
                        if (target_map_col, target_map_row) == F1_STAIRS_DOWN_POS:
                            new_floor_idx = 0; new_player_map_coords = F0_STAIRS_DOWN_ARRIVAL_POS
                        elif (target_map_col, target_map_row) == F1_STAIRS_DOWN_ARRIVAL_POS:
                            new_floor_idx = 0; new_player_map_coords = (int(player_start_pixel_x // TILE_SIZE), int(player_start_pixel_y // TILE_SIZE))
                        
                        if new_floor_idx != -1:
                            current_floor = new_floor_idx
                            player['map_x'], player['map_y'] = new_player_map_coords
                            action_taken_this_turn = True; add_message(f"Moved to Floor {current_floor + 1}.")
                            # Update map/enemy data immediately after floor change for this frame
                            current_map_data = all_floor_maps[current_floor]
                            current_enemies_list = all_enemies_on_floors[current_floor]
                
                if action_taken_this_turn: 
                    player['x'] = player['map_x'] * TILE_SIZE + (TILE_SIZE - player['width']) // 2
                    player['y'] = player['map_y'] * TILE_SIZE + (TILE_SIZE - player['height']) // 2

            # --- NPC Interaction Logic (only if no stair interaction occurred) ---
            print("DEBUG: Checking NPC/Shop Interaction")
            if not action_taken_this_turn and player_is_moving_to_new_tile and \
               0 <= target_map_row < len(current_map_data) and 0 <= target_map_col < len(current_map_data[0]):
                # current_map_data is already up-to-date for the current floor
                tile_type_at_target_for_interaction = current_map_data[target_map_row][target_map_col] 
                
                if tile_type_at_target_for_interaction == NPC_WISE_MAN_TILE:
                    if NPC_WISE_MAN_TILE in NPC_DIALOGUE:
                        add_message(NPC_DIALOGUE[NPC_WISE_MAN_TILE])
                    else:
                        add_message("The person stands silently.")
                    action_taken_this_turn = True 
                
                elif tile_type_at_target_for_interaction == SHOPKEEPER_TILE:
                    in_shop_menu = True
                    shop_message = "Welcome! Press number to buy, ESC to exit."
                    action_taken_this_turn = True


            # --- Combat Logic (only if no stair, NPC or Shop interaction occurred) ---
            print("DEBUG: Checking Combat Interaction")
            if not action_taken_this_turn and player_is_moving_to_new_tile:
                # current_enemies_list is already up-to-date for the current floor
                enemy_to_fight = None
                enemy_idx = -1
                for i, enemy in enumerate(current_enemies_list): 
                    if enemy['map_x'] == target_map_col and enemy['map_y'] == target_map_row:
                        enemy_to_fight = enemy
                        enemy_idx = i
                        break
                
                if enemy_to_fight:
                    updated_enemy = handle_combat(player, enemy_to_fight)
                    current_enemies_list[enemy_idx] = updated_enemy 

                    if updated_enemy['hp'] <= 0:
                        # Award gold
                        if 'gold_drop' in updated_enemy:
                            player['gold'] += updated_enemy['gold_drop']
                            add_message(f"Gained {updated_enemy['gold_drop']} gold from {updated_enemy['name']}.")
                        
                        # Award XP
                        if 'xp_yield' in updated_enemy:
                            player['experience'] += updated_enemy['xp_yield']
                            add_message(f"Gained {updated_enemy['xp_yield']} XP from {updated_enemy['name']}.")
                            # Check for level up (potentially multiple times)
                            while check_level_up(player):
                                pass # The function handles messages and stat changes

                        current_enemies_list.pop(enemy_idx)
                    
                    if player['hp'] <= 0:
                        game_over = True
                        add_message("Game Over.") 
                    
                    action_taken_this_turn = True 

            # --- Door Interaction Logic (only if no combat or stair interaction occurred) ---
            print("DEBUG: Checking Door Interaction")
            if not action_taken_this_turn and 0 <= target_map_row < len(current_map_data) and 0 <= target_map_col < len(current_map_data[0]):
                tile_type_at_target = current_map_data[target_map_row][target_map_col] # Re-fetch, map could change if multi-step actions were allowed
                if tile_type_at_target == DOOR_TILE and player_is_moving_to_new_tile:
                    if player["keys"] > 0:
                        player["keys"] -= 1
                        current_map_data[target_map_row][target_map_col] = FLOOR_TILE_TYPE # Open door
                        add_message("Opened a door.")
                        action_taken_this_turn = True 
                    else:
                        add_message("You need a key!")
                        action_taken_this_turn = True 
            
            # --- Movement and Wall Collision (if no action like combat, door, or stairs consumed the turn) ---
            print(f"DEBUG: Entering final movement block. action_taken_this_turn: {action_taken_this_turn}")
            if not action_taken_this_turn:
                temp_player_rect = pygame.Rect(prospective_x, prospective_y, player["width"], player["height"])
                collision_result = check_collision(temp_player_rect, current_map_data, TILE_SIZE)
                print(f"DEBUG: Collision check result for combined move: {collision_result}")
                if not collision_result:
                    player["x"] = prospective_x
                    player["y"] = prospective_y
                    # Update map_x and map_y based on pixel position after successful move
                    player["map_x"] = int(player["x"] // TILE_SIZE) 
                    player["map_y"] = int(player["y"] // TILE_SIZE)
                    print(f"DEBUG: Player Pos Updated To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")
                else: # Sliding logic
                    moved_x_only = False
                    temp_player_rect_x_only = pygame.Rect(prospective_x, original_y, player["width"], player["height"])
                    if original_x != prospective_x : # Only check X-slide if there was an X movement attempt
                        collision_x_result = check_collision(temp_player_rect_x_only, current_map_data, TILE_SIZE)
                        print(f"DEBUG: Collision check result for X-only move: {collision_x_result}")
                        if not collision_x_result:
                            player["x"] = prospective_x
                            player["map_x"] = int(player["x"] // TILE_SIZE)
                            # player["y"] remains original_y for this part of slide check
                            player["map_y"] = int(original_y // TILE_SIZE) 
                            moved_x_only = True
                            print(f"DEBUG: Player Pos Updated (X-SLIDE) To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")

                    # Y-only slide: If X-slide happened, check Y from new player X. Else, from original X.
                    # If only Y movement was intended, prospective_x is original_x.
                    current_x_for_y_slide_check = player["x"] if moved_x_only else original_x
                    temp_player_rect_y_only = pygame.Rect(current_x_for_y_slide_check, prospective_y, player["width"], player["height"])
                    if original_y != prospective_y : # Only check Y-slide if there was a Y movement attempt
                        collision_y_result = check_collision(temp_player_rect_y_only, current_map_data, TILE_SIZE)
                        print(f"DEBUG: Collision check result for Y-only move (from x={current_x_for_y_slide_check}): {collision_y_result}")
                        if not collision_y_result:
                            player["y"] = prospective_y
                            player["map_y"] = int(player["y"] // TILE_SIZE)
                            # Ensure map_x is correct based on whether X-slide occurred or not
                            player["map_x"] = int(current_x_for_y_slide_check // TILE_SIZE)
                            # If X-slide also happened, player["x"] is already prospective_x
                            # If only Y-slide, player["x"] remains original_x (current_x_for_y_slide_check)
                            if not moved_x_only: player["x"] = original_x # Correct pixel X if only Y moved
                                
                            print(f"DEBUG: Player Pos Updated (Y-SLIDE) To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")


            # --- Item Pickup Logic (if player position actually changed from original) ---
            # This should use the player's NEW map_x, map_y after any movement or floor change.
            if player["map_x"] != int(original_x // TILE_SIZE) or player["map_y"] != int(original_y // TILE_SIZE) or action_taken_this_turn: # check if map position changed or stairs used
                # If stairs were used, action_taken_this_turn is true, and player is on a new tile.
                # Item pickup should occur on the new tile.
                # The current map_col and map_row for item pickup should be player['map_x'] and player['map_y']
                
                map_col_for_item = player['map_x']
                map_row_for_item = player['map_y']
                
                # Ensure current_map_data is up-to-date if floor changed
                current_map_data_for_items = all_floor_maps[current_floor]

                if 0 <= map_row_for_item < len(current_map_data_for_items) and 0 <= map_col_for_item < len(current_map_data_for_items[0]):
                    # Check tile type on the *current* floor map after potential floor change
                    tile_type_under_player = current_map_data_for_items[map_row_for_item][map_col_for_item]
                    
                    if tile_type_under_player == KEY_TILE:
                        player["keys"] += 1; current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE 
                        add_message("Picked up a Key.")
                    elif tile_type_under_player == POTION_TILE:
                        player["hp"] = min(player["max_hp"], player["hp"] + POTION_HEAL_AMOUNT); current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
                        add_message(f"Picked up a Potion. +{POTION_HEAL_AMOUNT} HP.")
                    elif tile_type_under_player == SWORD_TILE:
                        player["atk"] += SWORD_ATK_BOOST; current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
                        add_message(f"Picked up a Sword. +{SWORD_ATK_BOOST} ATK.")
                    elif tile_type_under_player == SHIELD_TILE:
                        player["def"] += SHIELD_DEF_BOOST; current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
                        add_message(f"Picked up a Shield. +{SHIELD_DEF_BOOST} DEF.")
                    elif tile_type_under_player == SUPER_POTION_TILE:
                        heal_amount = SUPER_POTION_HEAL_AMOUNT
                        player['hp'] = min(player['max_hp'], player['hp'] + heal_amount)
                        add_message(f"Picked up Super Potion. +{heal_amount} HP.")
                        current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
                    elif tile_type_under_player == STEEL_SWORD_TILE:
                        atk_boost = STEEL_SWORD_ATK_BOOST
                        player['atk'] += atk_boost
                        add_message(f"Picked up Steel Sword. +{atk_boost} ATK.")
                        current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
                    elif tile_type_under_player == STEEL_SHIELD_TILE:
                        def_boost = STEEL_SHIELD_DEF_BOOST
                        player['def'] += def_boost
                add_message(f"Picked up Steel Shield. +{def_boost} DEF.")
                current_map_data_for_items[map_row_for_item][map_col_for_item] = FLOOR_TILE_TYPE
            # --- End of Game Logic Block (if not game_over) --- (This comment was part of the previous diff, ensuring it's correctly placed or removed if it implies the end of the indented block)

    # End of 'if not in_shop_menu:' block
    else: # Player is in the shop menu (Drawing part only, event handling moved up)
        # --- Drawing Shop UI ---
        screen.fill(SHOP_UI_BACKGROUND_COLOR)
        
        # --- Drawing Shop UI ---
        screen.fill(SHOP_UI_BACKGROUND_COLOR)
        
        # Shop Title
        title_font = pygame.font.Font(None, 48) # Larger font for title
        title_surface = title_font.render("SHOP", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))

        # Player Gold
        gold_text = f"Your Gold: {player['gold']}"
        gold_surface = STATS_FONT.render(gold_text, True, WHITE)
        screen.blit(gold_surface, (50, 100))

        # Shop Items
        item_start_y = 150
        line_height = MESSAGE_FONT.get_height() + 10
        for i, item in enumerate(SHOP_INVENTORY):
            item_text = f"{i+1}. {item['name']} - {item['cost']} Gold"
            item_surface = MESSAGE_FONT.render(item_text, True, WHITE)
            screen.blit(item_surface, (50, item_start_y + i * line_height))
        
        # Shop Message (e.g., "Bought item", "Not enough gold")
        if shop_message:
            shop_msg_surface = MESSAGE_FONT.render(shop_message, True, WHITE)
            screen.blit(shop_msg_surface, (50, item_start_y + len(SHOP_INVENTORY) * line_height + 20))
            
        pygame.display.flip()

    # pygame.display.flip() # This was moved inside the main if/else for drawing

# Quit Pygame
pygame.quit()
