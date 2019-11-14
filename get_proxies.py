from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class ProxieGet:
	def __init__(self):
		self.URL = "https://free-proxy-list.net/"
		options = Options()
		options.add_argument("--headless")
		print("Opening driver")
		self.driver = webdriver.Chrome(executable_path = os.path.join("chromedriver", "chromedriver.exe"), options = options)
		self.proxies = []

	def req(self):
		self.driver.get(self.URL)
		#print(r.text)
		tro = self.driver.find_elements_by_class_name("odd")
		tre = self.driver.find_elements_by_class_name("even")
		tr = tro + tre
		print(len(tr))
		for p in tr:
			try:
				proxie_id, proxie_port, *args = p.find_elements_by_tag_name("td")
				self.proxies.append(f"{proxie_id.text}:{proxie_port.text}")
			except ValueError:
				pass

	def close_driver(self):
		self.driver.close()
		print("driver closed")

	def run(self):
		self.req()
		self.close_driver()

'''
pg = ProxieGet()
pg.run()
print(pg.proxies)
'''
