# System
import csv
import os
import time

# Third-party
import requests

FILENAME = './search.csv'
QUERY = 'language:swift+stars:10..20000+pushed:2016-01-01..2016-03-24'
TOKEN = ''

def main():
    try:
        os.remove(FILENAME)
    except:
        pass
    search()

def search(page=1, count=0):
    url = 'https://api.github.com/search/repositories?sort=stars&page=' + str(page) + '&q=' + QUERY
    headers  = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'token ' + TOKEN}
    response = requests.get(url, headers=headers)
    if response.headers['X-RateLimit-Remaining'] == '0':
        print('===== Rate Limit Exceeded: Wait a minute. =====')
        time.sleep(60)
        search(page, count)
        return
    json = response.json()
    total_count = json['total_count']
    for item in json['items']:
        count += 1
        full_name   = item['full_name']
        html_url    = item['html_url']
        description = item['description']
        stars       = str(item['stargazers_count'])
        print(str(count) + '/' + str(total_count) + ' -> ' + full_name + ': ' + stars)
        with open(FILENAME, 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([full_name, html_url, stars, description])
    if 'rel="next"' in response.headers['Link']:
        search(page + 1, count)
    else:
        print('===== FINISHED =====')

if __name__ == '__main__':
    main()
