import cPickle as pickle
from characterAPI import characterAPI
import urllib

n = 2
with open('heroes_' + str(n) + '.pkl','rb') as f:
    heroes = pickle.load(f)
print len(heroes)

for i,hero in enumerate(heroes):
    print i
    hero_char = characterAPI(urllib.quote(hero[u'name']))
    hero_char.setupFeatures()
    # Add the rest of the attributes that were not fetched previously
    hero['enemies'] = hero_char.get_enemies()
    hero['friends'] = hero_char.get_friends()
    hero['creators'] = hero_char.get_creators()
    hero['issue_credits'] = hero_char.get_issue_credits()
    hero['issues_died_in'] = hero_char.get_issues_died_in()
    hero['powers'] = hero_char.get_powers()
    hero['movies'] = hero_char.get_movies()
    hero['teams'] = hero_char.get_teams()
    hero['team_enemies'] = hero_char.get_team_enemies()
    hero['team_friends'] = hero_char.get_team_friends()
    print 'setup off!'

with open('heroes' + str(n) + '_allfeatures.pkl','wb') as f:
    pickle.dump(heroes,f)
    
print heroes[0].keys()
