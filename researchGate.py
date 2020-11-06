from selenium import webdriver
from selenium.webdriver import Chrome #https://www.selenium.dev/documentation/en/webdriver/driver_requirements/ && https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait #https://www.selenium.dev/documentation/en/webdriver/waits/
from selenium.webdriver.common.by import By #https://www.selenium.dev/documentation/en/webdriver/web_element/
import os


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
	print("hola")


	#Ignorar los certificados:
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('ignore-certificate-errors')
	chrome_options.add_argument('--ignore-ssl-errors')
	articlesData = []

	#Heroku paths
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--headless")

	#Chrome drivers
	chrome_path = os.path.abspath("../../usr/lib/chromium-browser/chromedriver")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

	driver.get('https://www.researchgate.net/search/publication?q="{}"'.format(search_param))
	print("entro a la pagina")
	totalPages = None
	currentPage = 1

	# Declaración de arreglo de datos a devolver
	articlesData = []
	
	try:
		# XPath de las páginas
		classpath = 'nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-s nova-c-button--color-grey nova-c-button--theme-bare nova-c-button--width-full'
		print("enc")
		pagesButtons = WebDriverWait(driver, timeout = 900).until(lambda d : d.find_elements_by_class_name(classpath))

		totalPages = int(pagesButtons[-2].text)
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
