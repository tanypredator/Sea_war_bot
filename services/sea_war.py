from random import randint


def _check_tile(y, x, map):
	# check the tile and its adjacent tiles
	check = map[y][x] == 0 and map[y-1][x] == 0 and map[y+1][x] == 0 and map[y][x-1] == 0 and map[y][x+1] == 0
	return check


def check_ship(length, orient, head_y, head_x, map):
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
	orientation_dict = {1: [-1, 0], 2: [0, 1], 3: [1, 0], 4: [1, 0]}
	for length in list_of_ships:
		# choose the tile for the ship head
		check = False
		while not check:
			head_y, head_x = randint(1, 8), randint(1, 8)
			# choose orientation
			orientation = randint(1, 4)
			orient = orientation_dict[orientation]
			if check_ship(length, orient, head_y, head_x, sea_map):
				check = True
				sea_map[head_y][head_x] = 1
				for deck in range(1, length):
					head_y += orient[0]
					head_x += orient[1]
					sea_map[head_y][head_x] = 1

	sea_map.pop()
	sea_map.pop(0)
	for i in sea_map:
		i.pop()
		i.pop(0)
	
	return sea_map


def check_hit(map, x, y):
	if map[y][x]:
		if map[y-1][x] or map[y+1][x] or map[y][x-1] or map[y][x+1]:
			return "hit"
		else: return "killed"
	else: return "miss"

'''map = create_map()
for row in map:
	print(row)
print(check_hit(map, 2, 2))
print(check_hit(map, 3, 3))
print(check_hit(map, 4, 4))'''

'''message = '1,1'.split(',')
coord_x = int(message[0]) - 1
coord_y = int(message[1]) - 1

sea_map_test = create_map()
print(sea_map_test)
print(coord_x, coord_y)
print(sea_map_test[coord_x][coord_y])'''
