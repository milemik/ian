from HomeScraper import HScraper
from SubribScraper import SScraper
from get_postcodes import Postcodes
from threading import Thread

def homes(state, ):
    hs = HScraper(state)
    hs.get_links()
    if len(hs.LINKS) > 0:
        hs.get_house_links()


def subribs(state):
    ss = SScraper(state)
    ss.get_links()
    if len(ss.LINKS) > 0:
        ss.get_info()


if __name__ == "__main__":
    p = Postcodes()
    pcodes = p.states
    #proxs = p.proxies
    #print(pcodes)
    for p in pcodes:
        #homes(p)
        #'''
        if p != "crosses":
            #t1 = Thread(target = homes, args=(p, ))
            t2 = Thread(target = subribs, args=(p, ))
            #t1.start()
            t2.start()
        #'''
