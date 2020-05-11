import sys
import random
import signal
import logging
import requests
import pandas as pd
from utils import *
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOG = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(asctime)s ⁠— %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

class Scraper:
    def __init__(self, driver, user, pw):
        self.browser = webdriver.Chrome(driver)
        self.contacts = self.get_namelist()
        self.login(user, pw)

    def login(self, user, pw):
        self.browser.get('https://www.linkedin.com/login')
        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(user)
        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(pw)
        elementID.submit()

    def get_namelist(self):
        namelist = []
        df = pd.read_excel('./hubspot.xlsx')
        for i in df.Recipient:
            namelist.append(i.split('@')[0]+' '+i.split('@')[1].split('.')[0])
        return namelist

    def run(self):
        self.scrape()
        self.browser.quit()
        with open('info.txt', 'w+', encoding="utf-8") as f:
            for item in self.henkilo_info:
                f.write("%s\n" % item)
        with open('job.txt', 'w+', encoding="utf-8") as f:
            for item in self.henkilo_job:
                f.write("%s\n" % item)

    def scrape(self):
        self.henkilo_info = []
        self.henkilo_job = []
        for i in self.contacts:
            LOG.info(f'Scraping {i}')
            soup = search_contact_by_name(self.browser, i)
            if soup:
                name_loc = soup.find('div',{'class','flex-1 mr5'}).find_all('ul')
                name = name_loc[0].find('li').get_text()
                loc = name_loc[1].find('li').get_text().strip()
                profile_title = soup.find('div',{'class','flex-1 mr5'}).find('h2').get_text().strip()
                info = format_values([name, loc, profile_title])
                self.henkilo_info.append(info)

                if soup.find('section', {'id':'experience-section'}):
                    LOG.info(f'Found experience-section {i}')
                    exp_section = soup.find('section',{'id':'experience-section'}).find('ul')
                    job_title = exp_section.find('div').find('a').find('h3').get_text().strip()
                    work_period = exp_section.find('div').find('a').findAll('h4')[0].find_all('span')[1].get_text().strip()
                    if exp_section.find('div').find('a').findAll('p')!= []:
                        company_name = exp_section.find('div').find('a').findAll('p')[1].get_text().strip()
                    else:
                        company_name = 'None'
                    if len(exp_section.find('div').find('a').findAll('h4'))>1:
                        experience = exp_section.find('div').find('a').findAll('h4')[1].find_all('span')[1].get_text().strip()
                    else:
                        experience = 'None'
                    job = format_values([name, job_title, company_name, work_period, experience])
                    self.henkilo_job.append(job)
                # else:
                #     LOG.error(f'no exp for {i}')
                #     sys.exit()

            print(f'{self.henkilo_info}\n{self.henkilo_job}\n------------------')


def main():

    # Config
    driver = 'C:\\Users\\sami_\\Work\\bin\\chromedriver.exe'
    username = 'sami_rouhe@hotmail.com'
    password = 'Ankkalinna1'

    # Scraper
    s = Scraper(driver, username, password)
    s.run()

if __name__ == '__main__':
    main()
