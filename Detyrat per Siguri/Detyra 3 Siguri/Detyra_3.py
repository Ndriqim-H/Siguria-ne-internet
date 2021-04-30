import requests
from bs4 import BeautifulSoup


def writeToFile(reddit, sort_by=""):

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://old.reddit.com/r/"+reddit+"/"+sort_by.lower()

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[1]
    body = list(html.children)[1]

    posts = (body.find_all(True, {'class': ['thing']}))
    if not posts:
        return {}

    titles = []
    authors = []
    comments = []
    likes = []

    for post in posts:
        titles.append(post.find(class_='title').get_text())
        authors.append(post.find(class_='author').get_text())

        if not(post.find(class_='comments') is None):

            comment_count = (post.find(class_='comments').text).split(" ")[0]
            if (comment_count == 'comment'):
                comment_count = '0'
        else:
            comment_count = '0'

        comments.append(comment_count)
        if (post.find("div", attrs={"class": "score likes"}) is None):
            like_count = 0
            likes.append(like_count)
        else:
            like_count = post.find(
                "div", attrs={"class": "score likes"}).text.lower()

            if like_count == "•":
                likes.append(0)
            elif(like_count.islower()):
                like_count = like_count.replace('k', '')
                likes.append(int(float(like_count)*1000))
            else:
                likes.append(int(like_count))

    return {"Titles": titles, "Authors": authors, "Comments": comments, "Likes": likes}
