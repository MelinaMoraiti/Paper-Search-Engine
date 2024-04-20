# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the datasets directory into the container at /app/datasets
COPY datasets /app/datasets

# Copy the sources directory into the container at /app/sources
COPY sources /app/sources

# Change directory to /app/sources
WORKDIR /app/sources

# Install requirements and download NLTK resources
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader wordnet punkt

EXPOSE 5000

CMD ["python", "app.py"]

