# 👨‍🔬📚 Academic Paper Search Engine 

## Overview

This project implements a comprehensive academic paper search engine using Python. It comprises a web crawler to collect metadata, text processing for content preparation, indexing for efficient search, and multiple retrieval algorithms (Boolean Retrieval, Vector Space Model, Okapi BM25) for result ranking. The system offers a user-friendly web interface using  Python's Flask web framework, with a retrieval algorithm dropdown list selection and filtering options for searches, including criteria such as author, subject, submission date, title, etc.

## 🎥 Preview 
![Search Engine Preview](/app%20screenshots/SearchEngineUsage.gif)

## 🛠️ Getting Started 

### Prerequisites:
- Python 3.9 or higher
- Git

1. **Clone the Repository:**
     ```bash
     git clone https://github.com/MelinaMoraiti/Academic-Papers-Search-Engine.git
     cd sources
     ```
2. **Install Dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
3. **Download nltk necessary resources:**
     ```bash
     python nltk_resources.py
     ```
4. **Create a .env file in the root directory of the project and configure it similar to the example.env:**
     - **FLASK_HOST:** Set the **host address** for your Flask application. If running locally, you can set this to localhost. If deploying to a server, use the server's IP address or domain name.
     - **FLASK_PORT:** Define the **port number** where your Flask application will run. The default Flask port is 5000.
     - **FLASK_DEBUG:** Enable or disable Flask's debugging mode. When enabled, Flask will reload itself on code changes and provide more detailed error messages. Set to **1/True** to enable debugging, or **0/False** to disable it.
     - **DATASET_PATH:** Specify the **local file path** to the dataset that your Flask application will use.
     
5. **Run the Application:**
     ```bash
     python app.py
     ```
     The web interface should now be accessible at `http://localhost:5000` in your web browser.
6. **Perform a Search:**
   -  Perform a search using the user-friendly interface.
   -  Choose a retrieval algorithm from the dropdown list.
   -  Use filtering options to refine your search.

## 🔮💡 Future Ideas 

- [x] **Utilizing arXiv's Public API for Faster Data Collection**
- [ ] **Implementation of Multi-Threading for Data Processing**
- [ ] **Pagination Support for Result Presentation**
- [X] **Create a Dockerfile**

## 🙏 Acknowledgements 

- Thank you to arXiv for use of its open access interoperability.
