import paper_crawler
import file_operations
import text_processing
categories = ['cs','cond-mat','astro-ph','math','q-bio','q-fin','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','stat','econ']  
category = ['stat']
#target_urls = paper_crawler.create_urls(categories,200)
#papers_data = paper_crawler.crawl_websites(target_urls)
#file_operations.save_data(papers_data,'arXiv_papers.json')
#file_operations.save_data(papers_data,'arXiv_papers.csv')
papers_data=file_operations.retrieve_data('arXiv_papers.csv')
print(papers_data[3]['Abstract'])
print(text_processing.tokenize_text(papers_data[3]['Title']))
print(text_processing.normalize_text(papers_data[3]['Abstract']))

