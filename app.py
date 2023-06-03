import pandas as pd, time, json
from flask import Flask, render_template, request


app = Flask(__name__)

def loadJson(x):
    if x is not None:
        return json.loads(x)
    return []

def reScrape():
    # TO-DO: rescrape after a certain time
    pass

def loadData():
    start = time.time()
    papers = pd.read_json("./scrapedData/papers.json")
    authors = pd.read_json("./scrapedData/authors.json")

    print(f"Loaded files in {time.time() - start} seconds")
    return papers, authors

PAPERS, AUTHORS = loadData()

@app.route('/')
def home():
    return render_template('Home.html')

def search_papers(query):
    papers = PAPERS[PAPERS['title'].str.contains(query, case=False) |
                PAPERS['tags'].str.contains(query, case=False) |
                PAPERS['authors'].str.contains(query, case=False)]
    
    return papers.to_dict('records')


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')  # Get the search query from the form
    matchingPapers = search_papers(query)  # Call the function to search for papers
    return render_template('Results.html', papers=matchingPapers, query=query)


if __name__ == '__main__':
    app.run(debug=True)