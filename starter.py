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

# def get_img_from_img_page(soup):
#     return 1

def get_img_by_File(soup, scale, limit):
    img_list = []
    img_dict = {}
    n = 0
    for link in soup.find_all('a', href=True):
        if '/wiki/' in link['href'] and 'File:' in link['href'] and '.jpg' in link['href']:
            if link['href'] in img_list:
                continue
            else:

                img_page_address = 'http://commons.wikimedia.org' + link['href']
                img_list.append(link['href'])
                img_page = get_page(img_page_address)
                img_page_soup = BeautifulSoup(img_page)
                miniature = get_img_by_src(img_page_soup)
                n += 1
                img_dict[miniature[scale]] = img_page_address
                # liczba powyzej pozwala regulowac wielkosc grafik
                if n >= limit:
                    break
        else:
            continue
    return img_dict

@app.route("/<query>/<scale>/<limit>")
def scrape_and_list(query, scale, limit):
    cap_list = []
    address = get_address(query)
    content = get_page(address)
    content = BeautifulSoup(content)
    results = get_img_by_File(content, int(scale), int(limit))
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run()
