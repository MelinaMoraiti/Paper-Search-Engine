from file_operations import retrieve_data
from text_processing import preprocess_paper
from SearchEngine import SearchEngine
class Evaluator:
    def __init__(self, search_engine, ground_truth):
        self.search_engine = search_engine
        self.ground_truth = ground_truth

    @staticmethod
    def precision(retrieved_docs, relevant_docs):
        if len(retrieved_docs) > 0:
            return len(set(retrieved_docs) & set(relevant_docs)) / len(retrieved_docs)
        else:
            return 0

    @staticmethod
    def recall(retrieved_docs, relevant_docs):
        return len(set(retrieved_docs) & set(relevant_docs)) / len(relevant_docs) if len(relevant_docs) > 0 else 0

    @staticmethod
    def f1_score(precision, recall):
        return 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    @staticmethod
    def average_metrics(precision_values, recall_values, f1_values):
        avg_precision = sum(precision_values) / len(precision_values)
        avg_recall = sum(recall_values) / len(recall_values)
        avg_f1 = sum(f1_values) / len(f1_values)
        return avg_precision, avg_recall, avg_f1

    def evaluate(self, queries, retrieval_algorithm):
        precision_values = []
        recall_values = []
        f1_values = []
        for query in queries:
            if retrieval_algorithm=='vsm':
                _, results, _ = self.search_engine.search(query)
            elif retrieval_algorithm == 'boolean':
                results,_, _ = self.search_engine.search(query)
            elif retrieval_algorithm == 'okapiBM25':
                _, _, results = self.search_engine.search(query)
            else: return
            relevant_docs = self.ground_truth.get(query, [])
            precision_values.append(self.precision(results, relevant_docs))
            recall_values.append(self.recall(results, relevant_docs))
            f1_values.append(self.f1_score(precision_values[-1], recall_values[-1]))
        avg_precision, avg_recall, avg_f1 = self.average_metrics(precision_values, recall_values, f1_values)
        return {
            'avg_precision': avg_precision,
            'avg_recall': avg_recall,
            'avg_f1': avg_f1
        }

papers_collection = retrieve_data('../files/arXiv_papers_less.json')
preprocessed_metadata = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_metadata[document_id] = preprocess_paper(paper)

search_engine = SearchEngine(preprocessed_metadata)
search_engine.build_inverted_index()
queries = ['cs.AI','Neural networks','9 December','Oren Ben-Zwi']
ground_truth = {
    'cs.AI': ['arXiv:2312.00455', 'arXiv:2312.00742', 'arXiv:2312.00621'],
    'Neural networks': ['arXiv:2312.00073', 'arXiv:2312.00456', 'arXiv:2312.02829'],
    '9 December': ['arXiv:2312.05647','arXiv:2312.06694','arXiv:2312.05566','arXiv:2312.05700','arXiv:2312.06690','arXiv:2312.05655','arXiv:2312.05475','arXiv:2312.07562','arXiv:2312.05527','arXiv:2312.05555','arXiv:2312.05553','arXiv:2312.05501','arXiv:2312.05728','arXiv:2312.05712','arXiv:2312.06693'],
    'Oren Ben-Zwi': ['arXiv:2312.00522']
}
evaluator = Evaluator(search_engine, ground_truth)
results = evaluator.evaluate(queries,'boolean')
print(f"Average Precision: {results['avg_precision']}")
print(f"Average Recall: {results['avg_recall']}")
print(f"Average F1 Score: {results['avg_f1']}")

