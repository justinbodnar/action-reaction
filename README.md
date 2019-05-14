# Action-Reaction V2

A Python script to automate content aggregation and redistribution.

For every action there is an equal and opposite reaction.

Content is taken from a specified source (the action), and sent to a specified platform (the reaction).

# Overview

The /lib/ directory contains the superclasses Action.py and Reaction.py. Specific Actions and Reactions are child classes of these. In this way, new functionality can be written as plugins.

# Action.py Superclass

	def __init__( self, name, log_file_name, api_config_string ):
	def update_log( self ):
	def log( self ):
	def name( self ):
	def api_config( self ):

# Reaction.py Superclass

	def __init__( self, name, api_config_string, filename, caption ):
	def name( self ):
	def api_config( self ):

