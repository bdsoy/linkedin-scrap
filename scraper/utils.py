import logging
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

LOG = logging.getLogger(__name__)
SLEEP = 3

def search_contact_by_name(browser, name):
    sleep(SLEEP)
    browser.find_element_by_class_name('search-global-typeahead__input').clear()
    elementID = browser.find_element_by_class_name('search-global-typeahead__input')
    elementID.send_keys(name)
    elementID.send_keys(Keys.ENTER)
    sleep(SLEEP)

    try:
        browser.find_element_by_class_name('name').click()
        sleep(SLEEP)

        """
       SCROLL_PAUSE_TIME = 5
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        for i in range(3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            import time
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        """

        # Here is the problematic part! This is prety unelegant but works for now.
        # Have to scroll down until the whole profile page is surely loaded
        for x in range(10):
            elementID.send_keys(Keys.PAGE_DOWN)
            sleep(0.5)


        src = browser.page_source
        soup = BeautifulSoup(src, 'html5lib')
        return soup

    except Exception as e:
        LOG.warn(e)
        try:
            sleep(SLEEP)
            browser.find_element_by_class_name('search-global-typeahead__input').clear()
            elementID = browser.find_element_by_class_name('search-global-typeahead__input')
            elementID.send_keys(name.split(' ')[0])
            elementID.send_keys(Keys.ENTER)
            sleep(SLEEP)
            browser.find_element_by_class_name('name').click()
            sleep(SLEEP)
            src = browser.page_source
            soup = BeautifulSoup(src, 'lxml')
            return soup

        except:
            LOG.info('this pp {} not in linkedin'.format(name.split(' ')[0]))
            return None

def format_values(vals: list):
    ret = []
    for v in vals:
        v = v.replace('\n', '').strip()
        ret.append(v)
    return ret
