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

	# #display
	# display = Display(visible=False, size=(1920, 1080))  
	# display.start()

	# Ignorar los certificados:

	# chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
	# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	# chrome_options.add_experimental_option('useAutomationExtension', False)
	# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--window-size=1920,1080')
	# chrome_options.add_argument("--remote-debugging-port=5000")
	# chrome_options.add_argument("start-maximized")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")


	

	# Instanciando el webdriver de Chrome (Chromium)
    chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)


	# Navegar hacia el URL deseado con el nombre a buscar ya dentro del URI
    url = 'https://academic.microsoft.com/search?q="{}"'.format(search_param)
    driver.get(url)
    print("entro a la pagina")
    
    #busca el primer nombre de la lista y hace click en su perfil
    time.sleep(3)
    search = driver.find_element_by_class_name("disambiguations")
    search = driver.find_element_by_class_name("ma-card")
    search = driver.find_element_by_class_name("header")
    search = driver.find_element_by_class_name("name")
    search.click()
    print("success")


    # entra al perfil y empieza a buscar los datos a extraer
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    time.sleep(1)
    return driver.page_source
    # main = driver.find_element_by_class_name("main")
    # titlePage = main.find_element_by_xpath("//h1[@class='title au-target']")
    # print(titlePage.text)
    # results = main.find_element_by_class_name("results")
    # results = results.find_element_by_class_name("ma-paper-results")

    # articles = results.find_elements_by_xpath("//ma-card[@class='au-target']")
    # for article in articles:
    #     paper = article.find_element_by_class_name("primary_paper")
    #     paperTitle = paper.find_element_by_xpath("//a[@class='title au-target']")
    #     test = paperTitle.get_attribute("data-appinsights-title")
    #     print(str(test))

 