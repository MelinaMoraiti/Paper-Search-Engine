from QueryProcessor import QueryProcessor
from file_operations import retrieve_data
from text_processing import preprocess_paper
from InvertedIndex import InvertedIndex
from RankingAlgorithms import RankingAlgorithm
class SearchEngine:
    def __init__(self, preprocessed_documents=None,inverted_index=None):
        self.inverted_index = inverted_index
        self.preprocessed_documents = preprocessed_documents
        self.ranking = RankingAlgorithm()
    def build_inverted_index(self):
        inverted_index = InvertedIndex()
        for document_id,preprocessed_text in self.preprocessed_documents.items():
            self.preprocessed_documents[document_id] = preprocessed_text
            inverted_index.add_document(document_id, preprocessed_text)
        self.inverted_index = inverted_index
    def search(self, query):
        self.query_processor =  QueryProcessor(self.inverted_index, self.preprocessed_documents)
        boolean_results, vsm_results, okapiBM25_results = self.query_processor.process_query(query)
        if boolean_results or vsm_results or okapiBM25_results:
            return boolean_results, vsm_results, okapiBM25_results
        else:
            return "No matches"
    def rank_results(self,results,query):
        ranked_results={}
        for result_id in results:
            ranked_results[result_id] = self.preprocessed_documents[result_id]
        ranked_results = self.ranking.tf_idf_ranking(ranked_results,query)
        return ranked_results
    def filter_results(self, results, filters, papers_collection):
        filtered_papers = []
        for arxiv_id in results:
            paper = next((p for p in papers_collection if p['arXiv ID'] == arxiv_id), None)
            if paper:
                filter_match = all(
                    (value.lower() in map(str.lower, paper[key])) if isinstance(paper[key], list) and key != 'Authors' else
                    any(value.lower() in author.lower() for author in paper[key].split(', ')) if ['Authors', 'Subjects', 'Subject_Tags'] else
                    paper[key].lower() == value.lower()
                    for key, value in filters.items()
                )
                if filter_match:
                    filtered_papers.append(paper)
        return filtered_papers
    def display_results(self,results):
        for paper in results:
            print(f"arXiv ID: {paper['arXiv ID']}")
            print(f"Title: {paper['Title']}")
            print(f"Authors: {paper['Authors']}")
            print(f"Subject Tags: {paper['Subject_Tags']}")
            print(f"Subjects: {paper['Subjects']}")
            print(f"Submitted Date: {paper['Submitted Date']}")
            print(f"Abstract: {paper['Abstract']}")
            print(f"PDF Link: {paper['PDF Link']}")
            print(f"{'-'*200}")

if __name__ == "__main__":
    papers_collection = retrieve_data('../files/arXiv_papers_less.json')
    preprocessed_metadata = {}
    for paper in papers_collection:
        document_id = paper['arXiv ID']
        preprocessed_metadata[document_id] = preprocess_paper(paper)
    search_engine = SearchEngine(preprocessed_metadata)
    search_engine.build_inverted_index()
    query = "data structures"
    boolean_results, vsm_results, okapiBM25_results  = search_engine.search(query)
    print(search_engine.rank_results(boolean_results,query))
    '''
    filters = {'Subjects': query}
    filtered_papers = search_engine.filter_results(boolean_results, filters, papers_collection)
    if filtered_papers:
        print(f"Filtered papers based on user-selected criteria:")
        search_engine.display_results(filtered_papers)
    else:
        print("No papers found based on the user-selected criteria.")
    '''

