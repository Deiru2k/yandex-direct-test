from tornado_resource.router import Router
from resources import auth, campaigns

v1 = Router(version="v1")

# Auth and Login
v1.add_resource(auth.Auth)
v1.add_resource(auth.Login)
v1.add_resource(campaigns.UserCampaignArchive)
v1.add_resource(campaigns.UserCampaignStop)
v1.add_resource(campaigns.UserCampaign)
v1.add_resource(campaigns.UserCampaignList)
