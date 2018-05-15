import time
import urllib.request
import json
import sqlite3
import os
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

db = sqlite3.connect('./Info/housingDB.db')
cursor = db.cursor()

def collectHomeInfo( url, address ):
    saveQestion = "would you like to save this information (Y/N): "
    save = YesNoFormat( saveQestion )

    if save in ['y', 'yes']:
        saveImageQuestion = "would you also like to store pictures of the home (Y/N): "
        saveImages = YesNoFormat( saveImageQuestion )
 
    driver = webdriver.Chrome()
    driver.get(url)

    searchBoxPath = '//*[@id="area"]'
    searchBox = driver.find_element_by_xpath( searchBoxPath )
    searchBox.send_keys( address )
    time.sleep(3)

    searchButtonPath = '//*[@id="findHomesButton"]' 
    searchButton = driver.find_element_by_xpath( searchButtonPath )
    searchButton.click()
    time.sleep(3)

    listedAddressPathTop = '//*[@id="leftColumn"]/div[5]/div/div/div[2]/div[1]/div[2]/a/span/span'
    listedAddressPathBottom = '//*[@id="leftColumn"]/div[5]/div/div/div[2]/div[1]/div[2]/a/span/div'
    listedAddress = driver.find_element_by_xpath( listedAddressPathTop ).text + " " 
    listedAddress += driver.find_element_by_xpath( listedAddressPathBottom ).text
    
    address = cleanAddress(address)
    if  address != cleanAddress(listedAddress):
        print("The address isn't listed online")
        driver.close()
        driver.quit()
        return

    viewDetailsButtonPath = '//*[@id="leftColumn"]/div[5]/div/div/div[2]/div[1]/div[5]/a'
    viewDetailButton = driver.find_element_by_xpath( viewDetailsButtonPath )
    viewDetailButton.click()
    time.sleep(3)
        
    homeData = {}
    homeData['address'] = address.replace(" ","_").replace(",","")

    pricePaths = ['//*[@id="homeFinder"]/div[2]/div/section[1]/div/div/div[2]/div/ul[1]/li[1]']
    price = testXPaths( driver, pricePaths )
    if price == 'n/a':
        homeData['price'] = 0
    else:
        homeData['price'] = price

    yearBuiltPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[6]/ul[1]/li[2]',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[13]/dd']
    yearBuilt = testXPaths( driver, yearBuiltPaths )
    if yearBuilt == 'n/a':
        homeData['yearBuilt'] = 0
    else:
        homeData['yearBuilt'] = yearBuilt

    daysListedPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[6]/ul[1]/li[3]']
    daysListed = testXPaths( driver, daysListedPaths )
    if daysListed == 'n/a':
        homeData['daysListed'] = 0
    else:
        homeData['daysListed'] = daysListed

    estMorgagePaths = ['//*[@id="homeFinder"]/div[2]/div/section[1]/div/div/div[2]/div/ul[2]/li[1]/a']
    estMorgage = testXPaths(driver, estMorgagePaths )
    homeData['estMorgage'] = estMorgage
   

    bedsPaths = ['//*[@id="homeFinder"]/div[2]/div/section[1]/div/div/div[2]/div/ul[3]/li[1]',
                '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[6]/dd']
    beds = testXPaths( driver, bedsPaths )
    if beds == 'n/a':
        homeData['beds'] = 0
    else:
        homeData['beds'] = beds

    
    bathsPaths = ['//*[@id="homeFinder"]/div[2]/div/section[1]/div/div/div[2]/div/ul[3]/li[2]',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[7]/dd']
    bath = testXPaths( driver, bathsPaths )
    homeData['bath'] = bath
    
    taxesPaths =['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div[3]/div/div/dl/dd',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[2]/dd']
    taxes = testXPaths( driver, taxesPaths )
    homeData['taxes'] = taxes
    
    coolingPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div[4]/div/div/dl/dd',
             '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[17]/dd']
    cooling = testXPaths( driver, coolingPaths )
    homeData['cooling'] = cooling

    sqrtfeetPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div[2]/div/div/dl[1]/dt',
             '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[11]/dd']
    sqrtfeet = testXPaths( driver, sqrtfeetPaths )
    homeData['sqrtfeet'] = sqrtfeet

    homeTypePaths = ['//*[@id="homeFinder"]/div[2]/div/section[1]/div/div/div[2]/div/ul[4]/li[1]',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/dl[5]/dd']
    homeType = testXPaths( driver, homeTypePaths )
    homeData['homeType'] = homeType

    realtorPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[2]/div/div/div[1]/a',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[2]/div/div/div[1]/span']
    realtor = testXPaths( driver, realtorPaths )    
    homeData['realtor'] = realtor

    agentPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[2]/div/div/div[3]/a',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[2]/div/div/div[3]/span']
    agent = testXPaths( driver, agentPaths )
    homeData['agent'] = agent
    

    agentPhonePaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[2]/div/div/div[2]']
    agentPhone = testXPaths( driver, agentPhonePaths )
    homeData['agentPhone'] = agentPhone
    

    desPaths = ['//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[6]/p',
            '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[7]/div/div/div/p']
    des = testXPaths( driver, desPaths )
    homeData['des']= des

    displayHomeInfo( homeData )
    
    if save in ['y', 'yes']:
        storeHouseInfo( homeData )
        collectPhotos(driver, saveImages, homeData['address'])

    driver.close()
    driver.quit()

"""Clears user delimitters from address"""
def cleanAddress(address):
    delimiters = re.compile(r'\W+')
    splitAddress = delimiters.split(address)
    newAddress = splitAddress[0]
    for txt in range(1, len( splitAddress ) ):
        newAddress += "_"+splitAddress[txt]

    return newAddress.lower()

"""Ensures the user always answer in a yes no format"""
def YesNoFormat(query):

        response = input (query)

        while response.lower() not in ['y','n','yes','no']:
            print("Please enter your answer in the form of yes or no")
            response = input(query)

        return response

"""Test if a field exists on a page, if no provides deafult value"""
def fieldExists(driver, xPath):
    
    field = ""

    try:
        field = driver.find_element_by_xpath( xPath )

    except: 
         return "n/a"

    return field.text

"""Since not all each fields can have the same xPath for different pages, it tests all known paths"""
def testXPaths(driver, paths):
    field = ""
    for x in paths:
        field = fieldExists(driver, x )
        if field != "n/a":
            break

    return field

"""scrapes all photos"""
def collectPhotos( driver, response, address ):
    if response.lower() in ['yes', 'y']:
        try:

            img = 1
            while(True):
                
                imgPath = '//*[@id="homeFinder"]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div/div/div[{}]/div/img'.format( img )
                src = driver.find_element_by_xpath( imgPath ).get_attribute( 'src' )

                name = "{} {}.png".format(address, img)                
                path = "./Images/{}".format( name )

                image = urllib.request.urlretrieve( src, path )
                storeImgPath( address, name, path)
                img+=1

        except:
           print ( "Aquired all images" )
           print( "Check the programs Images directory to view your potential home" )

"""stores photos paths in images table"""
def storeImgPath(address, name, path):
   
    cursor.execute(  "SELECT * FROM Images WHERE path = ?;", (path,) )
    entry = cursor.fetchone()

    if entry is None:
        cursor.execute( "INSERT INTO Images values ( ?, ?, ?);", (path, name, address,) )

"""stores collected data into info table"""
def storeHouseInfo( homeData ):
    
    print(len( homeData['address']))
    #Checks if entry exists to ensure no redundancy
    cursor.execute( "SELECT * FROM Info WHERE Address = ?;", ( homeData['address'], ) ) 
    entry = cursor.fetchone()

    if entry is None:
        cursor.execute("""INSERT INTO Info VALUES (?,?,?,?,?,
                                                    ?,?,?,?,?,
                                                    ?,?,?,?,?);""", (
                                                    homeData['address'], homeData['price'],
                                                    homeData['yearBuilt'], homeData['daysListed'],
                                                    homeData['estMorgage'], homeData['beds'],
                                                    homeData['bath'], homeData['cooling'],
                                                    homeData['taxes'], homeData['sqrtfeet'],
                                                    homeData['homeType'], homeData['realtor'], 
                                                    homeData['agent'], homeData['agentPhone'], 
                                                    homeData['des'],) )
        print( "House data stored" )
    else:
        print( "House data already exists" )
"""Deletes all tables entries of an address from the database and erases all associated pictures from images folder"""
def deleteHouseData( address ):
    
    #Delete all photos for that house first
    for entry in cursor.execute(  "SELECT Path FROM Images WHERE Address = ?;", ( address, ) ):
        os.remove(entry[0])

    cursor.execute("DELETE FROM Images where address = ?;", ( address, ) )
    cursor.execute("DELETE FROM Info where address = ?;", ( address, ) )

    displayAllStoredAddresses()

"""Displays all stored addresses"""
def displayAllStoredAddresses():
    addressQuery = "SELECT Address from Info;"
    for address in  cursor.execute(addressQuery):
        print( address )

"""displays the number of photos associated with an address"""
def displayImageCount( address ):   
    cursor.execute( "SELECT * from Images where address =?;", ( address, ) )
    total =  len( cursor.fetchall() ) 
    print( "The total number of houses for address\n {}\n is {}".format( address, total ) )

"""displays all kown information about an address"""
def displayAddressInfo( address ):
        
    cursor.execute(  "SELECT * from Info where address = ?;", (address,) )
    entry = cursor.fetchone()
    
    if entry is None:
        print( "Unfortunately that address doesn't exist in your database")
    else:

        fields = ['address','price', 'yearBuilt', 'daysListed',
            'estMorgage', 'beds', 'bath', 'cooling',
            'taxes', 'sqrtfeet', 'homeType', 'realtor',
            'agent', 'agentPhone', 'des']

        homeData = {}
        for i in range( len( fields ) ):
            homeData[fields[i]] = entry[i]

        displayHomeInfo( homeData )

"""makes database tables if they don't exist"""
def makeTables():
    housingDataquery = """CREATE TABLE IF NOT EXISTS Info(Address BLOB PRIMARY KEY, 
                        Price REAL, YearBuilt TEXT, DaysListed INTEGER, 
                        EstMorgage TEXT, Bed INTEGER, Bathrooms TEXT,  
                        System TEXT, Taxes TEXT, Sqrtfeet TEXT, HomeType TEXT,
                        Realtor TEXT, Agent TEXT, AgentPhone TEXT, DES BLOB);"""

    cursor.execute( housingDataquery )
    
    imageQuery = """CREATE TABLE IF NOT EXISTS Images(Path BLOB PRIMARY KEY,
                    Name Text, Address BLOB,
                    FOREIGN KEY ( Address )
                    REFERENCES Info( Address ));"""

    cursor.execute( imageQuery )
    

def displayHomeInfo( HomeData ):
        
    print( "The price of the house is: {}".format( HomeData['price'] ) )
    print( "The year the home was built is: {}".format( HomeData['yearBuilt'] ) )
    print( "The number of days the home has been listed is: {}".format( HomeData['daysListed'] ) )
    print( "The estimated morage is: {}".format( HomeData['estMorgage'] ) )
    print( "The home contains {} number of bed rooms".format( HomeData['beds'] ) )
    print( "The home contains {} number of bathrooms".format( HomeData['bath'] ) )
    print( "The estimated tax on the home is {}".format( HomeData['taxes'] ) )
    print( "The home comes with a {} system".format( HomeData['cooling'] ) )
    print( "The sqrt footage of the home is: {}".format( HomeData['sqrtfeet'] ) )
    print( "This is a {}".format( HomeData['homeType'] ) )
    print( "The realtor is {}".format( HomeData['realtor'] ) )
    print( "The agent for the home is {}.".format( HomeData['agent'] ) )
    print( "The number to contact the agent is ".format( HomeData['agentPhone'] ) )
    print( "The home description is:\n{}".format( HomeData['des'] ) )

def main():
    
    makeTables()

    continueProgram = True
    while continueProgram:
            
        try:
            print("Please select from the following options")
            print("Press 1 to scrape houseing info for an address")
            print("Press 2 to list all the address currently stored in the database")
            print("Press 3 to return the number of pictures for an address")
            print("Press 4 to display the database information for an address")
            print("Press 5 to delete all records associated with an address")
            print("Press 6 to exit the program")
            choice = int( input( ) )
            
            
            if choice == 1:
                url = 'http://www.homefinder.com/'
                address = input( "Please enter an address you'd like information on:\n" )
                collectHomeInfo( url, address )

            elif choice == 2:
                displayAllStoredAddresses()
            
            elif choice == 3:
                address = input("Please enter an addresss you'd like information on:\n")
                displayImageCount( cleanAddress( address ) )               

            elif choice == 4:
                address = input( "Please enter an address:\n" )
                displayAddressInfo( cleanAddress( address ) )

            elif choice == 5:
                address = input( "Please enter an address:\n" )
                deleteHouseData( cleanAddress( address ) )

            elif choice == 6:
                continueProgram = False

            else:
                print("Please enter a value between 1 and 6")
            
             
                
        except ValueError:
            print("Please enter and integer!")

    cursor.close()
    db.commit()
    db.close()

    
main()
