import paper_crawler
import file_operations

categories = ['cs','cond-mat','astro-ph','math','q-bio','q-fin','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','stat','econ']  
#query = ['Distributed Systems']

target_urls = paper_crawler.create_urls(categories,50,50)
papers_data = paper_crawler.crawl_websites(target_urls)
# Saving Data in files.
file_operations.save_data(papers_data,'../files/arXiv_papers_less.json')
file_operations.save_data(papers_data,'../files/arXiv_papers_less.csv')


