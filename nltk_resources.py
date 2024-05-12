import nltk
import os

# Set download directory to user/nltk_data
nltk.download_dir = os.path.expanduser('~/nltk_data')

# Download WordNet and punkt resources
nltk.download('wordnet', download_dir=nltk.download_dir)
nltk.download('punkt', download_dir=nltk.download_dir)
nltk.download('stopwords', download_dir=nltk.download_dir)