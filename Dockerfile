# Pull official base image
FROM python:3.10-alpine

# Set work directory
WORKDIR /usr/src/app

# Copy requiremenets.txt to /usr/src/app
COPY requirements.txt ./

# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project to /usr/src/app
COPY . .

# Run application 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
