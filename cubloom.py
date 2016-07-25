import pygame
import random
import math
import copy

colors = [[255, 0, 0], [0, 0, 255], [0, 255, 0], [255, 255, 255], [0, 0, 0]]

size_x = 3
size_y = 4

top_margin = 50
left_margin = 50

if size_x >= size_y:
	square_size = (700 - (top_margin * 2)) / size_x
else:
	square_size = (700 - (top_margin * 2)) / size_y
gaps = 10
box = square_size - (gaps * 2)

if size_x > size_y:
	top_margin += (size_x - size_y) * (square_size / 2)
if size_x < size_y:
	left_margin += (size_y - size_x) * (square_size / 2)

class World():
	def __init__(self):
		pygame.init()
		self.resolution = [700,700]
		self.screen = pygame.display.set_mode(self.resolution)
		pygame.display.set_caption("Cubloom Test Drive")
		
		self.font = pygame.font.Font(None, 30)
		self.clock = pygame.time.Clock()
		
		self.screen.fill([200, 200, 200])
		
		self.grid = []
		for i in range(size_x):
			self.grid.append([-1] * size_y)
		
		self.fill()
		self.next = copy.deepcopy(self.grid)
		self.selected = ["0", "0"]
		self.last_shift = "0"
		
		self.clicked = False
		self.minit = False
		self.start = [0, 0]
		self.move = [0, 0]
		self.pos = [0, 0]
		
		self.stop = False
	
	def fill(self, care = True):
		for i, val in enumerate(self.grid):
			for j, val2 in enumerate(val):
				if care:
					if val2 == -1:
						self.grid[i][j] = random.randint(0, 4)
				else:
					self.grid[i][j] = random.randint(0, 4)
	
	def shift(self, coords, shiphtur):
		if shiphtur == 0:
			return self.grid
		grd = copy.deepcopy(self.grid)
		if coords[0] == "0":
			temp = []
			temp = self.grid[coords[1]]
			if shiphtur < 0:
				for i in range(size_y):
					j = i + shiphtur
					while j < 0:
						j += size_y
					grd[coords[1]][j] = temp[i]
			else:
				for i in range(size_y):
					j = i + shiphtur
					while j > size_y - 1:
						j -= size_y
					grd[coords[1]][j] = temp[i]
			return grd
		else:
			temp = []
			for r in self.grid:
				temp.append(r[coords[0]])
			if shiphtur < 0:
				for i in range(size_x):
					j = i + shiphtur
					while j < 0:
						j += size_x
					grd[j][coords[0]] = temp[i]
			else:
				for i in range(size_x):
					j = i + shiphtur
					while j > size_x - 1:
						j -= size_x
					grd[j][coords[0]] = temp[i]
			return grd
	
	def m_set(self, x, y):
		if abs(x - self.start[0]) > 10 or abs(y - self.start[1]) > 10:
			if abs(x - self.start[0]) < abs(y - self.start[1]):
				self.move[0] = "0"
			else:
				self.move[1] = "0"
			self.minit = True
	
	def input(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if x < left_margin and y < top_margin:
					self.fill(False)
				self.clicked = True
				self.start[0] = x
				self.start[1] = y
				mx, my = self.pos_index(x, y)
				self.selected[0] = mx
				self.selected[1] = my
				self.last_shift = 0
				#print "Mouse is found at (" + str(x) + ", " + str(y) + ")"
			if event.type == pygame.MOUSEMOTION:
				if self.clicked:
					x, y = pygame.mouse.get_pos()
					if self.minit:
						if self.move[0] == "0":
							self.move[1] = y - self.start[1]
						if self.move[1] == "0":
							self.move[0] = x - self.start[0]
					else:
						self.m_set(x, y)
					self.pos[0] = x
					self.pos[1] = y
				
			if event.type == pygame.MOUSEBUTTONUP:
				self.move = [0, 0]
				self.clicked = False
				self.minit = False
			if event.type == pygame.KEYDOWN:
				k = event.key
				if k == pygame.K_ESCAPE:
					self.stop = True
	
	def pos_index(self, x, y):
		if x < left_margin + 1:
			x += square_size
		if y < top_margin + 1:
			y += square_size
		if x > 699 - left_margin:
			x -= square_size
		if y > 699 - top_margin:
			y -= square_size
		return (math.floor((x - left_margin) / square_size), math.floor((y - top_margin) / square_size))
	
	def math_pos(self, x, y, add = False):
		if add:
			temp = []
			for p in self.move:
				temp.append(int(p))
			consol = [gaps + left_margin + (x * square_size) + temp[0], gaps + top_margin + (y * square_size) + temp[1], box, box]
			return consol
		return [gaps + left_margin + (x * square_size), gaps + top_margin + (y * square_size), box, box]
	
	def pos_ranges(self, tt):
		temp = [left_margin + (tt[0] * square_size), left_margin + square_size + (tt[0] * square_size)]
		temp.append(top_margin + (tt[1] * square_size))
		temp.append(top_margin + square_size + (tt[1] * square_size))
		return temp
	
	def far_enough(self):
		res = self.pos_ranges(self.selected)
		indices = self.pos_index(self.pos[0], self.pos[1])
		if self.move[0] == "0":
			min = res[0]
			max = res[1]
			slide = self.pos[0]
			indices = indices[0]
			nim = 1
		else:
			min = res[2]
			max = res[3]
			slide = self.pos[1]
			indices = indices[1]
			nim = 0
		dist = 0
		if slide > max:
			dist = slide - max
		if slide < min:
			dist = min - slide
		if dist > 20 and indices != self.pos_index(self.pos[0], self.pos[1])[nim]:
			return True
		return False
	
	def logic(self):
		if self.move[0] == "0":
			tc = ["0", int(self.selected[0])]
			if self.move[1] > 0:
				if self.move[1] > square_size / 2:
					tm = self.move[1] - (square_size / 2)
					tm = int(math.ceil(tm / float(square_size)))
					if tm == self.last_shift:
						return
					#print tc, tm
					self.next = self.shift(tc, tm)
					self.last_shift = tm
			if self.move[1] < 0:
				if self.move[1] < -(square_size / 2):
					tm = self.move[1] + (square_size / 2)
					tm = int(math.floor(tm / float(square_size)))
					if tm == self.last_shift:
						return
					#print tc, tm
					self.next = self.shift(tc, tm)
					self.last_shift = tm
		if self.move[1] == "0":
			tc = [int(self.selected[1]), "0"]
			if self.move[0] > 0:
				if self.move[0] > square_size / 2:
					tm = self.move[0] - (square_size / 2)
					tm = int(math.ceil(tm / float(square_size)))
					if tm == self.last_shift:
						return
					#print tc, tm
					self.next = self.shift(tc, tm)
					self.last_shift = tm
			if self.move[0] < 0:
				if self.move[0] < -(square_size / 2):
					tm = self.move[0] + (square_size / 2)
					tm = int(math.floor(tm / float(square_size)))
					if tm == self.last_shift:
						return
					#print tc, tm
					self.next = self.shift(tc, tm)
					self.last_shift = tm
		if not self.clicked:
			#print "dick"
			self.grid = self.next
	
	def equalized(self, x, y):
		if x == "0":
			t = y
			while t < top_margin - box:
				t += 700 - (top_margin * 2)
			while t > 700 - top_margin:
				t -= 700 - (top_margin * 2)
		if y == "0":
			t = x
			while t < left_margin - box:
				t += 700 - (left_margin * 2)
			while t > 700 - left_margin:
				t -= 700 - (left_margin * 2)
		return t
	
	def draw(self):
		if self.clicked:
			if self.move[0] == "0":
				width = box
				top = 0
				left = self.math_pos(self.selected[0], self.selected[1])[0]
				height = 700
			else:
				width = 700
				height = box
				left = 0
				top = self.math_pos(self.selected[0], self.selected[1])[1]
			pygame.draw.rect(self.screen, [200, 200, 200], (left, top, width, height))
		else:
			self.screen.fill([200, 200, 200])
		for i, val in enumerate(self.grid):
			for j, val2 in enumerate(val):
				recte = self.math_pos(i, j)
				if self.clicked:
					if self.move[0] == "0":
						if i == self.selected[0]:
							recte = self.math_pos(i, j, True)
							recte[1] = self.equalized("0", recte[1])
							if recte[1] < top_margin:
								'''
								while recte[1] < top_margin - box:	
									recte[1] += 700 - (top_margin * 2)
								'''
								if recte[1] > top_margin - box:
									recte[3] = recte[1] - (top_margin - box)
									rect2 = recte
									rect2[3] = box - recte[3]
									rect2[1] = (700 - top_margin) - rect2[3]
									pygame.draw.rect(self.screen, colors[val2], rect2)
									recte[1] = top_margin
									recte[3] = box - recte[3]
							if recte[1] > 700 - top_margin - box:
								'''
								while recte[1] > 700 - top_margin:
									recte[1] -= 700 - (top_margin * 2)
								'''
								if recte[1] < 700 - top_margin:
									recte[3] = (700 - top_margin) - recte[1]
									rect2 = recte
									rect2[3] = box - recte[3]
									rect2[1] = top_margin
									pygame.draw.rect(self.screen, colors[val2], rect2)
									recte[3] = box - recte[3]
									recte[1] = (700 - top_margin) - recte[3]
					if self.move[1] == "0":
						if j == self.selected[1]:
							recte = self.math_pos(i, j, True)
							recte[0] = self.equalized(recte[0], "0")
							if recte[0] < left_margin:
								'''
								while recte[0] < left_margin - box:	
									recte[0] += 700 - (left_margin * 2)
								'''
								if recte[0] > left_margin - box:
									recte[2] = recte[0] - (left_margin - box)
									rect2 = recte
									rect2[2] = box - recte[2]
									rect2[0] = (700 - left_margin) - rect2[2]
									pygame.draw.rect(self.screen, colors[val2], rect2)
									recte[0] = left_margin
									recte[2] = box - recte[2]
							if recte[0] > 700 - left_margin - box:
								'''
								while recte[0] > 700 - left_margin:
									recte[0] -= 700 - (left_margin * 2)
								'''
								if recte[0] < 700 - left_margin:
									recte[2] = (700 - left_margin) - recte[0]
									rect2 = recte
									rect2[2] = box - recte[2]
									rect2[0] = left_margin
									pygame.draw.rect(self.screen, colors[val2], rect2)
									recte[2] = box - recte[2]
									recte[0] = (700 - left_margin) - recte[2]
				pygame.draw.rect(self.screen, colors[val2], recte)
		pygame.display.update()
	
	def run(self):
		while not self.stop:
			self.input()
			self.logic()
			self.draw()
			self.clock.tick(30)

if __name__ == "__main__":
	W = World()
	W.run()