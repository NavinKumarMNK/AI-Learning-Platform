#!/bin/bash

# Replace with your URL
app_version="app-v0.1.0"
url="https://github.com/NavinKumarMNK/AI-Learning-Platform/releases/download/$app_version/app.zip"

# Download the file
wget "$url" -O temp_file.tar.gz

# Create the directory if it doesn't exist
mkdir -p ./static/megacad

# Extract the file to the specified directory
unzip -o temp_file.tar.gz -d ./static/megacad

# Remove the temporary file
rm temp_file.tar.gz


