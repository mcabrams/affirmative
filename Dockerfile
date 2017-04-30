############################################################
# Dockerfile to build Django / Python Application Containers
# Based on python 3.4.2
############################################################

# Set the base image to Python
FROM python:3.6.1

WORKDIR /django

# Add dependency files to the FS
ADD requirements.txt /django/

# Install python dependencies
RUN pip install -r /django/requirements.txt
