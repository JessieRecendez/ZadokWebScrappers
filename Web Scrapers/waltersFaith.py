# Walters Faith
# 2023-08-17
#####
# REMEMBER Pomellato was unique as far as their page scroll goes!!!!!!!!!!!!!!!!!!!!!!!!!

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol  for the                             \u2103
# this is a simple bullet point black dot                               \u30fb
# this is just an empty space                                           \u2005
# this is the &nbsp;                                                    \xa0
# this is ~ a wavy dash used in approximate japanese price              \u301c
# this is ® the registered sign                                         \u00AE
# this is Â letter a with a circumflex                                  \u00C2
#

import requests
from bs4 import BeautifulSoup
import time
import re
from csv import writer
from selenium import webdriver
import random


driver = webdriver.Chrome()
url = "https://waltersfaith.com/collections/rings"
# rings
# necklaces
# earrings
# bracelets-cuffs
# charms
# sterling-silver
driver.get(url)

delay = random.uniform(0, 2.5)
prev_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to load more content
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(1.5)    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    
    # Update the previous height of the page
    prev_height = new_height

# Get the page source and create a Beautiful Soup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
products = soup.find_all('div', class_='grid__item--collection-template')

# save as file type in same folder
with open('waltersFailthRings.xlsx', 'a', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    header = ["Image", "Hero Image", "Model Image", "SKU", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4", "Shape", "Style", "Melee Stone Shape", "Link Type", "Earring Type", "Feature", "Melee Stone Continue"]  # name columns
    thewriter.writerow(header)

    for product in products:
        productLink = "https://waltersfaith.com" + product.find('a', class_='grid-view-item__image-container').get("href")
            
        try:
            model2 = "https:" + product.find('img', class_='grid-view-item__image__second').get("src").replace('250x', '1024x').replace('300x300', '1024x1024')
            model2 = re.sub(r'\?.*', '', model2)
        except:
            model2 = ""
            
        try:
            price = product.find('span', class_='product-price__price').text.replace('$', '').replace(',', '').replace(".00", "").replace('\n', '').replace("\u301c", "")
        except:
            price = ""
            
        productTitle = product.find('div', class_='grid-view-item__title').text.replace("14k Gold", "").replace('\n', '').replace("\u301c", "").replace('Mm ', 'mm ').title()
        
        collectionMatch = r'\b(Bell|Carrington|Classic|Clive|Clive II|Dora|Garnet|Grant|Keynes|Lytton|Morrell|Ottoline|Quentin|OC X WF|Saxon|Sydney|Thoby|Woolf)\b'
        collections = re.search(collectionMatch, productTitle, re.IGNORECASE)
        if collections:
            collections = collections.group(0)
        else:
            collections = ""

        chainMatch = r'\b(Link|Paperclip|Rope|Braided|Cuban|Curb|Mariner|Rolo|Box|Boa)\b'
        chainType = re.search(chainMatch, productTitle, re.IGNORECASE)
        if chainType:
            chainType = chainType.group(0).replace('Boa', 'Snake')
        else:
            chainType = ""

        productShapeMatch = r'\b(Butterfly|Bar|Ram Head|Door Knocker|Snake Head|Lion Head|Tubular|Feather|Ice Pick|V|Safety Pin|Dog Bone|Clover|Horseshoe|Star|Lightning Bolt|Small Cirlce|Seashell|Dollar Sign|Lotus|Baseball|Soccer|Football|Basketball|Small Double Circle|Circle|Open Circle|Tablet|Leaf|Ribbon|Infinity|Peace Sign|Triangle|Square|Horse Shoe|Sunburst|Wishbone|Fish|Frog|Owl|Dog|Dog Bone|Arrow|Cat|Happy Face|Hamsa|Anchor|Palm Tree| Key|Skull & Crossbones|Skull|Skeleton|Flower|Heart|Slanted Heart|Open Heart|Locket|Bumble Bee|Dog Tag|Tassel|Snake|Cross|Circle|Starfish|Zipper|Texas|Boot)\b'
        itemShape = re.search(productShapeMatch, productTitle, re.IGNORECASE)
        if itemShape:
            itemShape = itemShape.group(0)
        else:
            itemShape = ""

        ContinMatch = r'\b(Eternity)\b'
        meleeStoneCont = re.search(ContinMatch, productTitle, re.IGNORECASE)
        if meleeStoneCont:
            meleeStoneCont = meleeStoneCont.group(0)
        else:
            meleeStoneCont = ""

        styleMatch = r'\b(Braided|Cathedral|Chunky|Cluster|Halo|Double Halo|Double Prong|Double Shank|Split Shank|East West|Filigree|Floral|Kite Set|Knife Edge|Lattice|Milgrain|Ribbon|Rope|Scallop)\b'
        productStyle = re.search(styleMatch, productTitle, re.IGNORECASE)
        if productStyle:
            productStyle = productStyle.group(0)
        else:
            productStyle = ""

        earringTypeMatch = r'\b(Stud|Studs|Hoop|Dangle|Drop|Chandelier|Cuff|Climber|Huggie|Huggies|Omega|Jacket)\b'
        productEarringType = re.search(earringTypeMatch, productTitle, re.IGNORECASE)
        if productEarringType:
            productEarringType = productEarringType.group(0)
        else:
            productEarringType = ""

        shapeMatch = r'\b(Baguette|Round|Princess|Asscher|Cushion|Oval|Emerald|Radiant|Heart)\b'
        gemShape = re.search(shapeMatch, productTitle, re.IGNORECASE)
        if gemShape:
            gemShape = gemShape.group(0).strip()
        else:
            gemShape = ""

        productMatch = r'\b(Ring|Bracelet|Bangle|Brooch|Cuff|Cufflinks|Necklace|Choker|Collar|Pendant|Earring|Earrings|Hoop|Hoops|Huggie|Huggies|Stud|Studs|Earrings|Charm|Charms)\b'
        productType = re.search(productMatch, productTitle, re.IGNORECASE)
        if productType:
            productType = productType.group(0).lower().replace('hoops', 'earrings').replace('hoop', 'earrings').replace('huggies', 'earrings').replace('huggie', 'earrings').replace('studs', 'earrings').replace('stud', 'earrings').replace('collar', 'necklace').replace('chocker', 'necklace').title()
        else:
            productType = ""

        featureMatch = r'\b(Lariat|Tennis|Stretch|Overpass|Bypass|Convertable|Faceted|Fluted|Graduated|Graduating|Elongated|Twist|Twisted|2 Row|3 Row|4 Row|Adjustable|Station|3 Station|4 Station|5 Station|6 Station|7 Station|15 Station|19 Staion|Flex|Zodiac)\b'
        featureType = re.search(featureMatch, productTitle, re.IGNORECASE)
        if featureType:
            featureType = featureType.group(0).replace('\n', '').strip()
        else:
            featureType = ''

        # Hence, click into each URL to get even more possible unique data
        productPage = requests.get(productLink)
        productSoup = BeautifulSoup(productPage.content, 'html.parser')
        
        time.sleep(delay)
        # Sku may be availble only within each product page, so this may need to be moved
        skuData = productSoup.find('div', class_='product-single__description').text
        sku = re.search(r'Style\s?#?:?\s?(\w+\d+-\w+)\s?', skuData, re.IGNORECASE)
        if sku:
            sku = sku.group(1).replace('\xa0', ' ').replace('&nbsp;', ' ').replace('Style#: ', 'Style #: ').replace('Style # ', 'Style #: ').replace('STYLE # ', 'Style #: ').replace('Style #:', 'Style #: ').replace('Style #:\xa0', 'Style #: ').strip()
        else:
            sku = ""
            
        try:
            hero = "https:" + productSoup.find('img', class_='feature-row__image').get("src").replace('_300x300', '_1024x1024').replace('_360x', '_1024x')
            hero = re.sub(r'\?.*', '', hero)
        except:
            hero = ""
        
        stoneMatch = r'\b(Apatite|Rainbow Sapphire|Morganite|Citrine|Rock Crystal|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|Emerald|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
        stoneTypes = re.findall(stoneMatch, productTitle, re.IGNORECASE)
        stoneType1 = ""
        stoneType2 = ""
        stoneType3 = ""
        stoneType4 = ""
        if len(stoneTypes) > 1:
            try:
                stoneType1 = stoneTypes[0].title()
            except:
                stoneType1 = ''
            try:
                stoneType2 = stoneTypes[1].title()
            except:
                stoneType2 = ''
            try:
                stoneType3 = stoneTypes[2].title()
            except:
                stoneType3 = ''
            try:
                stoneType4 = stoneTypes[3].title()
            except:
                stoneType4 = ''
        else:
            try:
                stoneType1 = stoneTypes[0].title()
            except:
                stoneType1 = ''

        metalMatch = r'\b(14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|14k Gold|18k Gold|18k White Gold|18k Yellow Gold|18k Rose Gold|18k Pink Gold|Platinum|Black Rhodium|Sterling Silver)\b'
        metalTypes = re.findall(metalMatch, productTitle, re.IGNORECASE)
        metalType1 = ""
        metalType2 = ""
        metalType3 = ""
        if len(metalTypes) > 1:
            try:
                metalType1 = metalTypes[0].title().replace('14K', '14k').replace('18K', '18k')
            except:
                metalType1 = ''
            try:
                metalType2 = metalTypes[1].title().replace('14K', '14k').replace('18K', '18k')
            except:
                metalType2 = ''
            try:
                metalType3 = metalTypes[2].title().replace('14K', '14k').replace('18K', '18k')
            except:
                metalType3 = ''
        else:
            try:
                metalType1 = metalTypes[0].title().replace('14K', '14k').replace('18K', '18k')
            except:
                metalType1 = '' 

        info = ["=image(B2)", hero, model2, productLink, sku, productType, price, productTitle, '', collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont]
        thewriter.writerow(info)
        print(len(info))
        print("=image(B2)", hero, model2, productLink, sku, productType, price, productTitle, '', collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont)

# Close the web driver when we're done
driver.quit()
