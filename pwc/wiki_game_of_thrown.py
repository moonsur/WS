import requests
from bs4 import BeautifulSoup as bs

rurl = 'https://en.wikipedia.org/w/index.php' + \
'?title=List_of_Game_of_Thrones_episodes&oldid=802553687'
r = requests.get(rurl)
html_soup = bs(r.content, 'html.parser')
"""
Getting all anchor text and url.
"""
a_list = []
all_a = html_soup.find_all('a')
#for a in all_a: 
    #hrf = str(a.get('href'))
    #if 'https://en.wikipedia.org' not in hrf:
     #   hrf = 'https://en.wikipedia.org' + hrf

    #a_list.append((a.text,hrf))

#print(a_list) 
"""
Download all images from the page
"""


# import os.path as path
# img_list = []
# all_img = html_soup.find_all('img')
# dir_name = r"C:\Users\monsu\WS\pwc\images"
# for image in all_img:
#     print(image.get('alt'),"=>",image.get('src')) 
#     lnk = str(image.get('src'))
#     if 'https' not in lnk and 'wikimedia.org' not in lnk:
#         lnk = 'https://en.wikipedia.org'+lnk   
#     elif 'https' not in lnk and 'wikimedia.org' in lnk:
#         lnk = 'https:'+lnk
#     print(lnk)
#     if '.png' in lnk: 
#         complete_path = path.join(dir_name,path.basename(lnk))        
#         print(complete_path)
#         with open(complete_path,'wb') as f:
#             f.write(requests.get(lnk).content)



# Scrape Navigation pannel

# first_nav = html_soup.select_one('nav#p-navigation')
# print(first_nav.find('h3').text)
# links = first_nav.select('div>ul>li>a')
# for link in links:
#     print(link.text,'=>',link.get('href'))
# navs = first_nav.find_next_siblings('nav')
# for nav in navs[:-1]:    
#     links = nav.select('div>ul>li>a')
#     if len(links) != 0:
#         print(nav.select_one('h3').text)
#         for link in links:
#             print(link.text, '=>',link.get('href'))

for link in html_soup.select('ol.references cite a[href]'):
    print(link.get('rel'))