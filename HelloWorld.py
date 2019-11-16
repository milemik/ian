import requests
from bs4 import BeautifulSoup as bs
import random
# from get_proxies import ProxieGet
import json
import csv

'''
    THIS IS NOT SOME HELLO WORLD FILE, ITS A SCRAPERRRRR!!!!!!!
'''


class Scraper:

    def __init__(self):
        with open("proxies.json", "r") as f:
            self.PROXIES = json.load(f)
        AREA = "nt"
        self.URL = f"http://house.ksou.cn/p.php?q={AREA}"
        self.PROXIE = {"https": "https://195.46.20.146:21231",
                       "http": "http://195.46.20.146:21231"}
        self.HEADERS = {
            "User-Agent": "Mozila Firefox 1243.43435 NT Windows 10 13243"}
        self.PURL = "https://api.myip.com"
        self.DOMAIN = "http://house.ksou.cn/"
        self.LINKS = []
        self.bad_proxies = []

    def check_proxie(self):
        proxie_link = self.PROXIES[str(
            random.randint(0, len(self.PROXIES) - 1))]
        proxie = {{"https": f"https://{proxie_link}",
                   "http": "http://{proxie_link}"}}
        r = requests.get(self.PURL, proxies=self.PROXIE, headers=self.HEADERS)
        print(r.text)

    def send_req(self, url):
        prox = self.PROXIES[str(random.randint(0, len(self.PROXIES) - 1))]
        while True:
            if prox in self.bad_proxies:
                prox = self.PROXIES[str(
                    random.randint(0, len(self.PROXIES) - 1))]
            else:
                break
        proxie = {"https": f"https://{prox}", "http": f"http://{prox}"}
        print(proxie)
        while True:
            try:
                r = requests.get(url, proxies=proxie, headers=self.HEADERS)
                print(r)
                break
            except:
                print(f"Bad proxie: {prox}")
                self.bad_proxies.append(prox)
                prox = self.PROXIES[str(
                    random.randint(0, len(self.PROXIES) - 1))]
                proxie = {"https": f"https://{prox}", "http": f"http://{prox}"}
        soup = bs(r.text, "html.parser")
        return soup

    def get_links(self):
        soup = self.send_req(self.URL)

        all_links = soup.select("a", href=True)
        for x in all_links:
            if x['href'].endswith(".php") or "auction_result." in x['href']:
                pass
            else:
                self.LINKS.append(x['href'])
        print("Found %d" % len(self.LINKS))

    def get_house_links(self):
        for link in self.LINKS:
            new_link = self.DOMAIN + link
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
                    next_page += 1
                    print(f"Going to the next_page: {page_counter}")
                    soup = self.send_req(next_page)
                    # get home links
                    hlinks = soup.select("span.addr")
                    for hlink in hlinks:
                        # add home links to the h_links list
                        h_links.append(
                            self.DOMAIN + hlink.select("a")[0]["href"])
                else:
                    break
            print(len(h_links))
            for h_link in h_links:
                self.hous_info(h_link)

    def hous_info(self, url):
        print(url)
        soup = self.send_req(url)
        try:
            address = soup.select("span.addr")[0].text
        except IndexError:
            print("ERROR IN %s" % url)
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
            if "Land size:" in td[t].text and land_size == None:
                land_size = td[t].text.split(":")[1]
            if "Agent:" in td[t].text and agent == None and "}" not in td[t].text:
                agent = td[t].text.split("Agent:")[1]
            if "Distance:" in td[t].text and distance == None and "{" not in td[t].text:
                distance = td[t].text.split("Distance:")[1]
            if "Property Description:" in td[t].text and pp_des == None and "{" not in td[t].text:
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

        print("Address: %s" % address)
        print("Sold: %s" % sold)
        print("Last Sold: %s" % last_sold)
        print("Land Size: %s" % land_size)
        print("Agent: %s" % agent)
        print("Distance: %s" % distance)
        print("Property Description: %s" % pp_des)
        print("Recent Sold: %s" % recend_sold)
        
        info = [address, sold, last_sold, land_size, agent, distance, pp_des]
        for r in recend_sold:
            for i in r:
                info.append(i)
        self.write_to_csv(info)

    def write_to_csv(self, iinfo):
        with open("DATA.csv", "a") as f:
            fwriter = csv.writer(f)
            fwriter.writerow(iinfo)

s = Scraper()
# s.check_proxie()
s.get_links()
s.get_house_links()
