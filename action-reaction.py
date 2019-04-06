# -*- coding: utf-8 -*-
#
# action-reaction.py
#
# this python file contains the code to automate a social media cluster

import youtube_dl
import twitter
import time
import facebook
import os
import subprocess
import praw
import bs4
import requests
import random
import urllib
import ConfigParser

from fake_useragent import UserAgent
from imgurpython import ImgurClient
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc import WordPressPage
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

# verbose is global
verbose = True

######################################################################
# class for posting to WordPress                                     #
# https://gist.github.com/345161974/63573abdf1dc9c303d6740fb29496657 #
######################################################################
class Custom_WP_XMLRPC:
	def post_article(self,wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,PhotoUrl):
		self.path=os.getcwd()+"\\00000001.jpg"
		self.articlePhotoUrl=PhotoUrl
		self.wpUrl=wpUrl
		self.wpUserName=wpUserName
		self.wpPassword=wpPassword
		#Download File
		f = open(self.path,'wb')
		f.write(urllib.urlopen(self.articlePhotoUrl).read())
		f.close()
		#Upload to WordPress
		client = Client(self.wpUrl,self.wpUserName,self.wpPassword)
		filename = self.path
		# prepare metadata
		data = {'name': 'picture.jpg','type': 'image/jpg',}

		# read the binary file and let the XMLRPC library encode it into base64
		with open(filename, 'rb') as img:
			data['bits'] = xmlrpc_client.Binary(img.read())
		response = client.call(media.UploadFile(data))
		attachment_id = response['id']
		#Post
		post = WordPressPost()
		post.title = articleTitle
		post.content = articleContent
		post.terms_names = { 'post_tag': articleTags,'category': articleCategories}
		post.post_status = 'publish'
		post.thumbnail = attachment_id
		post.id = client.call(posts.NewPost(post))
		print 'Post Successfully posted. Its Id is: ',post.id

def cleardir():
	os.system( "rm -f $(ls -I \"*.ini\" -I \"logs\" -I \"*.py\" -I \"*.md\")" )
	# why is this line here?
#	os.system( "for f in *; do mv \"$f\" `echo $f | tr ' ' '_'`; done" )

##########################
# post data to WordPress #
def postToWordPress(  verbose, config, section, title, filename ):
	if verbose:
		print( "Entering post to WordPress function." )
	wordpress_url = config.get( "wordpress", "url" )
	wordpress_username = config.get( "wordpress", "username" )
	wordpress_password = config.get( "wordpress", "password" )
	if verbose:
		print( "WordPress URL:  " + wordpress_url )
		print( "WordPress user: " + wordpress_username )
	try:
		xmlrpc_object = Custom_WP_XMLRPC( )
		xmlrpc_object.post_article( wordpress_url, wordpress_username, wordpress_password, title, "", " ", " ", filename )
	except Exception as e:
		cleardir()
		print( e )


#################################################
# print all albums and album_ids for a username #
def print_all_albums( client, username ):
        for album in client.get_account_albums(username):
                album_title = album.title if album.title else 'Untitled'
                print( "Album: " + album_title + ", " + album.id )

###########################################
# get all image links from an imgur album #
def all_images_from_imgur_album( imgur_client, imgur_album_id ):
        urls = []
        for image in imgur_client.get_album_images( imgur_album_id ):
                 urls = urls + [ str(image.link) ]
        return urls

#################################################
# return a random image url from an imgur album #
def random_image_from_imgur_album( imgur_client, imgur_album_id ):
        return random.choice( all_images_from_imgur_album( imgur_client, imgur_album_id ) )

##############################################
# function to post to a FaceBook "Like" page #
def postToFaceBook( verbose, config, section, text, filename ):
	if verbose:
		print( "Begining postToFaceBook function." )
	# check if the title is being posted
	if str(config.get(section,"scrape_title")) is "0":
		text2 = ""
	else:
		text2 = text
	# check if its a picture or video being posted
	if str(config.get(section,"scrape_image")) is "1":
		if verbose:
			print( "Image is about to be posted." )
#			print( "Token: " + config.get(section, "facebook_long_lived_access_token" ) )
		try:
			graph = facebook.GraphAPI( config.get( section, "facebook_long_lived_access_token" ) )
			graph.put_photo(image=open( filename, 'rb'), message = text2)
		except Exception as e:
			cleardir()
			print( e )
	elif str(config.get(section,"scrape_video")) is "1":
		if verbose:
			print( "Video is about to be posted" )
		try:
			# get facebook page id
			fbPageID = config.get(section, "facebook_page_id")
#			text2 = ""
			url="https://graph-video.facebook.com/" + fbPageID + "/videos?access_token="+config.get(section,"facebook_long_lived_access_token")+'&title='+text2+'&description='+text2
			if verbose:
				print( url )
			files = {'file':open(filename,'rb')}
			flag = requests.post(url, files=files).text
			if verbose:
				print( flag )
		except Exception as e:
			cleardir()
			print( e )
	if verbose:
		print( "Posted to " + section + "'s FaceBook at " + str( time.time()) )
#		print( "Text: " + text )
                print( "Filename: " + filename )

###############################
# function to post to Twitter #
def postToTwitter( verbose, config, section, text, filename ):
	try:
		if verbose:
			print( "Begining postToTwitter function." )
			print( "Text passed: " + text )
		# check if the title is being posted
		if str(config.get(section,"scrape_title")) is "0":
			text = ""
		tweeter = twitter.Api( consumer_key=config.get( section, "twitter_consumer_key"), consumer_secret=config.get(section, "twitter_consumer_secret"), access_token_key=config.get( section, "twitter_access_token_key"), access_token_secret=config.get( section, "twitter_access_token_secret" ) )
		tweeter.PostUpdate( status=unicode( text ), media=filename )
		if verbose:
			print( "Posted to " + section + "'s Twitter at " + str(time.time()) )
#			print( "Text: " + text )
			print( "Filename: " + filename )
	except Exception as e:
		cleardir()
		print( e )

##################################################
# function to grab pic/vid and title from reddit #
def grabData( verbose, picorvid, config, section, reddit ):

	if verbose:
		print( "Entering grabData function." )
		cleardir()

	# get logfile path
	log_file = "./logs/" + section + ".txt"

	# special case for ajh
	if section == "ajhydellwp" or section == "ajhydelltw":
		if verbose:
			print( "Using AJHFB log for AJHWP." )
		log_file = "./logs/ajhydellfb.txt"

	# if log file doesn't exist, lets just make one
	f = open(log_file, "a")
	f.close()
	if verbose:
		print( "Logfile: " + log_file )

	# grab submissions
	# check if we're using Reddit
	if config.get( section, "use_reddit" ) is "1":
		if verbose:
			print( "Begining scrape of Reddit." )
		submissions0 = reddit.subreddit(config.get( section, "subreddits")).hot(limit=500)
		if verbose:
			print( "Subreddits: " + config.get( section, "subreddits" ) )
		submissions = []
		for submission in submissions0:
#			print( submission )
			submissions.append( submission )
#		if verbose:
#			print( str(len(submissions)) + " submissions scraped." )

		# loop through submission options
		notDone = True
		for submission in submissions:
			if notDone:

				# if we're looking for videos, skip non video entries
				try:
					if picorvid is 2:
#						if verbose:
#							print( submission.url )
						if submission.url[8:9] != "v":
							continue
#					if verbose:
#						print( "Checking submission: " + str(submission.title) )
					badWord = False
					global badwords
					for badword in badwords:
						if badword in submission.title:
#							if verbose:
#								print( "Found a bad word" )
							badWord = True
					if badWord:
#						if verbose:
#							print( "Skipping" )
						continue
					# check log for duplicates
					if submission.title in open( log_file, "r" ).read():
#						if verbose:
#							print( "Found duplicate, skipping." )
						continue
					else:
						if verbose:
							print( "Adding entry to log." )
						log = open( log_file, "a+" )
						log.write( submission.title )
						log.close()
					# download the image or video
					# 1 implies picture, 2 implies video
					if picorvid is 1:
						r = requests.get( submission.url, allow_redirects=True)
						filename = submission.url.split("/")[-1]
						file = open( filename, 'wb' ).write( r.content )
						if verbose:
							print( "Downloaded image: " + filename )
						notDone = False
					elif picorvid is 2:
						ydl_opts = {}
						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download( [submission.url] )
							vid_count = 0
							for file in os.listdir("./" ):
								if ".mp4" in file:
									filename = file
									vid_count = vid_count + 1
									if verbose:
										print( "Downloaded video: " + filename )
							print( "A total of " + str( vid_count ) + " videos were found in the directory..." )
						notDone = False
					else:
						filename = "ERROR"
					if verbose:
						print( "Scraped submission: " + submission.title )
					return submission.title, filename, submission.url
				except Exception as e:
					cleardir()
					if verbose:
						print( e )

	# check if we're using imgur
	elif config.get( section, "use_imgur" ) is "1":
		if verbose:
			print( "Begining scrape of Imgur." )
		# gather imgur configuration information
		imgur_album_id = config.get( section, "imgur_album" )
		imgur_username = config.get( "imgur", "imgur_username" )
		imgur_client_id = config.get( "imgur", "imgur_client_id" )
		imgur_client_secret = config.get( "imgur", "imgur_client_secret" )
		# instantiate imgur client object
		if verbose:
			print( "Instantiating Imgur client." )

		try:
			imgur_client = ImgurClient( imgur_client_id, imgur_client_secret )
			if verbose:
				print( "Imgur object instantiated." )
			# grab a random image from our album
			# loop until we find an image we haven't used recently
			while True:
				random_image_url = random_image_from_imgur_album( imgur_client, imgur_album_id )
				# check log for duplicates
				if random_image_url in open( log_file, "r" ).read():
					if verbose:
						print( "Found duplicate, skipping." )
						continue
				else:
					if verbose:
						print( "Adding entry to log." )
					log = open( log_file, "a+" )
					log.write( random_image_url + "\n" )
					log.close()
					break

			# let's see if it's time to empty out log file
			num_lines = sum(1 for line in open( log_file ) )
			if verbose:
				print( "Number of lines in " + log_file + ": " + str( num_lines ) )
			if num_lines > 99:
				if verbose:
					print( "Clearing " + log_file )
				log = os.remove( log_file )

			if verbose:
				print( "Random URL: " + random_image_url )
			r = requests.get( random_image_url, allow_redirects=True)
			filename = random_image_url.split("/")[-1]
			file = open( filename, 'wb' ).write( r.content )
			if verbose:
				print( "Downloaded image: " + filename )
			return "", filename, ""
		except Exception as e:
			cleardir()
			print( e )
			return -1

	# if we get here, there's an error in the config.ini file
	# return a -1 error code
	else:
		if verbose:
			print( "ERROR! The config file doesn't specify a content source." )
		return -1

#################
# main function #
def main():

	global verbose

	config = ConfigParser.ConfigParser()
	config.read( "config.ini" )

	# load blacklist
	global badwords
	raw_blacklist = config.get( "words", "blacklist" )
	badwords = raw_blacklist.split( "," )

	# load configuration for reddit client objects
	try:
		reddit_client_id = config.get( "reddit", "reddit_client_id" )
		reddit_client_secret = config.get( "reddit", "reddit_client_secret" )
		reddit_username = config.get( "reddit", "reddit_username" )
		reddit_password = config.get( "reddit", "reddit_password" )
		reddit = praw.Reddit( client_id=reddit_client_id, client_secret=reddit_client_secret, password=reddit_password, user_agent=UserAgent().random, username=reddit_username )
	except Exception as e:
		cleardir()
		if verbose:
			print( "Error instantiating Reddit client object." )
			print( "If you're not using Reddit as a source, you can ignore this." )
		print( e )
		exit()

	# loop through accounts in config file
	for section in config.sections():

		if verbose:
			print
			print( "##########################" )
			print( "Current config.ini section: " + section )

		#################################################
		# check if this entry is enabled #
		try:
			if config.get( section, "on" ) is "0":
				if verbose:
					print( "Section set to \"off.\" Skipping." )
				continue
		except Exception as e:
			cleardir()
			if verbose:
#				print( e )
				continue

		try:
			# scrape data
			if str( config.get( section, "scrape_image" ) ) is "1":
				data_type = 1
				if verbose:
					print( "Scraping image for " + section + "." )
			elif str( config.get( section, "scrape_video" ) ) is "1":
				data_type = 2
				if verbose:
					print( "Scraping video for " + section + "." )
			title, filename, url = grabData( verbose, data_type, config, section, reddit )
			if verbose:
				print( "Text returned from grabData function: " + title )

			# if posting to facebook
			if str(config.get(section,"post_to_facebook")) is "1":
				if verbose:
					print( "Posting to FaceBook." )
					print( "Passing to function the text: " + title )
				postToFaceBook( verbose, config, section, title, filename )
			if str(config.get(section,"post_to_twitter")) is "1":
			# if posting to twitter
				if verbose:
					print( "Posting to Twitter." )
					print( "Passing to function the text: " + title )
				postToTwitter( verbose, config, section, title, filename )
			# if posting to wordpress
			if str(config.get(section,"post_to_wordpress")) is "1":
				if verbose:
					print( "Posting to WordPress." )
					print( "Passing to function the text: " + title )
				postToWordPress( verbose, config, section, title, url )
		# catch exceptions
		except Exception as e:
			cleardir()
			print( e )

main()

