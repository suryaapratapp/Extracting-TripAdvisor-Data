'''S dot pratap at liverpool dot ac dot uk | Surya Pratap
- User can change website (city location) @line22. Make sure to add "{}" at the exact position present (after "oa" in the website)
NOTE: @line22 In range(0, 150, 30), here 30 is the amount of hotels present on one page, whereas 150 is the quantity of hotels we are extracting. User can change the quantity of the hotels as per their requirements.'''

'''importing libraries'''
from bs4 import BeautifulSoup
import re
from requests_html import HTMLSession
import requests
import urllib.request
from lxml import html
import pandas as pd
import numpy as np

url_list = []
names = []
title = []
review = []
date = []
rating = []
hotelname = []
WebSites = ("https://www.tripadvisor.co.uk/Hotels-g186338-oa{}-London_England-Hotels.html?offset=30".format(i) for i in range(0, 150, 30))

for theurl in WebSites:
    # print(theurl)
    response = urllib.request.urlopen(theurl)
    soup = BeautifulSoup(response, "html.parser")
    for link in soup.find_all('a', href=True):
    # if "/Hotel Review" in link['href']:
        if link['href'].startswith("/Hotel_Review") and link['href'].endswith("#REVIEWS"):
            url_list.append("https://www.tripadvisor.co.uk"+link['href'])
url_list = list(set(url_list))
# print(url_list)
for url in url_list:
    print(url)
    # url = re.sub(r"(-Reviews-)", r"\1or-", url)
    # for i in range(0, 10, 5):
    #     # print(i)
    #     if i < 5:
    #         url = url.replace("-or-", "-or%d-"%i)
    #     else:
    #         url = url.replace("-or%d-"%(i-5), "-or%d-"%i)
    #     print(url)
    session = HTMLSession()
    response = session.get(url)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    soup = BeautifulSoup(response.content, "html.parser")
    totalreview = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/a/span[2]/text()")
    total_rating = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/span/text()")
    hotel_name = tree.xpath("//*[@id='HEADING']/text()")
    hotelname.append(''.join(hotel_name))
    # print(hotelname)
    bubble_rating = soup.find(attrs={"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"})      #bubble rating of the latest review
    Rating = bubble_rating.select_one('span.ui_bubble_rating')['class']
    Rating = Rating[1].split('_')[-1]
    rating.append(Rating[0])
    ii = 2

    Reviewer = tree.xpath(
        "//*[@id='component_15']/div/div[3]/div[%d]/div[1]/div/div[2]/span/a/text()" % 3)  # latest reviewer name
    Reviewer = ''.join(Reviewer)

    Review = tree.xpath(
        "//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()" % (3, ii))
    Review = ''.join(Review)

    ReviewTitle = tree.xpath(
        "//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()" % (3, ii))
    ReviewTitle = ''.join(ReviewTitle)

    RatingDate = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[1]/div/div[2]/span/text()" % 3)
    RatingDate = ''.join(RatingDate)

    if Review == []:  # if the list is empty
        ii += 1
        full_review = tree.xpath(
            "//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()" % (3, ii))
    ii = 2

    if ReviewTitle == []:
        ii += 1
        ReviewTitle = tree.xpath(
            "//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()" % (3, ii))
        
    names.append(Reviewer)
    review.append(Review)
    title.append(ReviewTitle)
    date.append(RatingDate)
        
print(hotelname)
d = dict(A=np.array(hotelname), B=np.array(names), C=np.array(date), D=np.array(rating), E=np.array(title), F=np.array(review))
# df = pd.DataFrame({"Hotel Name":hotelname, "Reviewer":names, "Review Date":date, "Review Rating":rating, "Review Title":title, "Review":review})    #list to csv columns
df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in d.items()]))
df.dropna(how="all", inplace=True)  # remove blank rows
df.to_csv('output1.csv', index=False, encoding="utf-8")  # save data to csv
