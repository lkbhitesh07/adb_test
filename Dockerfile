# Use an official Ubuntu-based image as the base image
FROM ubuntu:20.04

# Install required packages and dependencies
RUN apt-get update && apt-get install -y gnupg wget

# Import the MongoDB public GPG key
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -

# Add the MongoDB repository to the sources list
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Update the package list and install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Install Yarn and Python 3 pip
RUN apt-get install -y yarn python3-pip

# Create the data directory
RUN mkdir -p /data/db

# Expose the default MongoDB port
EXPOSE 27017

# Start the MongoDB service
CMD ["mongod"]

# Set environment variables
ENV ENV_TYPE staging
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
ENV PYTHONPATH=$PYTHONPATH:/src/

# Copy the dependencies file to the working directory
COPY src/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt
