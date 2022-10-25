# from linkedin_api import linkedin
from linkedin_api import Linkedin
import json

# Authenticate using any Linkedin account credentials
api = Linkedin('monsur.domtech@gmail.com', 'monsur#20')

# GET a profile
# profile = api.get_profile('billy-g')
profile = api.get_profile('samsul-alam-stp')

# parsed = json.loads(profile)
print(json.dumps(profile, indent=4))
# print(profile)

# GET a profiles contact info
contact_info = api.get_profile_contact_info('samsul-alam-stp')
print(contact_info)

# GET 1st degree connections of a given profile
# connections = api.get_profile_connections('ACoAAAftUf0BwEkGtth3FcyLRpl1ePpWei5aYQE')
# print(connections)

network = api.get_profile_network_info('samsul-alam-stp')
print(json.dumps(network, indent=4))