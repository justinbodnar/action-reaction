######################
# action-reaction.py #
# by Justin Bodnar   #
######################

from lib.Action import Action
from lib.Reaction import Reaction
from lib.ImgurAction import ImgurAction
from lib.FaceBookImageReaction import FaceBookImageReaction


print( "###########" )
print( "name: " + a.name() )
print( "log: " + a.log() )
print( "api_config: " )
print(  a.api_config() )
print( "###########" )
one, two = a.get_image()
t = FaceBookImageReaction( "ronpaul", rapi, one, two )
t.post_image()
