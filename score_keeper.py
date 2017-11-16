from birdy.twitter import UserClient, TwitterClientError
from collections import defaultdict
import os

twitter = UserClient('VxihO3nqNHKxS8wHJ1RbBJ9O6',
                    '0O5uvNiartkXxMynEufXU89UwBkTTOt9sIzquYTRpDXk1LFC0P',
                    '930956740031590400-OPm95rGIWOXPPuCIjilsast0HiPxkL8',
                    '0CdlbpHy7uUYkIMfq2q42xOgiKksbNQ27yulW5CTFhUQd')



class TwitterScoreKeeper(object):
	def __init__(self):
		self.tw_screen_name = 'snake_pysnake'
		self.current_user = os.getlogin()
		self.score = 0
		self.__init_high_scores()

	def __init_high_scores(self):
		try:
			self.high_scores = self.__get_scores()
			self.current_high_score = self.__get_top_scorer()
		except TwitterClientError:
			self.high_scores = {}
			self.current_high_score = ('No Network','')

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
		if self.score > self.current_high_score[1]:
			self.__set_scores(self.score)
	
	def get_high_scores(self):
		return self.high_scores

	



class ScoreStore(object):
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


if __name__ == '__main__':
	t = TwitterScoreStore()
	t.increment()
	t.increment()
	t.increment()
	t.increment()
	t.set_high_score()
	print(t.get_high_scores())
