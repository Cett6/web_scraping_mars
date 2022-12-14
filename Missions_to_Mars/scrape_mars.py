# import dependencies
from cgitb import html
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

#create master scrape function
def Scrape_All():

    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #collecting data
    data = {
        'mars_news': mars_news_scrape(browser)[0],
        'mars_headline': mars_news_scrape(browser)[1],
        'mars_img': mars_img_scrape(browser),
        'mars_facts': Mars_Facts_Table_Scrape(),
        'mars_highres_imgs': mars_highres_img_scrape(browser)
    }

    #quit browser
    browser.quit()

    #return scraped data
    return data


#create function to scrape the mars news site for latest news title and paragraph header
def mars_news_scrape(browser):

    #mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    #time delay
    time.sleep(1)
    
    #scrape page into THE SOOOOOOOUP
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #making a global interest
    global latest_title, latest_paragraph
    
    #retrieve the latest news title
    latest_title = soup.find('div', class_='content_title').get_text()
    
    #retreive paragraph text for latest news title
    latest_paragraph = soup.find('div', class_='article_teaser_body').get_text()
    
    #return latest title and paragraph
    return latest_title, latest_paragraph



#create function to expore mars for an image
def mars_img_scrape(browser):
    
    #url to scrape
    url = 'https://spaceimages-mars.com/'
    
    #visit our browser and pass in the URL 
    browser.visit(url)
    
    #let it sleep for that pesky website safeguard
    time.sleep(1)
    
    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #make image url's variable available for reference elsewhere
    global featured_image_url
    
    #scrape that pic
    featured_image_url = soup.find('img', class_='headerimage fade-in').get('src')
    
    #concatenate website url with image url for full url string
    featured_image_url = f"{url}{featured_image_url}"  

    return featured_image_url 



#use pandas to read tabular html data from Mars Facts Web page
def Mars_Facts_Table_Scrape():

    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)

    #indexing only Mars info
    Mars_Table = tables[1]

    #setting column headers
    Mars_Table.columns = ['Description','Mars']

    #setting index to first description column
    Mars_Table = Mars_Table.set_index('Description')

    #convert data to html table string
    html_table = Mars_Table.to_html()

    #stripping unwanted lines
    html_table = html_table.replace('\n', '')

    return html_table


#create function to scrape the high-rez Mars pics from the site
def mars_highres_img_scrape(browser):

    #url to scrape
    url = 'https://marshemispheres.com/'

    #visit our browser and pass in the URL 
    browser.visit(url)

    #again with the safeguard
    time.sleep(1)

    #make variable containing dictionary url containing images
    global hemisphere_image_urls

    #empty dictionary for images
    hemisphere_image_urls = []

    #scrape page in da soup
    html = browser.html

    #parse html with beautful soup
    soup = bs(html, 'html.parser')

    #retrieve all clickables that contain new pages with high-rez images
    links = browser.find_by_css('a.product-item img')

    #for loop to grab each image
    for x in range(4):

        #click each image's page link
        browser.find_by_css('a.product-item img')[x].click()

        #click on each individual image page's sample download
        link_image_url = browser.links.find_by_partial_text('Sample').first['href']
        link_image_title = browser.find_by_css('h2.title').text

        #saving image url to list
        Image_URL = {}
        Image_URL['img_url'] = link_image_url
        Image_URL['title'] = link_image_title
        hemisphere_image_urls.append(Image_URL)

        #return browser back to main page for next image
        browser.back()

        print(Image_URL)
    
    return hemisphere_image_urls