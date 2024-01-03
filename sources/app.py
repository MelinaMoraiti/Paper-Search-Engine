from flask import Flask, render_template, request
import os
from SearchEngine import SearchEngine
from RankingAlgorithms import RankingAlgorithm
from file_operations import retrieve_data
from text_processing import preprocess_paper
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

papers_collection = retrieve_data('../files/arXiv_papers.json')
preprocessed_metadata = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_metadata[document_id] = preprocess_paper(paper)
search_engine = SearchEngine(preprocessed_metadata)
ranking = RankingAlgorithm()
search_engine.build_inverted_index()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        algorithm = request.form['algorithm']
        filter_criteria = request.form['filter_criteria']
        boolean_results,vsm_results,okapiBM25_results = search_engine.search(query)
        if algorithm == 'boolean':
            results = boolean_results
        elif algorithm == 'vsm':
            results = vsm_results
        elif algorithm == 'okapiBM25':
            results = okapiBM25_results
        else:
            return render_template('index.html', error_message='Invalid retrieval algorithm.')
        if results: results_ranked = search_engine.rank_results(results,query)
        else: return render_template('results.html', query=query, no_results=True)
        if filter_criteria != 'none':
            filters = {filter_criteria: query}  
            results = search_engine.filter_results(results_ranked, filters, papers_collection)
        if results_ranked:
            result_papers = []
            for arxiv_id in results_ranked:
                paper = next((p for p in papers_collection if p['arXiv ID'] == arxiv_id), None)
                if paper:
                    result_papers.append(paper)
            return render_template('results.html', query=query, papers=result_papers)
        else:
            return render_template('results.html', query=query, no_results=True)

    return render_template('search_form.html')

if __name__ == '__main__':
    app.run(debug=True)
