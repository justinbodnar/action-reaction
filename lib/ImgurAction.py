#####################
# ImgurAction Class #
# by Justin Bodnar  #
#####################
from Action import Action
from imgurpython import ImgurClient
import requests
import random

class ImgurAction( Action ):

	# get a single image
	def get_image( self ):
		# instantiate imgur api object
		try:
			imgur_client = ImgurClient( self._api_config["imgur_client_id"], self._api_config["imgur_client_secret"] )
		# catch errors
		except Exception as e:
			print( "Error instantiating Imgur API object" )
			print( e )
		# get list of all images in this album
		urls = []
		for image in imgur_client.get_album_images( self._api_config["imgur_album_id"] ):
			urls = urls + [ str( image.link ) ]
		attempts = 0
		url = random.choice( urls )
		while attempts < 50:
			if url in self._log:
				url = random.choice( urls )
				attempts = attempts + 1
			else:
				break
		# download the image
		r = requests.get( url, allow_redirects=True )
		filename = "./tmp/" + url.split("/")[-1]
		file = open( filename, 'wb' ).write( r.content )
		# update the logfile
		self._log = self._log + "\n" +  url
		self.update_log( )
		return filename, ""
