import requests
import os
from bs4 import BeautifulSoup

os.system("cls")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

url = "http://reddit.com/r/"


def make_detail_url(id):
    return f"{url}{id}/top/?t=month"


def save_db(id):
    subreddit = make_detail_url(id)
    subreddit_detail = requests.get(subreddit, headers=headers)
    soup = BeautifulSoup(subreddit_detail.content, "html.parser")
    thread_div = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
    boxs = thread_div.find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})

    db_list = []
    for b in boxs:
        link = b.find("a", {"class": "SQnoC3ObvgnGjWt90zD9Z"})
        if link != None:
            link = link.get("href")
            title = b.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).text
            vote = b.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).text

            db = {
                "title": title,
                "vote": vote,
                "link": f"https://reddit.com{link}",
                "id": id
            }
            db_list.append(db)

    return db_list


def add_subreddit(id):
    try:
        return save_db(id)
    except AttributeError:
        return None
