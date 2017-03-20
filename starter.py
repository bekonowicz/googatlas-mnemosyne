import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_address(keyword):
    address = "http://en.wikipedia.org/wiki/" + keyword
    return address

def get_page(url):
    r = requests.get(url)
    return r.text

def get_img_by_src(soup):
    # function for locating images by sources
    img_list = []
    for img in soup.find_all("img"):
        # exclusion of .pngs excludes all the icons and other glyphs on Wiki
        if ".png" in img.get("src"):
            continue
        else:
            img_list.append(img.get("src"))
    return img_list

def get_img_by_File(soup, scale, limit):
    # function for locating images by particular url structure
    # limit sets the limit for results
    # scale sets the size of the loaded images: 0 - large, 1 - miniature
    img_list = []
    img_dict = {}
    counter = 0
    for link in soup.find_all('a', href=True):
        if '/wiki/' in link['href'] and 'File:' in link['href'] and '.jpg' in link['href']:
            if link['href'] in img_list:
                # avoiding duplicates, fix for Wikipedias random structure at times
                continue
            else:
                img_page_address = 'http://commons.wikimedia.org' + link['href']
                img_list.append(link['href'])
                img_page = get_page(img_page_address)
                img_page_soup = BeautifulSoup(img_page)
                miniature = get_img_by_src(img_page_soup)
                counter += 1
                img_dict[miniature[scale]] = img_page_address
                if counter >= limit:
                    break
        else:
            continue
    return img_dict


@app.route("/save", methods=['POST', 'GET'])
def add_save():
    if request.method == 'POST':
        # effect = request.form['forward']
        dial = request.form.getlist('pick')
        return render_template("save.html", choice=dial)

@app.route("/", methods=['POST', 'GET'])
def run_search():
    error = None
    if request.method == 'POST':
        answer = request.form['keyword']
        result = '/' + answer + '/1/1'
        return redirect(result)

    return render_template('land_page.html', error=error)

@app.route("/<query>/<scale>/<limit>", methods=['POST', 'GET'])
def scrape_and_list(query, scale, limit):
    address = get_address(query)
    content = get_page(address)
    content = BeautifulSoup(content)
    results = get_img_by_File(content, int(scale), int(limit))
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run()
