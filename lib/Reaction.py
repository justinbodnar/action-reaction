########################
#   Action-Reaction    #
#                      #
# Reaction Super Class #
#   By Justin Bodnar   #
########################

import json

class Reaction:

	###############
	# constructor #
	###############
	def __init__( self, name, api_config_string, filename, caption ):
		self._name = name
		self._filename = filename
		self._caption = caption
		self._api_config = json.loads( api_config_string )
		self._text = "Text not yet set."
		self._data = "Data not yet set."

	###########
	# getters #
	###########
	def name( self ):
		return self._name
	def api_config( self ):
		return self._api_config
