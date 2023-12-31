from QueryProcessor import QueryProcessor
from file_operations import retrieve_data
from text_processing import preprocess_paper
from InvertedIndex import InvertedIndex
class SearchEngine:
    def __init__(self, preprocessed_documents=None,inverted_index=None):
        self.inverted_index = inverted_index
        self.preprocessed_documents = preprocessed_documents
    def build_inverted_index(self):
        inverted_index = InvertedIndex()
        for document_id,preprocessed_text in self.preprocessed_documents.items():
            self.preprocessed_documents[document_id] = preprocessed_text
            inverted_index.add_document(document_id, preprocessed_text)
        self.inverted_index = inverted_index
    def search(self, query):
        query_processor = QueryProcessor(self.inverted_index, self.preprocessed_documents)
        boolean_results, vsm_results, okapiBM25_results = query_processor.process_query(query)
        if boolean_results or vsm_results or okapiBM25_results:
            return boolean_results, vsm_results, okapiBM25_results
        else:
            return "No matches"
    def filter_results(self, results, filters, papers_collection):
        filtered_papers = []
        for arxiv_id in results:
            paper = next((p for p in papers_collection if p['arXiv ID'] == arxiv_id), None)
            if paper:
                filter_match = all(paper[key].lower() == value.lower() for key, value in filters.items())
                if filter_match:
                    filtered_papers.append(paper)
        return filtered_papers
    def display_results(self,results):
        for paper in results:
            print(f"arXiv ID: {paper['arXiv ID']}")
            print(f"Title: {paper['Title']}")
            print(f"Authors: {paper['Authors']}")
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
    query = "1 December, 2023;"
    boolean_results, vsm_results, okapiBM25_results = search_engine.search(query)
    print(boolean_results)

    filters = {'Submitted Date': query}
    filtered_papers = search_engine.filter_results(boolean_results, filters, papers_collection)
    if filtered_papers:
        print(f"Filtered papers based on user-selected criteria:")
        search_engine.display_results(filtered_papers)
    else:
        print("No papers found based on the user-selected criteria.")

