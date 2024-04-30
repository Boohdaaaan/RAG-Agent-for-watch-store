FROM python:3.10

# Set working directory within the container
WORKDIR /agent

# Copy the current directory to the container's working directory
COPY . /agent

# Upgrade pip and install required Python packages from requirements.txt without caching
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8000"]