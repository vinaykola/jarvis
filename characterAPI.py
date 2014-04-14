from util import util
from collections import defaultdict

class characterAPI:
    def __init__(self,name):
        self.superheroname = name
        self.featuresDictionary = defaultdict()
    
    # Possibly add "story_arc_credits" and "volume_credits"
    def setupFeatures(self):
        base = util("characters",["aliases","birth","character_enemies","character_friends","count_of_issue_appearances","creators","description","gender","id","image","issue_credits","issues_died_in","powers","real_name","movies","name","origin","publisher","teams","team_enemies","team_friends"])#,"story_arc_credits"])
        self.featuresDictionary = base.getFeatures(self.superheroname)

    def get_aliases (self):
        a = self.featuresDictionary["results"]["aliases"]
        return a

    def get_birth(self):
        a = self.featuresDictionary["results"]["birth"]
        return a

    def get_creators (self):
        return map( lambda x: (x['name'], x['api_detail_url']), self.featuresDictionary['results']['creators'])

    def get_description (self):
        a = self.featuresDictionary["results"]["description"]
        return a

    def get_gender (self):
        a = self.featuresDictionary["results"]["gender"]
        return a

    def get_id (self):
        a = self.featuresDictionary["results"]["id"]
        return a

    def get_image(self):
        return self.featuresDictionary["results"]["image"]
        
    def get_count_of_issue_appearances (self):
        a = self.featuresDictionary["results"]["count_of_issue_appearances"]
        return a

    def get_issue_credits (self):
        return self.featuresDictionary["results"]["issue_credits"]

    def get_issues_died_in (self):
        return self.featuresDictionary["results"]["issues_died_in"]

    def get_movies(self):
        return map( lambda x: (x['name'], x['api_detail_url']), self.featuresDictionary["results"]["movies"])

    def get_real_name(self):
        a = self.featuresDictionary["results"]["real_name"]
        return a

    def get_origin(self):
        a = self.featuresDictionary["results"]["origin"]
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

    def get_publisher(self):
        return self.featuresDictionary["results"]["publisher"]

    # def get_story_arc_credits(self):
    #   return self.featuresDictionary["results"]["story_arc_credits"]

    def get_teams(self):
        return map( lambda x: (x['name'], x['api_detail_url']), self.featuresDictionary["results"]["teams"])

    def get_team_enemies(self):
        return map( lambda x: (x['name'], x['api_detail_url']), self.featuresDictionary['results']['team_enemies'])

   
