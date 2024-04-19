# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Change directory to /app/sources
WORKDIR /app/sources

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader all

EXPOSE 5000

CMD ["python", "app.py"]

