from random import randint, choice


def _check_tile(y: int, x: int, sea_map: list[list]):
    # check the tile and its adjacent tiles
    check = sea_map[y][x] + sea_map[y - 1][x] + sea_map[y + 1][x] + sea_map[y][x - 1] + sea_map[y][x + 1] + \
            sea_map[y - 1][x - 1] + sea_map[y - 1][x + 1] + sea_map[y + 1][x - 1] + sea_map[y + 1][x + 1]
    return check


def check_ship(length: int, orient: list, head_y: int, head_x: int, map: list[list]):
    # check if the tile isn't already occupied
    if not _check_tile(head_y, head_x, map):
        check = True
        # check if the ship will fit in the map
        tail_y = head_y + orient[0] * (length - 1)
        tail_x = head_x + orient[1] * (length - 1)
        if tail_y < 1 or tail_y > 8 or tail_x < 1 or tail_x > 8:
            check = False
        else:
            # check that the ships won't hit one another
            for deck in range(1, length):
                head_check_y = head_y
                head_check_x = head_x
                head_check_y += orient[0]
                head_check_x += orient[1]
                if _check_tile(head_check_y, head_check_x, map):
                    check = False
            return check


def create_AI_map():
    # create an empty game map
    sea_map = [[0] * 10 for i in range(10)]

    list_of_ships = [3, 3, 2, 2, 1, 1, 1]
    ships_in_game = {}
    orientation_dict = {1: [-1, 0], 2: [0, 1], 3: [1, 0], 4: [1, 0]}
    count = 1
    for length in list_of_ships:
        # choose the tile for the ship head
        check = False
        while not check:
            head_y, head_x = randint(1, 8), randint(1, 8)
            # choose orientation
            orientation = randint(1, 4)
            orient = orientation_dict[orientation]
            # if the ship of this length, head position and orientation fits, place it:
            if check_ship(length, orient, head_y, head_x, sea_map):
                check = True
                # add the ship and its coords to the dict of ships placed on map:
                ship_name = f'{length}_{count}'
                ships_in_game[ship_name] = []
                ships_in_game[ship_name].append([head_y, head_x])
                sea_map[head_y][head_x] = 1
                for deck in range(1, length):
                    head_y += orient[0]
                    head_x += orient[1]
                    sea_map[head_y][head_x] = 1
                    ships_in_game[ship_name].append([head_y, head_x])
        count += 1

    for i in range(3):
        poi = randint(2, 8)
        check_poi = False
        while not check_poi:
            poi_x, poi_y = randint(1, 8), randint(1, 8)
            if not _check_tile(poi_y, poi_x, sea_map):
                check_poi = True
                sea_map[poi_y][poi_x] = poi

    return (sea_map, ships_in_game)


def player_map():
    # create an empty game map
    return [[0] * 10 for i in range(10)]


def player_ship_placement(player_ships: dict, player_map: list[list]):
    ships_count = 7
    # check each tile of player map with ships placed
    for y in range(1, 9):
        for x in range(1, 9):
            # once a tile with ship found:
            if player_map[y][x] == 1:
                n = player_map[y - 1][x]
                e = player_map[y][x + 1]
                s = player_map[y + 1][x]
                w = player_map[y][x - 1]
                ne = player_map[y - 1][x + 1]
                se = player_map[y + 1][x + 1]
                sw = player_map[y + 1][x - 1]
                nw = player_map[y - 1][x - 1]
                # if 2 or more adjacent tiles are occupied,
                # it can be valid if they are all in vertical or horizontal line
                if _check_tile(y, x, player_map) > 2:
                    if (ne + se + sw + nw) > 0:
                        return ("diagonal placement", player_ships)

                    elif (n + s) > 1:
                        # find, which ship already placed is near the tile
                        check = False
                        for ship in player_ships:
                            # check that it is not already too long
                            if [y - 1, x] in player_ships[ship] and len(player_ships[ship]) < 2:
                                # if it isn't too long, add the tile to the ship
                                player_ships[ship].append([y, x])
                                check = True
                        if not check:
                            return ("ship too long", player_ships)
                    elif (e + w) > 1:
                        check = False
                        for ship in player_ships:
                            if [y, x - 1] in player_ships[ship] and len(player_ships[ship]) < 2:
                                player_ships[ship].append([y, x])
                                check = True
                        if not check:
                            return ("ship too long", player_ships)
                # if only one adjacent tile is occupied
                # it can be valid if it is not in diagonal
                elif _check_tile(y, x, player_map) == 2:
                    if (ne + se + sw + nw) > 0:
                        return ("diagonal placement", player_ships)
                    else:
                        # if the tile occupied is up or left to the current tile,
                        # it must be already in the dictionary of ships
                        if n == 1:
                            check = False
                            for ship in player_ships:
                                if [y - 1, x] in player_ships[ship] and len(player_ships[ship]) < 3:
                                    player_ships[ship].append([y, x])
                                    check = True
                            if not check:
                                return ("ship too long", player_ships)
                        elif w == 1:
                            check = False
                            for ship in player_ships:
                                if [y, x - 1] in player_ships[ship] and len(player_ships[ship]) < 3:
                                    player_ships[ship].append([y, x])
                                    check = True
                            if not check:
                                return ("ship too long", player_ships)
                        # if the tile occupied is down or right to the current tile,
                        # then the current tile is first to be added to the dictionary of ships
                        else:
                            ship_name = str(y) + str(x)
                            player_ships[ship_name] = []
                            player_ships[ship_name].append([y, x])
                # if there are no tiles occupied nearby,
                # the current tile is the one-tile ship
                else:
                    ship_name = str(y) + str(x)
                    player_ships[ship_name] = []
                    player_ships[ship_name].append([y, x])
    if len(player_ships) != ships_count:
        return ("wrong placement", player_ships)
    else:
        return ("placement confirmed", player_ships)


# find out, which ship was shot
def _get_ship_shot(ships, x, y):
    for ship in ships:
        if [y, x] in ships[ship]:
            return ship


def _check_ship_killed(ship, hits):
    check = True
    if len(ship) > 1:
        for deck in ship:
            if deck not in hits:
                check = False
    return check


def shot_result(sea_map, ships, hits, x, y):
    # if the shot hits any ship:
    if sea_map[y][x] == 1:
        hits.append([y, x])
        ship_shot = _get_ship_shot(ships, x, y)
        if _check_ship_killed(ships[ship_shot], hits):
            return "killed"
        else:
            return "hit"
    elif sea_map[y][x] == 0:
        return "miss"
    else:
        return ("mermaid", "squid", "fish", "dragon", "boat",
                "island", "volcano")[sea_map[y][x] - 2]


def get_AI_tiles_for_shot():
    AI_tiles_for_shot = []
    for y in range(1, 9):
        for x in range(1, 9):
            AI_tiles_for_shot.append([y, x])
    return AI_tiles_for_shot


def enemy_shot_result(player_map, player_ships, enemy_hits, x, y):
    # if the shot hits any ship:
    if player_map[y][x] == 1:
        enemy_hits.append([y, x])
        ship_shot = _get_ship_shot(player_ships, x, y)
        if _check_ship_killed(player_ships[ship_shot], enemy_hits):
            return "killed_player"
        else:
            return "hit_player"
    elif player_map[y][x] == 0:
        return "miss_player"


def AI_shot(AI_tiles_for_shot: list, AI_hits: list, player_map, player_ships):
    shot = choice(AI_tiles_for_shot)
    y = shot[0]
    x = shot[1]

    result = enemy_shot_result(player_map, player_ships, AI_hits, x, y)

    if result == "killed_player":
        tiles_to_remove = [[y, x], [y - 1, x - 1], [y - 1, x], [y - 1, x + 1], [y, x + 1], [y + 1, x + 1], [y + 1, x],
                           [y + 1, x - 1], [y, x - 1]]
        for tile in tiles_to_remove:
            if tile in AI_tiles_for_shot:
                AI_tiles_for_shot.remove(tile)
    elif result == "hit_player":
        tiles_to_remove = [[y, x], [y - 1, x - 1], [y - 1, x + 1], [y + 1, x + 1], [y + 1, x - 1]]
        for tile in tiles_to_remove:
            if tile in AI_tiles_for_shot:
                AI_tiles_for_shot.remove(tile)
    else:
        AI_tiles_for_shot.remove([y, x])

    return (x, y, result, AI_tiles_for_shot, AI_hits)
