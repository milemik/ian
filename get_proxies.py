from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
from datetime import datetime

class ProxieGet:
	def __init__(self):
		td = datetime.now()
		self.today = f"{td.year}-{td.month}-{td.day}"
		self.URL = "https://free-proxy-list.net/"
		options = Options()
		options.add_argument("--headless")
		print("Opening driver")
		self.driver = webdriver.Chrome(executable_path = os.path.join("chromedriver", "chromedriver"), options = options)
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

	def create_json(self):
		numerate = 0
		data = {}
		#print(self.proxies)
		for p in self.proxies:
			data[numerate] = p
			numerate += 1
		print(data)
		print("Creating json file")
		with open(f"proxies.json", "w") as f:
			f.write(json.dumps(data, indent=2))


	def close_driver(self):
		self.driver.close()
		print("driver closed")

	def run(self):
		self.req()
		self.close_driver()
		self.create_json()
		print("FINISHEd")

pg = ProxieGet()
pg.run()
#print(pg.proxies)

