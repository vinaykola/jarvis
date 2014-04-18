import pickle
import urllib2 as ulib2
from BeautifulSoup import BeautifulSoup as bs

def get_heroes():
	#return pickle.load(open('heroes_100.pkl'))
	return ["Batman"]

list_of_heroes=get_heroes()

for hero in list_of_heroes:
	url = 'http://dc.wikia.com/wiki/'+hero+'_Recommended_Reading'
	soup = bs(ulib2.urlopen(url).read())
	for header in soup.findAll('h2'):
		print '\n'+header.text
		for item in header.findNextSiblings()[0].findAll('li'):
			print item.a.text

#soup.findAll('h2')[0].findNextSiblings()[0].findAll('li')[0].a.text

