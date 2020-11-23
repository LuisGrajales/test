import os
from selenium import webdriver
from selenium.webdriver import Chrome 
import time


def findMicrosoft (search_param):
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
    time.sleep(2)
    try:
        driver.find_element_by_class_name("not-found")
        return "Sin resultados"
    except:
        pass
    search = driver.find_element_by_class_name("author-card")
    search = search.find_element_by_class_name("header")
    search = search.find_element_by_xpath("//div[@class='name']/a").get_attribute('href')
    driver.get(search)
    time.sleep(2)

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
                "collaborators" : authors
            }

            # Agregamos el artículo a la lista
            articlesData.append(data)
        try:
            button = driver.find_element_by_xpath("//i[@class='icon-up right au-target']")
            button.click()
            time.sleep(1)

        except:
            return articlesData
