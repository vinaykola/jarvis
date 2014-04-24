import cPickle as pickle

def unpickle(filename):
	f = open(filename,"rb") 
	heroes = pickle.load(f)
	return heroes

a = unpickle('heroes788_allfeatures_56000.pkl')

print a[4000]['publisher']['name']
