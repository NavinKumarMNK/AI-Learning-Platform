#!/bin/bash

# Load variables from .env file
if [ -f globals.env ]; then
    set -a
    . globals.env
    set +a
else
    echo ".env file not found"
    exit 1
fi

# Function to read a value from the YAML file
read_yaml_value() {
  config_file="config.yaml"
  key=$1
  shyaml get-value "$key" < "$config_file" 
}

# Read values directly from the YAML file
llm_model=$(read_yaml_value app.model.llm)
stt_model=$(read_yaml_value app.model.stt)
emb_model=$(read_yaml_value app.model.emb)

# Check if values were retrieved
if [ -z "$llm_model" ]; then
    echo "llm_model name is not set"
fi 

if [ -z "$stt_model" ]; then
    echo "stt_model name is not set"
fi

if [ -z "$emb_model" ]; then
    echo "emb_model name is not set"
fi

# Downloading the models (update logic if needed for LLM download)
echo "Downloading the llm_model: $llm_model"
huggingface-cli download "$llm_model"  

echo "Downloading the stt_model: $stt_model"
huggingface-cli download "$stt_model"

echo "Downloading the emb_model: $emb_model"
huggingface-cli download "$emb_model"
