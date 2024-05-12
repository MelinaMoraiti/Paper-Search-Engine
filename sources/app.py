from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from SearchEngine import SearchEngine
from file_operations import retrieve_data
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

load_dotenv()
#get environment variables from .env
host = os.getenv("FLASK_HOST", "127.0.0.1") 
port = int(os.getenv("FLASK_PORT", 5000))
debug = os.getenv("FLASK_DEBUG", "True").lower() in ['true', '1']
dataset_path = os.getenv("DATASET_PATH","../datasets/arXiv_papers.csv")

papers_collection = retrieve_data(dataset_path)
search_engine = SearchEngine()
search_engine.build_preprocessed_documents(papers_collection)
search_engine.build_inverted_index()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        algorithm = request.form['algorithm']
        filter_criteria = request.form['filter_criteria']
        if algorithm == 'boolean':
            boolean_results, _, _ = search_engine.search(query)
            results = boolean_results
        elif algorithm == 'vsm':
            _, vsm_results, _ = search_engine.search(query)
            results = vsm_results
        elif algorithm == 'okapiBM25':
            _, _, okapiBM25_results = search_engine.search(query)
            results = okapiBM25_results
        else:
            return render_template('search_form.html', error_message='Invalid retrieval algorithm.')
        if results: 
            if algorithm == 'boolean': results_ranked = search_engine.rank_results(results,query)
            else: results_ranked =results
            if filter_criteria != 'none':
                filters = {filter_criteria: query}  
                filtered_results = search_engine.filter_results(results_ranked, filters, papers_collection)
                if filtered_results:
                    return render_template('results.html', query=query,papers=filtered_results,num_results=len(filtered_results))
                else: return render_template('results.html', query=query, no_results=True,num_results=0)
            else: 
                result_papers=[]
                for arxiv_id in results_ranked:
                    paper = next((p for p in papers_collection if p['arXiv ID'] == arxiv_id), None)
                    if paper:
                        result_papers.append(paper)
                return render_template('results.html', query=query,papers=result_papers,num_results=len(result_papers))
        else: 
            return render_template('results.html', query=query, no_results=True, num_results=0)
    return render_template('search_form.html')
            
if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
