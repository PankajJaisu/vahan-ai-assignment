    # Use the official Python image
FROM --platform=linux/amd64 python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# Remove null bytes from Python files

RUN apt-get update && apt-get install -y dos2unix
RUN find . -name "*.py" -exec dos2unix {} \;
RUN find . -name "*.py" -exec iconv -f utf-8 -t utf-8 -c -o {} {} \;


# Run migrations
RUN python manage.py migrate --no-input