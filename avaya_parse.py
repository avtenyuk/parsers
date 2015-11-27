# coding: utf-8

import time
import json
import re

from grab import Grab
from grab.error import DataNotFound


xpath = {'home_url': 'https://avayacorp.authoria.net/joblist.html?erpc=alljobs',
         'next_page': ".//*[contains(@id,'Next')]/@href",
         'joblist': ".//td[@class='listheadingbackground']/table//tr/td[contains(@class,'listrowbackground')]/span/a",
         'id': ".//span[contains(text(), 'ID')]",
         'function': ".//td[@class='tablebackgroundcolor']/table//tr[6]//tr[1]/td[2]",
         'location': ".//td[@class='tablebackgroundcolor']/table//tr[6]//tr[3]/td[2]",
         'name': ".//span[@class='pageheading']",
         'description': ".//span[@class='sectionbody']/p/text()",

         }

basic_url = 'https://avayacorp.authoria.net/'
sleep = 1


def get_profile_urls():
    all_jobs = []
    g = Grab(log_file='log.html')
    g.go(xpath['home_url'])
    print 'start'
    urls = g.doc.select(xpath['joblist'])
    for url in urls:
        full_url = basic_url + url.select('@href').text()
        all_jobs.append(full_url)
    next_page = g.doc.select(xpath['next_page']).text()
    page = 1
    while True:
        print 'Page - ', page
        need_url = basic_url + next_page
        print need_url
        g.go(basic_url + next_page)
        urls = g.doc.select(xpath['joblist'])
        for url in urls:
            full_url = basic_url + url.select('@href').text()
            all_jobs.append(full_url)
        try:
            next_page = g.doc.select(xpath['next_page']).text()
            print 'next_page', next_page
            time.sleep(sleep)
            page += 1
        except DataNotFound:
            break
    print 'total count: ', len(all_jobs)
    print 'finish'
    return all_jobs


def get_json_file(urls):
    g = Grab()
    data = []
    for i, url in enumerate(urls):
        print i, url
        item = {}
        g.go(url)
        item["url"] = url
        item["id"] = re.search("\d+", g.doc.select(xpath['id']).text()).group(0)
        item["function"] = re.sub(r'- ', '', g.doc.select(xpath['id']).text())
        item["location"] = g.doc.select(xpath['location']).text()
        item["name"] = g.doc.select(xpath['name']).text()
        item["description"] = u" ".join(g.doc.select(xpath['description']).text_list())
        data.append(item)
        time.sleep(sleep)

    with open('output.json', 'w') as f:
        f.write(json.dumps(data))
    print 'Done'


def open_json_file():
    with open('output.json', 'r') as json_file:
        data = json.loads(json_file.read())
        print data


def main():
    profile_urls = get_profile_urls()
    get_json_file(profile_urls)


if __name__ == "__main__":
    main()
    #open_json_file()
