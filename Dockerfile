# Docker file for the abalone age classification project
# DSCI_522_GROUP_28

# Use miniconda image 
FROM continuumio/miniconda3

# Work directory
RUN useradd -ms /bin/bash abalone
WORKDIR /home/abalone

# Non interactive command line
ARG DEBIAN_FRONTEND=noninteractive

# Update package list
RUN apt-get update -y

# Install development tools, gnu make, chrome driver
# Clean the downloaded package
RUN apt-get install gcc python3-dev chromium-driver make -y &&\
    apt-get clean -y &&\
    apt-get autoremove

# Copy envronment.yml to container
COPY environment.yml .

# Build the environment:
RUN conda env create -f ./environment.yml

# Remove environment.yml from docker image
RUN rm -rf ./environment.yml 

# Make RUN commands use the new environment:
RUN echo "conda activate abalone" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN rm /opt/conda/envs/abalone/bin/python
RUN ln -s /opt/conda/envs/abalone/bin/python3 /opt/conda/envs/abalone/bin/python 
ENV PATH="/opt/conda/envs/abalone/bin:$PATH"

# Permission to abalone user
RUN apt-get install acl -y &&\
    setfacl -R -m u:abalone:rwx /home/abalone

# Add user
USER abalone
