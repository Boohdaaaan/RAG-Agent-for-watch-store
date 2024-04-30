FROM python:3.10

# Set working directory within the container
WORKDIR /app

# Copy the current directory to the container's working directory
COPY . /app

# Upgrade pip and install required Python packages from requirements.txt without caching
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]
