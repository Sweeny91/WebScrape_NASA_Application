from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\Windows/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Sleep to lag process in order to run properly
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    ## Part 1: NASA Mars News
    # Find the latest news title and its contants and save in a varaibe for later reference
    latest_article = soup.select_one("ul.item_list li.slide")

    # Extract the title from the latest article 
    latest_title = latest_article.find('div', class_="content_title").text.strip()

    # Extract the paragraph content from the latest article 
    latest_paragraph = latest_article.find('div', class_="article_teaser_body").text.strip()

    # Extract the url from the latest article
    latest_image = soup.find('div', class_="image_and_description_container")
    href = latest_image.a["href"]
    latest_link = url + href

    news_dict = {"news_title": latest_title, "news_paragraph": latest_paragraph}


    ## Part 2: Mars Facts
    # Visit the Mars Facts Site and use Pandas .read_html method to save the table in a variable for later reference
    mars_facts = pd.read_html("https://space-facts.com/mars")[0]
    mars_table = pd.DataFrame(mars_facts)

    # Clean data frame for readability purposes
    mars_df = mars_table.rename(columns={0:"Feature", 1:"Value"})
    mars_df.set_index("Feature", inplace=True)

    # Convert the data to a HTML table string
    mars_html = mars_df.to_html()
    mars_html = mars_df.replace("\n", "")
    
    # Export to external HTML file
    mars_df.to_html('mars_table.html')


    ## Part 3: Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # Save Mars Hemisphere URL in variable and initate browser
    mars_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_url)

    # Initiate browser and store in bs4 object
    html = browser.html
    soup = bs(html, "html.parser")

    # Create empty dictionary to store image links
    hemi_dict = []

    # store images section in varaible for reference and print
    products = soup.find('div', class_="collapsible results")

    # CERBERUS
    # Store Cerberus Image section in its own varaible for attribute extraction
    cerberus = products.find_all('div', class_="item")[0]

    # Store Cerberus title in variable
    c_title = cerberus.find('h3').text.strip()

    # Store Cerberus image link in variable
    c_image_ext = cerberus.a["href"]
    image_primary_url = "https://astrogeology.usgs.gov"
    c_image_link = image_primary_url + c_image_ext

    # Now visit link and initiate browser
    browser.visit(c_image_link)
    html = browser.html
    soup = bs(html, "html.parser")

    # Access image href and store in variable
    c_downloads = soup.find('div', class_="downloads")
    c_image = c_downloads.find_all("a")[0]["href"]

    # Create dictionary and append to Hemisphere dictionary list
    cerberus_dict = {"title": c_title, "img_url": c_image}
    hemi_dict.append(cerberus_dict)

    # SCHIAPARELLI
    # Store schiaparelli Image section in its own varaible for attribute extraction
    schiaparelli = products.find_all('div', class_="item")[1]

    # Store schiaparelli title in variable
    sc_title = schiaparelli.find('h3').text.strip()

    # Store schiaparelli image link in variable
    sc_image_ext = schiaparelli.a["href"]
    sc_image_link = image_primary_url + sc_image_ext

    # Now visit link and initiate browser
    browser.visit(sc_image_link)
    html = browser.html
    soup = bs(html, "html.parser")

    # Access image href and store in variable
    sc_downloads = soup.find('div', class_="downloads")
    sc_image = sc_downloads.find_all("a")[0]["href"]

    # Create dictionary and append to Hemisphere dictionary list
    schiaparelli_dict = {"title": sc_title, "img_url": sc_image}
    hemi_dict.append(schiaparelli_dict) 

    # SYRTIS
    # Store syrtis Image section in its own varaible for attribute extraction
    syrtis = products.find_all('div', class_="item")[2]

    # Store syrtis title in variable
    sy_title = syrtis.find('h3').text.strip()

    # Store syrtis image link in variable
    sy_image_ext = syrtis.a["href"]
    sy_image_link = image_primary_url + sy_image_ext

    # Now visit link and initiate browser
    browser.visit(sy_image_link)
    html = browser.html
    soup = bs(html, "html.parser")

    # Access image href and store in variable
    sy_downloads = soup.find('div', class_="downloads")
    sy_image = sy_downloads.find_all("a")[0]["href"]

    # Create dictionary and append to Hemisphere dictionary list
    syrtis_dict = {"title": sy_title, "img_url": sy_image}
    hemi_dict.append(syrtis_dict)

    # VALLES
    # Store Valles Image section in its own varaible for attribute extraction
    valles = products.find_all('div', class_="item")[3]

    # Store Valles title in variable
    v_title = valles.find('h3').text.strip()

    # Store Valles image link in variable
    v_image_ext = valles.a["href"]
    v_image_link = image_primary_url + v_image_ext

    # Now visit link and initiate browser
    browser.visit(v_image_link)
    html = browser.html
    soup = bs(html, "html.parser")

    # Access image href and store in variable
    v_downloads = soup.find('div', class_="downloads")
    v_image = v_downloads.find_all("a")[0]["href"]

    valles_dict = {"title": v_title, "img_url": v_image}
    hemi_dict.append(valles_dict)

    # Store all scraped data into dictionary
    mars_dict = {"Mars News": news_dict, "Mars Facts": mars_df, "Mars Hemispheres": hemi_dict}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict