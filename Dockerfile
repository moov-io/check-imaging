# Use a Miniconda base image
FROM continuumio/miniconda3:latest

# Set the working directory inside the container
WORKDIR /app

# Copy environment.yml if you have one for Conda packages
# COPY environment.yml .
# RUN conda env create -f environment.yml
# ENV PATH="/opt/conda/envs/your_env_name/bin:$PATH"
# ACTIVATE CONDA ENVIRONMENT (if using environment.yml)
# RUN echo "conda activate your_env_name" >> ~/.bashrc
# SHELL ["/bin/bash", "--login", "-c"]

# Create a new Conda environment for your application
RUN conda create -n check-image python=3.13 -y
# Activate the Conda environment for subsequent commands
SHELL ["conda", "run", "-n", "check-image", "/bin/bash", "-c"]

# Copy requirements.txt and install Python dependencies using pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Uvicorn (if not in requirements.txt)
RUN pip install --no-cache-dir uvicorn

# Install Ollama (using the official script for Linux)
# This assumes you want Ollama server running within this container
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy your application code
COPY . .

# Expose the port Uvicorn will listen on (e.g., 8000)
EXPOSE 8000

# Command to run your application with Uvicorn
# Replace 'main:app' with your actual FastAPI application entry point
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]