# coding=utf-8
import web
from web import form
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())
vpass = form.regexp("Must be more than 5", lambda x:len(x)>5)

myform = form.Form(
form.Textbox('blabla', form.notnull, description="Dear GoogAtlas, print me an Atlas beginning with..."),
)

lista = []
tytul = "blablabla"

# part of the names is in Polish
# treat it as a part of a sentiment

r  = requests.get("https://en.wikipedia.org/wiki/Warsaw")
print r
data = r.text
soup = BeautifulSoup(data)	
tytulik = soup.title
tytul = tytulik.string



class index:
	def GET(self): 
		form = myform()
		return render.formtest(form)

	def POST(self): 
		lista = []
		slownik = {}
		form = myform() 
		if not form.validates(): 
			return render.formtest(form)
		else:
			alfa = form.d.blabla
			alfa = unidecode(alfa)
			r  = requests.get("https://en.wikipedia.org/wiki/" + str(alfa))
			data = r.text
			soup = BeautifulSoup(data)	
			tytulik = soup.title
			tytul = tytulik.string
			for img in soup.find_all("img"):
				if ".png" in img.get("src"):
					continue
				else:
					slownik[img.get("src")] = img.get("alt")
					print img.get("alt")
		return render.wyniki(slownik, tytul)

if __name__=="__main__":
	web.internalerror = web.debugerror
	app.run()