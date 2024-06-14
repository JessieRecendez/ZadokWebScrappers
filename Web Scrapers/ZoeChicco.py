# Zoe Chicco
# 2023-05-03
# so you need to scrape EACH product type page
# still need to improve variants such as metal types, chain lengths and earring pairs
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
# this is a ZERO WITH NO-BREAK SPACE                                    \ufeff

import requests
from bs4 import BeautifulSoup
import time
import re
from csv import writer

base_url = "https://zoechicco.com/collections/anklets?page="
# earrings                                    ^^^ replace product type page
# necklaces
# bracelets
# rings
# charms
# anklets
pageNum = 1

while True:
    url = base_url + str(pageNum)
    page = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(page.content, 'html.parser')

    products = soup.find_all('div', class_='ProductItem__Wrapper')
    
    # save as file type in same folder
    with open('ZoeChiccoAllAnklets.xlsx',  'a', encoding='utf-8', newline='') as f:
        thewriter = writer(f)
        header = ["SKU", "True SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4", "Shape", "Style", "Melee Stone Shape", "Link Type", "Earring Type", "Feature", "Melee Stone Continue"]  # name columns
        thewriter.writerow(header)

        if not products:
            break

        for product in products:
            productLink = 'https://zoechicco.com/' + product.find('a').get('href')
            price = product.find('span', class_='ProductItem__Price').text.replace('$', '').replace(',', '')
            productTitle = product.find('h2', class_='ProductItem__Title').text.replace('é', 'e').replace("É", "E")
            
            # make a request to the product page to get the SKU
            productPage = requests.get(productLink)
            productSoup = BeautifulSoup(productPage.content, 'html.parser')
            try:
                hero = 'https:' + productSoup.find('a', class_='Product__SlideshowNavImage').get("href")
                hero = re.sub(r'\?.*', '', hero)
            except:
                hero = ""
            try:
                sku = productSoup.find('option').get('data-sku').replace('/n', '')
            except:
                sku = ""
            
            collectionMatch = r'\b(20x20 Collabs|Amore|Baguette Diamond|Baguette Diamonds|BFF & BEST BABE|Birthstone|Black Diamond|Black Diamonds|Blue Sapphires| A la Carte Charms|Emeralds|Feel The Love|Floating Diamond|Floating Diamonds|Gold Bars|Gold Beads|Gold Discs & Shapes|Hardware|Heavy Metal|Horizon|Identity|Itty Bitty Symbol|Itty Bitty Symbols|Itty Bitty Words & Letters|Lockets, Padlocks & Dog Tags|Mantra|Marquise Diamond|Marquise Diamonds|Medallion|Medallions|Midi Bitty Symbol|Midi Bitty Symbols|Opal|Paris Collection|Pave Diamond|Pave Diamonds|Pearl|Pearls|Personalized|Princess Diamond|Princess Diamonds|Prong Diamond|Prong Diamonds|Rainbow|Ruby|Simple Gold|Tennis|Total Eclipse|Turquoise|Zodiac)\b'
            collections = re.search(collectionMatch, productTitle, re.IGNORECASE)
            if collections:
                collections = collections.group(0)
            else:
                collections = ""

            chainMatch = r'\b(Link|Paperclip|Rope|Braided|Cuban|Curb|Mariner|Rolo|Box)\b'
            chainType = re.search(chainMatch, productTitle, re.IGNORECASE)
            if chainType:
                chainType = chainType.group(0)
            else:
                chainType = ""

            productShapeMatch = r'\b(Butterfly|Bar|Ram Head|Door Knocker|Snake Head|Lion Head|Feather|Ice Pick|V|Safety Pin|Dog Bone|Clover|Horseshoe|Star|Lightning Bolt|Small Cirlce|Seashell|Dollar Sign|Lotus|Baseball|Soccer|Football|Basketball|Small Double Circle|Circle|Open Circle|Tablet|Leaf|Ribbon|Infinity|Peace Sign|Triangle|Square|Horse Shoe|Sunburst|Wishbone|Fish|Frog|Owl|Dog|Dog Bone|Arrow|Cat|Happy Face|Hamsa|Anchor|Palm Tree| Key|Skull & Crossbones|Skull|Skeleton|Flower|Heart|Slanted Heart|Open Heart|Locket|Bumble Bee|Dog Tag|Tassel|Snake|Cross|Circle|Starfish|Zipper|Texas|Boot)\b'
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
            
            productMatch = r'\b(Ring|Bracelet|Bangle|Brooch|Cuff|Cufflinks|Necklace|Choker|Collar|Pendant|Earring|Earrings|Hoop|Hoops|Stud|Studs|Earrings|Charm|Charms)\b'
            productType = re.search(productMatch, productTitle, re.IGNORECASE)
            if productType:
                productType = productType.group(0).replace("Ring", "Fashion Ring").replace("Hoop", "Earrings").replace("Hoops", "Earrings").replace("Stud", "Earrings").replace("Studs", "Earrings").replace("Collar", "Necklace").replace('ss', 's')
            else:
                productType = ""
            
            earringTypeMatch = r'\b(Stud|Hoop|Dangle|Drop|Chandelier|Cuff|Climber|Huggie|Huggie|Omega|Jacket)\b'
            productEarringType = re.search(earringTypeMatch, productTitle, re.IGNORECASE)
            if productEarringType:
                productEarringType = productEarringType.group(0)
            else:
                productEarringType = ""
                
            featureMatch = r'\b(Lariat|Flat-Link|Tennis|Stretch|Overpass|Bypass|Convertable|Graduated|Twist|Twisted|2 Row|3 Row|4 Row|Adjustable|Station|3 Station|4 Station|5 Station|6 Station|7 Station|15 Station|19 Staion|Flex|Zodiac)\b'
            featureType = re.search(featureMatch, productTitle, re.IGNORECASE)
            if featureType:
                featureType = featureType.group(0).replace('\n', '').strip()
            else:
                featureType = ''

            stoneMatch = r'\b(Apatite|Rainbow Sapphire|Morganite|Citrine|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|\b(?!Cut Emerald\b)Emerald\b|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Labradorite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
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

            metalMatch = r'\b(14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|14k Gold|18k Yellow|18k White|18k Yellow and white|18k Yellow Gold & white|18k Gold|18k White Gold|18k Yellow Gold|18k Rose Gold|18k Pink Gold|Platinum)\b'
            metalTypes = re.findall(metalMatch, productTitle, re.IGNORECASE)
            metalType1 = ""
            metalType2 = ""
            metalType3 = ""
            if len(metalTypes) > 1:
                try:
                    metalType1 = metalTypes[0].title()
                except:
                    metalType1 = ''
                try:
                    metalType2 = metalTypes[1].title()
                except:
                    metalType2 = ''
                try:
                    metalType3 = metalTypes[2].title()
                except:
                    metalType3 = ''
            else:
                try:
                    metalType1 = metalTypes[0].title()
                except:
                    metalType1 = ''
            
            try:
                description = productSoup.find('div', class_='Rte').get_text(strip=True).replace('é', 'e').replace('\xa0', '').replace('\ufeff', '')
            except:
                description = ''
        
            info = [sku, '', hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, '', chainType, productEarringType, featureType, meleeStoneCont]
            # write the row to the output file
            thewriter.writerow(info)
            print(len(info))
            print(sku, '', hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, '', chainType, productEarringType, featureType, meleeStoneCont)

    
    pageNum += 1