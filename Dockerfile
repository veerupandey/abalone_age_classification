# Docker file for the abalone age classification project
# DSCI_522_GROUP_28

# Use miniconda image 
FROM continuumio/miniconda3@sha256:92d7896124d940cb1815d3b59d8eaab9a8e86c801af2437658581465044b0a06



# Work directory
RUN useradd -ms /bin/bash abalone
WORKDIR /home/abalone

# Non interactive command line
ARG DEBIAN_FRONTEND=noninteractive

# Update package list
# Install access control, development tools, 
# gnu make, chrome driver
# Clean the downloaded package
RUN apt-get update && \
    apt-get install -y \
    acl gcc python3-dev chromium-driver make \
    && rm -rf /var/lib/apt/lists/*

# Copy envronment.yml to container
COPY environment.yml .

# Build the environment:
RUN conda env create -f ./environment.yml

# Remove environment.yml from docker image
RUN rm -rf ./environment.yml 

# Make RUN commands use the new environment:
RUN echo "conda activate abalone" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN rm /opt/conda/envs/abalone/bin/python && \
    ln -s /opt/conda/envs/abalone/bin/python3 /opt/conda/envs/abalone/bin/python 
ENV PATH="/opt/conda/envs/abalone/bin:$PATH"

# Permission to abalone user
RUN setfacl -R -m u:abalone:rwx /home/abalone

# Add user
USER abalone
