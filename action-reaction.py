######################
# action-reaction.py #
# by Justin Bodnar   #
######################

from lib.Action import Action
from lib.ImgurAction import ImgurAction

t = ImgurAction( "x", "y", api )

print( "###########" )
print( "name: " + t.name() )
print( "log: " + t.log() )
print( "api_config: " )
print(  t.api_config() )
print( "###########" )
t.get_image()
