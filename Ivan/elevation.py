import sys
from splinter import Browser
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_elevation():
    all_zip = set()
    fr = open(r'data/IvanExport.csv','rU')
    for line in fr.readlines():
        items = line.rstrip().split(",")
        zip = items[7]
        all_zip.add(zip)
        
    print len(all_zip)
    
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

def test2():
    url = r'http://veloroutes.org/elevation/'
    driver = webdriver.Firefox()
    driver.get(url)
#     btn = driver.find_element_by_id('qBtn')
#     print btn
#     print btn.get_attribute('innerHTML')
#     print btn.get_attribute('outerHTML')
    
    elem = driver.find_element_by_id("loc")
    elem.clear()
    elem.send_keys("02140")
    elem.send_keys(Keys.RETURN)
    
    driver.implicitly_wait(10)
    rst = driver.find_elements_by_xpath('//div[contains(text(), "Elevation for")]')
    rst_xml = rst[0].get_attribute('outerHTML')
    
    
#     table = driver.find_element_by_tag_name('table')
#     if table:
#         print table.get_attribute('outerHTML')

        
if __name__ == '__main__':
    #get_elevation()
    #test2()
    s = '<div class="eleResults">Elevation for <span style="font-size:20px">02140</span> is <span style="font-size:20px">42</span> feet<br><ul><li>The latitude for this location is: 42.4039980</li><li>The longitude for this location is: -71.1129389</li><li>Click <a href="http://veloroutes.org/bikemaps/?x=-71.1129389&amp;y=42.4039980&amp;z=11" style="font-size:20px;">here</a> to create a route at this location.</li></ul></div>'
    #root = etree.fromstring(s)
    s = '<div class="eleResults">Elevation for <span style="font-size:20px">02140</span> is <span style="font-size:20px">42</span></div>'
    root = etree.fromstring(s)
    print root.text
    for child in root:
        print child.tag, child.text
    