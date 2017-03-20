from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/save", methods=['POST', 'GET'])
def add_save():
    if request.method == 'POST':
        # effect = request.form['forward']
        dial = request.form.getlist('pick')
        return render_template("save.html", choice=dial)

@app.route("/", methods=['POST', 'GET'])
def run_search():
    if request.method == 'POST':
        answer = request.form['keyword']
        result = '/' + answer + '/1/1'
        return redirect(result)

    return render_template('land_page.html', error=error)

@app.route("/<query>/<scale>/<limit>", methods=['POST', 'GET'])
def scrape_and_list(query, scale, limit):
    address = functions.get_address(query)
    content = functions.get_page(address)
    content = functions.make_soup(content)
    results = functions.get_img_by_File(content, int(scale), int(limit))
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run()
