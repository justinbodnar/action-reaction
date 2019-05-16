# Action-Reaction V2

A Python script to automate content aggregation and redistribution.

For every action there is an equal and opposite reaction.

Content is taken from a specified source (the Action), and sent to a specified platform (the Reaction).

# Overview

The /lib/ directory contains the superclasses Action.py and Reaction.py. Specific Actions and Reactions are child classes of these. In this way, new functionality can be written as plugins.

# Action.py Superclass

Class Data:
	self._log_file_name	# string representing the name of the log file
	self._name = name	# string representing an arbitrary name
	self._api_config	# dictionary of values from the JSON passed to the constructor
	self._log		# string representing the contents of the log file

	def __init__( self, name, log_file_name, api_config_string ):
The constructor takes in a string for an arbitrary name, a string for the name of the log file (directory not included), and a string of formatted JSON data for the API. The constructor takes the formatted JSON string, and converts it into a dictionary.

	def update_log( self ):
The update_log function simply appends the newest data to the log file. This should be called in the function defined in the child class.

	def log( self ):
	def name( self ):
	def api_config( self ):
These functions are getters, and meant to display the raw strings when debugging or writing new Action modules.

	def act()
A child class needs only to write a single function 'act' to work with the private class variables. This function should return two strings, filename, data, respectively. These two returned strings can be passed directly to the constructor of a Reaction.

# Reaction.py Superclass

Class Data:
	self._name		# string representing an arbitrary name
	self._filename		# string representing the filename of the content
	self._caption		# string representing the caption of the content
	self._api_config	# dictionary of JSON values for the API

	def __init__( self, name, api_config_string, filename, caption )
The constructor takes in a string for an arbitrary name, a string of formattes JSON data for the API, a string for the filename of the content to be uploaded, and a string for any text to be passed along with the content. The JSON data is converted into a dictionary.

	def name( self )
	def api_config( self )
These functions are getters, and meant to display the raw strings when debugging or writing new Reaction modules.

A child class needs only to write a single function 'react' to work with the private class variables.
