from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31'
url_get = requests.get(url)
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find_all('div',{'class':'lister-item-content'})


row_length = len(table)

data = []
for ta in table:
    judul = ta.find('a').text.strip()
    rating = ta.find('strong').text.strip()
    metascore1 = ta.find('span',{'class':'metascore favorable'})
    metascore = metascore1.get_text(strip=True) if metascore1 else 'N/A'
    votes = ta.find('span',{'name':'nv'}).text.strip()
    print(judul)
    print(rating)
    print(metascore)
    print(votes)
    data.append([judul,rating,metascore,votes])

#change into dataframe
df = pd.DataFrame(data,columns=['judul','rating','metascore','votes'])

#insert data wrangling here
df['rating'] = df['rating'].astype('float')
df['votes'] = df['votes'].str.replace(',','').astype(int)
df['metascore']=df['metascore'].replace(['N/A'],'0')
df['metascore'] = df['metascore'].astype('float')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["rating"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)