FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Copy code
COPY . /src/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port (so ECS Load Balancer can route to it)
EXPOSE 80

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
