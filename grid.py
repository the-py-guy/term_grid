import os, time, uuid
import colored
from colored import stylize

class sub_grid_manager:

	def __init__(self):
		self.sub_grids = {}
		self.covered = {}

	def get_start_of(self,name):
		try:
			return self.sub_grids[name]
		except:
			return None

class grid:
	
	def __init__(self,size):
		self.sub_grid_manager = sub_grid_manager()
		self.grid = {}
		self.max = None
		self.name = uuid.uuid4()
		self.background_color = None

		if size == 'window':
			rows, columns = os.popen('stty size', 'r').read().split()
			size = {'x':int(columns), 'y':int(rows)-1}
			self.max = {'x':int(columns)-1, 'y':int(rows)-2}
			
		else:
			size = size.split(':')
			self.max = {'x':int(size[0])-1, 'y':int(size[1])-1}
			size = {'x':int(size[0]), 'y':int(size[1])}
			

		for i in range(0,size['y']):
			y = size['y'] - (i + 1)
			self.grid[y] = {}
			for x in range(0,size['x']):
				self.grid[y][x] = {'pixel':' '}

	def show(self):
		os.system('clear')
		grid = self.grid
		for y in grid:
			row = ''
			for x in grid[y]:
				row = row + grid[y][x]['pixel']
			print(row)

	def change_pixel(self,pixel,x,y):
		try:
			self.sub_grid_manager.covered[str(x)+','+str(y)] = {'pixel':self.grid[y][x]['pixel']}
			self.grid[y][x]['pixel'] = pixel
		except:
			pass

	def erase_pixel(self,x,y):
		try:
			if type(self.grid[y][x]) == dict:
				old = self.sub_grid_manager.covered[str(x)+','+str(y)]
				self.grid[y][x]['pixel'] = old['pixel']
				del self.sub_grid_manager.covered[str(x)+','+str(y)]
		except:
			pass

	def place_sub_grid(self,matrix,start_x,start_y):
		name = matrix.name
		grid = matrix.grid

		if self.sub_grid_manager.get_start_of(name) != None:
			self.remove_sub_grid(matrix)
		self.sub_grid_manager.sub_grids[name] = {'x':start_x, 'y':start_y}

		for y in grid:
			for x in grid[y]:
				self.change_pixel(grid[y][x]['pixel'],x+start_x,y+start_y)

	def remove_sub_grid(self,matrix):
		name = matrix.name
		start = self.sub_grid_manager.get_start_of(name)
		grid = matrix.grid
		try:
			for y in grid:
				for x in grid[y]:
					self.erase_pixel(x+int(start['x']),y+int(start['y']))
			
			del self.sub_grid_manager.sub_grids[name]
		except:
			pass

	def outline(self,color):
		size = self.max
		for y in range(0,size['y']+1):
			self.change_pixel(stylize(" ", colored.bg(color)),size['x'],y)
			self.change_pixel(stylize(" ", colored.bg(color)),0,y)

		for x in range(0,size['x']):
			self.change_pixel(stylize(" ", colored.bg(color)),x,size['y'])
			self.change_pixel(stylize(" ", colored.bg(color)),x,0)

	def background(self,color):
		self.background_color = color
		for y in self.grid:
			for x in self.grid[y]:
				pixel = self.grid[y][x]
				pixel['pixel'] = stylize(" ", colored.bg(color))












