from bs4 import BeautifulSoup
import requests

url = 'http://www.webscrapingfordatascience.com/postform3/'
r = requests.get(url)
html_soup = BeautifulSoup(r.text,'html.parser')
pval = html_soup.find('input',{'name':'protection'}).get('value')
#print(r.text)
formdata = {
'name': 'Seppe',
'gender': 'M',
'pizza': 'like',
'haircolor': 'brown',
'comments': '',
'protection':pval,
}
rp = requests.post(url, data=formdata)
print(rp.text)