import requests
from bs4 import BeautifulSoup as bs
import random
# from get_proxies import ProxieGet
import json
import csv

'''
   Suburb Profiles ARE HERE 
    THIS IS NOT SOME HELLO WORLD FILE, ITS A SCRAPERRRRR!!!!!!!
'''


class Scraper:

    def __init__(self):
        with open("proxies.json", "r") as f:
            self.PROXIES = json.load(f)
        AREA = "nt"
        self.URL = f"http://house.speakingsame.com/profile.php?q={AREA}"
        self.PROXIE = {"https": "https://195.46.20.146:21231",
                       "http": "http://195.46.20.146:21231"}
        self.HEADERS = {
            "User-Agent": "Mozila Firefox 60.1 NT Windows 10 "}
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

    def hous_info(self, url):
        print(url)
        soup = self.send_req(url)

        address = house_price = municipality = num_of_houses_units = last_year = last_year_precent = last_year_high = days_on_market =  None
        recend_sold = []
        #Create a list of house values and house price and house rent will be there
        #house_price, house_rent= house_list
        house_list = []
        # units_price, units_rent = units
        units = []
        #land_price, land_rent = lands
        lands = []
        agents = []
        features = []
        schools = []

        td = soup.select("td")
        tr = soup.select("tr")
        # FIND ADDRESS
        for numt in range(len(td)):
            try:
                bname = td[numt].select("b")[0]
                if ", " in bname:
                    address = bname
            except:
                pass
        features_num = 1

        if address != None:
            forms = soup.select("form")
            for f in forms:
                if "price is " in f.text:
                last_year_precent = f.text
            for tnum in range(len(td)):
                if "House" == td[tnum].text:
                    house_list.append(td[tnum+1].text)
                if "Unit" == td[tnum].text:
                    units.append(td[tnum+1].text)
                if "Land" == td[tnum].text:
                    lands.append(td[tnum+1].text)

                if "Municipality" in td[tnum].text:
                    municipality = td[tnum+2].text
                if "Number of houses/units" in td[tnum].text:
                    num_of_houses_units = td[tnum+2].text
                if "Houses/units sales last 12 months" in td[tnum].text:
                    last_year = td[tnum+2].text
                if "Highest price last 12 months" in td[tnum].text:
                    last_year_high = td[tnum+2].text
                if "Days on Market" in td[tnum].text:
                    days_on_market = td[tnum+2].text
                if "Features" == td[tnum].text
                    while True:
                        features.append(td[tnum+features_num])
                        features_num += 1
                        if "." not in td[tnum+features_num].text:
                            break
                if "PopulationSize" == td[tnum].text:
                    popul_size = td[tnum+3].text
                    popul_size_area = td[tnum+4].text
                    popul_size_city = td[tnum+5].text

                if "Country of Origin" == td[tnum].text:
                    count_of_origin = td[tnum+3].text
                    count_of_origin_area = td[tnum+4].text
                    count_of_origin_city = td[tnum+5].text

                if "Born Overseas - Top 5" == td[tnum].text:
                    born_overseas_1 = td[tnum+3].text
                    born_overseas_1_area = td[tnum+4].text
                    born_overseas_1_city = td[tnum+5].text

                    born_overseas_2 = td[tnum+6].text
                    born_overseas_2_area = td[tnum+7].text
                    born_overseas_2_city = td[tnum+8].text

                    born_overseas_3 = td[tnum+9].text
                    born_overseas_3_area = td[tnum+10].text
                    born_overseas_3_city = td[tnum+11].text

                    born_overseas_4 = td[tnum+12].text
                    born_overseas_4_area = td[tnum+13].text
                    born_overseas_4_city = td[tnum+14].text

                    born_overseas_5 = td[tnum+15].text
                    born_overseas_5_area = td[tnum+16].text
                    born_overseas_5_city = td[tnum+17].text

                if "Median household income" == td[tnum].text:
                    income_duration = td[tnum+3].text
                    income_duration_area = td[tnum+4].text
                    income_duration_city = td[tnum+5].text

                if "Assault" == td[tnum].text:
                    crime_assault_area = td[tnum+1].text
                    crime_assault_city = td[tnum+2].text
                if "Damage" == td[tnum].text:
                    crime_demage_area = td[tnum+1].text
                    crime_demage_city = td[tnum+2].text
                if "Robbery" == td[tnum].text:
                    crime_robbery_area = td[tnum+1].text
                    crime_robbery_city = td[tnum+2].text
                if "Sexual offences" == td[tnum].text:
                    crime_sex_offences_area = td[tnum+1].text
                    crime_sex_offences_city = td[tnum+2].text
                if "Theft" == td[tnum].text:
                    crime_theft_area = td[tnum+1].text
                    crime_theft_city = td[tnum+2].text
                #AGENTS
                if "Agent Name" == td[tnum].text:
                    anum = 0
                    while True:
                        anum += 1
                        if "Note: " in td[tnum+anum].text:
                            break
                        else:
                            agents.append([td[tnum+anum].text, td[tnum+anum+1]])
                         
                if "School Name" in td[tnum].text:
                    snum = 0
                    while True:
                        snum += 1
                        if "school" not in td[tnum+snum].text:
                            break
                        else:
                            schools.append([td[tnum+snum].text, td[tnum+snum+1].text])


        self.write_to_csv(info)

    def write_to_csv(self, iinfo):
        with open("SDATA.csv", "a") as f:
            fwriter = csv.writer(f)
            fwriter.writerow(iinfo)

s = Scraper()
# s.check_proxie()
s.get_links()