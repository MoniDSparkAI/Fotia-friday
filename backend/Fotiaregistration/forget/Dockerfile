FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Expose port 5001 to allow external access
EXPOSE 5003

# Set the command to run your application on port 5001
CMD ["python", "forget.py"]
