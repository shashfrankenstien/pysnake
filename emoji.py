# Reference - https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py
import random


class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	
	def __getattr__(self, attr):
		if attr.startswith('__'):
			raise AttributeError
		return self.get(attr, None)
	
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__



Foods = dotdict({
	'MUSHROOM': u'\U0001F344',
	'TOMATO': u'\U0001F345',
	'AUBERGINE': u'\U0001F346',
	'GRAPES': u'\U0001F347',
	'MELON': u'\U0001F348',
	'WATERMELON': u'\U0001F349',
	'TANGERINE': u'\U0001F34A',
	'BANANA': u'\U0001F34C',
	'PINEAPPLE':  u'\U0001F34D',
	'APPLE1' : u'\U0001F34E',
	'APPLE2' : u'\U0001F34F',
	'PEACH': u'\U0001F351',
	'CHERRIES': u'\U0001F352',
	'STRAWBERRY': u'\U0001F353',
	'HAMBURGER': u'\U0001F354',
	'PIZZA': u'\U0001F355',
	'BONE': u'\U0001F356',
	'LEG': u'\U0001F357',
	'CRACKER': u'\U0001F358',
	'BALL': u'\U0001F359',
	'RICE1': u'\U0001F35A',
	'RICE2': u'\U0001F35B',
	'BOWL': u'\U0001F35C',
	'SPAGHETTI': u'\U0001F35D',
	'BREAD': u'\U0001F35E',
	'FRIES': u'\U0001F35F',
	'POTATO': u'\U0001F360',
	'DANGO': u'\U0001F361',
	'ODEN': u'\U0001F362',
	'SUSHI': u'\U0001F363',
	'SHRIMP': u'\U0001F364',
	'DESIGN': u'\U0001F365',
	'CREAM1': u'\U0001F366',
	'ICE': u'\U0001F367',
	'CREAM2': u'\U0001F368',
	'DOUGHNUT': u'\U0001F369',
	'COOKIE': u'\U0001F36A',
	'BAR': u'\U0001F36B',
	'CANDY': u'\U0001F36C',
	'LOLLIPOP': u'\U0001F36D',
	'CUSTARD': u'\U0001F36E',
	'POT': u'\U0001F36F',
	'SHORTCAKE': u'\U0001F370',
	'FOOD': u'\U0001F372',
	'COOKING': u'\U0001F373',
	'HANDLE':  u'\U0001F375',
	'CUP': u'\U0001F376',
	'GLASS1': u'\U0001F377',
	'GLASS2' :u'\U0001F378',
	'DRINK': u'\U0001F379',
	'MUG': u'\U0001F37A',
	'CAKE': u'\U0001F382',
})
Faces = dotdict({
	'FACE1':u'\U0001F601',
	'FACE2':u'\U0001F602',
	'FACE3':u'\U0001F603',
	'FACE4':u'\U0001F604',
	'FACE5':u'\U0001F605',
	'FACE6':u'\U0001F606',
	'FACE7':u'\U0001F609',
	'FACE8':u'\U0001F60A',
	'FACE9':u'\U0001F60B',
	'FACE10':u'\U0001F60C',
	'FACE11':u'\U0001F60D',
	'FACE12':u'\U0001F60F',
	'FACE13':u'\U0001F612',
	'FACE14':u'\U0001F613',
	'FACE15':u'\U0001F614',
	'FACE16':u'\U0001F616',
	'FACE17':u'\U0001F618',
	'FACE18':u'\U0001F61A',
	'FACE19':u'\U0001F61C',
	'FACE20':u'\U0001F61D',
	'FACE21':u'\U0001F61E',
	'FACE22':u'\U0001F620',
	'FACE23':u'\U0001F621',
	'FACE24':u'\U0001F622',
	'FACE25':u'\U0001F623',
	'FACE26':u'\U0001F624',
	'FACE27':u'\U0001F625',
	'FACE28':u'\U0001F628',
	'FACE29':u'\U0001F629',
	'FACE30':u'\U0001F62A',
	'FACE31':u'\U0001F62B',
	'FACE32':u'\U0001F62D',
	'FACE33':u'\U0001F630',
	'FACE34':u'\U0001F631',
	'FACE35':u'\U0001F632',
	'FACE36':u'\U0001F633',
	'FACE37':u'\U0001F635',
	'FACE38':u'\U0001F637',
	'FACE39':u'\U0001F638',
	'FACE40':u'\U0001F639',
	'FACE41':u'\U0001F63A',
	'FACE42':u'\U0001F63B',
	'FACE43':u'\U0001F63C',
	'FACE44':u'\U0001F63D',
	'FACE45':u'\U0001F63E',
	'FACE46':u'\U0001F63F',
	'FACE47':u'\U0001F640',
	'SUNFACE':u'\U0001F31E',
})
Deadly = dotdict({
	'OGRE':u'\U0001F479',
	'GOBLIN':u'\U0001F47A',
	# 'SKULL':u'\U0001F480'
})
Borders = dotdict({
	'HORIZONTAL':u'\U0001F6A5',
	'HORIZONTAL2':u'\U00002796',
	'VERTICAL':u'\U0001F6A6',
	'VERTICAL2':u'\U0001F539',
})

def get_foods():
	return list(Foods.values())

def get_faces():
	return list(Faces.values())

def get_deadly():
	return list(Deadly.values())

def get_random_food():
	return random.choice(get_foods())

def get_random_face():
	return random.choice(get_faces())

def get_random_deadly():
	return random.choice(get_deadly())


if __name__ == '__main__':
	print(Foods)
	print(Faces)
	print(Deadly)