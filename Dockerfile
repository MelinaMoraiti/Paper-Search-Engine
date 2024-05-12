FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY requirements.txt requirements.txt

# Install requirements and download NLTK resources
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader stopwords wordnet punkt

# Copy the datasets, sources directories into the container at /app
COPY datasets sources .

# Copy .env file into the container 
COPY .env .env
EXPOSE 5000

CMD ["python", "sources/app.py"]

