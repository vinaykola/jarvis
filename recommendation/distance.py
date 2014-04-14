from __future__ import division
from characterAPI import characterAPI
import cPickle as pickle


# Features of a character:
# * Aliases
# * Birth
# * Character Enemies
# * Character Friends
# * Count of Issue appearances
# * Creators
# * Description
# * Gender
# * ID
# * Image
# * Issue Credits
# * Issues Died in
# * Powers
# * Real Name
# * Movies
# * Name
# * Origin
# * Publisher
# * Teams
# * Team Enemies
# * Team Friends

# Testing code
def main():

    names = ['Superman', 'Batman']

    supes = characterAPI("Superman")
    bats = characterAPI("Batman")

    for man in [supes,bats]:
        man.setupFeatures()

    batman = {}
    superman = {}

    for man, man_char in zip([batman,superman],[bats,supes]):
        man['aliases'] = man_char.get_aliases()
        man['birth'] = man_char.get_birth()
        man['enemies'] = man_char.get_enemies()
        man['friends'] = man_char.get_friends()
        man['count_of_issue_appearances'] = man_char.get_count_of_issue_appearances()
        man['creators'] = man_char.get_creators()
        man['description'] = man_char.get_description()
        man['gender'] = man_char.get_gender()
        # issue credits. add later
        # issues died in?
        # 
        man['powers'] = man_char.get_powers()
        man['movies'] = man_char.get_movies()
        man['origin'] = man_char.get_origin()
        
        man['publisher'] = man_char.get_publisher()
        #man['story_arc_credits'] = man_char.get_story_arc_credits()
        man['teams'] = man_char.get_teams()
        man['team_enemies'] = man_char.get_team_enemies()
        man['team_friends'] = man_char.get_team_friends()

    with open('batman.pkl','wb') as f_man:
        pickle.dump(batman,f_man)
        #batman = pickle.load(f_man)
    
    with open('superman.pkl','wb') as f_man:
        pickle.dump(superman,f_man)
        #superman = pickle.load(f_man)

    
    print distance(batman,superman)

# Returns Jacard similarity coefficient
def list_similarity(list1,list2):
    set1,set2 = set(list1),set(list2)
    
    n = len(set1.intersection(set2))
    return n / (len(set1) + len(set2) - n) 
    
def numeric_distance(char1,char2):
    pass

def get_description_distance(desc1,desc2):
    return 1

# Returns 1 if it matches, 0 if it doesn't
def get_mismatch(g1,g2):
    if g1 == g2:
        return 0
    else:
        return 1

# For now, implementing using Python dicts till feature space is fixed.
# Have to transition to numpy for speed.

def distance(char1, char2):
    # TODO: Should I add "count_of_issue_appearances"?
    features = ['friends','enemies','creators','description','gender','powers','movies','origin','publisher','teams','team_enemies','team_friends']

    weights = {}
    for feature in features:
        weights[feature] = 1.0

    dist  = 0
        
    distances = {}
            
    distances['friends'] = 1 - list_similarity(char1['friends'],char2['friends'])
    distances['enemies'] = 1 - list_similarity(char1['enemies'],char2['enemies'])
    distances['creators'] = 1 - list_similarity(char1['creators'],char2['creators'])
    distances['description'] = get_description_distance(char1['description'], char2['description'])
    distances['gender'] = get_mismatch(char1['gender'],char2['gender'])
    distances['powers'] = 1 - list_similarity(char1['powers'],char2['powers'])
    distances['movies'] = 1 - list_similarity(char1['movies'],char2['movies'])
    distances['origin'] = get_mismatch(char1['origin'],char2['origin'])
    distances['publisher'] = get_mismatch(char1['publisher'],char2['publisher'])
    distances['teams'] = 1 - list_similarity(char1['teams'],char2['teams'])
    distances['team_enemies'] = 1 - list_similarity(char1['team_enemies'],char2['team_enemies'])
    distances['team_friends'] = 1 - list_similarity(char1['team_friends'],char2['team_friends'])

    for features in features:
        dist += distances[feature] * weights[feature]
    
    return dist

if __name__ == '__main__':
    exit (main())
