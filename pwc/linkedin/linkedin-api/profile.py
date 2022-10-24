# from linkedin_api import linkedin
from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('monsur.domtech@gmail.com', 'monsur#20')

# GET a profile
profile = api.get_profile('billy-g')
print(profile)

# GET a profiles contact info
contact_info = api.get_profile_contact_info('billy-g')
print(contact_info)

# GET 1st degree connections of a given profile
connections = api.get_profile_connections('1234asc12304')