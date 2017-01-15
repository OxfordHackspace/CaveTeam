import svgwrite
import math
import random

max_score = 6

def get_vertical_offset(size):
	opposite = size * math.sin(math.radians(60))
	return 2 * opposite

def get_horizontal_offset(size):
	adjactent = size * math.cos(math.radians(60))
	return adjactent + size

def get_score_colour(score):
	gradient=100.0 * (1.0 - (float(score)/float(max_score)))
	colour=svgwrite.rgb(100, gradient, gradient, '%')	
	return colour

def draw_image(centre, img, drawing):
	offset_centre = (centre[0] - 172, centre[1] - 149)
	image = svgwrite.image.Image(href=img, insert=offset_centre)
	drawing.add(image)

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
	hex = svgwrite.shapes.Polygon(points, stroke=svgwrite.rgb(255, 255, 255, '%'), stroke_width=10, stroke_opacity=100, fill_opacity=0)
	drawing.add(hex)

def add_score(score, centre, drawing):	
	score_text = svgwrite.text.Text(str(score), insert=centre, font_size=100, fill='white')
	drawing.add(score_text)

def add_victory(centre, drawing):
	end_text = svgwrite.text.Text('EXIT', insert=centre)
	drawing.add(end_text)

def add_start(centre, drawing):
	start_text = svgwrite.text.Text('START', insert=centre)
	drawing.add(start_text)

def add_slime(centre, drawing):
	start_text = svgwrite.text.Text('SLIME', insert=centre)
	drawing.add(start_text)

def get_reserved_start_squares(rows, columns):
	half_point = rows / 2
	yield (0, half_point)
	yield (0, half_point - 1)
	yield (0, half_point + 1)
	yield (1, half_point)
	yield (1, half_point + 1)

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
	return (row, column)

def choose_slime_start(starting_position, victory_position):
	slime_pos = victory_position
	# Don't allow slime within three of the starting position or ending position
	while(get_locations_distance(slime_pos, victory_position) <= 3 or
		  get_locations_distance(slime_pos, starting_position) <= 3):
		slime_pos=(random.randint(0, columns-1), random.randint(0, rows-1))
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
	position = (0, 0)

	starting_pos = choose_starting_position()
	victory_pos = choose_victory_position(starting_pos)
	slime_pos = choose_slime_start(starting_pos, victory_pos)

	for column in range(0, columns):
		for row in range(0, rows):
			position = get_hex_centre(row, column, size)
			if(get_locations_distance((row, column), starting_pos) == 0):
				draw_hex(size, position, 'green', dwg)
				add_start(position, dwg)
			elif(get_locations_distance((row, column), starting_pos) == 1):
				draw_hex(size, position, 'white', dwg)
				add_score(0, position, dwg)
			elif(get_locations_distance((row, column), victory_pos) == 0):
				draw_image(position, '../img/exit.png', dwg)
				add_victory(position, dwg)
			elif(get_locations_distance((row, column), slime_pos) == 0):
				draw_image(position, '../img/slime_tile.png', dwg)
				draw_hex(size, position, 'green', dwg)
				add_slime(position, dwg)
			else:
				score = random.randint(1, max_score)
				draw_image(position, '../img/stone_tile_v2.png', dwg)
				draw_hex(size, position, get_score_colour(score), dwg)
				add_score(score, position, dwg)

			'''
			draw_image(position, '../img/rock_tile.png', dwg)
			draw_hex(size, position,' white', dwg)
			'''

	dwg.save()	

rows = 6
columns = 18
size = 150 / math.sin(math.radians(60))
create_board(rows, columns, size)