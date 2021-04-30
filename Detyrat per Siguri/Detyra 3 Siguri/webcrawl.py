import requests
from bs4 import BeautifulSoup
import lxml
import urllib.request
import re
import csv


def writeToFile(reddit, sort_by=""):

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://old.reddit.com/r/"+reddit+"/"+sort_by.lower()
    # print(url)
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[1]
    body = list(html.children)[1]

    posts = (body.find_all(True, {'class': ['thing']}))
    if not posts:
        return {}
    # file = "C:\\Users\\Admin\\Desktop\\test.html"
    # f = open(file, "w")
    # f.write(str(str(html).encode("utf-8", "ignore")))
    # f.close()

    # open('output.csv', 'w')
    # counter = 1
    # for post in posts:
    #     title = (post.find(class_='title').get_text().strip()
    #              ).encode("utf-8", "ignore")
    #     author = post.find(class_='author').get_text().encode(
    #         "utf-8", "ignore")
    #     comments = post.find(class_='comments').get_text().encode(
    #         "utf-8", "ignore")
    #     likes = post.find("div", attrs={"class": "score likes"}).get_text().encode(
    #         "utf-8", "ignore")
    #     if likes == "•":
    #         likes = "None"
    #     post_line = [counter, title, author, likes, comments]
    #     with open('output_all.csv', 'a') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(post_line)

    #     with open('output.csv', 'a') as f2:
    #         writer2 = csv.writer(f2)
    #         writer2.writerow(post_line)
    #     counter += 1

    titles = []
    authors = []
    comments = []
    likes = []
    # titles = posts[0].find(class_='title').get_text()
    for post in posts:
        titles.append(post.find(class_='title').get_text())
        authors.append(post.find(class_='author').get_text())

        if not(post.find(class_='comments') is None):

            comment_count = (post.find(class_='comments').text).split(" ")[0]
            if (comment_count == 'comment'):
                comment_count = '0'
        else:
            comment_count = '0'
        # print((post.find(class_='comments').text).split(" ")[0])
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

    # print(len(comments))
    # print(len(titles))
    # print(len(comments))
    # print(len(likes))
    # print(comments)
    return {"Titles": titles, "Authors": authors, "Comments": comments, "Likes": likes}


# df = writeToFile("Kosovo", "hot")
# print(df)
