import requests
from bs4 import BeautifulSoup

url = 'https://bdnews24.com/'
r = requests.get(url)
#print(r.text)
html_soup = BeautifulSoup(r.content,'html.parser')
#print(html_soup)
test = html_soup.find('h6', class_='headline-m_headline__3_NhV headline-m_dark__en3hW')
print("*********************")
print(test.text)
print("*********************")
#headings = html_soup.select('div',{'data-test-id':'headline'})
headings = html_soup.find_all(['h2','h3','h4','h5','h6'])
#print(headings.prettify())
all_headings = set()
for heading in headings:
    all_headings.add(heading.text)
    #hs = heading.find_all(['h2','h3','h4','h5','h6'])
    #for h in hs:
        #all_headings.add(h.text)

for h in all_headings:
    print(h)    