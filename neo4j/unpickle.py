import cPickle as pickle

def unpickle(filename):
	f = open(filename,"rb") 
	heroes = pickle.load(f)
	return heroes


