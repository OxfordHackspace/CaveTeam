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
	hex = svgwrite.shapes.Polygon(points, stroke=svgwrite.rgb(10, 10, 16, '%'), fill=colour)
	drawing.add(hex)

def add_score(score, centre, drawing):	
	score_text = svgwrite.text.Text(str(score), insert=centre)
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

rows = 6
columns = 18
size = 100

board_size = (columns * get_vertical_offset(size), rows * get_horizontal_offset(size))
margin = (400, 2000)

dwg = svgwrite.Drawing('test_hex.svg', size=(board_size[0] + margin[0], board_size[1] + margin[1]))

position = (0, 0)

starting_indices=(0,rows/2)

x_pos=random.randint(columns/2, columns-1)
y_pos=random.randint(0, rows-1)
victory_pos=(x_pos, y_pos)

slime_pos=(random.randint(0, columns-1), random.randint(0, rows-1))

for i in range(0, columns):
	offset = 0
	if i % 2 == 0:
		offset = get_vertical_offset(size) / 2.0
	position = (position[0] + get_horizontal_offset(size), offset)
	for j in range(0, rows):
		position = (position[0], position[1] + get_vertical_offset(size))
		offset_x = i - starting_indices[0]
		offset_y = j - starting_indices[1]
		if (abs(offset_x) + abs(offset_y) <= 1) or (offset_x == 1 and offset_y == 1):
			draw_hex(size, position, 'white', dwg)
			if(abs(offset_x) + abs(offset_y) == 0):
				add_start(position, dwg)
			else:
				add_score(0, position, dwg)
		elif i == victory_pos[0] and j == victory_pos[1]:
			draw_hex(size, position, 'green', dwg)
			add_victory(position, dwg)
		elif i == slime_pos[0] and j == slime_pos[1]:
			draw_hex(size, position, 'green', dwg)
			add_slime(position, dwg)
		else:
			score = random.randint(1, max_score)
			draw_hex(size, position, get_score_colour(score), dwg)
			add_score(score, position, dwg)

dwg.save()	
