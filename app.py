from HomeScraper import HScraper
from SubribScraper import SScraper

if __name__ == "__main__":
    search_term = input("What is the STATE you want to search?\n")
    question = input("What do you want to search HOUSES or Subribs?\n(enter H or S)\n")
    while True:
        if question.upper() == "H":
            hs = HScraper(search_term)
            hs.get_links()
            hs.get_house_links()
            break
        elif question.upper() == "S":
            ss = SScraper(search_term)
            ss.get_links()
            ss.get_info()
            break
        else:
            print("INVALID INPUT\nPLEASE INSERT H or S for search Houses or Subribs")
            question = input("What do you want to search HOUSES or Subribs?\n(enter H or S)\n")
