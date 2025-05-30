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
FLOOR_TILE_TYPE = 0 
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
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1], 
    [1, 0, 1, 1, 0, 1, 1, 1, SHOPKEEPER_TILE, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, STAIRS_UP_TILE, 1], 
    [1, 0, 1, 1, 0, 1, 0, 1, NPC_WISE_MAN_TILE, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
    [1, 0, 4, 0, 0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 1], 
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
map_floor1 = [ 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, STAIRS_DOWN_TILE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1], 
    [1, 0, 1, 0, 10, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 1, 0, 0, STAIRS_DOWN_TILE, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 11, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
]
all_floor_maps = [map_floor0, map_floor1]

F0_STAIRS_UP_POS = (18, 3)
F1_STAIRS_DOWN_ARRIVAL_POS = (2, 1) 
F1_STAIRS_DOWN_POS = (5, 5)         
F0_STAIRS_DOWN_ARRIVAL_POS = (3, 3) 

map_floor0[F0_STAIRS_UP_POS[1]][F0_STAIRS_UP_POS[0]] = STAIRS_UP_TILE
map_floor1[F1_STAIRS_DOWN_ARRIVAL_POS[1]][F1_STAIRS_DOWN_ARRIVAL_POS[0]] = STAIRS_DOWN_TILE
map_floor1[F1_STAIRS_DOWN_POS[1]][F1_STAIRS_DOWN_POS[0]] = STAIRS_DOWN_TILE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Magic Tower")

BLACK = (0,0,0); RED = (255,0,0); FLOOR_COLOR = (100,100,100); WALL_COLOR = (50,50,50)
KEY_COLOR = (255,255,0); POTION_COLOR = (255,0,0); SWORD_COLOR = (173,216,230)
SHIELD_COLOR = (128,128,128); DOOR_COLOR = (139,69,19); STAIRS_COLOR = (138,43,226)
SUPER_POTION_COLOR = (255,105,180); STEEL_SWORD_COLOR = (192,192,192)
STEEL_SHIELD_COLOR = (112,128,144); NPC_COLOR = (0,0,200); SHOP_COLOR = (34,139,34)

POTION_HEAL_AMOUNT = 20; SWORD_ATK_BOOST = 5; SHIELD_DEF_BOOST = 2
SUPER_POTION_HEAL_AMOUNT = 50; STEEL_SWORD_ATK_BOOST = 10; STEEL_SHIELD_DEF_BOOST = 5

NPC_DIALOGUE = { NPC_WISE_MAN_TILE: "Greetings, traveler! The path ahead is perilous. Seek the Steel Sword on the next floor to aid you."}

BOSS_GUARDIAN_DATA = {'name':'Tower Guardian','hp':150,'atk':25,'def':10,'color':(139,0,0),'gold_drop':100,'xp_yield':100}
enemies_floor0 = [
    {'id':0,'name':'Green Slime','hp':30,'atk':8,'def':2,'map_x':5,'map_y':3,'color':(0,200,0),'gold_drop':5,'xp_yield':10},
    {'id':100,'name':'Goblin Archer','hp':20,'atk':12,'def':1,'map_x':7,'map_y':3,'color':(150,150,0),'gold_drop':8,'xp_yield':15},
    {'id':101,'name':'Goblin Archer','hp':20,'atk':12,'def':1,'map_x':10,'map_y':5,'color':(150,150,0),'gold_drop':8,'xp_yield':15},
    {'id':102,'name':'Shadow Mage','hp':25,'atk':15,'def':0,'map_x':15,'map_y':2,'color':(75,0,130),'gold_drop':12,'xp_yield':20},
    {'id':103,'name':'Green Slime','hp':30,'atk':8,'def':2,'map_x':2,'map_y':6,'color':(0,200,0),'gold_drop':5,'xp_yield':10},
]
enemies_floor1 = [
    {'id':200,'name':'Orc Warrior','hp':50,'atk':10,'def':5,'map_x':5,'map_y':3,'color':(0,100,0),'gold_drop':15,'xp_yield':25},
    {'id':202,'name':'Goblin Archer','hp':20,'atk':12,'def':1,'map_x':12,'map_y':4,'color':(150,150,0),'gold_drop':8,'xp_yield':15},
    {'id':203,'name':'Green Slime','hp':30,'atk':8,'def':2,'map_x':15,'map_y':2,'color':(0,200,0),'gold_drop':5,'xp_yield':10},
    {'id':204,'name':'Shadow Mage','hp':25,'atk':15,'def':0,'map_x':12,'map_y':6,'color':(75,0,130),'gold_drop':12,'xp_yield':20},
    {'id':250,'name':BOSS_GUARDIAN_DATA['name'],'hp':BOSS_GUARDIAN_DATA['hp'],'atk':BOSS_GUARDIAN_DATA['atk'], 
     'def':BOSS_GUARDIAN_DATA['def'],'map_x':15,'map_y':6,'color':BOSS_GUARDIAN_DATA['color'],
     'gold_drop':BOSS_GUARDIAN_DATA['gold_drop'],'xp_yield':BOSS_GUARDIAN_DATA['xp_yield']}
]
all_enemies_on_floors = [enemies_floor0, enemies_floor1]

player_start_pixel_x = TILE_SIZE*1.5; player_start_pixel_y = TILE_SIZE*1.5
player = {
    "x":player_start_pixel_x, "y":player_start_pixel_y,
    "map_x":int(player_start_pixel_x//TILE_SIZE), "map_y":int(player_start_pixel_y//TILE_SIZE),
    "width":32, "height":32, "speed":5, "hp":100, "max_hp":100,
    "atk":10, "def":5, "keys":0, "gold":0, "level":1, "experience":0, "xp_to_next_level":100
}

pygame.font.init()
STATS_FONT=pygame.font.Font(None,28); MESSAGE_FONT=pygame.font.Font(None,24)
GAME_OVER_FONT=pygame.font.Font(None,74); WHITE=(255,255,255); GREY=(200,200,200)

current_floor=1; message_log=[]; MAX_LOG_MESSAGES=5 # Start on floor 1 (index 0) or floor 2 (index 1)? Assuming 0-indexed, so 1 means second floor. Let's start on floor 0 for new game.
if not game_loaded_successfully: # If new game, start on floor 0
    current_floor = 0

in_shop_menu=False; shop_message=""
SHOP_INVENTORY=[
    {'id':'potion','name':'Health Potion','cost':15,'effect_type':'HEAL','amount':POTION_HEAL_AMOUNT},
    {'id':'super_potion','name':'Super Potion','cost':40,'effect_type':'HEAL','amount':SUPER_POTION_HEAL_AMOUNT},
    {'id':'key','name':'Key','cost':50,'effect_type':'ADD_KEY','amount':1},
    {'id':'atk_boost_small','name':'ATK Boost (+2)','cost':100,'effect_type':'ATK_BOOST','amount':2,'permanent':True},
    {'id':'def_boost_small','name':'DEF Boost (+1)','cost':80,'effect_type':'DEF_BOOST','amount':1,'permanent':True}
]
SHOP_UI_BACKGROUND_COLOR=(50,50,70)
player_surface=pygame.Surface((player["width"],player["height"])); player_surface.fill(RED)

def check_collision(player_rect, current_map_data, tile_size):
    for r in range(player_rect.top//tile_size, player_rect.bottom//tile_size + 1):
        for c in range(player_rect.left//tile_size, player_rect.right//tile_size + 1):
            if 0 <= r < len(current_map_data) and 0 <= c < len(current_map_data[0]):
                tile_val = current_map_data[r][c]
                if tile_val in [WALL_TILE_TYPE,DOOR_TILE,NPC_WISE_MAN_TILE,SHOPKEEPER_TILE]:  
                    if pygame.Rect(c*tile_size,r*tile_size,tile_size,tile_size).colliderect(player_rect): return True
    return False

def draw_map(screen, current_map_data, tile_size):
    for r_idx, row in enumerate(current_map_data):
        for c_idx, tile in enumerate(row):
            rect = pygame.Rect(c_idx*tile_size, r_idx*tile_size, tile_size, tile_size)
            if tile in [FLOOR_TILE_TYPE,KEY_TILE,POTION_TILE,SWORD_TILE,SHIELD_TILE,DOOR_TILE, 
                        STAIRS_UP_TILE,STAIRS_DOWN_TILE,SUPER_POTION_TILE,STEEL_SWORD_TILE, 
                        STEEL_SHIELD_TILE,NPC_WISE_MAN_TILE,SHOPKEEPER_TILE]:
                pygame.draw.rect(screen, FLOOR_COLOR, rect)
            if tile==WALL_TILE_TYPE: pygame.draw.rect(screen,WALL_COLOR,rect)
            elif tile==KEY_TILE: pygame.draw.rect(screen,KEY_COLOR,rect)
            elif tile==POTION_TILE: pygame.draw.rect(screen,POTION_COLOR,rect)
            elif tile==SWORD_TILE: pygame.draw.rect(screen,SWORD_COLOR,rect)
            elif tile==SHIELD_TILE: pygame.draw.rect(screen,SHIELD_COLOR,rect)
            elif tile==DOOR_TILE: pygame.draw.rect(screen,DOOR_COLOR,rect)
            elif tile==STAIRS_UP_TILE or tile==STAIRS_DOWN_TILE: pygame.draw.rect(screen,STAIRS_COLOR,rect)
            elif tile==SUPER_POTION_TILE: pygame.draw.rect(screen,SUPER_POTION_COLOR,rect)
            elif tile==STEEL_SWORD_TILE: pygame.draw.rect(screen,STEEL_SWORD_COLOR,rect)
            elif tile==STEEL_SHIELD_TILE: pygame.draw.rect(screen,STEEL_SHIELD_COLOR,rect)
            elif tile==NPC_WISE_MAN_TILE: pygame.draw.rect(screen,NPC_COLOR,rect)
            elif tile==SHOPKEEPER_TILE: pygame.draw.rect(screen,SHOP_COLOR,rect)

def draw_player_stats(screen, p_stats, font, pos, floor_num):
    texts=[f"Floor: {floor_num}",f"Level: {p_stats['level']}",f"XP: {p_stats['experience']}/{p_stats['xp_to_next_level']}",
             f"HP: {p_stats['hp']}/{p_stats['max_hp']}",f"ATK: {p_stats['atk']}",f"DEF: {p_stats['def']}",
             f"Keys: {p_stats['keys']}",f"Gold: {p_stats['gold']}"]
    for i,text in enumerate(texts): screen.blit(font.render(text,True,WHITE),(pos[0],pos[1]+i*(font.get_height()+5)))

def add_message(text): message_log.append(text); message_log[:]=message_log[-MAX_LOG_MESSAGES:]
def draw_message_log(screen,log,font,pos,color):
    for i,msg_text in enumerate(log): screen.blit(font.render(msg_text,True,color),(pos[0],pos[1]+i*(font.get_height()+3)))

def draw_enemies(screen,enemies_list,tile_size):
    for e in enemies_list: pygame.draw.rect(screen,e['color'],pygame.Rect(e['map_x']*tile_size+tile_size*0.1,e['map_y']*tile_size+tile_size*0.1,tile_size*0.8,tile_size*0.8))

def handle_combat(p,e):
    p_dmg=max(0,p['atk']-e['def']); e['hp']-=p_dmg; add_message(f"You hit {e['name']} for {p_dmg} damage.")
    if e['hp']>0: e_dmg=max(0,e['atk']-p['def']); p['hp']-=e_dmg; add_message(f"{e['name']} hits you for {e_dmg} damage.")
    else: add_message(f"Defeated {e['name']}.")
    return e

def check_level_up(p_obj):
    if p_obj['experience']>=p_obj['xp_to_next_level']:
        p_obj['level']+=1; p_obj['experience']-=p_obj['xp_to_next_level']; p_obj['xp_to_next_level']=int(p_obj['xp_to_next_level']*1.5)
        hp_b=20; atk_b=2; def_b=1
        p_obj['max_hp']+=hp_b; p_obj['atk']+=atk_b; p_obj['def']+=def_b; p_obj['hp']=p_obj['max_hp']
        add_message(f"Level Up! Level {p_obj['level']}."); add_message(f"MaxHP+{hp_b}, ATK+{atk_b}, DEF+{def_b}. Healed.")
        return True
    return False

def save_game():
    state={'player_data':player,'current_floor_index':current_floor,'all_floor_map_data':copy.deepcopy(all_floor_maps),
             'all_enemies_data':copy.deepcopy(all_enemies_on_floors),'message_log_data':list(message_log)}
    try:
        with open(SAVE_FILE,'w') as f: json.dump(state,f,indent=4); add_message("Game Saved.")
    except IOError: add_message("Error saving game.")

def load_game():
    global player,current_floor,all_floor_maps,all_enemies_on_floors,message_log, game_over, in_shop_menu, shop_message
    if not os.path.exists(SAVE_FILE): add_message("No save file found."); return False
    try:
        with open(SAVE_FILE,'r') as f: data=json.load(f)
        player.clear(); player.update(data['player_data']); current_floor=data['current_floor_index']
        all_floor_maps[:]=data['all_floor_map_data']; all_enemies_on_floors[:]=data['all_enemies_data']
        message_log[:]=data['message_log_data']
        player['x']=player['map_x']*TILE_SIZE+(TILE_SIZE-player['width'])//2; player['y']=player['map_y']*TILE_SIZE+(TILE_SIZE-player['height'])//2
        
        # Reset transient states that should not persist or might be problematic if loaded mid-state
        game_over = False 
        in_shop_menu = False
        shop_message = ""
        
        add_message("Game Loaded.")
        # It's important that current_map_data and current_enemies_list are updated after load
        # This will happen naturally at the start of the next game loop iteration.
        return True
    except(IOError,json.JSONDecodeError) as e: add_message(f"Error loading: {e}"); return False

game_loaded_successfully = load_game()
if not game_loaded_successfully: 
    add_message("Starting a new game.")
    current_floor = 0 # Ensure new games start on floor 0

running = True; game_over = False
if not game_loaded_successfully: game_over = False


# Main game loop
running = True
game_over = False 
if not game_loaded_successfully: 
    game_over = False
    current_floor = 0 

while running:
    current_map_data = all_floor_maps[current_floor]
    current_enemies_list = all_enemies_on_floors[current_floor]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_shop_menu:
            if event.type == pygame.KEYDOWN:
                item_index_to_buy = -1 
                if event.key == pygame.K_ESCAPE:
                    in_shop_menu = False
                    add_message("Exited shop.")
                    shop_message = "" 
                elif event.key == pygame.K_1: 
                    item_index_to_buy = 0
                elif event.key == pygame.K_2:
                    item_index_to_buy = 1
                elif event.key == pygame.K_3:
                    item_index_to_buy = 2
                elif event.key == pygame.K_4:
                    item_index_to_buy = 3
                elif event.key == pygame.K_5:
                    item_index_to_buy = 4

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
        
        else: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if not game_over: # Only save if not game over
                        save_game()
    
    if in_shop_menu:
        screen.fill(SHOP_UI_BACKGROUND_COLOR)
        title_font = pygame.font.Font(None, 48)
        title_surface = title_font.render("SHOP", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))
        gold_text = f"Your Gold: {player['gold']}"
        gold_surface = STATS_FONT.render(gold_text, True, WHITE)
        screen.blit(gold_surface, (50, 100))
        item_start_y = 150; line_height = MESSAGE_FONT.get_height() + 10
        for i, item in enumerate(SHOP_INVENTORY):
            item_text = f"{i+1}. {item['name']} - {item['cost']} Gold"
            item_surface = MESSAGE_FONT.render(item_text, True, WHITE)
            screen.blit(item_surface, (50, item_start_y + i * line_height))
        if shop_message:
            shop_msg_surface = MESSAGE_FONT.render(shop_message, True, WHITE)
            screen.blit(shop_msg_surface, (50, item_start_y + len(SHOP_INVENTORY) * line_height + 20))
        pygame.display.flip()
    
    elif game_over: 
        screen.fill(BLACK)
        draw_map(screen, current_map_data, TILE_SIZE)
        draw_enemies(screen, current_enemies_list, TILE_SIZE)
        screen.blit(player_surface, (player["x"], player["y"]))
        draw_player_stats(screen, player, STATS_FONT, (650, 20), current_floor + 1)
        draw_message_log(screen, message_log, MESSAGE_FONT, (650, 180), GREY)

        game_over_text_surface = GAME_OVER_FONT.render("Game Over", True, RED)
        text_rect = game_over_text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,128))
        screen.blit(overlay, (0,0))
        screen.blit(game_over_text_surface, text_rect)
        pygame.display.flip()

        # Game over sub-loop
        game_over_event_handled = False
        while game_over and not game_over_event_handled : # Loop until game_over is False (e.g. by closing window)
            for event_gm_over in pygame.event.get():
                if event_gm_over.type == pygame.QUIT:
                    running = False
                    game_over = False 
            pygame.time.wait(100) 
        if not running: continue 
            
    else: 
        screen.fill(BLACK)
        draw_map(screen, current_map_data, TILE_SIZE)
        draw_enemies(screen, current_enemies_list, TILE_SIZE)
        screen.blit(player_surface, (player["x"], player["y"]))
        draw_player_stats(screen, player, STATS_FONT, (650, 20), current_floor + 1)
        draw_message_log(screen, message_log, MESSAGE_FONT, (650, 180), GREY)
        pygame.display.flip() 

        action_taken_this_turn = False
        keys = pygame.key.get_pressed()
        # print(f"DEBUG: Keys - L:{keys[pygame.K_LEFT]}, R:{keys[pygame.K_RIGHT]}, U:{keys[pygame.K_UP]}, D:{keys[pygame.K_DOWN]}")
        
        original_x = player["x"]; original_y = player["y"]
        prospective_x = original_x; prospective_y = original_y
        if keys[pygame.K_LEFT]: prospective_x -= player["speed"]
        if keys[pygame.K_RIGHT]: prospective_x += player["speed"]
        if keys[pygame.K_UP]: prospective_y -= player["speed"]
        if keys[pygame.K_DOWN]: prospective_y += player["speed"]
        
        if prospective_x < 0:
            prospective_x = 0
        elif prospective_x > SCREEN_WIDTH - player["width"]:
            prospective_x = SCREEN_WIDTH - player["width"]
        
        if prospective_y < 0:
            prospective_y = 0
        elif prospective_y > SCREEN_HEIGHT - player["height"]:
            prospective_y = SCREEN_HEIGHT - player["height"]
        
        target_center_x=prospective_x+player["width"]/2; target_center_y=prospective_y+player["height"]/2
        target_map_col=int(target_center_x//TILE_SIZE); target_map_row=int(target_center_y//TILE_SIZE)
        # print(f"DEBUG: Original Pos (pixels): ({original_x}, {original_y}), Prospective Pos (pixels): ({prospective_x}, {prospective_y})")
        # print(f"DEBUG: Target Grid Cell: ({target_map_col}, {target_map_row})")

        player_is_moving_to_new_tile = (int(original_x//TILE_SIZE)!=target_map_col or int(original_y//TILE_SIZE)!=target_map_row)
        # print(f"DEBUG: Player attempting to move to new tile: {player_is_moving_to_new_tile}")

        if player_is_moving_to_new_tile and 0<=target_map_row<len(current_map_data) and 0<=target_map_col<len(current_map_data[0]):
            tile_type_at_target = current_map_data[target_map_row][target_map_col]
            # print(f"DEBUG: Checking Stairs Interaction. Tile at target: {tile_type_at_target}")

            if tile_type_at_target == STAIRS_UP_TILE:
                if current_floor==0 and (target_map_col,target_map_row)==F0_STAIRS_UP_POS:
                    current_floor=1; player['map_x'],player['map_y']=F1_STAIRS_DOWN_ARRIVAL_POS; action_taken_this_turn=True; add_message(f"Moved to Floor {current_floor+1}.")
                    current_map_data=all_floor_maps[current_floor]; current_enemies_list=all_enemies_on_floors[current_floor]
            elif tile_type_at_target == STAIRS_DOWN_TILE:
                if current_floor==1:
                    new_f_idx,new_p_coords = -1,(-1,-1)
                    if(target_map_col,target_map_row)==F1_STAIRS_DOWN_POS: new_f_idx=0; new_p_coords=F0_STAIRS_DOWN_ARRIVAL_POS
                    elif(target_map_col,target_map_row)==F1_STAIRS_DOWN_ARRIVAL_POS: new_f_idx=0; new_p_coords=(int(player_start_pixel_x//TILE_SIZE),int(player_start_pixel_y//TILE_SIZE))
                    if new_f_idx!=-1:
                        current_floor=new_f_idx; player['map_x'],player['map_y']=new_p_coords; action_taken_this_turn=True; add_message(f"Moved to Floor {current_floor+1}.")
                        current_map_data=all_floor_maps[current_floor]; current_enemies_list=all_enemies_on_floors[current_floor]
            
            if action_taken_this_turn and (tile_type_at_target == STAIRS_UP_TILE or tile_type_at_target == STAIRS_DOWN_TILE): # Pixel update only if stairs were taken
                player['x']=player['map_x']*TILE_SIZE+(TILE_SIZE-player['width'])//2; player['y']=player['map_y']*TILE_SIZE+(TILE_SIZE-player['height'])//2

            # print("DEBUG: Checking NPC/Shop Interaction (after stairs)")
            if not action_taken_this_turn: 
                if tile_type_at_target == NPC_WISE_MAN_TILE:
                    add_message(NPC_DIALOGUE.get(NPC_WISE_MAN_TILE,"The person stands silently.")); action_taken_this_turn=True
                elif tile_type_at_target == SHOPKEEPER_TILE:
                    in_shop_menu=True; shop_message="Welcome! Press number to buy, ESC to exit."; action_taken_this_turn=True
            
            # print("DEBUG: Checking Door Interaction (after stairs, NPC/Shop)")
            if not action_taken_this_turn: 
                if tile_type_at_target==DOOR_TILE:
                    if player["keys"]>0: player["keys"]-=1; current_map_data[target_map_row][target_map_col]=FLOOR_TILE_TYPE; add_message("Opened a door."); action_taken_this_turn=True
                    else: add_message("You need a key!"); action_taken_this_turn=True
        
        # print("DEBUG: Checking Combat Interaction")
        if not action_taken_this_turn and player_is_moving_to_new_tile: 
            enemy_to_fight,enemy_idx = None,-1
            for i,e in enumerate(current_enemies_list):
                if e['map_x']==target_map_col and e['map_y']==target_map_row: enemy_to_fight=e; enemy_idx=i; break
            if enemy_to_fight:
                updated_e = handle_combat(player,enemy_to_fight); current_enemies_list[enemy_idx]=updated_e
                if updated_e['hp']<=0:
                    if 'gold_drop' in updated_e: player['gold']+=updated_e['gold_drop']; add_message(f"Gained {updated_e['gold_drop']} gold from {updated_e['name']}.")
                    if 'xp_yield' in updated_e:
                        player['experience']+=updated_e['xp_yield']; add_message(f"Gained {updated_e['xp_yield']} XP from {updated_e['name']}.")
                        while check_level_up(player): pass
                    current_enemies_list.pop(enemy_idx)
                if player['hp']<=0: game_over=True; add_message("Game Over.")
                action_taken_this_turn=True
        
        # print(f"DEBUG: Entering final movement block. action_taken_this_turn: {action_taken_this_turn}")
        if not action_taken_this_turn:
            temp_rect = pygame.Rect(prospective_x,prospective_y,player["width"],player["height"])
            collision_res = check_collision(temp_rect,current_map_data,TILE_SIZE)
            # print(f"DEBUG: Collision check result for combined move: {collision_res}")
            if not collision_res:
                player["x"]=prospective_x; player["y"]=prospective_y; player["map_x"]=int(player["x"]//TILE_SIZE); player["map_y"]=int(player["y"]//TILE_SIZE)
                # print(f"DEBUG: Player Pos Updated To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")
            else:
                moved_x_only=False
                temp_rect_x=pygame.Rect(prospective_x,original_y,player["width"],player["height"])
                if original_x!=prospective_x:
                    col_x_res=check_collision(temp_rect_x,current_map_data,TILE_SIZE)
                    # print(f"DEBUG: Collision check result for X-only move: {col_x_res}")
                    if not col_x_res:
                        player["x"]=prospective_x; player["map_x"]=int(player["x"]//TILE_SIZE); player["map_y"]=int(original_y//TILE_SIZE); moved_x_only=True
                        # print(f"DEBUG: Player Pos Updated (X-SLIDE) To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")
                
                curr_x_slide=player["x"] if moved_x_only else original_x
                temp_rect_y=pygame.Rect(curr_x_slide,prospective_y,player["width"],player["height"])
                if original_y!=prospective_y:
                    col_y_res=check_collision(temp_rect_y,current_map_data,TILE_SIZE)
                    # print(f"DEBUG: Collision check result for Y-only move (from x={curr_x_slide}): {col_y_res}")
                    if not col_y_res:
                        player["y"]=prospective_y; player["map_y"]=int(player["y"]//TILE_SIZE); player["map_x"]=int(curr_x_slide//TILE_SIZE)
                        if not moved_x_only: player["x"]=original_x
                        # print(f"DEBUG: Player Pos Updated (Y-SLIDE) To: ({player['x']}, {player['y']}), Map Pos: ({player['map_x']}, {player['map_y']})")

        if player["map_x"]!=int(original_x//TILE_SIZE) or player["map_y"]!=int(original_y//TILE_SIZE) or action_taken_this_turn:
            map_col_item=player['map_x']; map_row_item=player['map_y']
            map_data_items=all_floor_maps[current_floor]
            if 0<=map_row_item<len(map_data_items) and 0<=map_col_item<len(map_data_items[0]):
                tile_under=map_data_items[map_row_item][map_col_item]
                if tile_under==KEY_TILE: player["keys"]+=1; map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message("Picked up a Key.")
                elif tile_under==POTION_TILE: player["hp"]=min(player["max_hp"],player["hp"]+POTION_HEAL_AMOUNT); map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up a Potion. +{POTION_HEAL_AMOUNT} HP.")
                elif tile_under==SWORD_TILE: player["atk"]+=SWORD_ATK_BOOST; map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up a Sword. +{SWORD_ATK_BOOST} ATK.")
                elif tile_under==SHIELD_TILE: player["def"]+=SHIELD_DEF_BOOST; map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up a Shield. +{SHIELD_DEF_BOOST} DEF.")
                elif tile_under==SUPER_POTION_TILE: player['hp']=min(player['max_hp'],player['hp']+SUPER_POTION_HEAL_AMOUNT); map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up Super Potion. +{SUPER_POTION_HEAL_AMOUNT} HP.")
                elif tile_under==STEEL_SWORD_TILE: player['atk']+=STEEL_SWORD_ATK_BOOST; map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up Steel Sword. +{STEEL_SWORD_ATK_BOOST} ATK.")
                elif tile_under==STEEL_SHIELD_TILE: player['def']+=STEEL_SHIELD_DEF_BOOST; map_data_items[map_row_item][map_col_item]=FLOOR_TILE_TYPE; add_message(f"Picked up Steel Shield. +{STEEL_SHIELD_DEF_BOOST} DEF.")
    else: 
        screen.fill(SHOP_UI_BACKGROUND_COLOR)
        title_font=pygame.font.Font(None,48); title_surf=title_font.render("SHOP",True,WHITE); screen.blit(title_surf,(SCREEN_WIDTH//2-title_surf.get_width()//2,30))
        gold_surf=STATS_FONT.render(f"Your Gold: {player['gold']}",True,WHITE); screen.blit(gold_surf,(50,100))
        item_y=150; line_h=MESSAGE_FONT.get_height()+10
        for i,item in enumerate(SHOP_INVENTORY):
            screen.blit(MESSAGE_FONT.render(f"{i+1}. {item['name']} - {item['cost']} Gold",True,WHITE),(50,item_y+i*line_h))
        if shop_message: screen.blit(MESSAGE_FONT.render(shop_message,True,WHITE),(50,item_y+len(SHOP_INVENTORY)*line_h+20))
        pygame.display.flip()

pygame.quit()
