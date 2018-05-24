import time
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from difflib import SequenceMatcher
from selenium.webdriver.common.keys import Keys

# Initialize browser
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def find_latest_news_title():
    """Returns the latest News Article from the article url provided"""

    # Initialize browser
    browser = init_browser()
    
    article_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(article_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    title_results = soup.find_all('div', class_="content_title")
    
    news_titles = []

    for result in title_results:
        title_text = result.text.strip()
        news_titles.append(title_text)
    
    news_title = news_titles[0]
    return news_title

def find_latest_news_description():
    """Returns a description of the latest news article from the url provided"""

    article_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    response = requests.get(article_url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    description_results = soup.find_all('div', class_="rollover_description_inner")
    
    news_descriptions = []

    for result in description_results:
        description_text = result.text.strip()
        news_descriptions.append(description_text)
        
    news_description = news_descriptions[0]
    
    return news_description

def find_feature_image():
    """Returns feature image url from NASA's website"""
    
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    #!which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(image_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    feature_images = soup.find_all('article', class_='carousel_item')

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    image_tags = []

    for item in feature_images:
        target_item = str(item.a)
        split_target = target_item.split(" ")
        image_tags.append(split_target)

    text_list = []
    score_list = []

    for y in image_tags[0]:

        similarity = similar(y, 'data-fancybox-href="/spaceimages/images/')

        text_list.append(y)
        score_list.append(similarity)

    target_url = str(text_list[score_list.index(max(score_list))])
    target_url_list = target_url.split('"')

    beg_url = 'https://www.jpl.nasa.gov'

    featured_image_url = beg_url + target_url_list[1]

    return featured_image_url

def find_most_recent_weather_tweet():
    """Returns most recent tweet about weather on Mars"""
    
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    twitter_results = soup.body.find_all('div', class_="js-tweet-text-container")
    
    recent_tweets = []

    for tweet in twitter_results:
        recent = tweet.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        for tweet_text in recent:
            recent_tweets.append(tweet_text.text.strip())
            
    most_recent_weather_tweet = recent_tweets[0]
    
    return most_recent_weather_tweet

def find_mars_hemisphere_images():
    """Returns image urls of Mars Hemispheres"""
    #!which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    description_class = soup.find_all('div', class_='description')

    hemisphere_names = []

    for hemispheres in description_class:
        hemisphere_names.append(hemispheres.find('h3').text)

    start_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_images_windows = []

    for hemispheres_image in hemisphere_images:
        browser.click_link_by_partial_text(hemispheres_image)
        hemispheres_url = browser.url
        new_page = soup.body.find_all('div', class_='container')
        for sample in new_page:
            browser.click_link_by_text('Sample')
        hemisphere_images_windows.append(browser.windows)
        browser.visit(start_url)

    full_hemisphere_images = []

    for full_images in hemisphere_images_windows[3]:
        full_hemisphere_images.append(full_images.url)

    full_hemisphere_image_urls = [
        {"title": hemisphere_names[3], "img_url": full_hemisphere_images[1]},
        {"title": hemisphere_names[2], "img_url": full_hemisphere_images[2]},
        {"title": hemisphere_names[1], "img_url": full_hemisphere_images[3]},
        {"title": hemisphere_names[0], "img_url": full_hemisphere_images[4]},
    ]
    
    return full_hemisphere_image_urls

    
