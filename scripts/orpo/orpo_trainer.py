import gc
import os
import torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
)
from trl import ORPOConfig, ORPOTrainer, setup_chat_format

import yaml

with open("config.yaml", "r") as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(f"Error reading config.yaml: {exc}")
        exit(1)

base_model = config["base_model"]
new_model = config["new_model"]
torch_dtype = torch.float16
attn_implementation = "eager"

config["bnb_config"]["bnb_4bit_compute_dtype"] = torch_dtype
bnb_config = BitsAndBytesConfig(**config["bnb_config"])

peft_config = LoraConfig(**config["peft_config"])
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation=attn_implementation,
)
model, tokenizer = setup_chat_format(model, tokenizer)
model = prepare_model_for_kbit_training(model)

dataset_name = configp['dataset']
dataset = load_dataset(dataset_name, split="all")
dataset = dataset.shuffle(seed=42).select(range(1000))


def format_chat_template(row):
    row["chosen"] = tokenizer.apply_chat_template(row["chosen"], tokenize=False)
    row["rejected"] = tokenizer.apply_chat_template(row["rejected"], tokenize=False)
    return row


dataset = dataset.map(
    format_chat_template,
    num_proc=os.cpu_count(),
)
dataset = dataset.train_test_split(test_size=config["test_size"])

orpo_args = ORPOConfig(**config["train_config"])

trainer = ORPOTrainer(
    model=model,
    args=orpo_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    peft_config=peft_config,
    tokenizer=tokenizer,
)
trainer.train()
trainer.save_model(new_model)

tokenizer = AutoTokenizer.from_pretrained(base_model)
fp16_model = AutoModelForCausalLM.from_pretrained(
    base_model,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
fp16_model, tokenizer = setup_chat_format(fp16_model, tokenizer)

model = PeftModel.from_pretrained(fp16_model, new_model)
model = model.merge_and_unload()

model.save_pretrained(
    new_model,
    tokenizer=tokenizer,
)
