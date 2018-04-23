import svgwrite
import math
import random

def get_vertical_offset(size):
	opposite = size * math.sin(math.radians(60))
	return 2 * opposite

def get_horizontal_offset(size):
	adjactent = size * math.cos(math.radians(60))
	return adjactent + size

def draw_hex(size, centre, colour, drawing):
	adjactent = size * math.cos(math.radians(60))
	opposite = size * math.sin(math.radians(60))
	half = size / 2.0
	top_left = (centre[0] - half, centre[1] - opposite)
	top_right = (centre[0] + half, centre[1] - opposite)
	left = (centre[0] - (half + adjactent), centre[1])
	right = (centre[0] + (half + adjactent), centre[1])
	bottom_left = (centre[0] - half, centre[1] + opposite)
	bottom_right = (centre[0] + half, centre[1] + opposite)
	
	points=[top_left, top_right, right, bottom_right, bottom_left, left]
	hex = svgwrite.shapes.Polygon(points, stroke=svgwrite.rgb(0, 0, 0, '%'), stroke_width=10, stroke_opacity=100, fill=colour, fill_opacity=100)
	drawing.add(hex)

def add_score(score, centre, drawing):	
	score_text = svgwrite.text.Text(str(score), insert=centre, font_size=100, fill='black')
	drawing.add(score_text)

def add_victory(centre, drawing):
	# hex = svgwrite.shapes.Polygon(points, fill=svgwrite.rgb(0, 255, 0, '%'), fill_opacity=100)
	end_text = svgwrite.text.Text('EXIT', font_size=50, insert=centre, fill='black')
	drawing.add(end_text)

def add_start(centre, drawing):
	start_text = svgwrite.text.Text('START', font_size=50, insert=centre, fill='black')
	drawing.add(start_text)

def add_slime(centre, drawing):
	start_text = svgwrite.text.Text('SLIME', font_size=50, insert=centre, fill='black')
	drawing.add(start_text)

def get_locations_distance(pos1, pos2):
	# if we are an even number of columns away
	# then 
	if((pos1[1] - pos2[1]) % 2 == 0):
		return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
	else:
		horizontal_offset = abs(pos1[1] - pos2[1])
		# The vertical on odd rows we can either move across (and up) or across (and down)
		# for one move in either case. 
		vertical_offset = min(abs(pos1[0] - pos2[0]), abs(pos1[0] - (pos2[0] + 1)))
		return horizontal_offset + vertical_offset

def choose_starting_position():
	return (rows/2, 0)	

def choose_victory_position(starting_position):
	# don't allow the victory point in the fist half of the board
	# or (if the board is _really_ small in either of the first two columns)
	min_column = max(columns/2, starting_position[0] + 2)
	column=random.randint(min_column, columns-1)
	row=random.randint(0, rows-1)
	victory_pos = (column, row)
	return victory_pos

def choose_slime_start(starting_position, victory_position):
	# Don't allow slime within three of the starting position
	min_column = starting_position[0] + 2
	column = random.randint(min_column, columns-1)
	row = random.randint(0, rows-1)
	slime_pos = (column, row)
	#	If the slime is in the same position as the exit, try again
	if (slime_pos == victory_position):
		slime_pos = choose_slime_start(starting_position, victory_position)
	return slime_pos

def get_hex_centre(row, column, size):
	offset = 0
	if column % 2 == 0:
		offset = get_vertical_offset(size) / 2.0
	return ((column + 1) * get_horizontal_offset(size), offset + ((row + 1) * get_vertical_offset(size)))

def create_board(rows, columns, size):
	board_size = (columns * get_horizontal_offset(size), rows * get_vertical_offset(size))
	margin = (200, 600)
	dwg = svgwrite.Drawing('board.svg', size=(board_size[0] + margin[0], board_size[1] + margin[1]))
	# Background Colour
	dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='white'))
	position = (0, 0)

	starting_pos = choose_starting_position()
	victory_pos = choose_victory_position(starting_pos)
	slime_pos = choose_slime_start(starting_pos, victory_pos)

	for column in range(0, columns):
		for row in range(0, rows):
			position = get_hex_centre(row, column, size)

			if (slime_pos == (column,row)):
				draw_hex(size, position, '#00FF00', dwg)
				add_slime(position, dwg)

			elif (victory_pos == (column,row)):
				draw_hex(size, position, '#0000FF', dwg)
				add_victory(position, dwg)

			elif(get_locations_distance((row, column), starting_pos) == 0):
				draw_hex(size, position, '#FFFF00', dwg)
				add_start(position, dwg)
				
			elif(get_locations_distance((row, column), starting_pos) == 1):
				draw_hex(size, position, '#FFFFFF', dwg)
				add_score(0, position, dwg)
				
			else:
				score = random.randint(1, threshold)
				draw_hex(size, position, "#FFFFFF", dwg)
				add_score(score, position, dwg)

	dwg.save()	

rows = 6
columns = 18
players = 4
threshold = players * 3
size = 150 / math.sin(math.radians(60))
create_board(rows, columns, size)
