import requests
from bs4 import BeautifulSoup
import pprint


def read_pages(base_url):
    hn=[]
    for page in range(1, 3): 
        res = requests.get(f'{base_url}?p={page}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titleline') 
        subtext = soup.select('.subtext')
        hn.extend(create_custom_hn(links, subtext))
    return sort_stories_by_votes(hn)


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links): 
        title = item.getText()
        href = item.a.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})

    return hn


pprint.pprint(read_pages('https://news.ycombinator.com/'))
