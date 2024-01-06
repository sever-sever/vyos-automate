FROM debian:10

# Install required dependencies
RUN apt-get update && apt-get install -y \
    ansible \
    python3

# Install not required dependencies
RUN apt-get install -y \
    git \
    mc \
    && rm -rf /var/lib/apt/lists/*

# Make build directory
RUN mkdir -p /home/build
WORKDIR /home/build
