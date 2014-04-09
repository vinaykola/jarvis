from util import util
from characterAPI import characterAPI

character = characterAPI("Superman")
character.setupFeatures()
aliases = character.get_aliases()
birth = character.get_birth()
powers = character.get_powers()
for word in powers:
	print word



