# reddit-to-facebook-and-twitter
A Python script to scrape subreddits and post image or video content to Twitter and FaceBook accounts.

After months of writing new python scripts to automate FaceBook and Twitter pages, I found myself staring at a directory of python files. Enough was enough, and I decided to write a single script to read a configuration file where a single entry can be used to determine what's to be scraped, how it's to be scraped, and where it's to be posted to.

The script allows the user to automate the scraping of content from subreddits (both images and videos, with or without post title), and the posting of the submissions to a FaceBook "like" page or Twitter account. The design allows the user to easily add new entries to the configuration file, which the main script reads as instructions. The script iterates through the config.ini file, and follows the instructions for each entry. Example configuration entries are included in the default config.ini.

The config.ini is self explanatory, and uses 1 or 0 as True or False.
