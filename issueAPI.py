from util import util
from collections import defaultdict

class issueAPI:
    def __init__(self,name):
        self.superheroname = name
        self.featuresDictionary = defaultdict()

    # Possibly add "story_arc_credits" and "volume_credits"
    def setupFeatures(self):
        base = util("issues",["name","image"])#,"story_arc_credits"])
        self.featuresDictionary = base.getFeatures(self.superheroname)

    def get_name(self):
        return self.featuresDictionary["results"]["name"]

    def get_image(self):
        return self.featuresDictionary["results"]["image"]
