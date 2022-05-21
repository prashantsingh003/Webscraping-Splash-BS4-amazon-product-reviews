import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist=[]
def get_soup(url):
    r=requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2})
    soup=BeautifulSoup(r.text,'html.parser')
    return soup

def get_reviews(soup):
    reviews=soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            review={
                'product':soup.title.text.replace('Amazon.com: Customer reviews:','').strip(),
                'title' : item.find('a',{'data-hook':'review-title'}).text.strip(),
                'rating' : item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars',"").strip(),
                'review_date' : item.find('span',{'data-hook':'review-date'}).text.replace('\n',""),
                'item_data' : item.find('span',{'data-hook':'review-body'}).text.replace('\n',"")
                }
            reviewlist.append(review)
    except:
        pass

for i in range(100):
    url='https://www.amazon.com/Canon-M50-Mirrorless-Accessory-Including/product-reviews/B07KMHTZVS/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'+'&pageNumber='+str(i+1)
    soup=get_soup(url)
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break
df=pd.DataFrame(reviewlist)
reviews = pd.ExcelWriter('reviews.xlsx')
df.to_excel(reviews)
reviews.save()