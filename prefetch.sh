#!/bin/bash

export HF_HUB_ENABLE_HF_TRANSFER=1

# Function to read a value from the YAML file
read_yaml_value() {
  config_file="config.yaml"
  key=$1
  shyaml get-value "$key" < "$config_file" 
}

# Read values directly from the YAML file
llm_model=$(read_yaml_value app.model.llm)
stt_model=$(read_yaml_value app.model.stt)

# Check if values were retrieved
if [ -z "$llm_model" ]; then
    echo "llm_model name is not set"
    exit 1
fi 

if [ -z "$stt_model" ]; then
    echo "stt_model name is not set"
    exit 1
fi

# Downloading the models (update logic if needed for LLM download)
# echo "Downloading the llm_model: $llm_model"
# huggingface-cli download "$llm_model"  

echo "Downloading the stt_model: $stt_model"
huggingface-cli download "$stt_model"
