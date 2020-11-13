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
    # url= "file:///C:/Users/luisl/Desktop/alexandro%20escudero%20nahon%20-%20Search%20Results%20_%20Microsoft%20Academic.html"
    driver.get(url)
    print("entro a la pagina")
    title = driver.title
    print(title)
    time.sleep(3)
    search = driver.find_element_by_class_name("disambiguations")
    print(search)
    search = driver.find_element_by_class_name("header")
    print(search)
    search = driver.find_element_by_class_name("name")
    print(search)
    search.click()
    print("success")

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    time.sleep(1)
    name = driver.find_element_by_class_name("caption").text
    print(name)



    return title