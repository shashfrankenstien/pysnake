from threading import Thread
from sg_utils import dotdict
from collections import deque, defaultdict
from score_keeper import TwitterScoreKeeper
from getkeys import getch, keys
from emoji import emoji
import base64
import copy
import random
import string
import json
import os
import time

USE_EMOJI = 0
GRADUAL_FOOD_TOSS = 1
LEVEL_UP_AT = {
	0:1,
	10:2,
	25:3
}

def print_it(it):
	print((' '*10)+str(it))

class Colors(object):
	RED = 31
	GREEN = 32
	YELLOW = 33
	BLUE = 34
	PINK = 35
	LIGHT_BLUE = 36
	WHITE = 37

	@staticmethod
	def colorize(message, color, bold=False):
		if isinstance(color, list):
			color = random.choice(color)
		color_code = '{};{}'.format(1 if bold else 0, color)
		# return "\u001b[{}m".format(color_code)+message+"\u001b[0m"
		return "\033[{}m".format(color_code)+message+"\033[0m"



class SnakeGame(object):
	def __init__(self, width=61):
		self.width = width
		self.height = 35

		self.board_color = Colors.BLUE
		self.top_bottom_wall_char = '='
		self.side_wall_char = '|'
		self.title = '@snake_pysnake'
		self.score = TwitterScoreKeeper()
		# self.high_score_store = '.high_score'
		# self.__set_high_score()


		self.inputs = deque()
		self.input_thread = None
		self.playing = False
		self.refresh_rate = 0.1

		self.snake = Snake(emoji.get_random_face() if USE_EMOJI else 'o', 
			head_x=self.width/2, 
			head_y=self.height/2, 
			length=4,
			color=Colors.GREEN)

		if USE_EMOJI:
			self.edibles = emoji.get_foods()
			self.poisons = emoji.get_deadly()
		else:
			self.edibles = [Colors.colorize(x, [Colors.LIGHT_BLUE, Colors.GREEN, Colors.YELLOW, Colors.WHITE]) for x in ['$', '%', '@', '#','^', '&']+list(string.ascii_lowercase)]
			self.poisons = [Colors.colorize(x,Colors.RED) for x in ['X']]

		
		self.obstacle = Obstacles(
			edibles = self.edibles,
			poisons = self.poisons,
			board_height=self.height,
			board_width=self.width)



	def __make_title(self):
		level = 'Level: {}'.format(self.obstacle.current_level)
		# top_scorer, top_score = self.score.current_high_score
		# high_score = 'High Score: {} {}'.format(top_scorer, top_score)
		side_length = int((self.width-len(self.title))/2)
		l_side = ' '*(side_length)
		r_side = ' '*(side_length - len(level))
		# return Colors.colorize('{}{}{}{}{}'.format(high_score, l_side, self.title, r_side, score), Colors.WHITE)

		side = ' '*side_length
		return Colors.colorize('{}{}{}{}'.format(l_side, self.title, r_side, level), Colors.WHITE)


	def __make_footer(self):
		score = 'Score: {}'.format(self.score.score)
		top_scorer, top_score = self.score.current_high_score
		high_score = 'High Score: {} {}'.format(top_scorer, top_score)
		side_length = int((self.width)/2)
		l_side = ' '*(side_length - len(high_score))
		r_side = ' '*(side_length - len(score))
		return Colors.colorize('{}{}{}{}'.format(high_score, l_side, r_side, score), Colors.WHITE)


	def __blank_board(self):
		board = []
		top_botom = Colors.colorize(self.top_bottom_wall_char,self.board_color)
		sides = Colors.colorize(self.side_wall_char,self.board_color)
		board.append([top_botom]*self.width)
		for i in range(self.height):
			board.append([sides] + [' ']*(self.width-(len(self.side_wall_char)*2)) + [sides])
		board.append([top_botom]*self.width)
		return board


	def __crash_message(self, message, board, color=None):
		messages = message.split('\n')
		if self.score.current_high_score[1] and self.score.score>self.score.current_high_score[1]:
			messages.append('New High Score! {}'.format(self.score.score))
		messages += ['', 'Press any key to quit']
		start_y = int((self.height-len(messages))/2)
		for row in range(len(messages)):
			m = messages[row]
			start_x = int((self.width-len(m))/2)
			for char in range(len(m)):
				board[start_y+row][start_x+char] = Colors.colorize(m[char], color) if color else m[char]
		return board


	def did_hit_border(self, x, y):
		if x == 0 or x == self.width-1 or y == 0 or y == self.height+1:
			return True
		else:
			return False


	def __render_snake(self, board):
		msg = None
		new_head = self.snake.move()
		if not new_head:
			msg = 'Cannibalized!'
			self.quit()
		else:
			new_x, new_y = new_head
			if self.did_hit_border(new_x,new_y):
				msg = 'Crashed!'
				self.quit()
			elif self.obstacle.is_poisonous(new_x,new_y):
				msg = 'Poisoned!'
				self.quit()
			elif self.obstacle.exists(new_x,new_y):
				self.snake.eat(self.obstacle.get_food_at(new_x,new_y))
				self.obstacle.got_eaten(new_x,new_y)
				self.score.increment()

		for x,y in self.snake.address:
			board[y][x] = self.snake.char
		if msg: board = self.__crash_message(msg, board, Colors.RED)
		return board

	def __do_level_change(self):
		if self.score.score in LEVEL_UP_AT:
			self.obstacle.level_up(LEVEL_UP_AT[self.score.score])


	def render(self):
		self.__do_level_change()
		os.system('clear')
		print_it(self.__make_title())
		board = self.__blank_board()
		board = self.obstacle.toss(board, n=20)
		board = self.__render_snake(board)
		for row in board:
			print_it(''.join(row))
		print_it(self.__make_footer())


	def __read_keys(self):
		key = None
		while self.playing:
			# key = getkey()
			key = getch()

			if key:
				self.inputs.appendleft(key)
				key = None


	def chalaa(self):
		self.playing = True
		self.input_thread = Thread(target=self.__read_keys)
		self.input_thread.start()
		while self.playing:
			self.render()
			try:
				key = self.inputs.pop()
				if key == keys.Q: 
					self.quit()
				elif key == keys.UP or key == keys.W:
					self.snake.turn_up()
				elif key == keys.DOWN or  key == keys.S:
					self.snake.turn_down()
				elif key == keys.RIGHT or key == keys.D:
					self.snake.turn_right()
				elif key == keys.LEFT or key == keys.A:
					self.snake.turn_left()
			except IndexError:
				pass
			time.sleep(self.refresh_rate)
		self.score.set_high_score()
		self.input_thread.join()


	def quit(self):
		self.playing = False




class Obstacles(object):
	def __init__(self, edibles, poisons, board_height, board_width, feeding_interval=100):
		self.height = board_height
		self.width = board_width
		self.__sweeper = '.'
		self.edibles = [e for e in edibles if e!=self.__sweeper]
		self.poisons = [p for p in poisons if p!=self.__sweeper]
		self.edibles_count = 0
		self.poison_move_tracker = 0

		self.locations = defaultdict(dict)
		self.new_locations = defaultdict(dict)

		self.levels = {
			1: dotdict({
				'feeding_interval': feeding_interval,
				'feed_wait_time': feeding_interval+1,
				'gradual_food_toss': 0,
				'food_gradation':1
			}),
			2: dotdict({
				'feeding_interval': int(self.height)*2,
				'feed_wait_time': (int(self.height)*2)+1,
				'gradual_food_toss': 1,
				'food_gradation':2
			}),
			3: dotdict({
				'feeding_interval': int(self.height),
				'feed_wait_time': int(self.height)+1,
				'gradual_food_toss': 1,
				'food_gradation':1
			})
		}
		self.current_level = 1
		

	def toss(self, board, n=10):
		if self.__can_toss():
			self.new_locations = defaultdict(dict)
			food_count = int(n*0.3)
			self.edibles_count = food_count
			for i in range(n):
				x = random.randrange(1,self.width-2)
				y = random.randrange(1,self.height-2)
				if food_count:
					self.new_locations[y][x] = random.choice(self.edibles)
					food_count -= 1
				else:
					self.new_locations[y][x] = random.choice(self.poisons)
			self.levels[self.current_level].feed_wait_time = 0
			self.poison_move_tracker = 0

		return self.__render(board)



	def __render(self, board):
		curr_L = self.levels[self.current_level]
		if GRADUAL_FOOD_TOSS and curr_L.gradual_food_toss:
			y = int(curr_L.feed_wait_time/curr_L.food_gradation)
			if y in self.locations:
				del self.locations[y]
			if y in self.new_locations:
				self.locations[y] = self.new_locations[y]
			if y+1<self.height: self.locations[y+1] = {x:self.__sweeper for x in range(1, self.width-1)}
		else:
			self.locations = self.new_locations

		for y in self.locations:
			for x in self.locations[y]:
				board[y][x] = self.locations[y][x]
		return board


	def __can_toss(self):
		if self.levels[self.current_level].feed_wait_time > self.levels[self.current_level].feeding_interval:
			return True
		elif self.edibles_count==0:
			return True
		else:
			self.levels[self.current_level].feed_wait_time+=1
			return False

	def exists(self, x, y):
		return y in self.locations and x in self.locations[y] and self.locations[y][x]!=self.__sweeper

	def is_poisonous(self,x,y):
		if self.exists(x, y) and self.locations[y][x] in self.poisons:
			return True
		else:
			return False

	def get_food_at(self,x,y):
		return self.locations[y][x]

	def got_eaten(self, x, y):
		if self.locations[y][x] in self.edibles:
			self.edibles_count -= 1
			del self.locations[y][x]

	def level_up(self, level):
		if level in self.levels:
			self.current_level = level




class Snake(object):
	def __init__(self, snake_char, head_x, head_y, length=2, color=None):
		if color:
			self.char = Colors.colorize(snake_char, color)
		else:	
			self.char = snake_char
		self.direction = 'U' #U,D,L,R
		self.head_x = int(head_x)
		self.head_y = int(head_y)
		self.address = self.__create_snake(length)
		self.alive = True
		self.pop_tail = True

	def __create_snake(self, length):
		ad = deque()
		for i in range(0,length):
			ad.append((self.head_x,self.head_y+i))
		return ad

	def turn_left(self):
		if self.direction != 'R':
			self.direction = 'L'

	def turn_right(self):
		if self.direction != 'L':
			self.direction = 'R'

	def turn_up(self):
		if self.direction != 'D':
			self.direction = 'U'

	def turn_down(self):
		if self.direction != 'U':
			self.direction = 'D'

	def move(self):
		if self.alive:
			if self.direction == 'U':
				self.head_y -= 1
			elif self.direction == 'D':
				self.head_y += 1
			elif self.direction == 'R':
				self.head_x += 1
			elif self.direction == 'L':
				self.head_x -= 1
			new_head = (self.head_x, self.head_y)
			if new_head in self.address:
				self.alive = False
				return self.alive
			else:
				if self.pop_tail: 
					self.address.pop()
				self.address.appendleft(new_head)
				self.pop_tail = True
				return new_head
		else:
			raise Crash('Snake is dead')

	def eat(self, food):
		if USE_EMOJI:
			self.char = emoji.get_random_face()
		else:
			self.char = food
		self.pop_tail = False



class Crash(Exception):
	pass



if __name__ == '__main__':
	SnakeGame().chalaa()
	# print(Colors.colorize('hello', Colors.BLUE))




