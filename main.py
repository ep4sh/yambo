#    Copyright (C) 2019, Pasha Radchenko, <ep4sh2k@gmail.com> 
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

import yampy
import json
import feedparser
import random
import sys
import os

# yammer credentials

try:  
    access_token = os.environ["YAMMER_TOKEN"]
except KeyError: 
  print "Please export the environment variable YAMMER_TOKEN"
  sys.exit(1)

# News feeds URLS
news_feeds_urls = ['https://www.elastic.co/blog/feed']
# POST RETRY COUNT
retry_count = 5
current_retry = 0
# DevOps technology GroupId
group_for_posts = 16545101

# ***************************************
yammer = yampy.Yammer(access_token=access_token)
# Like the last thread


def like_last_thread(group_for_posts):
    msg = yammer.client.get("/messages/in_group/"+str(group_for_posts), limit=1)
    msg = json.dumps(msg)
    jsondata = json.loads(msg)
    thread_to_like = jsondata["messages"][0]["thread_id"]
    like = yammer.messages.like(thread_to_like)


# Get random pice of  news from RSS and forward to Yammer group
def repost_news(url, retry_count, current_retry):
    random_url = random.choice(url)
    random_post = random.randint(0, retry_count)
    NewsFeed = feedparser.parse(random_url)
    entry = NewsFeed.entries[random_post]
    try:
        while current_retry <= retry_count:
            data_list = []
            with open("data_file.json", "r") as read_file:
                data = json.load(read_file)
                data_list = data
                if entry.link in data_list:
                    print("found => {}".format(entry.link))
                    current_retry += 1
                    print("Try #"+str(current_retry)+"...")
                    get_news(url, retry_count, current_retry)
                else:
                    print("Not founded in list.. adding new one")
                    data_list.append(entry.link)
                    body = create_post(entry.link)
                    post(body, group_for_posts)
                    with open("data_file.json", "w") as write_file:
                        json.dump(data_list, write_file)
                    sys.exit()
    except FileNotFoundError:
        print("There is not any data file!")
        with open("data_file.json", "w") as write_file:
            data_list.append(entry.link)
            json.dump(data_list, write_file)
        body = create_post(entry.link)
        post(body,group_for_posts)


# generate a post
def create_post(link):
    greetings = ['Good day! ', 'Hi there! ',
                 'Hey, hey! ', 'Hey, people! ', 'Greetings! ']
    interes = ['I was interested in this post: ', 'Hope it could be useful: ',
               'I just want to share this cool stuff: ', "Some good stuff for DevOps: "]
    post_body = random.choice(greetings)+random.choice(interes)+link
    return post_body


# Post message in group
def post(body, group_id):
    res = yammer.messages.create(body, group_id)
    return res


def main():
    like_last_thread(group_for_posts)
    repost_news(news_feeds_urls, retry_count, current_retry)


if __name__ == "__main__":
    main()
