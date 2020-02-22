'''S dot pratap at liverpool dot ac dot uk | Surya Pratap'''
'''importing libraries'''


'''website = "https://www.tripadvisor.co.uk/Hotels-g186338-London_England-Hotels.html"'''
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
WebSites = ("https://www.tripadvisor.co.uk/Hotels-g186338-oa{}-London_England-Hotels.html?offset=30".format(i) for i in range(0, 30, 30))

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
    url = re.sub(r"(-Reviews-)", r"\1or-", url)
    for i in range(0, 10, 5):
        print(i)
        if i < 5:
            url = url.replace("-or-", "-or%d-"%i)
        else:
            url = url.replace("-or%d-"%(i-5), "-or%d-"%i)
        print(url)
        session = HTMLSession()
        response = session.get(url)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        soup = BeautifulSoup(response.content, "html.parser")
        totalreview = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/a/span[2]/text()")
        print(totalreview)
        # for totalreview in soup.findAll(attrs={"class": "hotels-hotel-review-about-with-photos-Reviews__seeAllReviews--3PpLR"}):
        # if __name__ == '__main__':
        # reviewcount = totalreview.replace(",", "").split()
        # print()
        total_rating = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/span/text()")
        hotel_name = tree.xpath("//*[@id='HEADING']/text()")
        hotelname.append(''.join(hotel_name))
        for bubble_rating in soup.findAll(attrs={
            "class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"}):  # to scrap bubble rating using its classname
            Rating = bubble_rating.select_one('span.ui_bubble_rating')['class']
            Rating = Rating[1].split('_')[-1]
            rating.append(Rating[0])

        for x in range(3, 8):
            ii = 2

            Reviewer = tree.xpath(
                "//*[@id='component_13']/div/div[3]/div[%d]/div[1]/div/div[2]/span/a/text()" % x)  # reviewer name
            Reviewer = ''.join(Reviewer)

            Review = tree.xpath(
                "//*[@id='component_13']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()" % (x, ii))
            Review = ''.join(Review)

            ReviewTitle = tree.xpath(
                "//*[@id='component_13']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()" % (x, ii))
            ReviewTitle = ''.join(ReviewTitle)

            RatingDate = tree.xpath("//*[@id='component_13']/div/div[3]/div[%d]/div[1]/div/div[2]/span/text()" % x)
            RatingDate = ''.join(RatingDate)

            if Review == []:  # if the list is empty
                ii += 1
                full_review = tree.xpath(
                    "//*[@id='component_13']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()" % (x, ii))
            ii = 2

            if ReviewTitle == []:
                ii += 1
                ReviewTitle = tree.xpath(
                    "//*[@id='component_13']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()" % (x, ii))

            names.append(Reviewer)
            review.append(Review)
            title.append(ReviewTitle)
            date.append(RatingDate)
hotelname = list(set(hotelname))
d = dict( A = np.array(hotelname), B = np.array(names), C = np.array(date), D = np.array(rating), E = np.array(title), F = np.array(review))
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items()]))
# df = pd.DataFrame({"Hotel Name": hotelname,"Reviewer": names, "Review Date": date, "Review Rating": rating, "Review Title": title, "Review": review})  # list to csv columns
df.dropna(how="all", inplace=True)  # remove blank rows
df.to_csv('tripadvisor.csv', index=False, encoding="utf-8")  # save data to csv
    # urli = (re.sub(r"(-Reviews-)", r"\1or%d-"%i, url) for i in range(0, 25, 5))
    # print(urli)
    # WebSites = (url%i for i in range(0, 25, 5))
    # print(WebSites)
# for theurl in WebSites:
#     time.sleep(2)
