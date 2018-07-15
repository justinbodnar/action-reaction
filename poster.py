# -*- coding: utf-8 -*-

# this python file contains the code to automate a social media cluster
# all content is scraped from reddit

import youtube_dl
import twitter
import time
import facebook
import os
import praw
import bs4
import requests
import random
import urllib
from fake_useragent import UserAgent
from imgurpython import ImgurClient
import ConfigParser

# these are black listed words
badwords = [ ]

##########################################
# print all albums and album_ids for a username
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
			graph.put_photo(image=open( filename, 'rb'), message = text)
		except Exception as e:
			print( e )
	elif str(config.get(section,"scrape_video")) is "1":
		if verbose:
			print( "Video is about to be posted" )
	try:
		# get facebook page id
		fbPageID = config.get(section, "facebook_page_id")
		url="https://graph-video.facebook.com/" + fbPageID + "/videos?access_token="+config.get(section,"facebook_long_lived_access_token")+'&title='+text2+'&description='+text
		if verbose:
			print( url )
		files = {'file':open(filename,'rb')}
		flag = requests.post(url, files=files).text
	except Exception as e:
		print( e )
	if verbose:
		print( "Flag: " + flag )
		print( "Posted to " + section + "'s FaceBook at " + str( time.time()) )
		print( "Text: " + text )
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
			print( "Text: " + text )
			print( "Filename: " + filename )
	except Exception as e:
		print( e )

##################################################
# function to grab pic/vid and title from reddit #
def grabData( verbose, picorvid, config, section, reddit ):

	if verbose:
		print( "Entering grabData function." )

	# get logfile path
	log_file = "./logs/" + section + ".txt"

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
		submissions0 = reddit.subreddit(config.get( section, "subreddits")).hot(limit=250)
		if verbose:
			print( "Subreddits: " + config.get( section, "subreddits" ) )
		submissions = []
		for submission in submissions0:
#			print( submission )
			submissions.append( submission )
		if verbose:
			print( str(len(submissions)) + " submissions scraped." )

		# loop through submission options
		notDone = True
		for submission in submissions:
			if notDone:

				# if we're looking for videos, skip non video entries
				try:
					if picorvid is 2:
						if verbose:
							print( submission.url )
						if submission.url[8:9] != "v":
							continue
					if verbose:
						print( "Checking submission: " + str(submission.title) )
					badWord = False
					global badwords
					for badword in badwords:
						if badword in submission.title:
							if verbose:
								print( "Found a bad word" )
							badWord = True
					if badWord:
						if verbose:
							print( "Skipping" )
						continue
					# check log for duplicates
					if submission.title in open( log_file, "r" ).read():
						if verbose:
							print( "Found duplicate, skipping." )
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
							print( submission.url )
							print( "Downloaded image: " + filename )
						notDone = False
					elif picorvid is 2:
						ydl_opts = {}
						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download( [submission.url] )
							for file in os.listdir("./" ):
								if ".mp4" in file:
									filename = file
								if verbose:
									print( "Downloaded video: " + filename )
						notDone = False
					else:
						filename = "ERROR"
					if verbose:
						print( "Scraped submission: " + submission.title )
					return submission.title, filename
				except Exception as e:
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
			return "", filename
		except Exception as e:
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

	verbose = False

	config = ConfigParser.ConfigParser()
	config.read( "config.ini" )

	# load blacklist
	global badwords
	raw_blacklist = config.get( "words", "blacklist" )
	badwords = raw_blacklist.split( "," )

	# load configuration for reddit client objects
#	config = ConfigParser.ConfigParser()
	try:
#		config.read( "config.ini" )
		reddit_client_id = config.get( "reddit", "reddit_client_id" )
		reddit_client_secret = config.get( "reddit", "reddit_client_secret" )
		reddit_username = config.get( "reddit", "reddit_username" )
		reddit_password = config.get( "reddit", "reddit_password" )
		reddit = praw.Reddit( client_id=reddit_client_id, client_secret=reddit_client_secret, password=reddit_password, user_agent=UserAgent().random, username=reddit_username )
	except Exception as e:
		if verbose:
			print( "Error instantiating Reddit client object." )
			print( "If you're not using Reddit as a source, you can ignore this." )
		print( e )
		exit()

	# loop through accounts in config file
	for section in config.sections():

		if verbose:
			print( "Current config.ini section: " + section )

		#################################################
		# check if this entry is enabled #
		try:
			if config.get( section, "on" ) is "0":
				if verbose:
					print( "Section set to \"off.\" Skipping." )
				continue
		except Exception as e:
			if verbose:
				print( e )
				continue

		try:
			# grab the image/video
			if str( config.get( section, "scrape_image" ) ) is "1":
				data_type = 1
				if verbose:
					print( "Scraping image for " + section + "." )
			elif str( config.get( section, "scrape_video" ) ) is "1":
				data_type = 2
				if verbose:
					print( "Scraping video for " + section + "." )
			title, filename = grabData( verbose, data_type, config, section, reddit )
			if verbose:
				print( "Text returned from grabData function: " + title )

			# post to FaceBook or Twitter
			if str(config.get(section,"post_to_facebook")) is "1":
				if verbose:
					print( "Passing to function the text: " + title )
				postToFaceBook( verbose, config, section, title, filename )
			if str(config.get(section,"post_to_twitter")) is "1":
				if verbose:
					print( "Passing to function the text: " + title )
				postToTwitter( verbose, config, section, title, filename )
		except Exception as e:

			# all errors are caught and printed within functions
			x = 1
#			print( e )

main()
# remove all files downloaded during the program's run
# this line has only been tested on Ubuntu
os.system( "rm $(ls -I \"*.ini\" -I \"*.py\" -I \"*.md\" )" )
