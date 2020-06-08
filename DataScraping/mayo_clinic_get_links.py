from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import scrapy
from scrapy.http import Request
import pickle
import csv

url = "https://connect.mayoclinic.org/groups"

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)


groups = driver.find_elements_by_class_name('header')
links = []


for each in groups:
    link = each.find_element_by_tag_name('a').get_attribute('href')
    links.append(link)

thread_list = []
for link in links[1:]:


    driver.get(link)

    threads = driver.find_elements_by_class_name('ch-post-title')

    for thread in threads:
        thread_link = thread.find_element_by_tag_name('a').get_attribute('href')
        thread_list.append(thread_link)

    while True:
        try:
            view_more = driver.find_elements_by_class_name('more')
            driver.get(view_more[0].get_attribute('href'))

            threads = driver.find_elements_by_class_name('ch-post-title')

            for thread in threads:
                thread_link = thread.find_element_by_tag_name('a').get_attribute('href')
                if thread_link.find('webinar') != -1:
                    continue
                thread_list.append(thread_link)
        except Exception as e:
            break
pickle.dump(thread_list, open("threads.p","wb"))
