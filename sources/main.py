import paper_crawler
import file_operations
from text_processing import preprocess_paper,preprocess_text
from InvertedIndex import InvertedIndex
from RankingAlgorithms import RankingAlgorithm
from QueryProcessor import QueryProcessor
from RetrievalAlgorithms import RetrievalAlgorithms
from VectorSpaceModel import VectorSpaceModel
"""
categories = ['cs','cond-mat','astro-ph','math','q-bio','q-fin','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','stat','econ']  
#query = ['Distributed Systems']

target_urls = paper_crawler.create_urls(categories,50,50)
papers_data = paper_crawler.crawl_websites(target_urls)
# Saving Data in files.
file_operations.save_data(papers_data,'../files/arXiv_papers_less.json')
file_operations.save_data(papers_data,'../files/arXiv_papers_less.csv')

"""
# load data from file
papers_collection = file_operations.retrieve_data('../files/arXiv_papers.json')
# text_processing
preprocessed_metadata = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_metadata[document_id] = preprocess_paper(paper)
#Create inverted index
inverted_index = InvertedIndex()
# Add papers to the inverted index
for doc_id, preprocessed_text in preprocessed_metadata.items():
    inverted_index.add_document(doc_id, preprocessed_text)

vector_space_model = VectorSpaceModel(preprocessed_metadata,0.1)
query = "Orange Apple"
VSM_results = vector_space_model.retrieve_documents_above_threshold(query)
print('-'*150)
print("VSM Retrieval Results:",VSM_results)
print('-'*150)
found_documents = {}
for i in VSM_results:
    found_documents[i] = preprocessed_metadata[i]
result_tfidf_ranking = RankingAlgorithm.tf_idf_ranking(found_documents, query)
print("TF-IDF Ranking Results:", result_tfidf_ranking)
result_vsm= RetrievalAlgorithms.vector_space_model(query, preprocessed_metadata,0.1)
print(f"VSM Results for {query}:", result_vsm)

query_processor = QueryProcessor(inverted_index)
result_docs = query_processor.process_query(query)
if result_docs:
    print(f"Boolean results for {query}:", result_docs)
else:
    print("No Matches")

