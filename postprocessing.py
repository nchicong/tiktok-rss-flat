from TikTokApi import TikTokApi
import csv
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
import shutil
import os

# Custom Domain
ghPagesURL = "https://nchicong.github.io/tiktok-rss-flat/"

api = TikTokApi.get_instance()

count = 10
opmlUsers = []
dest_dir = "rss"

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)
os.makedirs(dest_dir)

import urllib.request, json
with urllib.request.urlopen("https://jsonblob.com/api/jsonBlob/283f6f37-f78c-11eb-825b-2be69b85a7a0") as url:
    data = json.loads(url.read().decode())
    print(data)

# with open('subscriptions.csv') as f:
#     cf = csv.DictReader(f, fieldnames=['username'])
    for row in data.followingArray:
        # user = row['username']
        print(row)
        user = row;

        tiktoks = api.byUsername(user, count=count)
        
        fg = FeedGenerator()
        fg.id('https://www.tiktok.com/@' + user)
        fg.title(user)
        fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
        fg.link( href='http://tiktok.com', rel='alternate' )
        fg.logo(ghPagesURL + 'tiktok-rss.png')
        fg.subtitle('TikToks from ' + user)
        fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self' )
        fg.language('en')

        opmlUsers.append({
            "text": user,
            "title": user + ' TikTok',
            "xmlUrl": ghPagesURL + 'rss/' + user + '.xml'
        })

        for tiktok in tiktoks:
            fe = fg.add_entry()
            link = "https://www.tiktok.com/@" + user + "/video/" + tiktok['id']
            fe.id(link)
            fe.published(datetime.fromtimestamp(tiktok['createTime'], timezone.utc))
            fe.title(tiktok['desc'])
            fe.link(href=link)
            fe.description("<a href='" + link + "'><img src='" + tiktok['video']['originCover'] + "' /></a>")

        fg.rss_file('rss/' + user + '.xml') # Write the RSS feed to a file

        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        template = env.get_template('template.opml')

        output = template.render(users=opmlUsers)

        file1 = open("rss/list.opml", "w")
        file1.write(output)
        file1.close()
