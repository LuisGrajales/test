# working code
# from selenium import webdriver
# from selenium.webdriver import Chrome #https://www.selenium.dev/documentation/en/webdriver/driver_requirements/ && https://sites.google.com/a/chromium.org/chromedriver/downloads
# from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait #https://www.selenium.dev/documentation/en/webdriver/waits/
# from selenium.webdriver.common.by import By #https://www.selenium.dev/documentation/en/webdriver/web_element/
# import os
#working code good 
import os, sys
import warnings
import time,requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def findOnePage(search_param):


	# Ignorar los certificados:
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	chrome_options.add_argument('--ignore-ssl-errors')
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--headless")

	# Instanciando el webdriver de Chrome (Chromium)
	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")	
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
	
	# Navegar hacia el URL deseado con el nombre a buscar ya dentro del URI
	driver.get('https://www.researchgate.net/search/publication?q="{}"'.format(search_param))

	# XPath de las tarjetas de artículos
	containerxpath = '//div[@class="nova-o-stack__item"]'
	# Encontrar todas las tarjetas de artículos dentro de la página usanndo XPath
	articles = WebDriverWait(driver, timeout = 10).until(lambda d : d.find_elements_by_xpath(containerxpath))

	# Declaración de arreglo de datos a devolver
	articlesData = []

	# Ciclando cada uno de los articulos de la variable 'articles'
	for article in articles:
		# Existen por la estructura de la página dos textos con la misma clase, por eso se buscan varios elementos como possibleTitles.
		header = article.find_elements_by_xpath('.//div[@class="nova-e-text nova-e-text--size-l nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit nova-v-publication-item__title"]')
		# List Items que contienen los metadatos: Fecha, DOI, ISBN
		metadata = article.find_elements_by_xpath('.//li[@class="nova-e-list__item nova-v-publication-item__meta-data-item"]')
		# Spans que contienen los nombres de cada uno de los colaboradores
		collaborators = article.find_elements_by_xpath('.//span[@class="nova-v-person-inline-item__fullname"]')
		
		# Procesamiento de los webelements
		# Declaración de arreglo de todos los colaboradores
		collaboratorsTextArray = []
		for collaborator in collaborators:
			collaboratorsTextArray.append(collaborator.text)

		# Manejo de escenarios, no todos los articulos tienen DOI, ISBN o ambos.
		try:
			date = metadata[0].text
			if 1 < len(metadata):
				DOI = metadata[1].text[5:] if "DOI" in metadata[1].text else "No disponible"
				ISBN = metadata[1].text[6:] if "ISBN" in metadata[1].text else ""
			if 2 < len(metadata):
				ISBN = metadata[2].text[6:] if "ISBN" in metadata[2].text else "No disponible"

			# Objeto de artículo terminado
			data = {
					"title" : header[0].text,
					"date" : date,
					"DOI" : DOI,
					"ISBN" : ISBN,
					"collaborators" : collaboratorsTextArray
			}

			# Agregamos el artículo a la lista
			articlesData.append(data)
		except:
			pass

	# Terminar el proceso del navegador
	driver.quit()
	# print(articlesData)

	# Retornamos el arreglo de objetos artículo.
	return articlesData


def findResearchGate(search_param):
	print("probando")

	#Ignorar los certificados:
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	chrome_options.add_argument('--ignore-ssl-errors')
	articlesData = []

	#Heroku paths
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	# chrome_options.add_argument("--headless")

	#Chrome drivers
	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

	#windows size
	driver.set_window_size(1280,720)

	driver.get('https://www.researchgate.net/search/publication?q="{}"'.format(search_param))
	print("entro a la pagina")
	totalPages = None
	currentPage = 1

	# Declaración de arreglo de datos a devolver
	articlesData = []
	
	try:
		# XPath de las páginas
		classpath = "nova-o-stack__item pager-container"
		print("enc")
		pagesButtons = WebDriverWait(driver, timeout = 30).until(lambda d : d.find_elements_by_class_name(classpath))
		listbuttons = pagesButtons.find_elements_by_class_name("nova-c-button-group__item")
		totalPages = int(listbuttons[-2].text)
		print("encontre el numero de la pagina")

	except:
		return [{ "error" : "timeout" }]

	while currentPage <= totalPages:

		# XPath de las tarjetas de artículos
		containerclasspath = "nova-o-stack__item"
		# Encontrar todas las tarjetas de artículos dentro de la página usanndo XPath
		articles = WebDriverWait(driver, timeout = 120).until(lambda d : d.find_elements_by_class_name(containerclasspath))
		print("encontre los articulos")

		# Ciclando cada uno de los articulos de la variable 'articles'
		for article in articles:

			# Existen por la estructura de la página dos textos con la misma clase, por eso se buscan varios elementos como possibleTitles.
			header = article.find_elements_by_class_name("nova-e-text nova-e-text--size-l nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit nova-v-publication-item__title")
			# List Items que contienen los metadatos: Fecha, DOI, ISBN
			metadata = article.find_elements_by_class_name("nova-e-list__item nova-v-publication-item__meta-data-item")
			# Spans que contienen los nombres de cada uno de los colaboradores
			collaborators = article.find_elements_by_class_name("nova-v-person-inline-item__fullname")
			
			# Procesamiento de los webelements
			# Declaración de arreglo de todos los colaboradores
			collaboratorsTextArray = []
			for collaborator in collaborators:
				collaboratorsTextArray.append(collaborator.text)

			# Manejo de escenarios, no todos los articulos tienen DOI, ISBN o ambos.
			try:
				date = metadata[0].text
				if 1 < len(metadata):
					DOI = metadata[1].text[5:] if "DOI" in metadata[1].text else "No disponible"
					ISBN = metadata[1].text[6:] if "ISBN" in metadata[1].text else ""
				if 2 < len(metadata):
					ISBN = metadata[2].text[6:] if "ISBN" in metadata[2].text else "No disponible"

				# Objeto de artículo terminado
				data = {
						"title" : header[0].text,
						"date" : date,
						"DOI" : DOI,
						"ISBN" : ISBN,
						"collaborators" : collaboratorsTextArray
				}

				# Agregamos el artículo a la lista
				print(data)
				articlesData.append(data)
			except:
				pass

		pagesclasspath = "nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-s nova-c-button--color-grey nova-c-button--theme-bare nova-c-button--width-full"
		pagesButtons = WebDriverWait(driver, timeout = 120).until(lambda d : d.find_elements_by_class_name(pagesclasspath))

		nextPageButton = pagesButtons[-1]
		nextPageButton.click()

		currentPage += 1

	# Terminar el proceso del navegador
	driver.quit()
	# print(articlesData)

	# Retornamos el arreglo de objetos artículo.
	return articlesData

def findOnePageByClass(search_param):


	# Ignorar los certificados:
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	chrome_options.add_argument('--ignore-ssl-errors')
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--headless")

	# Instanciando el webdriver de Chrome (Chromium)
	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

	# Navegar hacia el URL deseado con el nombre a buscar ya dentro del URI
	driver.get('https://www.researchgate.net/search/publication?q="{}"'.format(search_param))

	# Class de las tarjetas de artículos
	containerclass = 'nova-o-stack__item'
	# Encontrar todas las tarjetas de artículos dentro de la página usanndo XPath
	articles = WebDriverWait(driver, timeout = 30).until(lambda d : d.find_elements_by_class_name(containerclass))
	print(len(articles))

	if (len(articles) == 7):
		return "Sin resultados"
	else:
		pagesclass = 'nova-c-button-group__item'
		pages = WebDriverWait(driver, timeout = 30).until(lambda d : d.find_elements_by_class_name(pagesclass))
		totalPages = pages[-2].text

		for x in range(1,int(totalPages)):
			articles = WebDriverWait(driver, timeout = 30).until(lambda d : d.find_elements_by_class_name(containerclass))
			pages = WebDriverWait(driver, timeout = 30).until(lambda d : d.find_elements_by_class_name(pagesclass))
			for article in articles:
				if (article.text == "About us"):
					break

				data = article.text.split('\n')
				print(data)

			pages[-1].click()

	# Terminar el proceso del navegador
	driver.quit()
	# print(articlesData)

	# Retornamos el arreglo de objetos artículo.
	return "Done"

def onlyHTML (search_param):
	print('probando')

	# #display
	# display = Display(visible=False, size=(1920, 1080))  
	# display.start()

	# Ignorar los certificados:
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	# chrome_options.add_argument("start-maximized")
	chrome_options.add_argument('--ignore-ssl-errors')
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	# chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument("--disable-dev-shm-usage")
	# chrome_options.add_argument("--remote-debugging-port=5000")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
	# chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")
	# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	# chrome_options.add_experimental_option('useAutomationExtension', False)
	# chrome_options.add_argument('--disable-blink-features=AutomationControlled')

	

	# Instanciando el webdriver de Chrome (Chromium)
	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
	# driver.add_cookie({"name":"sid","value":"dLbaTtOwpmMW7oF5mW2aP4B5PnjyXcSVJhHNFWynYHz1oZoNPdIy14cLu5GVJ6BiipMWBdU5xEsCzqM5zS10kXB3J09o6Gp4hAk0JjQKCciac2dmfOTYwpH9F1BKFDjy"})

	# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
	# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})


	# Navegar hacia el URL deseado con el nombre a buscar ya dentro del URI
	driver.get("https://academic.microsoft.com/author/2241863331/publication/search?q=Alexandro%20Escudero%20Nah%C3%B3n&qe=Composite(AA.AuId%3D2241863331)&f=&orderBy=0&skip=10&take=10")

	site = driver.page_source
	return site

def byPass (search_param):
	warnings.filterwarnings("ignore", category=DeprecationWarning) 
	delayTime = 2
	audioToTextDelay = 10
	filename = 'captcha_audio.mp3'
	byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
	googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
	
	PROXY = "20.186.110.157:3128"
	option = webdriver.ChromeOptions()
	option.add_argument("--no-sandbox")
	option.add_argument('lang=en')
	option.add_argument("--disable-gpu")
	option.add_argument("--headless")
	option.add_argument("--mute-audio")
	option.add_experimental_option("excludeSwitches", ["enable-logging"])
	option.add_argument('--proxy-server=%s' % PROXY)
	# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
	option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")

	def audioToText(mp3Path):

		driver.execute_script('''window.open("","_blank");''')
		driver.switch_to.window(driver.window_handles[1])

		driver.get(googleIBMLink)

		# Upload file

		time.sleep(1)
		driver.execute_script("window.scrollTo(0, 1000);")
		root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
		btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
		btn.send_keys(mp3Path)

		# Audio to text is processing

		time.sleep(audioToTextDelay)
		
		driver.execute_script("window.scrollTo(0, 1000);")
		text = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[6]/div/div/div/span')
		result = " ".join( [ each.text for each in text ] )

		driver.close()
		driver.switch_to.window(driver.window_handles[0])

		return result

	def saveFile(content,filename):
		with open(filename, "wb") as handle:
			for data in content.iter_content():
				handle.write(data)

	

	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")

	driver = webdriver.Chrome(chrome_path ,chrome_options=option)
	driver.get(byPassUrl)

	googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
	outeriframe = googleClass.find_element_by_tag_name('iframe')
	outeriframe.click()

	print("\n[>] Try Bypass reCAPTCHA...")

	allIframesLen = driver.find_elements_by_tag_name('iframe')
	audioBtnFound = False
	audioBtnIndex = -1

	for index in range(len(allIframesLen)):
		driver.switch_to.default_content()
		iframe = driver.find_elements_by_tag_name('iframe')[index]
		driver.switch_to.frame(iframe)
		driver.implicitly_wait(delayTime)
		try:
			audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
			audioBtn.click()
			audioBtnFound = True
			audioBtnIndex = index
			break
		except Exception as e:
			pass

	if audioBtnFound:
		try:
			while True:
				href = driver.find_element_by_id('audio-source').get_attribute('src')
				response = requests.get(href, stream=True)
				saveFile(response,filename)
				response = audioToText(os.getcwd() + '/' + filename)

				driver.switch_to_default_content()
				iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
				driver.switch_to.frame(iframe)

				inputbtn = driver.find_element_by_id('audio-response')
				inputbtn.send_keys(response)
				inputbtn.send_keys(Keys.ENTER)

				time.sleep(2)
				errorMsg = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]

				if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
					print("\n[>] Success")
					break
				
		except Exception as e:
			print(e)
			print('\n[>] Caught. Try to change proxy now.')
	else:
		print('\n[>] Button not found. This should not happen.')


#########################################################
            # MAIN EXECUTION - TESTING #
#########################################################

# Input provisional para el objeto de la búsqueda.
# search_param = input()

# Busqueda desde el código
# search_param = "escudero-nahón"
# search_param = "Sandra Luz Canchola-Magdaleno"
# search_param = "José Alejandro Vargas-Díaz"

# print(findResearchGate(search_param))
# input()
