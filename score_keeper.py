
from collections import defaultdict
import os

import json

from importlib.util import find_spec



def internet_on(url='http://www.google.com/', timeout=2):
	import requests
	print('Attempting Network Connection...')
	try:
		_ = requests.get(url, timeout=timeout)
		return True
	except requests.ConnectionError:
		print("No internet connection available.")
		return False


class TwitterScoreKeeper(object):
	def __init__(self):
		from birdy.twitter import UserClient, TwitterClientError
		twitter = UserClient('VxihO3nqNHKxS8wHJ1RbBJ9O6',
									'0O5uvNiartkXxMynEufXU89UwBkTTOt9sIzquYTRpDXk1LFC0P',
									'930956740031590400-OPm95rGIWOXPPuCIjilsast0HiPxkL8',
									'0CdlbpHy7uUYkIMfq2q42xOgiKksbNQ27yulW5CTFhUQd')

		self.tw_screen_name = 'snake_pysnake'
		self.current_user = os.getlogin()
		self.score = 0
		self.__init_high_scores()

	def __init_high_scores(self):
		self.high_scores = {}
		self.current_high_score = ('No Network','')
		if internet_on():
			try:
				self.high_scores = self.__get_scores()
				self.current_high_score = self.__get_top_scorer()
			except TwitterClientError:
				pass


	def increment(self):
		self.score += 1

	def __get_scores(self):
		resp = twitter.api.statuses.user_timeline.get(screen_name=self.tw_screen_name)
		scores = defaultdict(list)
		for data in resp.data:
			scores[data['text'].split(u'\U0001F389')[0].split()[-2].strip()].append(int(data['text'].split(u'\U0001F389')[-2].strip()))
		return scores

	def __get_top_scorer(self):
		hs_temp = {k: max(v) for k, v in self.high_scores.items()}
		scorer = max(hs_temp, key=hs_temp.get)
		return scorer, hs_temp[scorer]

	def __set_scores(self, score):
		status = u'New high score! {user} -> \U0001F389 {score} \U0001F389'.format(user=self.current_user, score=score)
		try:
			_ = twitter.api.statuses.update.post(status=status)
		except TwitterClientError:
			pass


	def set_high_score(self):
		if isinstance(self.current_high_score[1], int) and self.score > self.current_high_score[1]:
			self.__set_scores(self.score)
	
	def get_high_scores(self):
		return self.high_scores


	
	



class JsonScoreKeeper(object):
	def __init__(self):
		self.score_file = 'high_score.json'
		self.current_user = os.getlogin()
		self.score = 0
		self.__init_score_file()

	def __init_score_file(self):
		high_scores = self.__get_scores()
		if self.current_user not in high_scores:
			self.__set_scores(score=self.score)
		self.current_high_score = self.__get_top_scorer()
		
		
	def __get_scores(self):
		if not os.path.isfile(self.score_file):
			return {}
		with open(self.score_file, 'r') as handle:
			return json.load(handle)

	def __get_top_scorer(self):
		hs_temp = self.__get_scores()
		scorer = max(hs_temp, key=hs_temp.get)
		return scorer, hs_temp[scorer]

	def __set_scores(self, score):
		hstemp = self.__get_scores()
		hstemp[self.current_user] = score
		with open(self.score_file, 'w') as handle:
			json.dump(hstemp, handle, indent=4)


	def increment(self):
		self.score += 1

	def set_high_score(self):
		high_scores = self.__get_scores()
		if self.score > high_scores[self.current_user]:
			self.__set_scores(self.score)

	
	def get_high_scores(self):
		return self.__get_scores()


if find_spec("birdy") is not None:
	ScoreKeeper= TwitterScoreKeeper
else:
	ScoreKeeper = JsonScoreKeeper



if __name__ == '__main__':
	t = ScoreKeeper()
	t.increment()
	t.increment()
	t.increment()
	t.increment()
	t.set_high_score()
	print(t.get_high_scores())
