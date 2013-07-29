import board
import reward



STATE 		= []
width		= 30
height 		= 20
head 		= (5, 10)
food 		= [(10, 15), (5, 11), (15, 7), (2,4)]
enemies 	= [(3, 2), (5, 7), (17, 13), (8,12)]


class square(object):
	def __init__(self, type=None, id=None):
		self.type = type
		self.id = id

	def __len__(self):
		return True

	def __repr__(self):
		return self.type

for y in range(height):
	row = []
	for x in range(width):
		row.append([])

	STATE.append(row)


STATE[head[0]][head[1]].append({'type':'snake_head', 'id':'38024038-57cd-4e15-a1d9-663b5f3e85bf'})

for x, y in food:
	STATE[x][y].append({'type':'food', 'id':'e8514154-d957-46cf-9635-eb31be64339b'})


for x, y in enemies:
	STATE[x][y].append({'type':'snake', 'id':'e8514154-d957-46cf-9635-eb31be64339b'})


game = board.Board(STATE, '38024038-57cd-4e15-a1d9-663b5f3e85bf')

print STATE
print reward.calc_risks(game, food=True)
print reward.calc_risks(game, food=False)