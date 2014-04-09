from util import util
from collections import defaultdict

class characterAPI:
	def __init__(self,name):
		self.superheroname = name
		self.featuresDictionary = defaultdict()
	
	def setupFeatures(self):
		base = util("characters",["aliases","birth","character_enemies","character_friends","count_of_issue_appearances","creators","description","gender","id","powers","real_name","movies","name","origin"])
		self.featuresDictionary = base.getFeatures(self.superheroname)

	def get_aliases (self):
		a = self.featuresDictionary["results"]["aliases"]
		return a

	def get_birth(self):
		a = self.featuresDictionary["results"]["birth"]
		return a

	def get_creators (self):
		a = self.featuresDictionary["results"]["creators"]
		return a

	def get_description (self):
		a = self.featuresDictionary["results"]["description"]
		return a

	def get_gender (self):
		a = self.featuresDictionary["results"]["gender"]
		return a

	def get_id (self):
		a = self.featuresDictionary["results"]["id"]
		return a

	def get_count_of_issue_appearances (self):
		a = self.featuresDictionary["results"]["count_of_issue_appearances"]
		print a
		return a

	def get_movies(self):
		a = self.featuresDictionary["results"]["movies"]
		print a
		return a

	def get_real_name(self):
		a = self.featuresDictionary["results"]["real_name"]
		print a
		return a

	def get_origin(self):
		a = self.featuresDictionary["results"]["origin"]
		print a
		return a		

	def get_enemies (self):
	    enemies = map (lambda x:(x["name"], x["api_detail_url"]), self.featuresDictionary["results"]["character_enemies"])
	    return enemies

	def get_friends (self):
	    friends = map (lambda x:(x["name"], x["api_detail_url"]), self.featuresDictionary["results"]["character_friends"])
	    return friends

	def get_powers(self):
		powers = map (lambda x:(x["name"], x["api_detail_url"]),self.featuresDictionary["results"]["powers"])
		return powers



   