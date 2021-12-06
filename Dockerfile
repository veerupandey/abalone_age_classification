# Docker file for the abalone age classification project
# DSCI_522_GROUP_28

# Use miniconda image 
FROM python:3.8.12

# Work directory
WORKDIR /app

# Non interactive command line
ARG DEBIAN_FRONTEND=noninteractive

# Update package list
RUN apt-get update -y

# Install development tools
RUN apt-get install gcc python3-dev chromium-driver -y

# Install GNU make, chromium driver
RUN apt-get install make wget -y

# Install chrome for dataframe_image to work
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install ./google-chrome-stable_current_amd64.deb -y


# Install conda 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda --version

# Copy envronment.yml to container
COPY environment.yml .

# Build the environment:
RUN conda env create -f ./environment.yml


# Remove environment.yml from docker image
RUN rm -rf ./environment.yml ./Miniconda3-latest-Linux-x86_64.sh

# Use the new conda environment:
ENV PATH="/root/miniconda3/envs/abalone/bin:$PATH"