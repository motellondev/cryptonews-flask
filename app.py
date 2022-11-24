from flask import Flask, render_template
import requests
import xmltodict
import random
from bs4 import BeautifulSoup


# Rss posts obtained from each URL
post_limit = 6
# Rss urls array
rss_urls = ["https://cointelegraph.com/rss",
            "https://cointext.com/news/feed",
            "https://news.bitcoin.com/feed"]

app = Flask(__name__)

@app.route("/")
def home():
    data = get_data()
    return render_template("index.html", data=data)


def get_data():

    # Rss posts array
    rss_data = []

    for url in rss_urls:
        page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        # Parse XML content to dict
        xmldict = xmltodict.parse(page.text)
        # Get first posts from each URL
        for element in range(1,post_limit):
            # Parse description element to get text and image content
            html_content = xmldict["rss"]["channel"]["item"][element]["description"]
            post_desc = BeautifulSoup(html_content, features="html.parser")
            # Create post dict
            rss_post = {"title": xmldict["rss"]["channel"]["item"][element]["title"],
                        "link": xmldict["rss"]["channel"]["item"][element]["link"],
                        "description": post_desc.text, "image": post_desc.img["src"]}

            # Append to posts array
            rss_data.append(rss_post)

    # Randomize posts order
    random.shuffle(rss_data)
    return rss_data
