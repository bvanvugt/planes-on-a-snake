def calc_reward(board):
	food 		= []

	reward 		= {	'n': 	0,
					'e': 	0,
					'w': 	0,
					's': 	0}

	regions 	= {	'n': 	0,
					'e': 	0,
					'w': 	0,
					's': 	0}

	distances 	= {}

	# FIND THE FOOD
	for x in range(board.get_width()):
		for y in range(board.get_height()):
			if board.is_food(x,y):
				food.append((x,y))

	# ITERATE OVER FOOD ON BOARD
	for x, y in food:
		regions[board.get_direction_to_point(x,y)] += 1
		distances[(x,y)]  = board.get_distance_to_point(x,y)

	# ORDERED BY REGION AND DISTANCE
	regions_ordered 	= list(sorted(regions, key=regions.__getitem__))
	distances_orderd 	= list(sorted(distances, key=distances.__getitem__))

	#print regions_ordered
	#print distances_orderd

	for index, direction in enumerate(regions_ordered, start=1):
		reward[direction] = index*25

	return reward