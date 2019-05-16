#############################
# FaceBookImageAction Class #
# by Justin Bodnar          #
#############################
from Reaction import Reaction
import facebook

class FaceBookImageReaction( Reaction ):

	def react( self ):
		# instantiate facebook graph API object
		graph = facebook.GraphAPI( self._api_config["facebook_long_lived_access_token"] )
		graph.put_photo( image=open( self._filename, "rb" ), message=self._caption )
#		print( self._api_config )
#		print( self._filename )
#		print( self._caption )
