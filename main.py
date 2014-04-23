from util import util
from characterAPI import characterAPI

character = characterAPI("superman")
character.setupFeatures()
#character.setUpFeatures("http://www.comicvine.com/api/characters?api_key=37a0f6cdbe5752b2f272373ba6a21491ea2629eb&filter=name:Superman&format=json")
aliases = character.get_aliases()
birth = character.get_birth()
powers = character.get_powers()
for word in powers:
	print word



