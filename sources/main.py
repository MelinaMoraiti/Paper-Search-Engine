import paper_crawler
import file_operations
from text_processing import preprocess_paper,preprocess_text
from InvertedIndex import InvertedIndex
from QueryProcessor import QueryProcessor
from RetrievalAlgorithms import RetrievalAlgorithms
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
papers_collection = file_operations.retrieve_data('../files/arXiv_papers_less.json')
# text_processing
preprocessed_texts = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_texts[document_id] = preprocess_paper(paper)
query = "Cryptography and Security"
result_vsm= RetrievalAlgorithms.vector_space_model(query, preprocessed_texts,0.07)
print(f"VSM Results for {query}:", result_vsm)

#Create inverted index
inverted_index = InvertedIndex()
# Add papers to the inverted index
for doc_id, preprocessed_text in preprocessed_texts.items():
    inverted_index.add_document(doc_id, preprocessed_text)

query_processor = QueryProcessor(inverted_index)
result_docs = query_processor.process_query(query)
if result_docs:
    print(f"Boolean results for {query}:", result_docs)
else:
    print("No Matches")

