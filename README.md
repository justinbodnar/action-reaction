# Action-Reaction
A Python script to automate content aggregation and redistribution.

Content is taken from a specified source (the action), and sent to a specified platform (the reaction).

# Actions:

Imgur albums

Subreddits

MySQL Databases

# Reactions:

FaceBook

Twitter

WordPress (self-hosted)

# Getting Started

pip install -r requirements.txt

The config.ini includes a template to start with. Variables use 1 or 0 as True or False.

Add relevant API tokens.

Add a SINGLE action source by setting its variable to 1

Add any number of reactions by setting their variables to 1

Run the program once with: python action-reaction.py

For best automation set a cronjob to run Action-Reaction.
