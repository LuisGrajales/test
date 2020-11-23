import os
from selenium import webdriver
from selenium.webdriver import Chrome #https://www.selenium.dev/documentation/en/webdriver/driver_requirements/ && https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait #https://www.selenium.dev/documentation/en/webdriver/waits/
from selenium.webdriver.common.by import By #https://www.selenium.dev/documentation/en/webdriver/web_element/
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def findMicrosoft (search_param):
    print('probando')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")

    articlesData = []

	# Instanciando el webdriver de Chrome (Chromium)
    chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

	# Navegar hacia el URL deseado con el nombre a buscar ya dentro del URI
    url = 'https://academic.microsoft.com/search?q="{}"'.format(search_param)
    driver.get(url)
    print("entro a la pagina")
    try:
        driver.find_element_by_class_name("right")
    except:
        return "Sin resultados"
    
    #busca el primer nombre de la lista y hace click en su perfil
    time.sleep(3)
    search = driver.find_element_by_class_name("author-card")
    search = search.find_element_by_class_name("header")
    search = search.find_element_by_xpath("//div[@class='name']/a").get_attribute('href')
    print(search)
    driver.get(search)
    time.sleep(3)
    print("entro al perfil")


    while True:
        #dentro del perfil consigue la informacion
        # main = driver.find_element_by_class_name("main")
        # results = main.find_element_by_class_name("results")
        # results = results.find_element_by_class_name("ma-paper-results")
        # results = results.find_element_by_class_name("results")

        # articles = results.find_elements_by_xpath("//div[@class='ma-card']")
        articles = driver.find_elements_by_class_name("primary_paper")

        for article in articles:
            title = article.find_element_by_class_name("au-target").text
            date =  article.find_element_by_class_name("year").get_attribute('textContent')
            authors_div = article.find_elements_by_class_name("author")
            authors = []
            for author in authors_div:
                authors.append(author.get_attribute('innerText'))

            data = {
                "title" : title,
                "date" : date,
                # "DOI" : DOI,
                # "ISBN" : ISBN,
                "collaborators" : authors
            }

            # Agregamos el artículo a la lista
            articlesData.append(data)
            print("agrego los items a la lista")
        try:
            print("buscando sig pagina")
            button = driver.find_element_by_xpath("//i[@class='icon-up right au-target']")
            button.click()
            time.sleep(3)
            print("encontro sig pagina")
        except:
            return articlesData


def scrapeMicrosoft(search_param):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")

    chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    url = 'https://academic.microsoft.com/search?q="{}"'.format(search_param)
    driver.get(url)
    articlesData = []

    try:
        button = driver.find_element_by_class_name("right")
    except:
        return "Sin resultados"

    while True:

        articles = driver.find_elements_by_class_name("primary_paper")
        for article in articles:
            title = article.find_element_by_class_name("au-target").text
            date =  article.find_element_by_class_name("year").get_attribute('textContent')
            authors_div = article.find_elements_by_class_name("author")
            authors = []
            for author in authors_div:
                authors.append(author.get_attribute('innerText'))

            data = {
                "title" : title,
                "date" : date,
                # "DOI" : DOI,
                # "ISBN" : ISBN,
                "collaborators" : authors
            }

            # Agregamos el artículo a la lista
            articlesData.append(data)

        try:
            button = driver.find_element_by_class_name("right")
            button.click()  
        except:
            return articlesData

 