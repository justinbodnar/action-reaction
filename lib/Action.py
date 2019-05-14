######################
#  Action-Reaction   #
#                    #
# Action Super Class #
# By Justin Bodnar   #
######################

import json

class Action:

	###############
	# constructor #
	###############
	def __init__( self, name, log_file_name, api_config_string ):
		self._log_file_name = "./logs/" + log_file_name
		self._name = name
		self._api_config = json.loads( api_config_string )
		self._text = "Text not yet set."
		self._data = "Data not yet set."
		# try to open the log file
		try:
			self._log = open( self._log_file_name, "r+" ).read()
		# if it doesn't exist, create it
		except Exception as e:
			print( e )
			print( "Logfile not found.... creating one." )
			self._log = open(  self._log_file_name, "w+" ).read()

	##################
	# update logfile #
	##################
	def update_log( self ):
		# attempt to open our log file
		try:
			log_file = open( self._log_file_name, "w+" )
			log_file.write( self._log )
		except Exception as e:
			print( "Error opening logfile. Log file NOT updated." )
			print( e )

	###########
	# getters #
	###########
	def log( self ):
		return self._log
	def name( self ):
		return self._name
	def api_config( self ):
		return self._api_config
