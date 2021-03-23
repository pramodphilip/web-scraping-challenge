#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
from pprint import pprint
import pandas as pd
import time

#Function scrape defined here
def scrape():

    # Initializes dictionary to hold all information
    info_dict = {}

    # URL for NASA Mars News Site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Creaters browser window for scraping
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visits url, creates soup object
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Finds news titles, isolates first one
    titles = soup.find_all('div',class_='content_title')
    news_title = titles[1].text.strip()

    # Finds paragraph text
    news_p = soup.find('div',class_='article_teaser_body').text

    # Assigns latest news title and paragraph text
    # to info dictionary
    info_dict['latest_news_title'] = news_title 
    info_dict['latest_news_p'] = news_p

    # URL for JPL Featured Space Image, visits site
    jpl_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(jpl_url)

    # Creates target for browser to click 
    # to page with full sized image
    target = 'a[class="group  cursor-pointer block"]'
    browser.find_by_tag(target).click()    

    #Pauses for 3 seconds, allows web page to settle before grabbing HTML
    #Prevents issue of previous page's HTML being grabbed instead
    time.sleep(3)

    # Grabs html, creates soup object
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Finds div tags with full size image urls inside
    images = soup.find('div',class_="lg:w-auto w-full")

    # Isolates image url for full size jpeg
    featured_image_url = images.a['href']

    # Assigns featured image url to info dictionary
    info_dict['featured_image_url'] = featured_image_url

    # URL for Mars Facts website
    facts_url = 'https://space-facts.com/mars/'

    # Reads HTML, pulls tables from HTML as dataframes
    tables = pd.read_html(facts_url)

    # Extracts first table, renames columns
    # converts table back to HTML
    df = tables[0]
    df.columns = ['Fact','Value']  
    facts_html = df.to_html()
    facts_html = facts_html.replace('\n', '')

    # Assigns table in HTML format to info
    # dictionary
    info_dict['facts_html'] = facts_html

    # URL for USGS Astrogeology website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Visits URL
    browser.visit(url)

    # Initializes hemisphere image URL list
    hemisphere_image_urls = []

    # Extracts HTML from page, creates soup object
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Collects headers from page
    headers = soup.find_all('div', class_="description")

    for x in range(len(headers)):
        # References h3 text from current tag
        # Uses this reference to click to next page
        ref = headers[x].h3.text
        browser.find_by_text(ref).click()
    
        # Extracts HTML from page, creates soup object
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        browser.title
    
        # Collects div tags with class downloads
        # Extracts img URL from first div tag
        img = soup.find_all('div', class_="downloads")
        img_url = img[0].li.a['href']
    
        # Collects h2 tags from page
        # Extracts title text from first tag
        titles = soup.find_all('h2',class_="title")
        title = titles[0].text
    
        # Creates small dictionary with keys title
        # and img_url
        # Appends to hemisphere image URL list
        img_dict = {"title":title,"img_url":img_url}
        hemisphere_image_urls.append(img_dict)
    
        # Goes back to previous page, starts loop over
        browser.back()

    # Quit browser
    browser.quit()

    # Assigns hemisphere image URL list to info
    # dictionary
    info_dict['hemis_dict'] = hemisphere_image_urls

    # Prints information dictionary for format checking
    print(info_dict)

    # Returns information dictionary
    return info_dict





