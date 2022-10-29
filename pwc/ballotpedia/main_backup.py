import requests
from bs4 import BeautifulSoup

base_url = 'https://ballotpedia.org'
my_headers = {
'User-Agent': 'Mozilla/10.0 (Windows NT 10.0; Win64; x64)'+\
'AppleWebKit/537.36 ' + ' (KHTML, like Gecko) Chrome/61.0.3163.100'+\
'Safari/537.36',
}
url = 'https://ballotpedia.org/Elections_by_state_and_year'
r = requests.get(url, headers=my_headers)
content = BeautifulSoup(r.text, 'html.parser')
body_content = content.select_one('div.mw-parser-output')
all_h2 = body_content.find_all('h2')
for h2 in all_h2:
    if h2.text.isnumeric():
        print(h2.text)
        elections_by_state = h2.find_next_sibling("p")
        if not elections_by_state is None:
            all_state = elections_by_state.find_all('a')
            for state in all_state:
                state_election_url = base_url + state['href']
                print(state.text,' = ', state_election_url)
            # break
        else:
            print('information hidden')
            print(h2.text)
            hidden_div = h2.find_next_sibling("div") 
            print(hidden_div.text)
            hidden_elections_by_state = hidden_div.select_one('table>tbody>tr[2]>td>p[1]')  
            if not hidden_elections_by_state is None:
                print(hidden_elections_by_state.text)
            else:
                print('target value not found')        