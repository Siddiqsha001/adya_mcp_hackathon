# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Copy application code
COPY . /src/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 80

ENV AWS_DEFAULT_REGION=us-east-1

# Run the FastAPI server using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
