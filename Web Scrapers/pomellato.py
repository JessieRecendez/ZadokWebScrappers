# Pomellato
# 2023-03-20
# The products pages use a scroll down to upload more products into the pages.
##### So this loads ALL products by scrolling down then back up and keeps doing this
##### until no more products or page heights doesn't change anymore.
################################

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol for the                              \u2103
# this is a simple bullet point black dot                               \u30fb
# this is just an empty space                                           \u2005
# this is the &nbsp;                                                    \xa0
# this is ~ a wavy dash used in approximate japanese price              \u301c
#

import requests
from bs4 import BeautifulSoup
import time
import re
from csv import writer
from selenium import webdriver
import random


driver = webdriver.Chrome()
url = "https://www.pomellato.com/en_us/jewelry"
delay = random.uniform(0, 1.5)
# Initialize a web driver (you may need to download a driver executable for your browser)
driver.get(url)

# Get the initial height of the page
prev_height = driver.execute_script("return document.body.scrollHeight")

# Keep scrolling down the page until the page height no longer increases
while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")    # goes down
    time.sleep(1.5)
    driver.execute_script("window.scrollBy(0, -1750);") # then comes up a few pixels

    # Wait for the page to load
    time.sleep(1)

    # Get the new height of the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Break the loop if the page height no longer increases
    if new_height == prev_height:
        break
    
    # Update the previous height of the page
    prev_height = new_height
    
# Get the page source and create a Beautiful Soup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the product information (you need to inspect the HTML structure to find the correct tags)
products = soup.find_all('div', class_='product-tile')

# save as file type in same folder
with open('Pomellato.xlsx', 'a', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    header = ["SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4"]  # name columns
    thewriter.writerow(header)

    for product in products:
        productLink = "https://www.pomellato.com" + product.find('a').get("href").replace("È", "E").replace('é', 'e')
        try:
            hero = "https://www.pomellato.com" + product.find('img', class_='product-picture-img').get("src").replace("300_300", "1080_1080").replace("È", "E").replace('é', 'e')
        except:
            hero = ""
            
        productTitle = product.find('h2').text.replace('\u301c', '').replace("È", "E")
        titleMatch = r'\b(Ring|Bracelet|Bangle|Necklace|Pendant|Earrings)\b'
        collectionMatch = r'\b(Nudo|Brera|Victoria|Orsetto|Iconica|Pomellato Together|Sabbia|Catene|Fantina|M\'Ama Non M\'Ama)\b'
        productType = re.search(titleMatch, productTitle)
        # Extracting the found product type
        if productType:
            productType = productType.group(0)
        else:
            productType = ""
        
        collections = re.search(collectionMatch, productTitle)
        if collections:
            collections = collections.group(0)
        else:
            collections = ""

        sku = product.find('img', class_='product-picture-img').get("src").replace('/r/assets/', '')
        # Define a regular expression to match the pattern to replace
        pattern = r'/.*$'
        # Use re.sub() to replace the matched pattern with the replacement string
        newSKU = re.sub(pattern, '', sku)

        # make a request to the product page to get the SKU
        # Hence, click into each URL to get even more possible unique data
        productPage = requests.get(productLink)
        productSoup = BeautifulSoup(productPage.content, 'html.parser')
        time.sleep(delay)
        try:
            price = productSoup.find('div', class_='cl-black fs-24 italic weight-600 nowrap').text.replace('$', '').replace(',', '').replace('\n', '').replace("\u301c", "").strip()
        except:
            price = ""
        try:
            description = productSoup.find('p', class_="mt5 cl-black fs-medium-small").text.replace('”', '"').replace('“', '"').replace("...", '').replace('\u2005', ' ').replace('\xa0', ' ').replace("’", "'").replace("‘", "'").replace('é', 'e')
        except:
            description = ""
        try:
            stone = productSoup.find('img', class_='product-picture-img').get("src").replace('citrine', 'Citrine').replace('tourmaline', 'Tourmaline').replace('tsavorite', 'Tsavorite').replace('malachite', 'Malachite').replace('jet', 'Jet').replace('garnet', 'Garnet').replace('emerald', 'Emerald').replace('peridot', 'Peridot').replace('ruby', 'Ruby').replace('amethyst', 'Amethyst').replace('agate', 'Agate').replace('turquoise', 'Turquoise').replace('prasiolite', 'Prasiolite').replace('diamond', 'Diamond').replace('rainbow-sapphire', 'Rainbow Sapphire').replace('orange-citrine', 'Orange Citrine').replace('black-diamond', 'Black Diamond').replace('blue-diamond', 'Blue Diamond').replace('brown-diamond', 'Brown Diamond').replace('champagne-diamond', 'Champagne Diamond').replace('green-diamond', 'Green Diamond').replace('pink-diamond', 'Pink Diamond').replace('yellow-diamond', 'Yellow Diamond').replace('green-tsavorite', 'Green Tsavorite').replace('black-jade', 'Black Jade').replace('green-jade', 'Green Jade').replace('white-jade', 'White Jade').replace('lapis-lazuli', 'Lapis Lazuli').replace('green-malachite', 'Green Malachite').replace('rainbow-moonstone', 'Rainbow Moonstone').replace('white-moonstone', 'White Moonstone').replace('black-mother-of-pearl', 'Black Mother of Pearl').replace('white-mother-of-pearl', 'White Mother of Pearl').replace('mother-of-pearl', 'Mother of Pearl').replace('green-amethyst', 'Green Amethyst').replace('green-quartz', 'Green Quartz').replace('lemon-quartz', 'Lemon Quartz').replace('black-night-quartz', 'Black Night Quartz').replace('rose-de-france', 'Rose de France').replace('rose-quartz', 'Rose Quartz').replace('black-sapphire', 'Black Sapphire').replace('blue-sapphire', 'Blue Sapphire').replace('light-blue-sapphire', 'Light Blue Sapphire').replace('dark-blue-sapphire', 'Dark Blue Sapphire').replace('green-sapphire', 'Green Sapphire').replace('pink-sapphire', 'Pink Sapphire').replace('orange-sapphire', 'Orange Sapphire').replace('purple-sapphire', 'Purple Sapphire').replace('white-sapphire', 'White Sapphire').replace('yellow-sapphire', 'Yellow').replace('black-spinel', 'Black Spinel').replace('blue-topaz', 'Blue Topaz').replace('english-blue-topaz', 'English Blue Topaz').replace('green-envy-topaz', 'Green Envy Topaz').replace('blue-london-topaz', 'London Blue Topaz').replace('morganite-topaz', 'Morganite Topaz').replace('pink-topaz', 'Pink Topaz').replace('sky-blue-topaz', 'Sky Blue Topaz').replace('swiss-blue-topaz', 'Swiss Blue Topaz').replace('white-topaz', 'White Topaz').replace('green-tourmaline', 'Green Tourmaline').replace('pink-tourmaline', 'Pink Tourmaline').replace('red-carnelian', 'Red Carnelian')
        except:
            stone = ""
        stoneMatch = r'\b(Apatite|Jet|Rainbow Sapphire|Morganite|Citrine|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|Emerald|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
        stoneTypes = re.findall(stoneMatch, stone, re.IGNORECASE)
        stoneType1 = ""
        stoneType2 = ""
        stoneType3 = ""
        stoneType4 = ""
        if len(stoneTypes) > 1:
            try:
                stoneType1 = stoneTypes[0]
            except:
                stoneType1 = ''
            try:
                stoneType2 = stoneTypes[1]
            except:
                    stoneType2 = ''
            try:
                stoneType3 = stoneTypes[2]
            except:
                    stoneType3 = ''
            try:
                stoneType4 = stoneTypes[3]
            except:
                stoneType4 = ''
        else:
            try:
                stoneType1 = stoneTypes[0]
            except:
                stoneType1 = ''
        try:
            metal = productSoup.find('img', class_='product-picture-img').get("src").replace('white-gold-14kt', '14k White Gold').replace('rose-gold-14kt', '14k Rose Gold').replace('yellow-gold-14kt', '14k Yellow Gold').replace('pink-gold-14kt', '14k Pink Gold').replace('white-gold-18kt', '18k White Gold').replace('rose-gold-18kt', '18k Rose Gold').replace('yellow-gold-18kt', '18k Yellow Gold').replace('pink-gold-18kt', '18k Pink Gold').replace('platinum', 'Platinum').replace('gold-14kt', '14k Gold').replace('gold-18kt', '18k Gold')
        except:
            metal = ""
        metalMatch = r'\b(14k Gold|14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|18k Gold|18k White Gold|18k Yellow Gold|18k Rose Gold|18k Pink Gold|Platinum)\b'
        metalTypes = re.findall(metalMatch, metal, re.IGNORECASE)
        metalType1 = ""
        metalType2 = ""
        metalType3 = ""
        if len(metalTypes) > 1:
            try:
                metalType1 = metalTypes[0]
            except:
                metalType1 = ''
            try:
                metalType2 = metalTypes[1]
            except:
                metalType2 = ''
            try:
                metalType3 = metalTypes[2]
            except:
                metalType3 = ''
        else:
            try:
                metalType1 = metalTypes[0]
            except:
                metalType1 = ''

        # make sure they match in the same order with the header
        info = [newSKU, hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, '', stoneType1, stoneType2, stoneType3, stoneType4]
        thewriter.writerow(info)
        print(len(info))
        print(newSKU, hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, '', stoneType1, stoneType2, stoneType3, stoneType4)

# Close the web driver when we're done
driver.quit()
