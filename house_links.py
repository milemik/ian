import requests
from bs4 import BeautifulSoup as bs
import random
# from get_proxies import ProxieGet
import json
import csv
from time import sleep
import re
import os
import pandas as pd
from selenium import webdriver
from threading import Thread
'''
    THIS IS NOT SOME HELLO WORLD FILE, ITS A SCRAPERRRRR!!!!!!!
'''


class HScraper:

    def __init__(self, area):
        with open("proxies.json", "r") as f:
            self.PROXIES = json.load(f)
        self.STATIC_PROXIE = ""
        #self.AREA = area
        #if len(str(self.AREA)) == 3:
        #    self.AREA = f"0{self.AREA}"
        #self.URL = f"http://house.ksou.cn/p.php?q={self.AREA}"
        self.HEADERS = {
            "User-Agent": "Mozila Firefox 1243.43435 NT Windows 10 13243"}
        self.PURL = "https://api.myip.com"
        self.DOMAIN = "http://house.ksou.cn/"
        self.LINKS = area
        self.bad_proxies = []
        self.TIMEOUT = 20
        # CREATE HEADER FOR CSV
        csvhead = ["Postcode", "Home Address", "Price Sold", "Last Sold", "Land Size", "Agent", "Distance", "Property Description", 
                    "Recent Sold: Address", "Recent Sold: date", "Recent Sold: price"
                  ]
        self.FILENAME = "house_links.txt"
        if self.FILENAME not in os.listdir():
            with open(self.FILENAME, "w") as fn:
                fwriter = csv.writer(fn)
                fwriter.writerow(["links"])
        #sleep(5)
        self.checked_urls = []
    '''
    def send_req(self, url):
        cookies = dict(cookies_are= "working")
        r = requests.get(url, proxies = self.STATIC_PROXIE, timeout = self.TIMEOUT, cookies = cookies, headers = self.HEADERS)
        print(r.status_code)
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
        else:
            sleep(30)
            r = requests.get(url)
            soup = bs(r.text, "html.parser")
        #sleep(3)
        return soup
        
    '''
    def send_req(self, url):
        prox = self.PROXIES[str(random.randint(0, len(self.PROXIES) - 1))]
        #prox = random.choice(self.PROXIES)
        while True:
            if prox in self.bad_proxies:
                prox = self.PROXIES[str(
                    random.randint(0, len(self.PROXIES) - 1))]
                #prox = random.choice(self.PROXIES)
            else:
                break
        proxie = {"https": f"https://{prox}", "http": f"http://{prox}"}
        print(proxie)
        error_count = 0
        while True:
            try:
                #print(proxie)
                r = requests.get(url, proxies=proxie, timeout = self.TIMEOUT)
                #print(r)
                if r.status_code == 200:
                    print("RESPONSE: OK")
                    break
                else:
                    error_count += 1
                    print("RESPONSE: BAD")
                    self.bad_proxies.append(prox)
                    prox = self.PROXIES[str(
                        random.randint(0, len(self.PROXIES) - 1))]
                    #prox = random.choice(self.PROXIES)
                    proxie = {"https": f"https://{prox}", "http": f"http://{prox}"}
            except requests.exceptions.RequestException:
                print(f"Bad proxie: {prox}")
                error_count += 1
                if error_count >= len(self.PROXIES):
                    print("All proxies are bad")
                    break
                self.bad_proxies.append(prox)
                prox = self.PROXIES[str(
                    random.randint(0, len(self.PROXIES) - 1))]
                #prox = random.choice(self.PROXIES)
                proxie = {"https": f"https://{prox}", "http": f"http://{prox}"}
        soup = bs(r.text, "html.parser")
        #sleep(3)
        return soup
    
    def get_links(self):
        print(self.URL)
        #self.browser.get(self.URL)
        soup = self.send_req(self.URL)
        all_links = soup.select("a")
        #all_links = self.browser.find_elemenets_by_tag_name("a")
        for x in all_links:
            if ", " in x.text:
                self.LINKS.append(x['href'])
                #self.LINKS.append(x.get_attribute("href"))
                print(x['href'])
                while True:
                    try:
                        with open("first_links.txt", "a") as f:
                            f.write(f"{x['href']}\n")
                        break
                    except OSError:
                        sleep(2)
                        pass
        #print(self.AREA)
        #print("Found %d" % len(self.LINKS))
        sleep(3)

    def write_house_links(self, hurl):
        with open("house_links.txt", "a") as f:
            f.write(f"{hurl}\n")

    def get_house_links(self):
        # Collect all the house links
        #for link in self.LINKS:
        new_link = self.DOMAIN + self.LINKS
        #new_link = self.DOMAIN + link
        soup = self.send_req(new_link)
        h_links = []
        hlinks = soup.select("span.addr")
        for hlink in hlinks:
            h_links.append(self.DOMAIN + hlink.select("a")[0]["href"])
        page_counter = 0
        while True:
            next_page = None
            alinks = soup.select("a", href=True)
            for a in alinks:
                if "Next >>" in a.text:
                    next_page = self.DOMAIN + a['href']
            # if you find next page, go to next page
            if next_page != None:
                page_counter += 1
                print(f"Going to the next_page: {page_counter}")
                soup = self.send_req(next_page)
                # get home links
                hlinks = soup.select("span.addr")
                for hlink in hlinks:
                    # add home links to the h_links list
                    while True:
                        try:
                            with open("links_houses.txt", "a") as f:
                                f.write(self.DOMAIN + hlink.select("a")[0]["href"] + "\n")
                            break
                        except OSError:
                            sleep(2)

                    #h_links.append(
                    #    self.DOMAIN + hlink.select("a")[0]["href"])

            else:
                break
        print(len(h_links))
        #for h_link in h_links:
        #    write_house_links(h_link)
        #for h_link in h_links:
        #    self.hous_info(h_link)

    def hous_info(self, url):
        #checked_urls = self.check_link()
        
        if url not in self.checked_urls:
            print(url)
            soup = self.send_req(url)
            addr_error = 0
            while True:
                try:
                    address = soup.select("span.addr")[0].text
                    break
                except IndexError:
                    print("ERROR IN %s" % url)
                    soup = self.send_req(url)
                    addr_error += 1
                    if addr_error > 3:
                        break
                        address == None
            agent = sold = last_sold = land_size = distance = pp_des = None
            recend_sold = []
            # print(address)
            td = soup.select("td")
            tr = soup.select("tr")
            for t in range(len(td)):
                if "Sold $" in td[t].text and sold == None and "}" not in td[t].text:
                    sold = td[t].text.split("Sold")[1].split()[0]
                if "Last Sold" in td[t].text and last_sold == None and "}" not in td[t].text:
                    last_sold = td[t].text.split("Last Sold")[1].split()[0]
                #if "Land size:" in td[t].text and land_size == None and "}" not in td[t].text:
                if "Land size:" in td[t].text and "}" not in td[t].text:
                    #print(td[t].text)
                    land_sze = re.findall("\d+ sqm|\d+,\d+ sqm", td[t].text)
                    if len(land_sze) > 0:
                        land_size = land_sze[0]
                if "Agent:" in td[t].text and agent == None and "}" not in td[t].text:
                    agent = td[t].text.split("Agent:")[1].split("Distance:")[0]
                if "Distance:" in td[t].text and distance == None and "{" not in td[t].text:
                    distance = td[t].text.split("Distance:")[1].replace(";", " ")
                if "Property Description:" == td[t].text and pp_des == None and "{" not in td[t].text:
                    pp_des = td[t + 1].text.encode("utf8")
            for t in range(len(tr)):
                if "AddressDatePrice" in tr[t].text:
                    for n in range(10):
                        if "Date" in tr[t + n].text or ">>" in tr[t + n].text or "}" in tr[t + n].text:
                            pass
                        if "More records" in tr[t + n].text:
                            break
                        else:
                            rs = tr[t + n].select("td")
                            radr = rs[0].text
                            rdate_sold = rs[1].text
                            rprice = rs[2].text
                            if "Address" not in radr and [radr, rdate_sold, rprice] not in recend_sold:
                                recend_sold.append([radr, rdate_sold, rprice])

            rs_for_csv = []
            if len(recend_sold) > 0:
                for rs_csv in recend_sold:
                    for fs_c in rs_csv:
                        rs_for_csv.append(fs_c)
            
            info = [self.AREA, address, sold, last_sold, land_size, agent, distance, pp_des] + rs_for_csv #recend_sold
            self.write_to_csv(info)
            self.enter_checked(url)
        else:
            print(f"{url} CHECKED!!!!!!!!!!!!!")

    def write_to_csv(self, iinfo):
        with open(self.FILENAME, "a") as f:
            fwriter = csv.writer(f)
            fwriter.writerow(iinfo)


def run(p):
    s = HScraper(p)
    # s.check_proxie()
    #s.get_links()
    s.get_house_links()
    print(s.LINKS)
    print("Found %d" % len(s.LINKS))

#'''
df = pd.read_csv("first_links.txt")
pcodes = df['links'].values.tolist()
for p in pcodes:
    t = Thread(target = run, args=(p,))
    t.start()
    '''
    s = HScraper(p)
    # s.check_proxie()
    s.get_links()
    print(s.AREA)
    print("Found %d" % len(s.LINKS))
    #s.get_house_links()
    '''
