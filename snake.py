from getkey import getkey, keys
from threading import Thread, Lock
from sg_utils import dotdict
from collections import deque
import requests
import base64
import random
import string
import json
import os
import time

GITHUB = 'https://api.github.com/repos/shashfrankenstien/pysnake/contents/'

class Colors(object):
	RED = 31
	GREEN = 32
	YELLOW = 33
	BLUE = 34
	PINK = 35
	LIGHT_BLUE = 36
	WHITE = 37

	def colorize(message, color, bold=False):
		if isinstance(color, list):
			color = random.choice(color)
		color_code = '{};{}'.format(1 if bold else 0, color)
		return "\u001b[{}m".format(color_code)+message+"\u001b[0m"

class Score(object):
	def __init__(self):
		self.score_file = 'high_score.json'
		self.current_user = os.getlogin()
		self.score = 0
		self.__init_score_file()

	def __init_score_file(self):
		if not os.path.isfile(self.score_file):self.__set_scores(scores={})
		high_scores = self.__get_scores()
		if not isinstance(high_scores, dict):
			self.__set_scores(scores={})
		elif self.current_user not in high_scores:
			high_scores[self.current_user] = self.score
			self.__set_scores(scores=high_scores)

	def __get_scores(self):
		with open(self.score_file, 'rb') as handle:
			return json.load(handle)

	def __set_scores(self, scores):
		with open(self.score_file, 'wb') as handle:
			json.dump(scores, handle, indent=4)


	def increment(self):
		self.score += 1

	def set_high_score(self):
		high_scores = self.__get_scores()
		if self.score > high_scores[self.current_user]:
			high_scores[self.current_user] = self.score
			self.__set_scores(high_scores)
	
	def get_my_high_score(self):
		return self.__get_scores()[self.current_user]


	def get_top_scorer(self, n):
		high_scores = self.__get_scores()



class SnakeGame(object):
	def __init__(self, width=61):
		self.width = width
		self.height = 35

		self.board_color = Colors.BLUE
		self.top_bottom_wall_char = '='
		self.side_wall_char = '|'
		self.title = 'PYTHON'
		self.score = 0
		self.high_score_store = '.high_score'
		self.__set_high_score()


		self.inputs = deque()
		self.input_thread = None
		self.playing = False
		self.refresh_rate = 0.1

		self.snake = Snake('o', 
			head_x=self.width/2, 
			head_y=self.height/2, 
			length=4,
			color=Colors.GREEN)

		self.edibles = [Colors.colorize(x, [Colors.LIGHT_BLUE, Colors.GREEN, Colors.YELLOW, Colors.WHITE]) for x in ['$', '%', '@', '#','^', '&']+list(string.ascii_lowercase)]
		self.poisons = [Colors.colorize(x,Colors.RED) for x in ['X']]
		self.food = Food(
			edibles = self.edibles,
			poisons = self.poisons,
			board_height=self.height,
			board_width=self.width,
			feeding_interval=100)

	def __set_high_score(self):
		high_score = 0
		if os.path.isfile(self.high_score_store): 
			with open('.high_score', 'r') as h:
				try:
					high_score = int(h.read())
				except:
					pass
		if not high_score:high_score = self.score

		if high_score<=self.score:
			high_score = self.score
		with open('.high_score', 'w') as h:
			h.write(str(high_score))
		self.high_score = high_score


	def __make_title(self):
		score = 'Score: {}'.format(self.score)
		high_score = 'High Score: {}'.format(self.high_score)
		side_length = int((self.width-len(self.title))/2)
		l_side = ' '*(side_length - len(high_score))
		r_side = ' '*(side_length - len(score))
		return Colors.colorize('{}{}{}{}{}'.format(high_score, l_side, self.title, r_side, score), Colors.WHITE)


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
		if self.score>self.high_score: 
			messages.append('New High Score! {}'.format(self.score))
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
			elif self.food.is_poisonous(new_x,new_y):
				msg = 'Poisoned!'
				self.quit()
			elif self.food.exists(new_x,new_y):
				self.snake.eat(self.food.locations[(new_x,new_y)])
				self.food.got_eaten(new_x,new_y)
				self.score += 1

		for x,y in self.snake.address:
			board[y][x] = self.snake.char
		if msg: board = self.__crash_message(msg, board, Colors.RED)
		return board


	def __toss_food(self, board):
		if self.food.can_toss():self.food.toss(15)
		for loc in self.food.locations:
			x,y = loc
			board[y][x] = self.food.locations[loc]
		return board

	def render(self):
		os.system('clear')
		print(self.__make_title())
		board = self.__blank_board()
		board = self.__toss_food(board)
		board = self.__render_snake(board)
		
		for row in board:
			print(''.join(row))


	def __read_keys(self):
		key = None
		while self.playing:
			key = getkey(blocking=True)
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
				if key == 'q': 
					self.quit()
				elif key == keys.UP:
					self.snake.turn_up()
				elif key == keys.DOWN:
					self.snake.turn_down()
				elif key == keys.RIGHT:
					self.snake.turn_right()
				elif key == keys.LEFT:
					self.snake.turn_left()
			except IndexError:
				pass
			time.sleep(self.refresh_rate)
		self.__set_high_score()
		self.input_thread.join()

	def quit(self):
		self.playing = False


class Food(object):
	def __init__(self, edibles, poisons, board_height, board_width, feeding_interval=20):
		self.height = board_height
		self.width = board_width
		self.edibles = edibles
		self.poisons = poisons
		self.locations = {}
		self.feeding_interval = feeding_interval
		self.feed_wait_time = feeding_interval+1
		self.edibles_count = 0

	def toss(self, n=10):
		self.locations = {}
		food_count = int(n*0.3)
		self.edibles_count = food_count
		for i in range(n):
			x = random.randrange(1,self.width-2)
			y = random.randrange(1,self.height-2)
			if food_count:
				self.locations[(x,y)] = random.choice(self.edibles)
				food_count -= 1
			else:
				self.locations[(x,y)] = random.choice(self.poisons)
		self.feed_wait_time = 0

	def can_toss(self):
		if self.feed_wait_time > self.feeding_interval:
			return True
		elif self.edibles_count==0:
			return True
		else:
			self.feed_wait_time+=1
			return False

	def exists(self, x, y):
		return (x,y) in self.locations

	def is_poisonous(self,x,y):
		if self.exists(x, y) and self.locations[(x,y)] in self.poisons:
			return True
		else:
			return False

	def got_eaten(self, x, y):
		if self.locations[(x,y)] in self.edibles:
			self.edibles_count -= 1
			del self.locations[(x,y)]




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
		self.char = food
		self.pop_tail = False



class Crash(Exception):
	pass



if __name__ == '__main__':
	SnakeGame().chalaa()
	# print(Colors.colorize('hello', Colors.BLUE))




