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

	print '%d Food(s): %s' % (len(food), food)

	#  THERE IS FOOD IN PLAY
	if food:

		# ITERATE OVER FOOD ON BOARD
		for x, y in food:

			# BASIC WEIGHTING TO DIRECTIONS
			regions[board.get_direction_to_point(x,y)] += 1

			#BUILD LIST OF FOOD POINTS AND DISTANCE
			distances[(x,y)] = board.get_distance_to_point(x,y)

		# ORDER THE DISTANCES FROM HEAD
		# REVERSED SO BIGGER INDEX IS CLOSER
		distances_orderd 	= list(sorted(distances, key=distances.__getitem__, reverse=True))


		# HEAVY WEIGHTING INDEX ADDED TO DIRECTION
		for index, point in enumerate(distances_orderd, start=1):
			regions[board.get_direction_to_point(point[0], point[1])] += index

		#ORDER BY WEIGHT
		regions_ordered = list(sorted(regions, key=regions.__getitem__))

		print 'Internal Weight: %s' % regions

		#EXTERNAL WEIGHTING IS SIMPLIFIED FOR NOW
		for index, direction in enumerate(regions_ordered, start=1):
			reward[direction] = index*13

	return reward


def calc_risks(board, food=True):

	items 		= []
	risk 		= {	'n': 	0,
					'e': 	0,
					'w': 	0,
					's': 	0}


	for x in range(board.get_width()):
		for y in range(board.get_height()):
			if food and board.is_food(x,y):
				items.append((x,y))
			elif not food and (board.is_snake(x,y) or board.is_wall(x,y)):
				items.append((x,y))


	print '%d %s(s): %s' % (len(items), {True:'Food'}.get(food, 'Enemy'), items)

	if items:

		# ITERATE OVER FOOD ON BOARD
		for x, y in items:

			# BASIC WEIGHTING TO DIRECTIONS
			regions[board.get_direction_to_point(x,y)] += 1

			#BUILD LIST OF FOOD POINTS AND DISTANCE
			distances[(x,y)] = board.get_distance_to_point(x,y)

		# ORDER THE DISTANCES FROM HEAD
		# REVERSED SO BIGGER INDEX IS CLOSER
		distances_orderd 	= list(sorted(distances, key=distances.__getitem__, reverse=True))


		# HEAVY WEIGHTING INDEX ADDED TO DIRECTION
		for index, point in enumerate(distances_orderd, start=1):
			regions[board.get_direction_to_point(point[0], point[1])] += index

		#ORDER BY WEIGHT
		regions_ordered = list(sorted(regions, key=regions.__getitem__))

		print 'Internal Weight: %s' % regions

		#EXTERNAL WEIGHTING IS SIMPLIFIED FOR NOW
		for index, direction in enumerate(regions_ordered, start=1):
			risk[direction] = index*25

	return risk

