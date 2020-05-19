import os, time, uuid
import colored
from colored import stylize

class matrix_manager:

	def __init__(self):
		self.matrices = {}
		self.covered = {}

	def get_start_of(self,name):
		try:
			return self.matrices[name]
		except:
			return None

class grid:
	
	def __init__(self,size):
		self.matrix_manager = matrix_manager()
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

	def plot_point(self,pixel,x,y):
		try:
			self.matrix_manager.covered[str(x)+','+str(y)] = {'pixel':self.grid[y][x]['pixel']}
			self.grid[y][x]['pixel'] = pixel
		except:
			pass

	def unplot_point(self,x,y):
		try:
			if type(self.grid[y][x]) == dict:
				old = self.matrix_manager.covered[str(x)+','+str(y)]
				self.grid[y][x]['pixel'] = old['pixel']
				del self.matrix_manager.covered[str(x)+','+str(y)]
		except:
			pass

	def plot_matrix(self,start,matrix):
		name = matrix.name
		grid = matrix.grid
		start = start.split(',')

		if self.matrix_manager.get_start_of(name) != None:
			self.unplot_matrix(matrix)
		self.matrix_manager.matrices[name] = {'x':int(start[0]), 'y':int(start[1])}

		for y in grid:
			for x in grid[y]:
				self.plot_point(grid[y][x]['pixel'],x+int(start[0]),y+int(start[1]))

	def unplot_matrix(self,matrix):
		name = matrix.name
		start = self.matrix_manager.get_start_of(name)
		grid = matrix.grid
		try:
			for y in grid:
				for x in grid[y]:
					self.unplot_point(x+int(start['x']),y+int(start['y']))
			
			del self.matrix_manager.matrices[name]
		except:
			pass

	def outline(self,color):
		size = self.max
		for y in range(0,size['y']):
			self.plot_point(stylize(" ", colored.bg(color)),size['x'],y)
			self.plot_point(stylize(" ", colored.bg(color)),0,y)

		for x in range(0,size['x']+1):
			self.plot_point(stylize(" ", colored.bg(color)),x,size['y'])
			self.plot_point(stylize(" ", colored.bg(color)),x,0)

	def background(self,color):
		self.background_color = color
		for y in self.grid:
			for x in self.grid[y]:
				pixel = self.grid[y][x]
				pixel['pixel'] = stylize(" ", colored.bg(color))












