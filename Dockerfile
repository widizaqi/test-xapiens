# use an official python runtime as a parent image
FROM python:3.9-slim

# set the working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# Install any required Python packages
RUN pip install --no-cache-dir --upgrade pip

# make port 8000 available to the world outside this container
EXPOSE 8000

# run server.py when container launches
CMD ["python", "server.py"]
