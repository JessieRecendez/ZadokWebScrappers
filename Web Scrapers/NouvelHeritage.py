# Nouvel Heritage
# DateScrapedWasSuccessful
#####
# REMEMBER Pomellato was unique as far as their page scroll goes!!!!!!!!!!!!!!!!!!!!!!!!!

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol  for the                             \u2103
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


url = "https://nouvelheritage.com/collections/view-all-jewelry"

# Set this to a higher value if the website takes longer to load more content
scroll_pause_time = 1
scroll_count = 0
max_scroll_count = 10  # Set this to a higher value if you want to scroll more times

# Initialize a web driver (you may need to download a driver executable for your browser)
driver = webdriver.Chrome()

while True:
    # Scroll down to load more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    scroll_count += 1

    # Wait for the page to load more content
    time.sleep(scroll_pause_time)

    # Get the HTML content of the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # normal scrape first, if else for variants, then go into pages scrape if nee more info
    products = soup.find_all('div', class_='featured-product__holder')

    # save as file type in same folder
    with open('NouvelHeritageAll.xlsx', 'a', encoding='utf-8', newline='') as f:
        thewriter = writer(f)
        header = ["SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4", "Shape", "Style", "Melee Stone Shape", "Link Type", "Earring Type", "Feature", "Melee Stone Continue"]  # name columns
        thewriter.writerow(header)

        # create if else for a find.all for variants
        if not products:
            break

        for product in products:
            productLink = "sometimesWebURLIsNeeded" + product.find('a', class_='btn').get("href")
            try:
                hero = "sometimesWebURLIsNeeded" + product.find('img', class_='maybeNotNeeded').get(
                    "src").replace("someAnnoyingLongEndingAfterFileType", "")
                hero = re.sub(r'\?.*', '', hero)
            except:
                hero = ""
            try:
                price = product.find('span', class_='price').text.replace('$', '').replace(
                    ',', '').replace(".00", "").replace('\n', '').replace("\u301c", "")
            except:
                price = ""
            productTitle = product.find('span', class_='visually-hidden').text.replace("14k Gold", "").replace('\n', '').replace("\u301c", "")
            collectionMatch = r'\b(Medallion Charms|Byzantine|Duchessa|Tiny Treasures|Diamonds By The Inch|Designer Gold|Palazzo Ducale|Perfect Gold Hoops|Tassel|Veneto|Love In Verona|Obelisco|Petals|Petite Venetian Princess|Pois Mois Luna|Primavera|Principessa|Princess Flower|Royal Opera|Royal Princess Flower|Siena|Symphony|Portofino|Perfect Diamond Hoops|Venetian Princess|Veneto)\b'
            collections = re.search(
                collectionMatch, productTitle, re.IGNORECASE)
            if collections:
                collections = collections.group(0)
            else:
                collections = ""

            chainMatch = r'\b(Link|Paperclip|Rope|Braided|Cuban|Curb)\b'
            chainType = re.search(chainMatch, productTitle, re.IGNORECASE)
            if chainType:
                chainType = chainType.group(0)
            else:
                chainType = ""

            productShapeMatch = r'\b(Butterfly|Bar|Circle|Open Circle|Tablet|Leaf|Ribbon|Infinity|Peace Sign|Triangle|Square|Horse Shoe|Sunburst|Wishbone|Fish|Frog|Owl|Dog|Dog Bone|Arrow|Cat|Happy Face|Hamsa|Anchor|Palm Tree| Key|Skull & Crossbones|Skull|Skeleton|Flower|Heart|Slanted Heart|Open Heart|Locket|Bumble Bee|Dog Tag|Tassel|Snake|Cross|Circle|Starfish|Zipper|Texas|Boot)\b'
            itemShape = re.search(
                productShapeMatch, productTitle, re.IGNORECASE)
            if itemShape:
                itemShape = itemShape.group(0)
            else:
                itemShape = ""

            ContinMatch = r'\b(Eternity)\b'
            meleeStoneCont = re.search(
                ContinMatch, productTitle, re.IGNORECASE)
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

            earringTypeMatch = r'\b(Stud|Hoop|Dangle|Drop|Chandelier|Cuff|Climber|Huggie|Huggie|Omega)\b'
            productEarringType = re.search(
                earringTypeMatch, productTitle, re.IGNORECASE)
            if productEarringType:
                productEarringType = productEarringType.groups(0)
            else:
                productEarringType = ""

            shapeMatch = r'\b(Butterfly|Bar|Leaf|Flower|Heart|Bumble Bee|Feather|Safety Pin|Dog Tag|Dog Bone|Clover|Snake|Horseshoe|Star|Lightning Bolt)\b'
            productShape = re.search(shapeMatch, productTitle, re.IGNORECASE)
            if productShape:
                productShape = productShape.group(0)
            else:
                productShape = ""

            shapeMatch = r'\b(Baguette|Round|Princess|Asscher|Cushion|Oval|Emerald|Radiant|Heart)\b'
            gemShape = re.search(shapeMatch, productTitle, re.IGNORECASE)
            if gemShape:
                gemShape = gemShape.group(0).strip()
            else:
                gemShape = ""

            productMatch = r'\b(Ring|Bracelet|Bangle|Necklace|Pendant|Earrings|Charm)\b'
            productType = re.search(productMatch, productTitle, re.IGNORECASE)
            # Extracting the found product type
            if productType:
                productType = productType.group(0)
            else:
                productType = ""

            featureMatch = r'\b(Tennis|Stretch|Overpass|Bypass|Convertable|Graduated|Twist|Twisted|2 Row|3 Row|4 Row|Adjustable|Station|3 Station|4 Station|5 Station|6 Station|7 Station|15 Station|19 Staion|Flex|Zodiac)\b'
            featureType = re.search(featureMatch, productTitle, re.IGNORECASE)
            if featureType:
                featureType = featureType.group(0).replace('\n', '').strip()
            else:
                featureType = ''

            # Sku may be availble only within each product page, so this may need to be moved
            sku = product.find(
                'span', class_="hopeForSomethingEasy").text.replace('\n', '')

            # make a request to the product page to get the SKU
            # Hence, click into each URL to get even more possible unique data
            productPage = requests.get(productLink)
            productSoup = BeautifulSoup(productPage.content, 'html.parser')
            try:
                stone = product.find('h2', class_='woocommerce-loop-product__title').replace('citrine', 'Citrine').replace('tourmaline', 'Tourmaline').replace('tsavorite', 'Tsavorite').replace('malachite', 'Malachite').replace('jet', 'Jet').replace('garnet', 'Garnet').replace('emerald', 'Emerald').replace('peridot', 'Peridot').replace('ruby', 'Ruby').replace('amethyst', 'Amethyst').replace('agate', 'Agate').replace('turquoise', 'Turquoise').replace('prasiolite', 'Prasiolite').replace('diamond', 'Diamond').replace('rainbow-sapphire', 'Rainbow Sapphire').replace('orange-citrine', 'Orange Citrine').replace('black-diamond', 'Black Diamond').replace('blue-diamond', 'Blue Diamond').replace('brown-diamond', 'Brown Diamond').replace('champagne-diamond', 'Champagne Diamond').replace('green-diamond', 'Green Diamond').replace('pink-diamond', 'Pink Diamond').replace('yellow-diamond', 'Yellow Diamond').replace('green-tsavorite', 'Green Tsavorite').replace('black-jade', 'Black Jade').replace('green-jade', 'Green Jade').replace('white-jade', 'White Jade').replace('lapis-lazuli', 'Lapis Lazuli').replace('green-malachite', 'Green Malachite').replace('rainbow-moonstone', 'Rainbow Moonstone').replace('white-moonstone', 'White Moonstone').replace('black-mother-of-pearl', 'Black Mother of Pearl').replace('white-mother-of-pearl', 'White Mother of Pearl').replace(
                    'mother-of-pearl', 'Mother of Pearl').replace('green-amethyst', 'Green Amethyst').replace('green-quartz', 'Green Quartz').replace('lemon-quartz', 'Lemon Quartz').replace('black-night-quartz', 'Black Night Quartz').replace('rose-de-france', 'Rose de France').replace('rose-quartz', 'Rose Quartz').replace('black-sapphire', 'Black Sapphire').replace('blue-sapphire', 'Blue Sapphire').replace('light-blue-sapphire', 'Light Blue Sapphire').replace('dark-blue-sapphire', 'Dark Blue Sapphire').replace('green-sapphire', 'Green Sapphire').replace('pink-sapphire', 'Pink Sapphire').replace('orange-sapphire', 'Orange Sapphire').replace('purple-sapphire', 'Purple Sapphire').replace('white-sapphire', 'White Sapphire').replace('yellow-sapphire', 'Yellow Sapphire').replace('black-spinel', 'Black Spinel').replace('blue-topaz', 'Blue Topaz').replace('english-blue-topaz', 'English Blue Topaz').replace('green-envy-topaz', 'Green Envy Topaz').replace('blue-london-topaz', 'London Blue Topaz').replace('morganite-topaz', 'Morganite Topaz').replace('pink-topaz', 'Pink Topaz').replace('sky-blue-topaz', 'Sky Blue Topaz').replace('swiss-blue-topaz', 'Swiss Blue Topaz').replace('white-topaz', 'White Topaz').replace('green-tourmaline', 'Green Tourmaline').replace('pink-tourmaline', 'Pink Tourmaline').replace('red-carnelian', 'Red Carnelian')
            except:
                stone = ""
            stoneMatch = r'\b(Apatite|Rainbow Sapphire|Morganite|Citrine|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|Emerald|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
            stoneTypes = re.findall(stoneMatch, productTitle, re.IGNORECASE)
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
                description = productSoup.find('div', class_="someSimpleTextSomewhere").text.replace(
                    '”', '"').replace('“', '"').replace("...", '').replace('\u2005', ' ').replace('\xa0', ' ')
            except:
                description = ""
            try:
                metal = productSoup.find('tag', class_="findMe").text
            except:
                metal = ""
            metalMatch = r'\b(14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|14k Gold|18k Gold|18k White Gold|18k Yellow Gold|18k Rose Gold|18k Pink Gold|Platinum)\b'
            metalTypes = re.findall(metalMatch, productTitle, re.IGNORECASE)
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
            info = [sku, hero, productLink, productType, price, productTitle, '', collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont]
            thewriter.writerow(info)
            print(len(info))
            print(sku, hero, productLink, productType, price, productTitle, '', collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont)

    # Check if we have scrolled enough times
    if scroll_count >= max_scroll_count:
        break

# Close the web driver when we're done
driver.quit()