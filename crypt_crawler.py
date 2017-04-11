import random
import json
import traceback
import pygame
import sys
import os
from pygame.locals import *

map_list = []

pygame.mixer.pre_init(96000, 16, 2, 4096)
pygame.init()

screen = pygame.display.set_mode((300,300))

def new_map(size):    
    """Create a matrix (2 dimensional list) 'X' characters.

    :param size: Integer dictates size of the matrix.
    """
    
    map_list.clear()
    
    for num in range(size):
        map_list.append([["X"] for num in range(size)])


def json_loader():
    """Open and load a json object.

    :returns map_file: A json object containing various game settings.
    """
    
    map_file = open("doc/map_file.json", "r")
    map_file = json.load(map_file)
    
    return map_file


def map_begin(size):
    """Modify middle items of the map_list matrix.

    :param size: Integer used to determine center of the matrix.
    """
    
    mid = size // 2
    
    map_list[mid - 2][mid - 2] = ["X."]
    map_list[mid - 2][mid - 1] = ["X."]
    map_list[mid - 2][mid] = ["X."]
    
    map_list[mid - 1][mid - 2] = ["X."]
    map_list[mid - 1][mid - 1] = ["SU", "@"]
    map_list[mid - 1][mid] = ["X."]
    
    map_list[mid][mid - 2] = ["X."]
    map_list[mid][mid - 1] = ["X."]
    map_list[mid][mid] = ["X."]


def space_finder(map_list):
    """Create a list of cartesian cordinates from a matrix.

    :param map_list: Matrix.
    :returns free_space: List containing cartesian cordinates in the
    form [x, y].
    """
    
    free_space = []
    
    for num in range(len(map_list)):
        row = map_list[num]
        carry = num
        
        for num in range(len(map_list[carry])):
            if row[num] == ["X."]:
                free_space.append([carry, num])
                
    return free_space


def space_selector(free_space):
    """Make random selection of cordinates

    :param free_space: List containing cartesian cordinates in the
    form [x, y].
    :returns selection[0], selection[1]: Randomly chosen x and y cordinates.
    """
    
    selection = random.choice(free_space)
    
    return selection[0], selection[1]


def quest_features(map_list):
    """Add progress essential game items to a matrix.
    
    :param map_list: matrix to be operated on.
    """
    
    map_file = open("doc/map_file.json", "r")
    map_file = json.load(map_file)
    
    quest_features = list(map_file["map_obj"][3]["quest_features"])
    
    for feature in quest_features:
        candidate = []
        
        for row in range(len(map_list)):
            for col in range(len(map_list[row])):
                if map_list[row][col] == [feature["replaces"]]:
                    candidate.append([row, col])
                    
        for item in range(int(feature["balance"])):
            choice = random.choice(candidate)
            map_list[choice[0]][choice[1]] = [feature["symbol"]]


def enemy_start(map_list, map_file, level):
    """Initialize enemy data, place enemy symbols in matrix.

    :param map_list: Matrix to be operated on.
    :param level: Integer determines the dificulty of enemies.
    :returns chara_data: Dictionary containing enemy data.
    """
    
    enemy_data = []
    enemy_obj = map_file["map_obj"][5]["enemies"]
    enemy_codes = []
    
    tile_ids = []
    
    for enemy in enemy_obj:
        if level >= enemy["level"]:
            for i in range(enemy["rarity"]):
                enemy_codes.append(enemy["code"])
                
    for row in range(len(map_list)):
        for col in range(len(map_list[row])):
            tile = map_list[row][col]
            
            for item in tile:
                if "e" in item and "we" not in item:
                    tile_id = str(random.randint(1, 9999))
                    tile_ids.append([tile_id, row, col])
                    
    for ids in tile_ids:
        map_list[ids[1]][ids[2]] = [ids[0]]
        random_code = random.choice(enemy_codes)
        
        for enemy in enemy_obj:
            if random_code == enemy["code"]:
                enemy_data.append
                (
                    {
                    "id" : ids[0],
                    "pos_x" : ids[1],
                    "pos_y" : ids[2],
                    "code" : random_code,
                    "health" : enemy["health"],
                    "attack" : enemy["attack"],
                    "name" : enemy["name"],
                    "alive" : True,
                    "removed" : False
                    }
                    )
                
    return enemy_data
            

def chara_start(map_list):
    """Initialize character data, place character symbol in matrix.

    :param map_list: Matrix to be operated on.
    :returns chara_data: Dictionary containing character data.
    """
    
    chara_data = {}
    
    for row in range(len(map_list)):
        for col in range(len(map_list[row])):
            if "@" in map_list[row][col]:
                chara_data["pos_x"] = row
                chara_data["pos_y"] = col
                
    chara_data["level"] = 1
    chara_data["armour"] = [0, 0]
    chara_data["attack"] = 5
    chara_data["hp"] = 100
    chara_data["range"] = 2
    chara_data["we_code"] = "000"
    chara_data["ar_code"] = "000"
    
    return chara_data


def death():
    """Give user option to restart the game"""
    
    question = True
    
    while question:
        choice = input("You have died \nWould you like to continue?(y/n) ")
        
        if choice == "n":
            sys.exit()
            question = False
            
        elif choice == "y":
            generate(None, None, map_list, json_loader(), 1)
            question = False
            
        else:
            print("Selection not recognized")


def details(map_list, map_file, rolls=100):
    """Add environmental details to the matrix at random.

    :param map_list: Matrix to be operated on.
    :param map_file: Json object containing information on environmental
    details.
    :param rolls: Integer that determines the abundace of details.
    """
    
    amounts = {}
    
    details = list(map_file["map_obj"][2]["details"])
    
    for detail in details:
        for num in range(rolls):
            if random.random() < detail["rarity"]:
                if detail["name"] in amounts:
                    amounts[detail["name"]] += 1
                else:
                    amounts[detail["name"]] = 1
                    
        free_space = []
        
        for row in range(len(map_list)):        
            for col in range(len(map_list[row])):
                if map_list[row][col] == ["."]:
                    free_space.append([row, col])
                    
        if detail["name"] in amounts:
            for num in range(amounts[detail["name"]]):
                tile = random.choice(free_space)
                map_list[tile[0]][tile[1]] = [detail["symbol"]]


def populate(map_list, level, map_file):
    """Add things (items, enemies, weapons and armour) to the matrix.

    :param map_list: Matrix to be operated on.
    :param level: Integer determines quality of added things.
    :param map_file: Json object containing information on things.
    """
    
    json_objects = [["ixxx", (map_file["map_obj"][4]["items"]), [] ],
                    ["exxx", (map_file["map_obj"][5]["enemies"]), [] ],
                    ["wexxx", (map_file["map_obj"][6]["weapons"]), [] ],
                    ["arxxx", (map_file["map_obj"][7]["armour"]), [] ]]
    
    for index in range(len(json_objects)):
        choice_pool = []
        
        for sub_object in json_objects[index][1]:
            if level >= sub_object["level"]:
                for num in range(sub_object["rarity"]):
                    choice_pool.append(sub_object["code"])
                    
        free_tiles = []
                
        for row in range(len(map_list)):
            for col in range(len(map_list[row])):
                if map_list[row][col] == [json_objects[index][0]]:
                    new_string = random.choice(choice_pool)
                    map_list[row][col][0] = map_list[row][col][0].replace("xxx", new_string)


def text_map_format(map_list):
    """Format matrix, clear screen and diplay as grid.

    :param map_list: Matrix to be formated.
    """
    
    map_str = ""
    
    for col in range(len(map_list)):
        for row in range(len(map_list[col])):
            map_str += (map_list[col][row][-1][-1] + " ")
            if row == len(map_list[col]) - 1:
                map_str += "\n"
                
    if os.name == "nt":
        os.system('cls')
    else:
        print("\033c")
        
    print(map_str)


def damage(chara_data, enemy_data, map_list):
    """Check for enemies in range after atack, deal damage

    :param chara_data: Object containing information about the character.
    :param enemy_data: Object containing infromation about the enemies.
    :param map_list: Matrix to be searched.
    """
    
    in_range = (
                map_list[chara_data["pos_x"]][chara_data["pos_y"]],
                map_list[chara_data["pos_x"] - 1][chara_data["pos_y"] - 1],
                map_list[chara_data["pos_x"]][chara_data["pos_y"] - 1],
                map_list[chara_data["pos_x"] + 1][chara_data["pos_y"] - 1], 
                map_list[chara_data["pos_x"] - 1][chara_data["pos_y"]],
                map_list[chara_data["pos_x"] + 1][chara_data["pos_y"]],
                map_list[chara_data["pos_x"] - 1][chara_data["pos_y"] + 1],
                map_list[chara_data["pos_x"]][chara_data["pos_y"] + 1],
                map_list[chara_data["pos_x"] + 1][chara_data["pos_y"] + 1]
                )
    
    enemies = []
    
    for tile in in_range:
        for item in tile:
            if item.isdigit():
                for enemy in enemy_data:
                    if enemy["id"] == item:
                        damage = (chara_data["attack"] // random.randint(1, 3))
                        enemy["health"] = enemy["health"] - damage
                        
                        print("You dealt", damage, "to", enemy["name"],
                             enemy["health"], "remaining")
    

def act(chara_data, enemy_data, map_list):
    """Execute enemy actions including attacking, dieing and moving,
    play sounds related to those actions,
    update the matrix with new position information.

    :param chara_data: Object containing information about the character.
    :param enemy_data: Object containing information about the ememies.
    :param map_list: Matrix to be operated on and searched through
    """
    
    move = False
    
    for enemy in enemy_data:
        if enemy["health"] <= 0:
            enemy["alive"] = False
            
        if enemy["alive"] == False and enemy["removed"] == False:
            enemy["removed"] = True
            
            pos = map_list[enemy["pos_x"]][enemy["pos_y"]]
            pos.pop(pos.index(enemy["id"]))
            pos.append(".")
            
            death_sounds = (
                "sound/effects/monsters/monster-1.ogg",
                "sound/effects/monsters/monster-2.ogg",
                "sound/effects/monsters/monster-3.ogg",
                "sound/effects/monsters/monster-4.ogg",
                "sound/effects/monsters/monster-5.ogg"
                )
                
            death_sound = random.choice(death_sounds)
            death = pygame.mixer.Sound(death_sound)
            death.play()
        
        in_range = (map_list[enemy["pos_x"]][enemy["pos_y"]],
                    map_list[enemy["pos_x"] - 1][enemy["pos_y"] - 1],
                    map_list[enemy["pos_x"]][enemy["pos_y"] - 1],
                    map_list[enemy["pos_x"] + 1][enemy["pos_y"] - 1],
                    map_list[enemy["pos_x"] - 1][enemy["pos_y"]],
                    map_list[enemy["pos_x"] + 1][enemy["pos_y"]],
                    map_list[enemy["pos_x"] - 1][enemy["pos_y"] + 1],
                    map_list[enemy["pos_x"]][enemy["pos_y"] + 1],
                    map_list[enemy["pos_x"] + 1][enemy["pos_y"] + 1])
        
        if enemy["alive"] == True:            
            for position in in_range:
                if "@" in position:
                    damage = (enemy["attack"] // (3 + chara_data["armour"][0]))
                    chara_data["hp"] -= damage
                    
                    attack_sounds = (
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-2.ogg",
                        "sound/effects/monsters/monster-3.ogg",
                        "sound/effects/monsters/monster-4.ogg",
                        "sound/effects/monsters/monster-5.ogg",
                        "sound/effects/monsters/monster-6.ogg",
                        "sound/effects/monsters/monster-7.ogg",
                        "sound/effects/monsters/monster-8.ogg",
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-1.ogg",
                        "sound/effects/monsters/monster-1.ogg"
                        )
                        
                    attack_sound = random.choice(attack_sounds)
                    attack = pygame.mixer.Sound(attack_sound)
                    attack.play()
                    
                    print("player was dealt:", damage, "points of damage by:",
                          enemy["name"])
                    
                else:
                    move = True

            if move:
                moves = ((map_list[enemy["pos_x"]][enemy["pos_y"] - 1], "pos_y", -1),
                         (map_list[enemy["pos_x"] - 1][enemy["pos_y"]], "pos_x", -1),
                         (map_list[enemy["pos_x"] + 1][enemy["pos_y"]], "pos_x",  1),
                         (map_list[enemy["pos_x"]][enemy["pos_y"] + 1], "pos_y",  1))

                viable_moves = []
                
                for move in moves:
                    if move[0][-1] == ".":
                        viable_moves.append(move)

                if viable_moves:
                    move_choice = random.choice(viable_moves)
                        
                    pos = map_list[enemy["pos_x"]][enemy["pos_y"]]
                    pos.pop(pos.index(enemy["id"]))
                    pos.append(".")
                    enemy[move_choice[1]] += move_choice[2]
                    pos = map_list[enemy["pos_x"]][enemy["pos_y"]]
                    pos.append(enemy["id"])


def chara_move(chara_data, key, map_list):
    """Update character position upon input and play coresponding sounds

    :param chara_data: Object containing information about the character.
    :param key: String coresponding to the key user pressed. 
    :param map_list: Matrix to be operated on and searched through.
    :except IndexError: Prevent user going beyond the matrix  
    """
    
    pos = map_list[chara_data["pos_x"]][chara_data["pos_y"]]
    pos.pop(pos.index("@"))
    
    try:
        if key == "w":
            if map_list[(chara_data["pos_x"] - 1)][chara_data["pos_y"]] != ["X"]:
                chara_data["pos_x"] -= 1
                
        elif key == "a":
            if map_list[chara_data["pos_x"]][(chara_data["pos_y"] - 1)] != ["X"]:
                chara_data["pos_y"] -= 1
                
        elif key == "s":
            if map_list[(chara_data["pos_x"] + 1)][chara_data["pos_y"]] != ["X"]:
                chara_data["pos_x"] += 1
                
        elif key == "d":
            if map_list[chara_data["pos_x"]][(chara_data["pos_y"] + 1)] != ["X"]:
                chara_data["pos_y"] += 1
                
        elif key == "wd" or key == "dw":
            if map_list[(chara_data["pos_x"] - 1)][chara_data["pos_y"] + 1] != ["X"]:
                chara_data["pos_x"] -= 1
                chara_data["pos_y"] += 1
                
        elif key == "wa" or key == "aw":
            if map_list[(chara_data["pos_x"] - 1)][chara_data["pos_y"] - 1] != ["X"]:
                chara_data["pos_x"] -= 1
                chara_data["pos_y"] -= 1
                
        elif key == "as" or key == "sa":
            if map_list[(chara_data["pos_x"] + 1)][chara_data["pos_y"] - 1] != ["X"]:
                chara_data["pos_x"] += 1
                chara_data["pos_y"] -= 1
                
        elif key == "sd" or key == "ds":
            if map_list[(chara_data["pos_x"] + 1)][chara_data["pos_y"] + 1] != ["X"]:
                chara_data["pos_x"] += 1
                chara_data["pos_y"] += 1

        else:
            print("Invalid Command")
                
    except IndexError:
        print("Out of bounds")
        
    footsteps = (
        "sound/effects/character/footstep04.ogg",
        "sound/effects/character/footstep05.ogg",
        "sound/effects/character/footstep06.ogg",
        "sound/effects/character/footstep09.ogg"
        )
    
    step = random.choice(footsteps)
    step_sound = pygame.mixer.Sound(step)
    step_sound.play()
    
    pos = map_list[chara_data["pos_x"]][chara_data["pos_y"]]
    pos.append("@")


def pick_up(item, chara_data, map_list, map_file):
    """Update character data to reflect newly aquired things

    :param item: String containing the item code.
    :param chara_data: Object containing information about the character.
    :param map_list: Matrix to be operated on.
    :param map_file: Object containing information about things the game.
    """
    
    code_value = item[-3:]
    
    pos = map_list[chara_data["pos_x"]][chara_data["pos_y"]]
    
    if "i" in item:
        item_obj = map_file["map_obj"][4]["items"]
        for item_type in item_obj:
            if code_value == item_type["code"]:
                chara_data["hp"] += item_type["effect"]
                print("You now have", chara_data["hp"], "HP")
                pos.pop(pos.index(item))
                pos.insert(0, ".")
                print("You picked up a", item_type["name"])
                
    if "w" in item:
        weapon_obj = map_file["map_obj"][6]["weapons"]
        for weapon in weapon_obj:
            if code_value == weapon["code"]:
                if weapon["code"] > chara_data["we_code"]:
                    chara_data["we_code"] = weapon["code"]
                    chara_data["attack"] = weapon["attack"]
                    pos.pop(pos.index(item))
                    pos.insert(0, ".")
                    print("You now weild a", weapon["name"])
                    
                elif weapon["code"] == chara_data["we_code"]:
                    print("You already weild a", weapon["name"])
                    
                else:
                    print(weapon["name"], "is worse than your weapon")

    if "a" in item:
        armour_obj = map_file["map_obj"][7]["armour"]
        for armour in armour_obj:
            if code_value == armour["code"]:
                if armour["code"] > chara_data["ar_code"]:
                    chara_data["ar_code"] = armour["code"]
                    chara_data["armour"] = armour["protection"]
                    pos.pop(pos.index(item))
                    pos.insert(0, ".")
                    print("You put on", armour["name"])
                    
                elif armour["code"] == chara_data["we_code"]:
                    print("You are already wearing", armour["name"])
                    
                else:
                    print(armour["name"], "is worse than your armour")


def input_loop(chara_data, enemy_data, map_list, map_file):
    """Handle interface, handle input, play sounds.

    :param chara_data: Object containing information about the character.
    :param enemy_data: Object containing information about the character.
    :param map_list: Matrix to be operated on.
    :param map_file: Object containing information about things the game.
    :returns chara_data, enemy_data, map_list, map_file, level: All the
    information needed to start a new level.
    """
    
    level = 1
    game_over = False
        
    while not game_over:
        for event in pygame.event.get():
            mods = pygame.key.get_mods()
            pos = map_list[chara_data["pos_x"]][chara_data["pos_y"]]
            if event.type == pygame.QUIT:
                sys.exit()
                
            if chara_data["hp"] <= 0:
                death_sound = pygame.mixer.Sound("sound/effects/game/magic1.ogg")
                death_sound.play()
                death()
                
            if "SD" in map_list[chara_data["pos_x"]][chara_data["pos_y"]]:
                level += 1
                mid = ((len(map_list)) // 2) - 1
                chara_data["pos_x"] = mid
                chara_data["pos_y"] = mid
                return chara_data, enemy_data, map_list, map_file, level
                
            for item in map_list[chara_data["pos_x"]][chara_data["pos_y"]]:
                if "i" in item or "we" in item or "ar" in item:
                    pick_up(item, chara_data, map_list, map_file)
                    
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    sys.exit()
                    
                elif event.key == pygame.K_r:
                    generate(1)
                    
                elif event.key == pygame.K_SPACE:
                    damage(chara_data, enemy_data, map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                    swings = (
                        "sound/effects/character/swing.ogg",
                        "sound/effects/character/swing2.ogg",
                        "sound/effects/character/swing3.ogg"
                        )
        
                    swing = random.choice(swings)
                    swing_sound = pygame.mixer.Sound(swing)
                    swing_sound.play()

                elif event.key == pygame.K_e:
                    command = input("Enter special command: ")
                    
                    chara_move(chara_data, command, map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                elif event.key == pygame.K_w:
                    chara_move(chara_data, "w", map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                elif event.key == pygame.K_a:
                    chara_move(chara_data, "a", map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                elif event.key == pygame.K_s:
                    chara_move(chara_data, "s", map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                elif event.key == pygame.K_d:
                    chara_move(chara_data, "d", map_list)
                    act(chara_data, enemy_data, map_list)
                    text_map_format(map_list)
                    
                print("Health:", chara_data["hp"],
                     "Attack:", chara_data["attack"],
                     "Armour:", chara_data["armour"][0])        


def generate(chara_data, enemy_data, map_list, map_file, level, debug=False):
    """Begins music and randomly generates map.

    :param chara_data: Object containing information about the character.
    :param enemy_data: Object containing information about the character.
    :param map_list: Matrix to be operated on.
    :param map_file: Object, contains information about things the game.
    :param level: Integer, represents the current level of the game.
    :param debug: Boolean, set to true if debug mode is active.
    """
    
    pygame.mixer.stop()
    
    soundtrack_tuple = (
        "sound/music/tomo.ogg",
        "sound/music/industrial_lullaby.ogg",
        "sound/music/The Old Mill.ogg",
        "sound/music/consent.ogg",
        "sound/music/basement.ogg"
        )
    
    chosen_track = random.choice(soundtrack_tuple)
    
    soundtrack = pygame.mixer.Sound(chosen_track)
    soundtrack.play()
    
    new_map(64)
    map_begin(64)
    
    for i in range(100):
        map_try(*space_selector(space_finder(map_list)), json_loader())
        
    quest_features(map_list)
    details(map_list, json_loader())
    populate(map_list, level, json_loader())
    text_map_format(map_list)

    if level == 1 or debug == True:
        next_input = input_loop(chara_start(map_list),
                                enemy_start(map_list, json_loader(), level),
                                map_list, json_loader())
        generate(*next_input)
        debug = False

    else:
        next_input = input_loop(chara_data,
                                enemy_start(map_list, json_loader(), level),
                                map_list, json_loader())
        generate(*next_input)


def map_try(cart_x, cart_y, map_file):
    """Test to see if a room can be created at a certain point

    :param cart_x: Integer, the x cordinate of the test point
    :param cart_y: Integer, the y cordinate of the test point
    :param map_file: Matrix, map to be operated on
    """
    free_coordinates = []
    
    features = list(map_file["map_obj"][0]["features"])
    new_feature = random.choice(features)
    
    sizex = new_feature["sizex"]
    sizey = new_feature["sizey"]
    
    free_coordinates.append(uptry(cart_x, cart_y, sizex, sizey, map_list))
    free_coordinates.append(downtry(cart_x, cart_y, sizex, sizey, map_list))
    free_coordinates.append(lefttry(cart_x, cart_y, sizex, sizey, map_list))
    free_coordinates.append(righttry(cart_x, cart_y, sizex, sizey, map_list))
    free_coordinates = [x for x in free_coordinates if x != False]
    
    if free_coordinates:
        chosen_coordinates = random.choice(free_coordinates)
        
    else:
        return False
    
    doorway = map_file["map_obj"][1]["joins"]
    
    map_list[cart_x][cart_y] = [random.choice(doorway)["symbol"]]
    
    for item in chosen_coordinates:
        if len(item) == 3:
            map_list[item[0]][item[1]] = ["X."]
            
        else:
            map_list[item[0]][item[1]] = ["."]
            

def uptry(cart_x, cart_y, sizex, sizey, map_list, tile_type=[["X"],["X."]]):
    """Test to see if a room or passageway will fit upward from a
    certain position.

    :param cart_x: Integer, x position of the test point.
    :param cart_y: Integer, y position of the test point.
    :param sizex: Integer, height of the room.
    :param sizey: Integer, width of the room.
    :param map_list: Matrix, the game map.
    :param tile_type: List, conditions required for new room generation
    """
    
    free_coordinates = []
    
    for num in range(1, sizex + 1):
        carry = num
        for num in range(1, sizey + 1):
            try:
                if map_list[cart_x - carry][cart_y + num] == tile_type[0]:
                    if cart_x - carry >= 1 and cart_y + num >= 1:
                        if carry == sizex or num == sizey:
                            free_coordinates.append([cart_x - carry,
                                                     cart_y + num,
                                                     tile_type[1]])
                            
                        else:
                            free_coordinates.append([cart_x - carry,
                                                     cart_y + num])
                            
                    else:
                        return False

                else:
                    return False
                
            except IndexError:
                return False
            
    return free_coordinates


def downtry(cart_x, cart_y, sizex, sizey, map_list, tile_type=[["X"],["X."]]):
    """Test to see if a room or passageway will fit downward from a
    certain position.

    :param cart_x: Integer, x position of the test point.
    :param cart_y: Integer, y position of the test point.
    :param sizex: Integer, height of the room.
    :param sizey: Integer, width of the room.
    :param map_list: Matrix, the game map.
    :param tile_type: List, conditions required for new room generation
    """

    free_coordinates = []
    
    for num in range(1, sizex + 1):
        carry = num
        for num in range(1, sizey + 1):
            try:
                if map_list[cart_x + carry][cart_y - num] == tile_type[0]:
                    if cart_x + carry >= 1 and cart_y - num >= 1:
                        if carry == sizex or num == sizey:
                            free_coordinates.append([cart_x + carry,
                                                     cart_y - num,
                                                     tile_type[1]])
                            
                        else:
                            free_coordinates.append([cart_x + carry,
                                                     cart_y - num])
                            
                    else:
                        return False
                    
                else:
                    return False
                
            except IndexError:
                return False
            
    return free_coordinates


def lefttry(cart_x, cart_y, sizex, sizey, map_list, tile_type=[["X"],["X."]]):
    """Test to see if a room or passageway will fit to the left of a
    certain position.

    :param cart_x: Integer, x position of the test point.
    :param cart_y: Integer, y position of the test point.
    :param sizex: Integer, height of the room.
    :param sizey: Integer, width of the room.
    :param map_list: Matrix, the game map.
    :param tile_type: List, conditions required for new room generation
    """

    free_coordinates = []
    
    for num in range(1, sizex + 1):
        carry = num
        for num in range(1, sizey + 1):
            try:
                if map_list[cart_x - carry][cart_y - num] == tile_type[0]:
                    if cart_x - carry >= 1 and cart_y - num >= 1:
                        if carry == sizex or num == sizey:
                            free_coordinates.append([cart_x - carry,
                                                     cart_y - num,
                                                     tile_type[1]])
                            
                        else:
                            free_coordinates.append([cart_x - carry,
                                                     cart_y - num])
                            
                    else:
                        return False
                    
                else:
                    return False
                
            except IndexError:
                return False
            
    return free_coordinates


def righttry(cart_x, cart_y, sizex, sizey, map_list, tile_type=[["X"],["X."]]):
    """Test to see if a room or passageway will fit to the right of a
    certain position.

    :param cart_x: Integer, x position of the test point.
    :param cart_y: Integer, y position of the test point.
    :param sizex: Integer, height of the room.
    :param sizey: Integer, width of the room.
    :param map_list: Matrix, the game map.
    :param tile_type: List, conditions required for new room generation
    """

    free_coordinates = []
    
    for num in range(1, sizex + 1):
        carry = num
        for num in range(1, sizey + 1):
            try:
                if map_list[cart_x + carry][cart_y + num] == tile_type[0]:
                    if cart_x + carry >= 1 and cart_y + num >= 1:
                        if carry == sizex or num == sizey:
                            free_coordinates.append([cart_x + carry,
                                                     cart_y + num,
                                                     tile_type[1]])
                            
                        else:
                            free_coordinates.append([cart_x + carry,
                                                     cart_y + num])
                            
                    else:
                        return False
                    
                else:
                    return False
                
            except IndexError:
                return False
            
    return free_coordinates


def main():
    pass


if __name__ == "__main__":
    generate(None, None, map_list, json_loader(), 1, False)
