# Use an official Python runtime as a parent image
FROM python:3.10.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World
# ENV PATH="/usr/local/lib/python3.10/site-packages:${PATH}"

# Run app.py when the container launches
# CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=80"]