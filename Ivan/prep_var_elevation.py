import sys
from splinter import Browser
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pprint import pprint
from prep_var_coast_dist import get_zip_gps

def get_all_zips():
    all_zip = set()
    fr = open(r'data/IvanExport.csv','rU')
    fr.readline()
    for line in fr.readlines():
        items = line.rstrip().split(",")
        zip = items[7]
        all_zip.add(zip)
        
    print len(all_zip)
    #pprint(all_zip)
    return all_zip
    
def test():
    url = r'http://veloroutes.org/elevation/'
    #executable_path = {'executable_path':'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'}
    #executable_path = {'executable_path':'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'}
    sys.path.append('C:\Users\Sophie\workspace\Hurricane\Ivan\geckodriver.exe')
    browser = Browser('firefox')
    browser.visit(url)

    txtbox = browser.find_by_id('loc')

    txtbox.fill('02140')
    
    btn = browser.find_element_by_id('qBtn')
    print btn
    print btn.get_attribute('innerHTML')

#     btn.click()
#     
#     
#     if browser.is_text_present('Elevation for', wait_time=10):
#         print 'enter'
#         #print browser.find_by_text('Elevation for') 
#         table = browser.find_by_tag('table')[0]
#         print table.get_attribute('innerHTML')

def test2(zipcodes):
    url = r'http://veloroutes.org/elevation/'
    driver = webdriver.Firefox()
    driver.get(url)
    
    for zipcode in zipcodes:
        print '-----------------'
        print zipcode
        
        # type in zipcode
        address = driver.find_element_by_id("loc")
        print address.get_attribute('value')
        address.clear()
        print address.get_attribute('value')
        address.send_keys(zipcode)
        print address.get_attribute('value')
        address.send_keys(Keys.RETURN)
        print address.get_attribute('value')
        #driver.implicitly_wait(10)
        
        # click button "Find elevation"
#         btn = driver.find_element_by_id("qBtn")
#         btn.click()
        
        
        # extract height
        driver.implicitly_wait(30)
#         element = WebDriverWait(driver, 10).until(\
#                 EC.text_to_be_present_in_element(\
#                 driver.find_elements_by_xpath('//div[contains(text(), "Elevation for ")]'), zipcode))
#         print element
        
        # how often does it refresh?
        #rst = driver.find_elements_by_xpath('//div[contains(text(), "Elevation for ")]')
        rst = driver.find_elements_by_xpath("//div[@class='eleResults']/span[2]")
        print rst[0].get_attribute('outerHTML')
#         for x in rst:
#             print x
#         s = rst[0].get_attribute('outerHTML')
#         #rst[0].clear()
#         print s
#         s = re.sub('<br>', '', s)
#         pat = '\d+'
#         match = re.findall(pat, s)
#         print match
#         ht = match[3]
#         print ht

def test3():
    url = r'https://www.daftlogic.com/sandbox-google-maps-find-altitude.htm'
    driver = webdriver.Firefox()
    driver.get(url)
    coord = '29.731734, -85.111872'
    address = driver.find_element_by_id("goto")
    address.clear()
    address.send_keys(coord)
    address.send_keys(Keys.RETURN)


           
if __name__ == '__main__':
    
#     codes = ['02140', '02148']
#     test2(codes)

    all_zip = get_all_zips()
    zip_to_gps = get_zip_gps()
    for zip in sorted(all_zip):
        gps = zip_to_gps[zip]
        print "%s, %.6f, %.6f" % (zip, gps[0], gps[1])
    #test3()




    