FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY requirements.txt requrements.txt

# Install requirements and download NLTK resources
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader wordnet punkt

# Copy the datasets directory into the container at /app/datasets
COPY datasets sources .

EXPOSE 5000

CMD ["python", "sources/app.py"]

