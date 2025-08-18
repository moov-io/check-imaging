# Use the official Miniconda3 image as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Create a Conda environment with a specific Python version
RUN conda create -n check-imaging-env python=3.12.11 -y

# Make RUN, CMD, and ENTRYPOINT commands use the Conda environment
SHELL ["conda", "run", "-n", "check-imaging-env", "/bin/bash", "-c"]

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application when the container launches
# Replace app.main:app with the correct path to your FastAPI app instance
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
