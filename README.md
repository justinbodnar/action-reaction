# Action-Reaction

A Python script to automate content aggregation and redistribution.

For every action there is an equal and opposite reaction.

Content is taken from a specified source (the action), and sent to a specified platform (the reaction).

# Getting Started

pip install -r requirements.txt

The config.ini includes a template to start with. Variables use 1 or 0 as True or False.

Add relevant API tokens.

Add a SINGLE action source by setting its variable to 1

Add any number of reactions by setting their variables to 1

Run the program once with: python action-reaction.py

For best automation set a cronjob to run Action-Reaction.

# Actions

Imgur: ( Keys available at https://api.imgur.com/oauth2/addclient ) Enabled by setting "use_img" to 1 in config.ini. Oauth authentication information is stored in the "imgur" section of config.ini. Uses the "imgur_album" variable to pull a random image from the album. Logs ensure an image must wait 50 turns before being reused.

NewsAPI: ( Keys available at https://newsapi.org ) Enabled by setting "use_newsapi" to 1 in config.ini. Uses the "queries" variable in config.ini to grab recent headlines. Currently only works with the FaceBook reaction.

Reddit: Enabled by setting "use_reddit" to 1 in config.ini. Reddit API credentials are stored in the "reddit" section. Uses the "subreddits" variable as a list to pull 300  "hot" threads, and post one. Can be set to grab image threads or video threads. Logs ensure content is never shared twice.

MySQL: TBA. Currently in development branch.

# Reactions

FaceBook: Enabled by setting "post_to_facebook" to 1 in config.ini. FaceBook Graph API tokens and FaceBook Page ID stored in config.ini. Can post images, videos, and links with preview.

Twitter: Enabled by setting "post_to_twitter" to 1 in config.ini. Twitter API tokens are set in config.ini. Currently only accepts images.

WordPress: Enabled by setting "post_to_wordpress" to 1 in config.ini. Uses XML-RPC to post images to WordPress installations. Login credentials to WordPress and the url to your xmlrpc.php file (http://WORDPRESS_URL/xmlrpc.php) in the "wordpress" section of config.ini. Currently only accepts images.

# Blacklisted Word

The "words" section of config.ini contains a single variable "blacklist" as a comma delimited list of strings to avoid in Actions.

# Current List of Valid Combinations

Imgur -> Twitter    (image)

Imgur -> FaceBook   (image)

Imgur -> WordPress  (image)

NewsAPI -> FaceBook (link))

Reddit -> Twitter   (image)

Reddit -> FaceBook  (image)

Reddit -> FaceBook  (video)
