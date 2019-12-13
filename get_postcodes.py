import pandas as pd
import json

class Postcodes:

    def __init__(self):
        df = pd.read_csv("Postcode List.csv")
        #print(df)
        self.states = df['Postcode'].values.tolist()
        with open("proxies.json", "r") as f:
            PROXIES = json.load(f)
        self.proxies = PROXIES
        '''
        self.states = []
        for post in posts:
        	if len(str(post)) < 4:
        		print(post)
        		self.states.append(int(f"0{post}"))
        	else:
        		self.states.append(post)
        #print(states)
        #just skip crosses
		'''

#p = Postcodes()
#print(p.states)
