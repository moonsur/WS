import requests
from bs4 import BeautifulSoup as bs
# rurl = 'https://en.wikipedia.org/w/index.php' + \
# '?title=List_of_Game_of_Thrones_episodes&oldid=802553687'
# r = requests.get(rurl)
# print('@'*100)
# content = bs(r.text, 'html.parser')
# #print(content.find('h1').text)
# #print(content.find('div',{'id':'p-logo'}).a.get('title'))
# #for found in content.findAll(['h1','h2']):
#  #   print(found.text)
# episodes = []
# ep_table = content.find_all('table', class_='wikiepisodetable')
# for table in ep_table:
#     headers = []
#     for header in table.find('tr').find_all('th', {'scope':'col'}):
#         headers.append(header.text)
#     for row in table.find_all('tr')[1:]:
#         val = []
#         for col in row.find_all(['th','td']):
#             val.append(col.text)
#         epdict = {}
#         for i in range(len(headers)):
#             epdict.update({headers[i]:val[i]})

#         episodes.append(epdict)

# print(episodes)   
 
#url = 'http://www.webscrapingfordatascience.com/usercheck/'
#url = 'http://www.webscrapingfordatascience.com/referercheck/secret.php'
url = 'http://www.webscrapingfordatascience.com/redirect/'
# my_headers = {
# 'User-Agent': 'Mozilla/10.0 (Windows NT 10.0; Win64; x64)'+\
# 'AppleWebKit/537.36 ' + ' (KHTML, like Gecko) Chrome/61.0.3163.100'+\
# 'Safari/537.36',
# 'Referer':'http://www.webscrapingfordatascience.com/referercheck/',
# }
# r = requests.get(url, headers=my_headers)
# r = requests.get(url, allow_redirects=False)
# print(r.request.headers)
# print(r.headers)
# html_soup = bs(r.text,'html.parser')
# print(html_soup.prettify()) 

######################################
#url = 'http://www.webscrapingfordatascience.com/authentication/'
# url = 'http://www.webscrapingfordatascience.com/cookielogin/'
#url = 'http://www.webscrapingfordatascience.com/cookielogin/secret.php'
# url = 'http://www.webscrapingfordatascience.com/redirlogin/'
# url = 'http://www.webscrapingfordatascience.com/trickylogin/'
# r = requests.get(url)
# my_cookie = r.cookies
# r = requests.post(url, params={'p':'login'}, data={'username':'dummy','password':1234}, allow_redirects=False, cookies=my_cookie)
# my_cookie = r.cookies
# # r = requests.get(url+'secret.php', cookies=my_cookie)
# r = requests.get(url,params={'p':'protected'}, cookies=my_cookie)
# print(r.text)
# print(r.request.headers)
# print(r.headers)

# url = 'http://www.webscrapingfordatascience.com/trickylogin/'
# my_session = requests.Session()
# my_session.headers.update({'User-Agent': 'Chrome!'})
# r = my_session.get(url)
# r = my_session.post(url, params={'p':'login'}, data={'username':'dummy','password':1234})
# r = my_session.get(url,params={'p':'protected'})
# print(r.text)
# print(r.request.headers)
# print(r.headers)


url = 'http://www.webscrapingfordatascience.com/files/kitten.jpg'
r = requests.get(url)
with open('image.jpg','wb') as myfile:
    for chunk in r.iter_content(chunk_size=4096):
        myfile.write(chunk)





