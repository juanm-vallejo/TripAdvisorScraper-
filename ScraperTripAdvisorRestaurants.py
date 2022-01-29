import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
##Function calls Selenium to get the HTML source of the input link. Get the quantity of Restaurants in the city.
##We use selenium given that the information is in a flexbox, the Request library struggles to get the HTML in that item.

def Initial():
    """
    Calls the request Library, gets the link to scrapre as input. The output is headers, desired link and total of restaurants in the city.
    """ 
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    link = str(input("Insert the link of the desired restaurant's city"))
    driver = webdriver.Chrome()
    driver.get(link)
    rawSource = driver.page_source
    source = bs(rawSource, 'html.parser')
    rawTotalRestaurants = source.find_all('span',{"class": 'ffdhf b'})
    totalRestaurants = int(((str(rawTotalRestaurants)).split('"ffdhf b">')[1]).split('</')[0])
    return(header, link, totalRestaurants)
##Turns the link into an scrappeable one. The link need to be ordered in a quantity of 30 restaurantes per page and its muliples.

def arrangeLink(link):
    """
    Recieves the link, which was input on Initial function, output a scrapable Link.
    """ 
    emp_str = ""
    for char in link:
        if char.isdigit():
            emp_str = emp_str + char
    position = link.find(emp_str) + len(emp_str)
    newLink = link[:position] + '-oa%s' + link[position:]

    return(newLink)
## This functions scrapes all the pages which cointains restaurants in the city. Selenium would be slow to go into each link,
## therefore, here we use the Requests library to get all the HTML, we filter by the needed classes. And get a list with all
## the restaurants to scrape.

def AllHTML(header, link ,totalRestaurants):
    """
    Recieves headers to call request, link to be arranged, quantity of restaurants in the desired city to be scraped.
    Returns list of the needed classes with the restaurants.
    """ 

    listOfAllClass = []
    for pag in range(0, totalRestaurants, 30):
        pages = requests.get(arrangeLink(link) %(pag), headers= header)
        soups = bs(pages.text, 'html.parser')
        pageHTMLs = soups.find_all('div',{"class": 'emrzT Vt o'})
        listOfAllClass.append(pageHTMLs)
    classList = []
    for ClassGroup in listOfAllClass:
        for Class in ClassGroup:
            classList.append(Class)
             
    return(classList)
## First function, If approved, go to getLink
## This function tests if the restaurants pass the cusine speciallity filter. The typeFood variable can be 
## filled with the kind of cusines that Tripadvisor has. The string must be equal to the ones in Tripadvisor.  

typeFood = []

def getFoodType(pageHTML):
    """
    Recieves HTML, searchs for the cusine filters, returns True if the restaurant has the kind of cusine, passed if not.
    """ 
    type = pageHTML.find('div', {'class': 'bhDlF bPJHV eQXRG'})
    typeStr = str(type)
    start = typeStr.find('"ceUbJ"') + len('"ceUbJ"')
    end = typeStr.find('</span></span>')
    substring = typeStr[start:end]

    if not typeFood:
        return(True)
    else:
        for food in typeFood:
            if food.lower() in (substring.lower()).strip():
                return(True)
            else:
                pass
## This function searchs for all the links needed to enter to get the information of Tripadvisor.
## In the page where all restaurants are listed we dont have the required info. Therefore, we grt the 
## referenced link to open all the information.

def getLink(pageHTML):
    """
    Recieves HTML, searchs for the selected restaurant link, returns the link to scrape for the information on the selected restaurant.
    """ 
    link= pageHTML.find('a', {'class': 'bHGqj Cj b'})
    linkStr = (str(link))
    start = linkStr.find('href="') + len('href="')
    end = linkStr.find('" target')
    substring = linkStr[start:end]

    return("https://www.tripadvisor.com" + substring)
#All the following functions clean the date to have a clearer dataframe.

def listKitchen(var):
    """
    Input, Kitchen/cusine related info. Output, list of cusine offered.
    """

    if "class" in str(var):
        var1 = str(var).split('>')[1]
        var2 = var1.split('<')[0]
        var3 = list(var2.split(','))
        return (var3)
    else:
        return(list(var.split(',')))

def intReviews(var):
    """
    Input, reviews related info. Output, integer quantity of reviews.
    """

    if "class" in str(var):
        var1 = str(var).split('>')[1]
        var2 = var1.split(' review')[0]
        if ',' in var2:
            var4 = var2.replace(',', '')
            return(var4)
        else:
            var3 = int(var2)
        return(var3)
    else:
        return(int(var))

def floatOverall(var):
    """
    Input, reviews average. Output, float overall punctuation.
    """

    if "class" in str(var):
        var1 = str(var).split('>')[1]
        var2 = var1.split('<')[0]
        var3 = float(var2)
        return (var3)
    else:
        return(float(var))

def strPriceRange(var):
    """
    Input, price range information. Output, str with the range and currency.
    """

    if '€' in str(var):
        if "class" in str(var):
            var1 = str(var).split('>')[1]
            var2 = var1.split('<')[0]
            var3 = str(var2)
            return (var3)
        else:
            return(str(var))
    else:
        return('Na')

def listPrices(var):
    """
    Input, price list of the restaurant. Output, list with prices.
    """

    if 'class' in str(var) and '€' in str(var):
        newVar = []
        var1 = str(var)
        var2 = list(var1.split(','))
        for item in var2:
            var3 = item.split('</span>')
            for price in var3:
                if '€' in str(price):
                    var4 = price.split('€')[1]
                    newVar.append(float(var4))
        return(newVar)
    else:
        return('Na')

def listPunctuation(var):
    """
    Input, punctuation info. Output, ordered quantity of punctuations (Excelent, Very Good, Average, Poor, Terrible).
    """
    
    newVar = []
    var1 = str(var)
    var2 = var1.split(',')
    for item in var2:
        var3 = item.split('>')[1]
        var4 = var3.split('<')[0]
        newVar.append(var4)
    return(newVar)

## This function opens all the links, which were previously filtered, to get the restaurant's information.
## We use selenium to open the link to avoid Ajax errors. The function avoids also any index error for the changes in the HTML
## in some particular page.

def potCustomer(link):
    """
    Recieves Link of the restaurant information, calls selenium to open the link. Returns dictionary with the desired information. 
    """ 
    try:
        driver = webdriver.Chrome()
        driver.get(link)
        rawSource = driver.page_source
        rawSourceSoup = bs(rawSource, 'html.parser')
        rawName = driver.find_elements(By.CLASS_NAME, 'fHibz')
        rawInfo = driver.find_elements(By.CLASS_NAME, 'dyeJW')
        rawWebsite = driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/span[3]/span/a')
        name = rawName[0].text
        kitchen = (rawSourceSoup.find_all('div',{"class": 'cfvAV'})[1])
        position = rawInfo[1].text
        address = rawInfo[3].text
        phoneNumber = rawInfo[4].text
        website = rawWebsite[0].get_attribute('href')
        numReviews = (rawSourceSoup.find_all('div',{"class": 'cfxpI ui_column is-12-mobile is-4-desktop'})[0].find_all('a',{"class": 'dUfZJ'}))[0]
        reviewsGen = rawSourceSoup.find_all('span',{"class": 'fdsdx'})
        priceRange = (rawSourceSoup.find_all('div',{"class": 'cfvAV'})[0])
        prices = rawSourceSoup.find_all('span',{"class": 'dXMSb d'})
        puntuationRaw = rawSourceSoup.find_all('div',{"class": 'prw_rup prw_filters_detail_checkbox'})
        puntuation = puntuationRaw[0].find_all('span',{"class": 'row_num'})

        db = {'CompanyName': str(name), 'Cusine': listKitchen(kitchen), 'Importance': position, 'Address': address, 'PhoneNumber': phoneNumber, 'Website': website, 'NumReviews': intReviews(numReviews), 'Overall': floatOverall(reviewsGen[0]), 'PriceRange': strPriceRange(priceRange), 'Prices': listPrices(prices), 'Puntuation': listPunctuation(puntuation)}
        return(db)
    except IndexError:
        pass
    
## This function agroups all the above. It calls every other function to get the information into a database.

def dataframe(classList):
    """
    Recieves list of classes, calls getFoodType, getLink, potCustomer. Returns database in pandas format. 
    """ 
    
    df = pd.DataFrame()

    for restaurant in classList:
        if getFoodType(restaurant) is True:
            link = getLink(restaurant)
            db = potCustomer(link)
            df = df.append(db, ignore_index=True)
        else:
            pass
    return df

baseData = Initial()
classList = AllHTML(baseData[0], baseData[1] , baseData[2])
df = dataframe(classList)
df.to_csv('ScrapedData.cvs')