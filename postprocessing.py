from TikTokApi import TikTokApi
# from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
import shutil
import os
from html import escape

# Custom Domain
ghPagesURL = "https://nchicong.github.io/tiktok-rss-flat/"

api = TikTokApi.get_instance(use_test_endpoints=True)

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

count = 10
opmlUsers = []
dest_dir = "rss"

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)
os.makedirs(dest_dir)

import urllib.request, json
with urllib.request.urlopen("https://jsonblob.com/api/jsonBlob/283f6f37-f78c-11eb-825b-2be69b85a7a0") as url:
    data = json.loads(url.read().decode())

# with open('subscriptions.csv') as f:
#     cf = csv.DictReader(f, fieldnames=['username'])
    for row in data["followingArray"]:
        # user = row['username']
        user = row;

        tiktoks = api.by_username(user, count=count, custom_verifyFp="verify_9f7cfc747acd73df633a273b257f468a")
        
        # fg = FeedGenerator()
        # fg.id('https://www.tiktok.com/@' + user)
        # fg.title(user)
        # fg.author( {'name':'Conor ONeill','email':'conor@conoroneill.com'} )
        # fg.logo(ghPagesURL + 'tiktok-rss.png')
        # fg.subtitle('TikToks from ' + user)
        # fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self')
        # fg.language('en')

        feed = {
            "title": user,
            "id": 'https://www.tiktok.com/@' + user,
            "link": ghPagesURL + 'rss/' + user + '.xml',
            "subtitle": 'TikToks from ' + user
        }
        feedEntries = []


        for tiktok in tiktoks:
            link = "https://www.tiktok.com/@" + user + "/video/" + tiktok['id']
            # fe = fg.add_entry()
            # fe.id(link)
            # fe.published(datetime.fromtimestamp(tiktok['createTime'], timezone.utc))
            # fe.title(tiktok['desc'])
            # fe.link(href=link)
            # # fe.description("<table style='width:100%'><tr><td style='text-align:center'><a href='" + link + "'>Link</a></td><td><img src='" + tiktok['video']['originCover'] + "' /></td></tr></table>")
            # # fe.description("<a href='" + link + "'><img src='" + tiktok['video']['originCover'] + "' /></a><br/><a href='" + link + "'>Link</a>")
            # fe.content(content="<p><a href='" + link + "'><img src='" + tiktok['video']['originCover'] + "' /></a><a href='" + link + "?is_copy_url=1&is_from_webapp=v1'>Link</a></p>", src=link, type="html")

            feedEntries.append({
              "link": "https://www.tiktok.com/@" + user + "/video/" + tiktok['id'] + "?is_copy_url=1&is_from_webapp=v1",
              "published": datetime.fromtimestamp(tiktok['createTime'], timezone.utc),
              "title": tiktok['desc'],
              "tiktokId": tiktok['id'],
              "image": tiktok['video']['originCover']
            })

        # fg.rss_file('rss/' + user + '.xml') # Write the RSS feed to a file

        xmlTemplate = env.get_template('template.xml')
        xmlOutput = xmlTemplate.render(f=feed, feedEntries=feedEntries)
        xmlFile = open('rss/' + user + '.xml', "w")
        xmlFile.write(xmlOutput)
        xmlFile.close()


        opmlUsers.append({
            "text": user,
            "title": user,
            "xmlUrl": ghPagesURL + 'rss/' + user + '.xml'
        })


    opmlTemplate = env.get_template('template.opml')
    opmlOutput = opmlTemplate.render(users=opmlUsers)

    opmlFile = open("rss/list.opml", "w")
    opmlFile.write(opmlOutput)
    opmlFile.close()
