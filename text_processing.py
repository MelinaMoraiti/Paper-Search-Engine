# text_processing.py
import nltk
import string
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
def tokenize_text(text):
    # Lowercasing
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    return tokens
# Sanitizes text from punctuation and stopwords
def clean_text(text):
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = tokenize_text(text)
    cleaned_tokens =[]
    for token in tokens:
        if token not in string.punctuation and stopwords:
            cleaned_tokens.append(token)
    return cleaned_tokens
def normalize_text(text):
    lemmatizer = WordNetLemmatizer()
    #stemmer = PorterStemmer()
    tokens = clean_text(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    #stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return lemmatized_tokens
   