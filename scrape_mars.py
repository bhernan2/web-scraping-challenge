from bs4 import BeautifulSoup 
import pandas as pd
import pymongo
from splinter import Browser
import requests

def scrape_all():
    #initiate for deployment
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False, incognito=True)    
    news_title, news_paragraph = mars_news(browser)

    #scrape and store
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "weather":twitter_weather(browser),
        "facts":mars_facts(),
        "hemispheres":hemispheres(browser)
    }

    browser.quit()
    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    news_title = news_soup.find('div', class_ ='list_text').text
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text

    return news_title, news_paragraph

def featured_image(browser): 
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image_url)
    html_image = browser.html
    image_soup = BeautifulSoup(html_image, 'html.parser')
    featured_image_url = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + featured_image_url

    return featured_image_url

import time

def twitter_weather(browser):
    twitter_weather_url= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_weather_url)
    time.sleep(5)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    results = weather_soup.find('article')
    mars_weather = results.find('div',lang="en").span.text

    return mars_weather

def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["parameters", "value"]
    df.set_index("parameters", inplace=True)

    #bootstrap styling 
    return df.to_html(classes="table table-striped")
  

def hemispheres(browser):
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)   
    hemisphere_image_urls = []
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
    
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
        # Navigate Backwards
        browser.back()

    return(hemisphere_image_urls)

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())









    
    



