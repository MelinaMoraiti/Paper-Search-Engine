from file_operations import retrieve_data
from text_processing import preprocess_paper
from sklearn.metrics import precision_score, recall_score, f1_score
from SearchEngine import SearchEngine
#from subprocess import run, PIPE

class Evaluator:
    def __init__(self, search_engine, ground_truth):
        self.search_engine = search_engine
        self.ground_truth = ground_truth

    def evaluate(self, queries):
        results = {
            'boolean': [],
            'vsm': [],
            'okapi_bm25': [],
        }
        for query in queries:
            boolean_papers, vsm_papers, okapi_papers = self.search_engine.search(query)

            # Evaluate Boolean retrieval
            boolean_metrics = self.calculate_metrics(boolean_papers)
            results['boolean'].append(boolean_metrics)

            # Evaluate VSM retrieval
            vsm_metrics = self.calculate_metrics(vsm_papers)
            results['vsm'].append(vsm_metrics)

            # Evaluate Okapi BM25 retrieval
            okapi_metrics = self.calculate_metrics(okapi_papers)
            results['okapi_bm25'].append(okapi_metrics)
        return results

    def calculate_metrics(self, retrieved_docs):
        y_true = [1 if doc_id in self.ground_truth else 0 for doc_id in retrieved_docs]
        y_pred = [1] * len(retrieved_docs)

        precision = precision_score(y_true, y_pred, zero_division=1)
        recall = recall_score(y_true, y_pred, zero_division=1)
        f1 = f1_score(y_true, y_pred, zero_division=1)

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
        }
    '''
    def save_results_to_file(self, queries, results, output_file):
        with open(output_file, 'w') as file:
            for i, query in enumerate(queries, start=1):
                for algorithm, metrics in results.items():
                    file.write(f"{algorithm} Q{i} {metrics[i-1]['precision']} {metrics[i-1]['recall']} {metrics[i-1]['f1']} run_id\n")
    def parse_trec_eval_output(self,trec_eval_output):
        parsed_metrics = {}  # Dictionary to store parsed metrics

        lines = trec_eval_output.split('\n')

        for line in lines:
            if line.strip():  # Skip empty lines
                fields = line.split()
            
                if fields[0] == 'runid':
                    continue  # Skip lines containing overall run information

                algorithm = fields[1]
                query_id = int(fields[2][1:])  # Extract query ID from "QX" format
                precision = float(fields[3])
                recall = float(fields[4])
                f1 = float(fields[5])

                if algorithm not in parsed_metrics:
                    parsed_metrics[algorithm] = {}

                parsed_metrics[algorithm][query_id] = {
                    'precision': precision,
                    'recall': recall,
                    'f1': f1,
                }
        return parsed_metrics
        '''

papers_collection = retrieve_data('../datasets/arXiv_papers_less.json')
preprocessed_metadata = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_metadata[document_id] = preprocess_paper(paper)

search_engine = SearchEngine(preprocessed_metadata)
search_engine.build_inverted_index()
queries = ['cs.AI', 'Neural networks', '9 December', 'Oren Ben-Zwi']
# Assuming ground_truth is VSM
total_ground_truth = []
for query in queries:
    ground_truth,_,_ = search_engine.search(query)
    total_ground_truth += ground_truth
evaluator = Evaluator(search_engine, total_ground_truth)
results = evaluator.evaluate(queries)

for algorithm, metrics_list in results.items():
    print(f"\nMetrics for {algorithm} retrieval:")
    for i, metrics in enumerate(metrics_list, start=1):
        print(f"{queries[i-1]}: Precision={metrics['precision']}, Recall={metrics['recall']}, F1={metrics['f1']}")
