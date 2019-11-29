from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
import os
import json
from datetime import datetime
from time import sleep

class ProxieGet:
	def __init__(self):
		self.PAGES = 5
		td = datetime.now()
		self.today = f"{td.year}-{td.month}-{td.day}"
		self.URL = "https://free-proxy-list.net/"
		options = Options()
		options.add_argument("--headless")
		print("Opening driver")
		#self.driver = webdriver.Chrome(executable_path = os.path.join("chromedriver", "chromedriver"), options = options)
		self.proxies = []
		self.driver = webdriver.Chrome(executable_path = os.path.join("chromedriver", "chromedriver"))

	def req(self):
		break_stat = False
		test_num = 0
		self.driver.get(self.URL)
		while test_num <= self.PAGES:
			#print(r.text)
			tro = self.driver.find_elements_by_class_name("odd")
			tre = self.driver.find_elements_by_class_name("even")
			tr = tro + tre
			print(len(tr))
			for p in tr:
				try:
					proxie_id, proxie_port, *args = p.find_elements_by_tag_name("td")
					if f"{proxie_id.text}:{proxie_port.text}" in self.proxies:
						break_stat = True
						break
					self.proxies.append(f"{proxie_id.text}:{proxie_port.text}")
				except ValueError:
					pass
			#next_but = self.driver.find_element_by_id("proxylisttable_next")

			next_but = self.driver.find_element_by_class_name("fg-button.ui-button.ui-state-default.next")
			self.driver.execute_script("window.scrollTo(0, 1200);")
			#sleep(10)
			try:
				next_but.click()
			except ElementClickInterceptedException:
				#sleep(2)
				self.driver.execute_script("window.scrollTo(0, 1400);")
				next_but = self.driver.find_elements_by_xpath("/html/body/section[1]/div/div[2]/div/div[3]/div[2]/div/ul/li[*]/a")[-2]
				next_but.click()
			if break_stat == True:
				break
			#sleep(3)

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

