from random import randint


def _check_tile(y: int, x: int, map: list[list]):
	# check the tile and its adjacent tiles
	check = map[y][x] == 0 and map[y-1][x] == 0 and map[y+1][x] == 0 and map[y][x-1] == 0 and map[y][x+1] == 0
	return check


def check_ship(length: int, orient: list, head_y: int, head_x: int, map: list[list]):
	# check if the tile isn't already occupied
	if _check_tile(head_y, head_x, map):
		check = True
		# check if the ship will fit in the map
		tail_y = head_y + orient[0]*(length-1)
		tail_x = head_x + orient[1]*(length-1)
		if tail_y < 1 or tail_y > 8 or tail_x < 1 or tail_x > 8:
			check = False
		else:
			# check that the ships won't hit one another
			for deck in range(1, length):
				head_check_y = head_y
				head_check_x = head_x
				head_check_y += orient[0]
				head_check_x += orient[1]
				if not _check_tile(head_check_y, head_check_x, map):
					check = False
			return check


def create_map():
	# create an empty game map
	sea_map = []
	for i in range(10):
		sea_map.append([0]*10)

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
				ship_name = str(length) + f'_{count}'
				ships_in_game[ship_name] = []
				ships_in_game[ship_name].append([head_y-1, head_x-1])
				sea_map[head_y][head_x] = 1
				for deck in range(1, length):
					head_y += orient[0]
					head_x += orient[1]
					sea_map[head_y][head_x] = 1
					ships_in_game[ship_name].append([head_y-1, head_x-1])
		count += 1
	
	for i in range(3):
		poi = randint(2, 8)
		check_poi = False
		while not check_poi:
			poi_x, poi_y = randint(1, 8), randint(1, 8)
			if _check_tile(poi_y, poi_x, sea_map):
				check_poi = True
				sea_map[poi_y][poi_x] = poi
	
	sea_map.pop()
	sea_map.pop(0)
	for i in sea_map:
		i.pop()
		i.pop(0)
	
	return (sea_map, ships_in_game)


def _get_ship_shot(ships, x, y):
	for ship in ships:
		for deck in ships[ship]:
			if [y, x] == deck:
				return ship
			
'''			return "hit"
		else: return "killed"
	else: return "miss"'''

def _check_ship_killed(ship, hits, x, y):
	check = True
	if len(ship) > 1:
		for deck in ship:
			if deck not in hits:
				check = False
	return check


def shot_result(play_map, hits, x, y):
	sea_map = play_map[0]
	ships = play_map[1]
	if sea_map[y][x] == 1:
		hits.append([y, x])
		ship_shot = _get_ship_shot(ships, x, y)
		if _check_ship_killed(ships[ship_shot], hits, x, y):
			return "killed"
		else: return "hit"
	elif sea_map[y][x] == 2:
		return "mermaid"
	elif sea_map[y][x] == 3:
		return "squid"
	elif sea_map[y][x] == 4:
		return "shark"
	elif sea_map[y][x] == 5:
		return "dragon"
	elif sea_map[y][x] == 6:
		return "boat"
	elif sea_map[y][x] == 7:
		return "island"
	elif sea_map[y][x] == 8:
		return "volcano"
	else: return "miss"
							

'''
map = create_map()
hits = []
for row in map[0]:
	print(row)

print(shot_result(map, hits, 2, 2))
print(shot_result(map, hits, 3, 3))
print(shot_result(map, hits, 4, 4))
print(map[1])'''

