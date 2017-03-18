import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

r = requests.get("http://en.wikipedia.org/wiki/Paris")
def get_address(keyword):
    address = "http://en.wikipedia.org/wiki/" + keyword
    return address

def get_page(url):
    r = requests.get(url)
    return r.text

def get_img_by_src(soup):
    img_list = []
    for img in soup.find_all("img"):
        if ".png" in img.get("src"):
            continue
        else:
            img_list.append(img.get("src"))
    return img_list

def get_img_by_File(soup):
    img_list = []
    img_dict = {}
    n = 0
    for link in soup.find_all('a', href=True):
        if '/wiki/' in link['href'] and 'File:' in link['href'] and '.jpg' in link['href']:
            img_list.append(link['href'])
            n += 1
            img_dict[n] = link['href']
        else:
            continue
    return img_dict

@app.route("/<query>")
def hello(query):
    cap_list = []
    address = get_address(query)
    content = get_page(address)
    content = BeautifulSoup(content)
    results = get_img_by_File(content)
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run()
