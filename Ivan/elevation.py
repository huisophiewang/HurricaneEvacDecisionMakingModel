import sys
from splinter import Browser

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
    browser.fill('Address:', '02140')
    btn = browser.find_by_name('Find elevation')
    btn.click()
        
if __name__ == '__main__':
    #get_elevation()
    test()
    