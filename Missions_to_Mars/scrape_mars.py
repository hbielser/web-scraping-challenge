import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def get_all():
    all_mars_data = {}
    all_mars_data['news_title'] = get_mars_news_title()
    all_mars_data['news_text'] = get_mars_news_text()
    all_mars_data['featured_image'] = get_featured_image()
    all_mars_data['mars_facts'] = get_mars_facts()
    all_mars_data['mars_hems'] = get_mars_hems()

    return all_mars_data

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def get_mars_news_title():
    browser = init_browser()

    scrape_url = 'https://mars.nasa.gov/news'
    browser.visit(scrape_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    soup = bs(html, "html.parser")

    slide_elem = soup.select_one("ul.item_list li.slide")

    mars_news_title = slide_elem.find("div", class_="content_title").get_text()

    browser.quit()

    return mars_news_title

def get_mars_news_text():
    browser = init_browser()

    scrape_url = 'https://mars.nasa.gov/news'
    browser.visit(scrape_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    soup = bs(html, "html.parser")

    slide_elem = soup.select_one("ul.item_list li.slide")

    mars_news_text = slide_elem.find("div", class_="article_teaser_body").get_text()

    browser.quit()

    return mars_news_text

def get_featured_image():
    browser = init_browser()

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    browser.links.find_by_partial_text('FULL').click()
    time.sleep(1) 
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup = bs(html, "html.parser")

    mars_image = soup.select_one('figure.lede a img').get('src')
    core_url = "https://www.jpl.nasa.gov"
    featured_image_url = core_url + mars_image

    browser.quit()

    return featured_image_url

def get_mars_facts():

    mars_table_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_table_url)
    mars_df = mars_table[0]
    mars_html = mars_df.to_html()

    return mars_html

def get_mars_hems():
    browser = init_browser()

    mars_hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    
    hems_list = []
    
    for x in range(0,4):

        html = browser.html
        soup = bs(html, 'html.parser')

        hems = soup.find_all('h3')[x]

        for hem in hems:
            hems_list.append(hem)

    hems_url_list = []
        
    for x in range(0,4):
        
        browser.links.find_by_partial_text(hems_list[x]).click()

        html = browser.html
        soup = bs(html, 'html.parser')

        hems_url = soup.select_one('ul li a').get('href')

        hems_url_list.append(hems_url)

        browser.back()

    hem_img_urls = [    
    {"title": hems_list[0], "img_url": hems_url_list[0]},
    {"title": hems_list[1], "img_url": hems_url_list[1]},
    {"title": hems_list[2], "img_url": hems_url_list[2]},
    {"title": hems_list[3], "img_url": hems_url_list[3]},
    ]

    browser.quit()

    return hem_img_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(get_all())